import sys
from python.impossible import *

def main():
    if len(sys.argv) == 1:
        raise RuntimeError('File not specified')

    file = open(sys.argv[1])
    content = file.read()
    file.close()

    isBase = False
    options = sys.argv[1:len(sys.argv)]

    if '--tokens' in options:
        print(f'Session tokens:')
        for n, v in zip(["COMMENT", "OUT", "SET", "STRING"], TOKEN_SYMBOLS):
            print(n, f'"{v}"')
    
    if '--base' in options:
        isBase = True
    
    lexer = Lexer(content, isBase)
    parser = Parser(lexer.makeTokens())
    parser.parseTokens()

if __name__ == '__main__':
    main()