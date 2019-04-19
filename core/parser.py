"""
    Accept a AST as input and parse it
"""


from pycparser import c_parser, c_ast, parse_file

ast = None

def is_sink_function(func_name, func_params):
    """
    decide whether this function call is a sink function
    """
    is_controllable = -1