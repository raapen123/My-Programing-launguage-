from Expression import *
import Lexer


class Not_Parsed(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.advance()
        self.errors = []

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_tok = self.tokens[self.position]

        return self.current_tok

    def parse_block(self, in_program):
        if not in_program:
            p = Composition(self.parse_Import("build"), self.parse_instruction())
        else:
            p = self.parse_instruction()
        while self.current_tok.type != EOF and self.current_tok.type != RBUCKLE:
            q = self.parse_instruction()
            p = Composition(p, q)
        return p

    def parse_Program(self, imported):
        if imported == True:
            return self.parse_block(True), self.errors
        else:
            return self.parse_block(False), self.errors

    def parse_instruction(self):
        if self.current_tok.type == IDENTIFIER:
            if self.current_tok.value == 'if':
                return self.parse_If()
            elif self.current_tok.value == 'write':
                return self.parse_Write()
            elif self.current_tok.value == 'input':

                return self.parse_Input()
            elif self.current_tok.value == 'Str':
                return self.parse_Str()
            elif self.current_tok.value == 'Int':
                return self.parse_Int()
            elif self.current_tok.value == 'Float':
                return self.parse_Float()
            elif self.current_tok.value == 'import':
                return self.parse_Import()
            elif self.current_tok.value == 'while':
                return self.parse_While()
            elif self.current_tok.value == 'skip':
                self.advance()
                return Skip()
            elif self.current_tok.value == 'len':
                return self.parse_Len()
            elif self.current_tok.value == 'append':
                return self.parse_Append()
            elif self.current_tok.value == 'del':
                return self.parse_Delete()
            elif self.current_tok.value == 'function':
                return self.parse_Function()
            elif self.current_tok.value == 'return':
                return self.parse_Return()
            else:
                return self.parse_sum()
        elif self.current_tok.type == HASHTAG:
            return self.parse_Assign()
        elif self.current_tok.type == LBUCKLE:
            self.advance()
            return self.parse_block(True)
        else:
            return self.parse_sum()

    def parse_If(self):
        self.advance()
        condition = self.parse_instruction()
        program = self.parse_instruction()
        if self.current_tok.type == IDENTIFIER and self.current_tok.value == 'else':
            self.advance()
            else_ = self.parse_instruction()

            return If(condition, program, else_)

        else:
            self.errors.append(Lexer.InvalidSyntax("else expendent"))
            self.advance()
            return Skip()

    def parse_sum(self):
        return self.bin_op(self.parse_mult, (SUM, SUB))

    def parse_mult(self):
        return self.bin_op(self.parse_condition, (MUL, DIV, MOD))

    def parse_condition(self):
        return self.bin_op(self.parse_term, (BIGGER, SMALLER, EQUALS, AND, OR))

    def parse_term(self):
        tok = self.current_tok
        if self.current_tok.type in (INT, FLOAT):
            self.advance()
            return Constant(tok.value)
        elif self.current_tok.type == IDENTIFIER:
            return self.parse_Variable()
        elif self.current_tok.type == STRING:
            self.advance()
            return Constant(tok.value)
        elif self.current_tok.type == LARRAY:
            return self.parse_array()
        elif self.current_tok.type == LPAREN:

            return self.parse_paren()
        elif self.current_tok.type == EOF:
            return
        else:
            raise Not_Parsed()

    def parse_paren(self):
        self.advance()
        ins = self.parse_instruction()
        if self.current_tok.type == RPAREN:
            self.advance()
            return ins
        else:
            self.errors.append(Lexer.InvalidSyntax('( expendent'))
            return Skip()

    def bin_op(self, func, op):
        left = func()
        while self.current_tok.type in op:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = Binary_operator(op_tok.type, left, right)
        return left

    def parse_var_name(self):
        name = self.current_tok.value
        self.advance()
        indexes = self.array_algorithm()

        return name, indexes

    def parse_Assign(self):
        self.advance()
        if self.current_tok.type == IDENTIFIER:
            name, indexes = self.parse_var_name()
            if self.current_tok.type == COLON:
                self.advance()
                value = self.parse_instruction()
                if indexes:
                    return IndexVar(name, value, indexes)
                return Var(name, value)
            else:
                self.errors.append(Lexer.InvalidSyntax(': expedient'))
                return Skip()
        else:
            self.errors.append(Lexer.InvalidSyntax('Name variable must be in alphabet'))
            return Skip()

    def parse_Write(self):
        self.advance()
        instruction = self.parse_instruction()
        return Write(instruction)

    def parse_Import(self, name=None):
        if name is None:
            self.advance()
            file = open(self.current_tok.value + '.g')
            self.advance()
        else:
            file = open(name + '.g')
        tokens, errors = Lexer.Lexer(file.read()).make_tokens()
        parser = Parser(tokens)
        parsed, errors2 = parser.parse_Program(True)
        return parsed

    def parse_While(self):
        self.advance()
        condition = self.parse_instruction()
        program = self.parse_instruction()

        return While(condition, program)

    def array_algorithm(self):
        indexes = []
        if self.current_tok.type != LARRAY:
            return indexes
        while True:
            if self.current_tok.type == LARRAY:
                self.advance()
                value = self.parse_instruction()
                if self.current_tok.type == RARRAY:
                    indexes.append(value)
                    self.advance()
                    continue

            else:
                return indexes

    def parse_array(self):
        array = []
        while self.current_tok.type != RARRAY:
            self.advance()
            value = self.parse_instruction()
            array.append(value)
            if self.current_tok.type == LARRAY:
                array.append(self.parse_array())
            elif self.current_tok.type == COMMA:
                continue
            elif self.current_tok.type == RARRAY:
                self.advance()
                return Constant(array)
        self.advance()
        return Constant(array)

    def parse_Variable(self):
        name, indexes = self.parse_var_name()
        if self.current_tok.type == LPAREN:
            self.advance()
            params = []
            while self.current_tok.type != RPAREN:
                if self.current_tok.type != COMMA and self.current_tok.type != RPAREN:
                    value = self.parse_instruction()
                    params.append(value)
                elif self.current_tok.type == COMMA:
                    self.advance()
                elif self.current_tok.type == RPAREN:
                    break
                else:
                    break
            self.advance()
            return EvalFunction(name, indexes, params)
        if name == 'True':
            return Constant(True)
        elif name == 'False':
            return Constant(False)
        elif name == 'null':
            return Constant(None)
        if indexes:
            return IndexVariable(name, indexes)
        return Variable(name)

    def parse_Append(self):
        self.advance()
        name, indexes = self.parse_var_name()
        if self.current_tok.type == COLON:
            self.advance()

            value = self.parse_instruction()
            self.advance()
            return Append(name, value, indexes)
        else:
            self.errors.append(Lexer.InvalidSyntax(': expedient'))
            return Skip()

    def parse_Delete(self):
        self.advance()
        name = self.current_tok.value
        self.advance()
        return Del(name)

    def parse_Function(self):
        self.advance()
        params = []
        if self.current_tok.type == LPAREN:
            self.advance()
            while self.current_tok.type != RPAREN:
                if self.current_tok.type != COMMA and self.current_tok.type != RPAREN:
                    value = self.current_tok.value
                    params.append(value)

                    self.advance()
                elif self.current_tok.type == COMMA:
                    self.advance()
            self.advance()
            program = self.parse_instruction()
            self.advance()
            return Function(program, params)
        else:
            program = self.parse_instruction()
            return Function(program, [])

    def parse_Return(self):
        self.advance()
        program = self.parse_instruction()
        return Returned(program)

    def parse_Input(self):
        self.advance()
        return Input()

    def parse_Str(self):
        self.advance()
        value = self.parse_instruction()
        return Str(value)

    def parse_Int(self):
        self.advance()
        value = self.parse_instruction()
        return Int(value)

    def parse_Float(self):
        self.advance()
        value = self.parse_instruction()
        return Float(value)

    def parse_Len(self):
        self.advance()
        value = self.parse_instruction()
        return Len(value)
