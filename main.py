from tools.finder import read
from tools.parser import parse
from tools.webclient import Web_client
from tools.execute import execute


def main():
    # imports settings and sequences from .\scenario folder and parse them into objects
    data = read()
    sequences = parse(data)
  #  Web_client()
    execute(sequences)


if __name__ == '__main__':
    main()
