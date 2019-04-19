"""
    some util functions that are used to read files/directories
"""



import os
import re
import sys
import time



class Directory(object):
    def __init__(self, abs_path):
        """
            absolute path of dir, no trailing slash
        """
        self.absolute_path = abs_path

    file_sum = 0
    result = {}
    files = []
    type_list = {}

    def extract_meta(self, file_abs_path, filename):
        file_name, file_ext = os.path.splitext(filename)
        self.file_sum += 1
        file_rela_path = file_abs_path.replace(self.absolute_path, '')
        self.type_list.setdefault(file_ext.lower(), []).append(file_rela_path)
        self.files.append(file_rela_path)


    def iterate_File(self, File_abs_path):
        """
            iterate over the whole File
            File can be a single file or a directory
            filename = file_name + file_ext
        """
        try:
            if os.path.isfile(File_abs_path):
                file_dir, filename = os.path.split(File_abs_path)
                self.extract_meta(File_abs_path, filename)
            else:
                """
                File_abs_path points to a directory
                """
                for Filename in os.listdir(File_abs_path):
                    if not self.in_filter(Filename):
                        try:
                            child_abs_path = os.path.join(File_abs_path, Filename)
                        except UnicodeDecodeError as e:
                            print(e)
                            continue
                    else:
                        continue

                    if os.path.isdir(child_abs_path):
                        self.iterate_File(child_abs_path)
                    if os.path.isfile(child_abs_path):
                        self.extract_meta(child_abs_path, Filename)
        except OSError as e:
            exit()



    def in_filter(self, filename):
        whitelist = [
            'node_modules',
            'vendor'
        ]
        if filename in whitelist:
            return True
        else:
            return False


    def collect_files(self):
        time_st = time.clock()
        self.iterate_File(self.absolute_path)
        for ext, filelist in self.type_list.items():
            ext = ext.strip()
            self.result[ext] = {'count': len(filelist), 'list':filelist}
        time_ed = time.clock()
        # sort result in lexicographical order of ext
        # self.result = sorted(self.result.items(), key=lambda t:t[0], reverse=False)
        return self.result, self.file_sum, time_ed-time_st


class Tool:
    def __init__(self):

        # `sed`
        if os.path.isfile('/bin/sed'):
            self.sed = '/bin/sed'
        elif os.path.isfile('/usr/bin/sed'):
            self.sed = '/usr/bin/sed'
        elif os.path.isfile('/usr/local/bin/sed'):
            self.sed = '/usr/local/bin/sed'
        else:
            self.grep = 'sed'


        # `grep` (`ggrep` on Mac)
        if os.path.isfile('/bin/grep'):
            self.grep = '/bin/grep'
        elif os.path.isfile('/usr/bin/grep'):
            self.grep = '/usr/bin/grep'
        elif os.path.isfile('/usr/local/bin/grep'):
            self.grep = '/usr/local/bin/grep'
        else:
            self.grep = 'grep'

        # `find` (`gfind` on Mac)
        if os.path.isfile('/bin/find'):
            self.find = '/bin/find'
        elif os.path.isfile('/usr/bin/find'):
            self.find = '/usr/bin/find'
        elif os.path.isfile('/usr/local/bin/find'):
            self.find = '/usr/local/bin/find'
        else:
            self.find = 'find'

        if 'darwin' == sys.platform:
            ggrep = ''
            gfind = ''
            for root, dir_names, file_names in os.walk('/usr/local/Cellar/grep'):
                for filename in file_names:
                    if 'ggrep' == filename or 'grep' == filename:
                        ggrep = os.path.join(root, filename)
            for root, dir_names, file_names in os.walk('/usr/local/Cellar/findutils'):
                for filename in file_names:
                    if 'gfind' == filename:
                        gfind = os.path.join(root, filename)
            if ggrep == '':
                print("brew install grep pleases!")
                sys.exit(0)
            else:
                self.grep = ggrep
            if gfind == '':
                print("brew install findutils pleases!")
                sys.exit(0)
            else:
                self.find = gfind
