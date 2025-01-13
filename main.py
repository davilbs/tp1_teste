import sys
from cli import CLI
from database import create_database

if __name__ == "__main__":
    create_database()
    cli = CLI(sys.stdin, sys.stdout)
    cli.start()
