##############################
### Impossible Language    ###
### By Andrei Merryweather ###
##############################

# ANCHOR - Imports
import string
from python.tokenSymbols import makeTokenSymbols

# ANCHOR - Constants
NUMBERS = '0123456789'
LETTERS = string.ascii_letters
NUMLETS = LETTERS + NUMBERS

# ANCHOR - Token types
TT_NUMBER = 'NUMBER'
TT_TEXT   = 'TEXT'
TT_SET    = 'SET'
TT_OUT    = 'OUT'

# ANCHOR - Token symbols
TOKEN_SYMBOLS = makeTokenSymbols(3)
TS_COMMENT = TOKEN_SYMBOLS[0] # Base: ';'
TS_SET = TOKEN_SYMBOLS[1] # Base: '%'
TS_OUT = TOKEN_SYMBOLS[2] # Base: '>'
TS_STRING = TOKEN_SYMBOLS[3] # Base: '"'

# ANCHOR - Token class
class Token:
    def __init__(self, _type, _value=None) -> None:
        self.type = _type
        self.value = _value
    
    def __repr__(self) -> str:
        return f'<{self.type}{"-" + self.value if self.value else ""}>'

# ANCHOR - Lexer class
class Lexer:
    def __init__(self, txt, _base=False) -> None:
        self.text = txt
        self.pos = -1
        self.cur_char = ''
        self.advance()

        self.base = _base
    
    def advance(self):
        self.pos += 1
        self.cur_char = self.text[self.pos] if self.pos < len(self.text) else None

    def makeNumber(self):
        result = ''
        while self.cur_char and self.cur_char in NUMBERS:
            result += self.cur_char
            self.advance()
        return result

    def makeText(self):
        result = ''
        self.advance() # Advance into string
        while self.cur_char and self.cur_char != (TS_STRING if not self.base else '"'):
            result += self.cur_char
            self.advance() # Advance in string
        
        if self.cur_char == (TS_STRING if not self.base else '"'):
            self.advance() # Advance out of string
            return result
        _ = '"'
        raise SyntaxError(f'TEXT must be closed with "{(TS_STRING if not self.base else _)}"')

    def skipComments(self):
        while self.cur_char != '\n':
            self.advance()

    def makeTokens(self):
        tokens = []

        while self.cur_char != None:
            # Skip through whitespace
            if self.cur_char in ' \n\t':
                self.advance()
            
            # Skip comments
            elif self.cur_char == (TS_COMMENT if not self.base else ';'):
                self.skipComments()
            
            # make numbers
            elif self.cur_char in NUMBERS:
                tokens.append(Token(TT_NUMBER, self.makeNumber()))
            
            # make text
            elif self.cur_char == (TS_STRING if not self.base else '"'):
                tokens.append(Token(TT_TEXT, self.makeText()))
            
            # set token
            elif self.cur_char == (TS_SET if not self.base else '%'):
                tokens.append(Token(TT_SET))
                self.advance()
            
            # out token
            elif self.cur_char == (TS_OUT if not self.base else '>'):
                tokens.append(Token(TT_OUT))
                self.advance()
            
            # unknown tokens
            # may cause program to not run :)
            else:
                raise SyntaxError(f'Invalid token "{self.cur_char}" at position {self.pos}')
        return tokens

# ANCHOR - Parser class
class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.cur_tok = None
        self.position = -1
        self.advance()

        self.cells = [0]*80000
    
    def advance(self):
        self.position += 1
        self.cur_tok = self.tokens[self.position] if self.position < len(self.tokens) else None
    
    def get(self, index):
        if index < len(self.cells):
            return self.cells[index]
        raise IndexError(f'Couldn\'t find cell at index "{index}"')
    
    def set(self, index, value):
        if index < len(self.cells):
            self.cells[index] = value
            return
        raise IndexError(f'Couldn\'t find cell at index "{index}"')

    def checkToken(self, _type):
        return self.cur_tok.type == _type

    def match(self, _type):
        if self.cur_tok.type == _type:
            return
        raise SyntaxError(f'Expected "{_type}", got "{self.cur_tok.type}"')

    def parseTokens(self):
        while self.cur_tok != None:
            # Base: > TEXT|NUMBER
            if self.cur_tok.type == TT_OUT:
                self.advance()
                if self.cur_tok != None and not self.checkToken(TT_TEXT) and not self.checkToken(TT_NUMBER):
                    raise SyntaxError(f'Expected "TEXT" or "NUMBER", got "{self.cur_tok.type}"')

                if self.cur_tok.type == TT_TEXT:
                    print(self.cur_tok.value)
                
                if self.cur_tok.type == TT_NUMBER:
                    print(self.get(int(self.cur_tok.value)))

                self.advance()
            
            # Base: % NUMBER TEXT|NUMBER
            elif self.cur_tok.type == TT_SET:
                self.advance()
                if self.cur_tok != None:
                    self.match(TT_NUMBER)
                else:
                    break
                cellNum = self.cur_tok.value
                self.advance()

                if self.cur_tok != None and not self.checkToken(TT_TEXT) and not self.checkToken(TT_NUMBER):
                    raise SyntaxError(f'Expected "TEXT" or "NUMBER", got "{self.cur_tok.type}"')
                
                self.set(int(cellNum), self.cur_tok.value)
                self.advance()

# ANCHOR - Test function
def test():
    lex = Lexer('% 10 50 > 10', True)
    tokens = lex.makeTokens()
    par = Parser(tokens)
    par.parseTokens()

# ANCHOR - Main check
if __name__ == '__main__':
    test()
