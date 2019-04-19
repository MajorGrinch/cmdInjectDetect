"""
define the structure of finding vulnerabilities
"""

class VulnerabilityInfo:
    def __init__(self):
        self.file_abs_path = None
        self.file_rela_path = None
        self.language = ''
        self.line_number = None
        self.code_content = None
        self.func_name = ''


    def to_dict(self):
        _dict = {}
        _dict.update(self.__dict__)
        return _dict