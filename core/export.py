"""
export scan result to File
"""

import os
import json

from prettytable import PrettyTable


def write_to_file(target, filename=None):
    """
    Export result to file
    :param target: scan target
    :param filename: filename to save
    """
    if not filename:
        print('[EXPORT] No filename given, do nothing.')
        return False



def list_to_prettytable(found_list):
    """
    print vulnerability list in console
    :param found_list: all vulnerabilities that found
    [ VulnerabilityInfo, .... ]
    """
    if len(found_list) == 0:
        print("No vulnerability found")
    else:
        output_table = PrettyTable(['#', 'Target File', 'Source Code Content'])
        output_table.align = 'l'
        for idx, info in enumerate(found_list):
            try:
                code = info.code_content[:50].strip()
            except AttributeError:
                code = info.code_content.decode('utf-8')[:100].strip()

            row = [idx, info.file_rela_path, code]
            output_table.add_row(row)

        print(output_table)
