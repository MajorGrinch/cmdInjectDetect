"""
list supported languages and their related operations
"""



supported_lan = {'c': ['.c'], 'php': ['.php', '.php4', '.php5']}
# ext_to_lan = {'.c': 'c', '.php' : 'php', '.php4' :'php', '.php5': 'php'}

def get_ext_to_lan():
    ext_to_lan = dict()
    for lan in supported_lan:
        exts = supported_lan[lan]
        for ext in exts:
            ext_to_lan[ext] = lan
    return ext_to_lan

ext_to_lan = get_ext_to_lan()