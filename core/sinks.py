"""
list all the sink functions of different languages that 
"""

dict_sink = {'c' : r'(system|exec|execlp)'}

input_func = {'c': ['scanf', 'fgets', 'gets', 'scanf', 'fscanf', 'sscanf','scanf_s', 'fscanf_s', 'sscanf_s']}

# function-parameter-controllable
fpc_reg_ex = '\s*\((.*)(?:\))'
fpc_single = '\\b[f]{fpc}'.format(fpc=fpc_reg_ex)
fpc_multi = '\\b[f]{fpc}'.format(fpc=fpc_reg_ex)