from tools.finder import read
from tools.parser import parse
from tools.webclient import WebClient
from tools.execute import execute


def main():
    # imports settings and sequences from .\library folder and parse them into objects
    data = read()
    sequences = parse(data)
    WebClient()
    execute(sequences)


if __name__ == '__main__':
    main()
