import sys
from cli import CLI

if __name__ == "__main__":
    cli = CLI(sys.stdin, sys.stdout)
    cli.start()