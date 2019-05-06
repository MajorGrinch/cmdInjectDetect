import os
import re
import multiprocessing
import subprocess
from .vulinfo import VulnerabilityInfo
from .export import list_to_prettytable
from .languages import supported_lan
from .sinks import dict_sink, fpc_multi, fpc_single
from .file_util import Tool
from .abst import SinkChecker
from pycparser import c_ast, c_parser, parse_file
from .data_flow_util import analyzeFunctionCall

class CmdInjDetect(object):
    """
    One CmdInjDetect instance serve one language
    """

    def __init__(self, target_File_path, lan):
        print("----" + target_File_path)
        self.target_File = target_File_path
        self.grep = Tool().grep
        self.language = lan



    def regular_match(self, target_File, lan):
        """
        target file/dir path and specific language
        """
        print("[CMD DETECT]", target_File)
        print("[CMD DETECT]", lan)
        if '|' in dict_sink[lan]:
            match_expr = fpc_multi.replace('[f]', dict_sink[lan])
        else:
            match_expr = fpc_single.replace('[f]', dict_sink[lan])
        # print(match_expr)
        filters = []
        for ext in supported_lan[lan]:
            filters.append('--include=*' + ext)
        exclude_dirs = ['.svn', '.cvs', '.hg', '.git', '.bzr']
        for dir in exclude_dirs:
            filters.append('--exclude-dir='+dir)

        param = [self.grep, "-snrP"] + filters + [match_expr, target_File]
        # print(type(param))

        result = ""
        try:
            p = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result, error = p.communicate()
        except Exception as e:
            print(e)
        try:
            result = result.decode('utf-8')
            error = error.decode('utf-8')
        except AttributeError as e:
            pass
        if len(error) != 0:
            print(error.strip())
        # print(result)
        return result



    def parse_match(self, match_vul_str):
        """
        parse every line that greps
        """
        res = VulnerabilityInfo()
        # print(match_vul_str)
        if ':' in match_vul_str:
            try:
                current_dir = os.getcwd()
                if os.path.isdir(self.target_File):
                    line_number_str, res.code_content = re.findall(r':(\d+):(.*)', match_vul_str)[0]
                    res.line_number = int(line_number_str)
                    # res.line_number = line_number_str
                    res.file_abs_path = match_vul_str.split(u':{n}:'.format(n=res.line_number))[0]
                else:
                    line_number_str, res.code_content = re.findall(r'(\d+):(.*)', match_vul_str)[0]
                    res.line_number = int(line_number_str)
                    # res.line_number = line_number_str
                    res.file_abs_path = self.target_File

                res.file_rela_path = res.file_abs_path.replace(current_dir, '')
            except Exception:
                res.file_abs_path = ''
                res.code_content = ''
                res.line_number = 0
        else:
            return None
        sensitive_func = dict_sink[self.language].strip('()').split('|')
        for func in sensitive_func:
            if re.search(func+r'\s*\(', res.code_content) is not None:
                res.func_name = func
        # print(res.file_abs_path, res.func_name)
        res.language = self.language
        # print(res.language)
        return res



    def process(self):
        """
        Detect the command line inection
        """
        match_results = self.regular_match(self.target_File, self.language)
        # print(type(match_results))
        # print(match_results)
        if match_results is None or match_results == '':
            print("[RegExp Match]Sink Function Pattern Not Found!")

        match_vulnerabilities = match_results.strip().split('\n')
        print('Pattern Matching: ',len(match_vulnerabilities))
        confirmed_vulnerabilities = []
        print('Analyzing AST to correct result...')
        for idx, match_vul in enumerate(match_vulnerabilities):
            match_vul = match_vul.strip()
            if match_vul == '':
                continue

            vulnerability = self.parse_match(match_vul)
            if vulnerability is None:
                print("This is not a vulnerability, continue parsing...")
                continue
            # is_test = False
            try:
                is_vul, reason = Core(self.target_File, vulnerability).scan()
                # print(reason)
                if is_vul:
                    # print(vulnerability.file_abs_path, vulnerability.line_number, reason)
                    confirmed_vulnerabilities.append(vulnerability)
            except Exception:
                raise

        return confirmed_vulnerabilities




class Core(object):
    """
    After regular expression match the pattern and make them list of vulnerabilities, this Core would check each of them whether they are annotated, in special path, or be corrected sanitized.
    """
    def __init__(self, target_File_path, vul_res):
        self.target_File = target_File_path
        self.file_path = vul_res.file_abs_path
        self.line_number = vul_res.line_number
        self.code_content = vul_res.code_content
        self.language = vul_res.language
        self.function_name = vul_res.func_name

    def is_special_file(self):
        special_path = [
            'node_modules/',
            '.log',
            '.log.',
        ]
        for path in special_path:
            if path in self.file_path:
                return True
        return False

    def is_annotation(self):
        """
        need improve
        cannot detect if the sink function is in the middle of annotation like
        /*
        system(cmd);
        */
        """
        sed = Tool().sed
        param = [sed, '{ln}!d'.format(ln=self.line_number), self.file_path]

        try:
            p = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result, error = p.communicate()
        except Exception as e:
            print(e)
        try:
            result = result.decode('utf-8')
            error = error.decode('utf-8')
        except AttributeError as e:
            pass
        if len(error) != 0:
            print(error.strip())
        result = result.strip()
        # print(result)
        match_results = re.findall(r'^(#|\/\*|\/\/)+', result)
        return len(match_results) > 0


    def scan(self):
        # print(self.target_File)
        # print(self.file_path)
        if self.is_annotation():
            return False, 'Annotation'
        if self.is_special_file():
            return False, 'Special Files'

        ast = parse_file(
            self.file_path,
            use_cpp=True,
            cpp_path='gcc',
            cpp_args=[
                '-E',
                r'-I/Users/kirk/homework/spring2019/cse637/class_project/cmdDetect/utils/fake_libc_include'
            ])
        checker = SinkChecker(self.file_path, self.line_number, self.function_name, ast, self.language)
        if checker.check_func_called() is False:
            return False, 'Not called'
        # if analyzeFunctionCall(self.line_number, self.function_name):
            # return True, 'Reachable By User Input'
        param = ["python2", "core/data_flow_util.py", str(self.line_number) , self.function_name]

        try:
            p = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            isControllable_str, error = p.communicate()
            isControllable = bool(isControllable_str)
            print("Reachable By User? " + str(isControllable))
            if isControllable:
                return True, 'Reachable By UserInput'
        except Exception as e:
            print(e)

        # if checker.is_param_controllable():
            # return True, 'Function Parameter is user controllable'
        return False, 'No reason'





def scan(target_File, curr_lan_set):
    """
    target_File is absolute path of target file/dir
    """
    found_vul = []
    def results_handler(results):
        if results is not None and isinstance(results, list):
            """
            Personally I tend to write if-else first and place for-loop inside them for performance issue.
            But I think the branch prediction technique in the CPU would take care of this since for a particular
            """
            # remove_path = ''
            # if os.path.isdir(target_File):
            #     remove_path = target_File
            # else:
            #     remove_path = os.path.dirname(target_File)
            # current_dir = os.getcwd()

            for res in results:
            #     res.file_rela_path = res.file_abs_path.replace(current_dir, '')
                found_vul.append(res)

    try:
        pool = multiprocessing.Pool()
        for lan in curr_lan_set:
            print("processing ",lan, "language files")
            pool.apply_async(scan_single_lan, args=(target_File, lan), callback=results_handler)

        pool.close()
        pool.join()
    except Exception:
        raise
    list_to_prettytable(found_vul)



def scan_single_lan(target_File, language):
    try:
        return CmdInjDetect(target_File_path=target_File, lan=language).process()
    except Exception:
        raise