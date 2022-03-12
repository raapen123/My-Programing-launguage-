from settings import *
from Parser import *


class Position:
    def __init__(self, idx, ln, col):
        self.idx = idx
        self.ln = ln
        self.col = col

    def advance(self, current_char):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col)


class Token:
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

    def __repr__(self):
        if self.value is not None: return f'{self.type}:{self.value}'
        return f'{self.type}'


class Error:
    def __init__(self, error_name, details, line=None):
        self.details = details
        self.error_name = error_name
        self.line = line

    def as_string(self):
        if self.line is not None:
            return f'In line: {self.line} \n{self.error_name}: {self.details}'
        else:
            return f'{self.error_name}: {self.details}'


class IllegalCharError(Error):
    def __init__(self, details, line):
        super().__init__("IllegalCharError", details, line)


class InvalidSyntax(Error):
    def __init__(self, details):
        super().__init__("InvalidSyntax", details)


class Lexer:
    def __init__(self, _input):
        self.text = _input
        self.pos = Position(-1, 0, -1)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t\n':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char.lower() in list(ALPHABET+'_'):
                tokens.append(self.make_identifier())
            elif self.current_char == '"' or self.current_char == "'":
                tokens.append(self.make_string())
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(SUM))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(COLON))
                self.advance()
            elif self.current_char == '#':
                tokens.append(Token(HASHTAG))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(SUB))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(MOD))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(LARRAY))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(RARRAY))

                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(COMMA))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(RBUCKLE))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(LBUCKLE))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(EQUALS))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(BIGGER))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(SMALLER))
                self.advance()
            elif self.current_char == '|':
                tokens.append(Token(OR))
                self.advance()
            elif self.current_char == '&':
                tokens.append(Token(AND))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(DOT))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'", self.pos.copy().ln)
        tokens.append(Token(EOF))
        return tokens, None

    def make_number(self):
        number = ''
        dot = 0
        while (self.current_char in list(DIGITS + '.')) and (self.current_char is not None):
            if self.current_char == '.':
                if dot == 1: break
                dot += 1
                number += self.current_char
            else:
                number += self.current_char
            self.advance()
        if dot == 0:
            return Token(INT, int(number))
        else:
            return Token(FLOAT, float(number))

    def make_identifier(self):
        text = ''
        while (self.current_char in list(DIGITS + ALPHABET + '_')) and (self.current_char is not None):
            text += self.current_char
            self.advance()
        return Token(IDENTIFIER, text)

    def make_string(self):
        string = ''
        self.advance()
        settings = False
        while self.current_char != '"' and self.current_char != "'":
            if self.current_char == '\\':
                settings = True
                self.advance()
                continue
            if self.current_char == 'n' and settings:
                string += '\n'
                settings = False
            elif self.current_char == '\\' and settings:
                string += '\\'
                settings = False
            else:

                string += self.current_char
            self.advance()
        return Token(STRING, string)


def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    parser = Parser(tokens)
    program, errors2 = parser.parse_Program(False)
    if error is None:
        return tokens, error, program, errors2
    else:
        return tokens, error, Skip()
