import subprocess
from sys import argv


if len(argv) > 1:
    command = 'joern {0}'.format(argv[1])
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = p.communicate()
        print(result)
    except Exception as e:
        pass
