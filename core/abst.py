"""
Implement analysis on target sink function.

In summary, one sinkchecker instance analyze one function call
"""

from pycparser import c_ast, c_parser, parse_file
from .sinks import input_func, str_func

class SinkChecker(object):
    def __init__(self, target_file_path, line_number, function_name, ast, language):
        self.file_path = target_file_path
        self.line_number = line_number
        self.function_name = function_name
        self.ast = ast
        self.language = language
        self.func_param_list = None
        # print(self.file_path, self.line_number)
        # print(self.input_functions)

    # def get_FuncCall_by_funcname(self, func_name, node):
    #     if func_name is None or func_name == '':
    #         return None
    #     for nextNode in node:
    #         pass


    def check_func_called(self):
        """
        see whether this function is called in this source code file
        """
        v = FuncCallVisitor(self.function_name, self.line_number)
        v.visit(self.ast)
        self.func_param_list = v.params
        # print(self.func_param_list)
        return v.func_is_called


    def get_func_params(self):
        if self.func_param_list is not None:
            return self.func_param_list
        self.check_func_called()
        return self.func_param_list

    def is_param_controllable(self):
        tv = TraceVariable(self.func_param_list[0], self.language)
        tv.visit(self.ast)
        return tv.is_from_input


class TraceVariable(c_ast.NodeVisitor):
    def __init__(self, var_name, language):
        self.target_var = var_name
        self.input_functions = input_func[language]
        self.is_from_input = False

    def visit_FuncCall(self, node):
        if node.name.name in self.input_functions:
            # print('input function: ', node.name.name)
            # print(node.args)
            for param in node.args:
                # print(repr(param))
                # if getattr(param, 'name', None) == self.target_var:
                    # self.is_from_input = True
                if self.target_var in repr(param):
                    self.is_from_input = True


class TraceStrFunc(c_ast.NodeVisitor):
    def __init__(self, var_name, language):
        self.target_var = var_name
        self.str_func = str_func[language]
        self.is_from_input = False
        self.target_passed_by = None

    def visit_FuncCall(self, node):
        if node.name.name in self.str_func:
            dest_var = node.args.exprs[0].name
            src_var = node.args.exprs[1].name
            # print(node.args.exprs)
            if self.target_var == dest_var:
                if 'argv' in repr(src_var):
                    self.is_from_input = True
                else:
                    self.target_passed_by = src_var

"""
traverse the whole ast to check whether a given function call
on the specific line gets called
"""
class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self, funcname, line_number):
        self.func_name = funcname
        self.line_number = line_number
        self.func_is_called = False
        self.params = []

    def visit_FuncCall(self, node):
        if node.name.name == self.func_name and self.line_number == node.name.coord.line:
            # print('%s called at %s' % (self.func_name, node.name.coord))
            self.func_is_called = True
            if node.args:
                # print(node.args)
                for param in node.args:
                    if getattr(param, 'name', None) is not None:
                        self.params.append(param.name)
                # print(type(node.args))
