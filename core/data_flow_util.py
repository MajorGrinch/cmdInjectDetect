
"""
interprocedure data flow analysis
should run under python2
"""

from joern.all import JoernSteps
import re
import os


transfer_funcs = {'c': ['fscanf','sscanf', 'fscanf_s', 'sscanf_s', 'sprintf', 'snpirntf', 'strcpy', 'strncpy', 'strcat', 'strncat', 'memcpy']}

userinput_funcs = {'c': ['scanf', 'fgets', 'gets', 'scanf_s', 'getenv', 'argv' ]}


transfer_funcs_re_expr = '(' + '|'.join(transfer_funcs['c']) + r')\s*\('

userinput_funcs_re_expr = '(' + '|'.join(userinput_funcs['c']) + r')\s*\('

db_url = 'http://3.83.184.179:7474/db/data/'


transfer_funcs_patt = re.compile(transfer_funcs_re_expr)
userinput_funcs_patt = re.compile(userinput_funcs_re_expr)


"""
query = 'getArguments("*system*", "0").definitions().defines()

find the symbol used as the first argument to sensitive function calls
"""

"""
query = 'getArguments("*system*", "0").definitions().defines()'
"""

checked_nodes = set() # nodes that have already been visited

def reachableByInput(node):
    """decide whether this node can be reached by user input

        First check all the reachable node by current node
        if we found some assginment, input, or string operation
        on current node, then we trace relevant nodes until we found
        possible input behaviors or the data flow ends.
    """
    # print("111"*30)
    checked_nodes.add(node)
    # print(node)
    out_edge_iterator = node.match_outgoing()
    # in_edge_iterator = node.match_incoming()

    cfg_next_list = []
    pdg_next_list = []
    pdg_prev_list = []

    for out_edge in out_edge_iterator:
        if out_edge.rel.type == "REACHES":
            pdg_next_list.append(out_edge.end_node)
        elif out_edge.rel.type == "POST_DOM":
            pdg_prev_list.append(out_edge.end_node)
        elif out_edge.rel.type == "FLOWS_TO":
            cfg_next_list.append(out_edge.end_node)

    if traceBackVariable(node):
        return True
    # check that the def has data dep on previous statement

    for next_node in pdg_next_list:
        """find out if this variable is modified before reaching
            the sensitive function calls
        """
        # print(next_node["code"])
        # nodeIdx = next_node.uri.path.segments[-1]
        if transfer_funcs_patt.search(next_node["code"]):
            if traceBackVariable(next_node):
                return True
    return False


def containsUserInput(node):
    return userinput_funcs_patt.search(node["code"]) is not None

def traceBackVariable(node):
    """ find out if this node depend on previous statements's data
    """
    checked_nodes.add(node)
    print(node)
    if containsUserInput(node):
        return True
    for edge in node.match_incoming():
        if edge.rel.type == "REACHES" and edge.start_node not in checked_nodes:
            ret_val = traceBackVariable(edge.start_node)
            if ret_val is True:
                return True

    return False


def analyzeFunctionCall(func_line, func_name):
    # callexpr_node = get_call_by_line_name(func_line, func_name)
    query = 'getArguments("*system*", "0").definitions().defines()'
    j = JoernSteps()
    j.setGraphDbURL(db_url)
    j.connectToDatabase()
    res = j.runGremlinQuery(query)
    print(res)
    is_controllable_by_user = reachableByInput(res[0])
    print(is_controllable_by_user)
    return is_controllable_by_user


def get_call_by_line_name(line, func_name):
    j = JoernSteps()
    j.setGraphDbURL(db_url)
    my_steps_dir = os.getcwd() + '/mysteps'
    j.addStepsDir(my_steps_dir)
    j.connectToDatabase()
    query = 'OR(getCallsTo("*{0}*").parents(), getCallsTo("*{0}*").ithArguments("0"))'.format(func_name)
    res = j.runGremlinQuery(query)
    for i in range(len(res)):
        r = res[i]
        if r["location"]:
            r_line = r["location"].split(':')[0]
            if int(r_line) == line:
                print(res[i+1])
                return res[i+1]


result = analyzeFunctionCall(25, "system")
print(result)