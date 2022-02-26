from Expression import *
from Lexer import *


class Not_Parsed(Exception):
    pass


class Parser:
    def __init__(self, input):

        self.input = Lexer(input).lex_Program()
        self.position = 0
        self.EOS = ';'

    def look_char(self):
        return self.input[self.position]

    def parse_block(self):

        c = self.look_char()
        p = self.parse_instruction()

        while not (p == "end" or c == self.EOS):
            q = self.parse_instruction()
            if q == 'end' or c == self.EOS:
                return p
            p = Composition(p, q)

            c = self.look_char()
            print(self.position)
            self.position+=1
        return p

    def parse_Program(self):
        return self.parse_block()

    def parse_instruction(self):
        c = self.look_char()
        if c[0] == IDENTIFIER:

            self.position += 1
            if c[1] == "let":

                return self.parse_Var()
            elif c[1] == "if":
                return self.parse_If()
            elif c[1] == "while":

                return self.parse_While()
            elif c[1] == "begin":
                self.position += 1
                return self.parse_block()
            elif c[1] == "end":
                return c[1]
            elif c[1] == "def":
                return self.parse_Function()
            elif c[1] == 'input':
                return self.parse_Input()
            elif c[1] == "write":
                return self.parse_Write()
            elif c[1] == "skip":
                return Skip()
            elif c[1] == "do":
                return self.parse_Do_Function()
            elif c[1] == "append":
                return self.parse_Append()
            elif c[1] == "delete":
                return self.parse_Delete()
            elif c[1] == "import":
                return self.parse_Import()
            else:
                return self.parse_sum()
        elif c == self.EOS:
            return 'end'
        else:
            return self.parse_sum()

    def parse_Var(self):
        word = self.look_char()[1]
        indexes = self.tab_algorithm()
        char = self.look_char()[0]
        if indexes:
            if char == EQUALS:
                s = self.parse_sum()
                return IndexVar(word, s, indexes)
        else:
            if char == EQUALS:
                s = self.parse_sum()
                return Var(word, s)

    def tab_algorithm(self):
        c = self.look_char()
        if c[0] != LARRAY:
            return []
        indexes = []
        while True:
            if c[0] == LARRAY:
                s = self.parse_sum()
                self.position -= 1
                c = self.look_char()
                if c[0] == RARRAY:
                    indexes.append(s)
                    self.position += 1
                    c = self.look_char()
                    continue
                else:
                    raise Not_Parsed("'[' ependent")
            else:
                return indexes

    def parse_If(self):
        c = self.parse_sum()
        t = self.parse_instruction()
        s = self.look_char()
        if s[1] == 'else' and s[0]==IDENTIFIER:
            q = self.parse_instruction()
            return If(c, t, q)
        else:
            raise Not_Parsed("'else' expendent")

    def parse_Input(self):
        self.position+=1
        s = self.look_char()
        return Input(s[1])

    def parse_Write(self):
        s = self.parse_sum()
        return Write(s)

    def parse_Import(self):
        s = self.look_char()[1]
        file = open(s + '.g')
        string = ''
        for i in file.readlines():
            string += i
        parser = Parser(string)
        return parser.parse_Program()

    def parse_Function(self):
        s = self.look_char()[1]

        self.position += 1

        p = self.parse_block()
        return Function(s, p)

    def parse_Do_Function(self):

        return EvalFunction(self.look_char()[1])

    def parse_While(self):
        c = self.parse_sum()
        b = self.parse_instruction()
        return While(c, b)

    def parse_sum(self):
        e = self.parse_mult()
        c = self.look_char()
        while c[0] == SUM or c[0] == SUB:
            self.position += 1
            f = self.parse_mult()
            e = Binary_operator(c[0], e, f)
            c = self.look_char()

        return e

    def parse_mult(self):
        e = self.parse_condition()
        c = self.look_char()
        while c[0] == MUL or c[0] == DIV or c[0] == MOD:
            self.position += 1
            f = self.parse_condition()
            e = Binary_operator(c[0], e, f)
            c = self.look_char()

        return e

    def parse_condition(self):
        e = self.parse_term()
        c = self.look_char()
        while c[0] == EQUALS or c[0] == SMALLER or c[0] == BIGGER or c[0] == OR or c[0] == AND:
            self.position += 1
            f = self.parse_term()
            e = Binary_operator(c[0], e, f)
            c = self.look_char()

        return e

    def parse_tab(self):
        self.position += 1
        tab = []
        while self.input[self.position] != self.EOS:
            if self.input[self.position][0]==IDENTIFIER:
                tab.append(self.parse_sum())
            c = self.look_char()
            if c[0] == COMMA:
                self.position += 1
                continue
            elif c == RARRAY:

                self.position += 1
                break
            elif c == LARRAY:

                self.position += 1
                tab.append(self.parse_tab())
            else:
                raise Not_Parsed("',' expendent")
        return Constant(tab)

    def parse_term(self):
        c = self.look_char()
        if c[0] == LPAREN:
            return self.parse_paren()
        elif c[0] == LARRAY:
            return self.parse_tab()
        elif c[0]==';':
            return
        elif c[0] == STRING:
            return Constant(c[1])
        elif c[0] == IDENTIFIER:
            return self.parse_Variable()
        elif c[0] == INT or c[0] == FLOAT:
            return Constant(c[1])

        else:
            print(c[0])
            raise Not_Parsed()
    def parse_Variable(self):
        s = self.look_char()
        if s[1] == 'true':
            return Constant(True)
        elif s[1] == 'false':
            return Constant(False)

        elif s[0]==IDENTIFIER:
            if s[0]==LARRAY:
                s2=self.tab_algorithm()
                return IndexVariable(s[1], s2)
            return Variable(s[1])

    def parse_paren(self):
        self.position += 1
        e = self.parse_sum()
        if self.look_char()[0] == LPAREN:
            self.position += 1
            return e
        else:
            raise Not_Parsed("')' expendent")

    def parse_Delete(self):
        s = self.look_char()
        return Del(s[1])

    def parse_Append(self):
        s = self.look_char()
        indexs = self.tab_algorithm()
        v = self.parse_sum()
        return Append(s[1], v, indexs)
