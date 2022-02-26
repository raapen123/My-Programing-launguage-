from settings import *


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0
        self.EOS = ';'
        self.input.replace(' ', '\n')
        self.input.replace(' ', '\t')
        self.input += self.EOS

    def look_char(self):
        while self.input[self.position] == ' ' and self.input[self.position] != self.EOS:
            self.position += 1
        return self.input[self.position]

    def lex_Program(self):
        program_tokens = []
        while self.input[self.position] != self.EOS:
            c = self.look_char()
            print(c)
            if c in DIGITS:
                program_tokens.append(self.lex_int())
            elif c == '(':
                program_tokens.append([LPAREN, None])
            elif c == ')':
                program_tokens.append([RPAREN, None])
            elif c == '[':
                program_tokens.append([LARRAY, None])
            elif c == ']':
                program_tokens.append([RARRAY, None])
            elif c.isalpha():
                program_tokens.append([IDENTIFIER, self.lex_identiefier()])
                self.position-=1
            elif c == '"':
                program_tokens.append([STRING, self.lex_string()])
            c = self.look_char()
            if c == '+':
                program_tokens.append([SUM, None])
            elif c == '-':
                program_tokens.append([SUB, None])
            elif c == '*':
                program_tokens.append([MUL, None])
            elif c == '/':
                program_tokens.append([DIV, None])
            elif c == '%':
                program_tokens.append([MOD, None])
            elif c == '=':
                program_tokens.append([EQUALS, None])
            elif c == '>':
                program_tokens.append([BIGGER, None])
            elif c == '<':
                program_tokens.append([SMALLER, None])
            elif c == '|':
                program_tokens.append([OR, None])
            elif c == '&':
                program_tokens.append([AND, None])
            elif c == ',':
                program_tokens.append([COMMA, None])
            if self.input[self.position] == self.EOS:
                break
            self.position+=1
        program_tokens.append(self.EOS)
        return program_tokens

    def lex_int(self):
        n = 0
        dot = 0
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        while (self.input[self.position] in digits) and self.input[self.position] != self.EOS:
            n *= 10
            n += int(self.input[self.position])
            self.position += 1
        if self.input[self.position] == '.':
            self.position += 1
            while (self.input[self.position] in digits) and self.input[self.position] != self.EOS:
                dot /= 10
                dot += int(self.input[self.position])
                self.position += 1
            dot /= 10
            return [FLOAT, n + dot]
        else:
            return [INT, n]

    def lex_identiefier(self):
        self.skip_whitechars()

        s = ''
        c = self.input[self.position]
        while c.isalnum() and c != self.EOS and c != '"':
            s = s + c
            self.position += 1
            c = self.input[self.position]
        return s

    def skip_whitechars(self):
        while self.input[self.position] == ' ' and self.input[self.position] != self.EOS:
            self.position += 1

    def lex_string(self):
        self.skip_whitechars()

        self.position+=1
        s = ''
        c = self.input[self.position]
        while c != self.EOS and c != '"':
            s = s + c
            self.position += 1
            c = self.input[self.position]
        return s

