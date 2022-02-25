


class Variable_not_found(Exception): pass


class Zero_Division_Error(Exception): pass


class Memory:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def __delitem__(self, key):
        del self.vars[key]

    def __setitem__(self, x, y):
        self.vars[x] = y

    def __getitem__(self, x):
        return self.vars[x]

    def getF(self, x):
        return self.functions[x]

    def setF(self, x, y):
        self.functions[x] = y


class Expression:
    def eval(self, m: Memory):
        return 0


class IndexVariable(Expression):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def eval(self, m: Memory):
        for x, y in m.vars.items():

            if str(x) == str(self.name):
                if type(y) == list:
                    if type(y[self.index.eval(m)]) == int or type(y[self.index.eval(m)]) == float:
                        return y[self.index.eval(m)]
                    else:

                        while True:
                            if type(y[self.index.eval(m)])==list:
                                y=y[self.index.eval(m)]
                            else:
                                return y[self.index.eval(m)].eval(m)
                else:
                    raise Variable_not_found("Varaiable with name " + self.name + " not is the list")
        raise Variable_not_found("Variable not found")


class Variable(Expression):
    def __init__(self, name):
        self.__name = name

    def eval(self, m: Memory):
        for x, y in m.vars.items():

            if str(x) == str(self.__name):
                if type(y) == float:
                    return float(y)
                elif type(y) == int:
                    return int(y)
                else:
                    return str(y)

        raise Variable_not_found("Cant search variable: " + str(self.__name))


class Constant(Expression):
    def __init__(self, value):
        self.__value = value

    def eval(self, m: Memory):
        return self.__value

    def __str__(self):
        return self.__value


class Binary_operator(Expression):
    def __init__(self, s: str, left: Expression, right: Expression):
        self.__symbol = s
        self.__left = left
        self.__right = right

    def eval(self, m: Memory):
        if self.__symbol == '+':
            return self.__left.eval(m) + self.__right.eval(m)
        elif self.__symbol == '-':
            return self.__left.eval(m) - self.__right.eval(m)
        elif self.__symbol == '*':
            return self.__left.eval(m) * self.__right.eval(m)
        elif self.__symbol == '%':
            return self.__left.eval(m) % self.__right.eval(m)
        elif self.__symbol == '=':
            return self.__left.eval(m) == self.__right.eval(m)
        elif self.__symbol == '<':
            return self.__left.eval(m) < self.__right.eval(m)
        elif self.__symbol == '>':
            return self.__left.eval(m) > self.__right.eval(m)
        elif self.__symbol == '|':
            return self.__left.eval(m) or self.__right.eval(m)
        elif self.__symbol == '&':
            return self.__left.eval(m) and self.__right.eval(m)
        try:
            if self.__symbol == '/':
                return self.__left.eval(m) / self.__right.eval(m)
        except ZeroDivisionError:
            raise Zero_Division_Error()


class Program:
    def eval(self, m):
        pass


class Skip(Program):
    def eval(self, m):
        pass


class Var(Program):
    def __init__(self, n, v):
        self.name = n
        self.value = v

    def eval(self, m):
        x=self.value.eval(m)
        if type(x)==list:
            m[self.name]=[i.eval(m) for i in x]
        else:
            m[self.name]=x


class IndexVar(Program):
    def __init__(self, n, v, i):
        self.name = n
        self.value = v
        self.index = i

    def eval(self, m):
        y=m[self.name]

        for c,i in enumerate(y):
            if c==len(y)-2:
                y[self.index[c].eval(m)]=self.value.eval()
            else:
                y=i[self.index[c].eval(m)]



class Input(Program):
    def __init__(self, v):
        self.var = v

    def eval(self, m):
        m[self.var] = Constant(int(input())).eval(m)


class Write(Program):
    def __init__(self, v):
        self.var = v

    def eval(self, m):
        x = self.var.eval(m)
        if type(x) == int or type(x) == float or type(x) == str:
            print(x)
        else:
            print(x.eval(m))


class Composition(Program):
    def __init__(self, r, l):
        self.right = r
        self.left = l

    def eval(self, m):
        self.right.eval(m)
        self.left.eval(m)


class If(Program):
    def __init__(self, c, t, e):
        self.condition = c
        self.b_then = t
        self.b_else = e

    def eval(self, m):
        if self.condition.eval(m):
            self.b_then.eval(m)
        else:
            self.b_else.eval(m)


class While(Program):
    def __init__(self, c, b):
        self.condition = c
        self.body = b

    def eval(self, m):
        if self.condition.eval(m):
            self.body.eval(m)
            self.eval(m)


class Function(Program):
    def __init__(self, n, b):
        self.name = n
        self.body = b

    def eval(self, m):
        m.setF(self.name, self.body)


class EvalFunction(Program):
    def __init__(self, n):
        self.name = n

    def eval(self, m):
        m.getF(self.name).eval(m)


class Append(Program):
    def __init__(self, name, value, indexs):
        self.name = name
        self.value = value
        self.indexs=indexs
    def eval(self, m):
        y = m[self.name]

        for c, i in enumerate(y):
            if c == len(y) - 2:
                y[self.indexs[c].eval(m)] = self.value.eval()
            else:
                y = i[self.indexs[c].eval(m)]
        y.append(self.value.eval(m))


class Del(Program):
    def __init__(self, name):
        self.name = name

    def eval(self, m):
        del m[self.name]
