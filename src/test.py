from Expression import *


class Not_Parsed(Exception):
    pass


class Parser:
    def __init__(self, input):

        self.input = input
        self.position = 0

        self.EOS = ';'
        self.input = self.input.replace("\n", ' ')
        self.input = self.input.replace("\t", ' ')
        self.input += self.EOS

    def skip_whitechars(self):
        while self.input[self.position] == ' ' and self.input[self.position] != self.EOS:
            self.position += 1

    def look_char(self):
        self.skip_whitechars()
        return self.input[self.position]

    def look_word(self):
        self.skip_whitechars()

        s = ''
        c = self.input[self.position]
        while c.isalnum() and c != self.EOS:
            s = s + c
            self.position += 1
            c = self.input[self.position]
        return s

    def parse_block(self):

        c = self.look_char()
        p = self.parse_instruction()

        while not (p == "end" or c == self.EOS):
            q = self.parse_instruction()
            if q == 'end' or c == self.EOS:
                return p
            p = Composition(p, q)

            c = self.look_char()
        return p

    def parse_Program(self):
        return self.parse_block()

    def parse_instruction(self):
        c = self.look_char()
        if c.isalpha():
            s = self.look_word()
            if s == "let":

                return self.parse_Var()
            elif s == "if":
                return self.parse_If()
            elif s == "while":

                return self.parse_While()
            elif s == "begin":
                self.position += 1
                return self.parse_block()
            elif s == "end":
                return s
            elif s == "def":
                return self.parse_Function()
            elif s == 'input':
                return self.parse_Input()
            elif s == "write":
                return self.parse_Write()
            elif s == "skip":
                return Skip()
            elif s == "do":
                return self.parse_Do_Function()
            elif s == "append":
                return self.parse_Append()
            elif s == "delete":
                return self.parse_Delete()
            elif s=="import":
                return self.parse_Import()
            else:
                return self.parse_sum()
        elif c == self.EOS:
            return 'end'
        else:
            return self.parse_sum()

    def parse_Var(self):
        word = self.look_word()
        indexes = self.tab_algorithm()
        char = self.look_char()
        if indexes:
            if char == '=':
                self.position += 1
                s = self.parse_sum()
                return IndexVar(word, s, indexes)
        else:
            if char == '=':
                self.position += 1
                s = self.parse_sum()
                return Var(word, s)

    def tab_algorithm(self):
        c = self.look_char()
        if c!='[':
            return []
        indexes = []
        while True:
            if c == '[':
                s = self.parse_sum()
                self.position -= 1
                c = self.look_char()
                if c == ']':
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
        s = self.look_word()
        if s == 'else':
            q = self.parse_instruction()
            return If(c, t, q)
        else:
            raise Not_Parsed("'else' expendent")

    def parse_Input(self):
        s = self.look_word()
        return Input(s)

    def parse_Write(self):
        s = self.parse_sum()
        return Write(s)
    def parse_Import(self):
        s=self.look_word()
        file=open(s+'.g')
        string=''
        for i in file.readlines():
            string+=i
        parser=Parser(string)
        return parser.parse_Program()

    def parse_Function(self):
        s = self.look_word()

        self.position += 1

        p = self.parse_block()
        return Function(s, p)

    def parse_Do_Function(self):

        return EvalFunction(self.look_word())

    def parse_While(self):
        c = self.parse_sum()
        b = self.parse_instruction()
        return While(c, b)

    def parse_sum(self):
        e = self.parse_mult()
        c = self.look_char()
        while c == "+" or c == "-":
            self.position += 1
            f = self.parse_mult()
            e = Binary_operator(c, e, f)
            c = self.look_char()

        return e

    def parse_mult(self):
        e = self.parse_condition()
        c = self.look_char()
        while c == "*" or c == "/" or c == '%':
            self.position += 1
            f = self.parse_condition()
            e = Binary_operator(c, e, f)
            c = self.look_char()

        return e

    def parse_condition(self):
        e = self.parse_term()
        c = self.look_char()
        while c == "=" or c == "<" or c == ">" or c == "|" or c == "&":
            self.position += 1
            f = self.parse_term()
            e = Binary_operator(c, e, f)
            c = self.look_char()

        return e

    def parse_tab(self):
        self.position += 1
        tab = []
        while self.input[self.position] != self.EOS:
            if self.input[self.position].isalnum():
                tab.append(self.parse_sum())
            c = self.look_char()
            if c == ',':
                self.position += 1
                continue
            elif c == ']':

                self.position += 1
                break
            elif c == '[':

                self.position += 1
                tab.append(self.parse_tab())
            else:
                raise Not_Parsed("',' expendent")
        return Constant(tab)

    def parse_term(self):
        c = self.look_char()
        if c == '(':
            return self.parse_paren()
        elif c == '[':
            return self.parse_tab()
        elif c == '"':
            return self.parse_String()
        elif c.isalpha():
            return self.parse_Variable()
        elif c.isalnum():
            return self.parse_Constant()

        else:
            raise Not_Parsed()

    def parse_String(self):
        self.position += 1
        s = ''
        c = self.input[self.position]
        while c != '"' and c != self.EOS:
            s += c
            self.position += 1
            c = self.input[self.position]
        if c == '"':
            self.position += 1
            return Constant(s)
        else:
            raise Not_Parsed("'\"' expendent")

    def parse_Constant(self):
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
            return Constant(n + dot)
        else:
            return Constant(n)

    def parse_Variable(self):
        s = self.look_word()
        if s == 'true':
            return Constant(True)
        elif s == 'false':
            return Constant(False)

        else:
            if self.input[self.position] == '[':
                self.position += 1
                s2 = self.parse_sum()
                if self.input[self.position] == ']':
                    self.position += 1
                    return IndexVariable(s, s2)
                else:
                    raise Not_Parsed("']' expendent")
            return Variable(s)

    def parse_paren(self):
        self.position += 1
        e = self.parse_sum()
        if self.look_char() == ')':
            self.position += 1
            return e
        else:
            raise Not_Parsed("')' expendent")

    def parse_Delete(self):
        s = self.look_word()
        return Del(s)

    def parse_Append(self):
        s = self.look_word()
        indexs=self.tab_algorithm()
        v = self.parse_sum()
        return Append(s, v,indexs)
