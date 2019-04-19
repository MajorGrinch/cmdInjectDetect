"""
    Running the tool in command line interface mode
"""



import os
import re
from .file_util import Directory
from .languages import supported_lan
from .export import write_to_file
from .engine import scan

def start(target_File_path, output):
    try:
        if not os.path.isabs(target_File_path):
            target_File_path = os.path.abspath(target_File_path)

        print("Target directory: {0}".format(target_File_path))
        target_File_path = target_File_path.rstrip('/')

        ext_cnt_files, file_cnt, duration = Directory(target_File_path).collect_files()

        src_cnt = 0
        for lan in supported_lan:
            exts = supported_lan[lan]
            for ext in exts:
                src_cnt += ext_cnt_files[ext]['count']

        print("Target directory scan complete. Find {0} source code files. Use {1} seconds.".format(src_cnt ,duration))
        # print(ext_to_lan)
        # run scan
        scan(target_File_path)

    except Exception as e:
        print(e)

    write_to_file(target=target_File_path, filename=output)
