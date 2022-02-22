from tools.finder import read
from tools.parser import parse
from tools.webclient import Web_client
from tools.run import run


def main():
    # imports settings and sequences from .\sequence folder and parse them into objects
    seq = read()
    objs = parse(seq)
    Web_client()

    # executes multiple files of multiple objects starting with settings
    for obj in objs:
        for o in obj:
            run(o)


if __name__ == '__main__':
    main()
