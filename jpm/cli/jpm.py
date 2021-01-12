import os
import sys


def play(args):
    pass


def main(args):
    """Run the program"""
    try:
        play(args)
    except Exception as e:
        print(e, file=sys.stderr)
        return not os.EX_OK
    return os.EX_OK
