"""
main function
"""

import sys
import time
import argparse
from . import cli


def main():
    try:
        time_st = time.time()
        argparser = argparse.ArgumentParser('Command Line Injection Detection')

        argparser.add_argument('-t', '--target', help='file, folder')
        argparser.add_argument('-o', '--output', help='output result to file')

        args = argparser.parse_args()
        cli.start(args.target, args.output)
        time_ed = time.time()
        print('Scan complete! Duration: {0}s'.format(time_ed-time_st))

    except Exception as e:
        pass


if __name__ == '__main__':
    main()
