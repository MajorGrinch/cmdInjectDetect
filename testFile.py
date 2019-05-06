"""
some test functions
"""


import subprocess

param = ["python2", "core/data_flow_util.py", str(25) , "system"]

try:
    p = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = p.communicate()
    result = bool(result)
    print(result)
except Exception as e:
    print(e)