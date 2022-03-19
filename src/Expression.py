from settings import *


class Variable_not_found(Exception): pass


class Zero_Division_Error(Exception): pass


class Memory:
    def __init__(self):
        self.vars = {}
        self.in_function = False

    def __delitem__(self, key):
        del self.vars[key]

    def __setitem__(self, x, y):
        self.vars[x] = y

    def __getitem__(self, x):
        return self.vars[x]

    def copy(self):
        m = Memory()
        m.vars = self.vars.copy()
        return m


class Expression:
    def eval(self, m: Memory):
        return


class IndexVariable(Expression):
    def __init__(self, name,indexes):
        self.name = name
        self.index = indexes
    def eval(self, m: Memory):
        for x, y in m.vars.items():
            if str(x) == str(self.name):
                y=y[0]
                if type(y) == list:
                    for i in range(len(self.index)):
                        if type(y) == list:
                            y = y[self.index[i].eval(m)]
                    if not type(y) in (int,str,float,list):
                        return y.eval(m)
                    else:
                        return y
                else:

                    return y
        raise Variable_not_found("Variable not found")



class Constant(Expression):
    def __init__(self, value):
        self.__value = value

    def eval(self, m: Memory):
        if type(self.__value) == list:
            __value = []
            for i in self.__value:
                __value.append(i.eval(m))
            return __value
        return self.__value


class Binary_operator(Expression):
    def __init__(self, s: str, left: Expression, right: Expression):
        self.__symbol = s
        self.__left = left
        self.__right = right

    def eval(self, m: Memory):
        if self.__symbol == SUM:
            return self.__left.eval(m) + self.__right.eval(m)
        elif self.__symbol == SUB:
            return self.__left.eval(m) - self.__right.eval(m)
        elif self.__symbol == MUL:
            return self.__left.eval(m) * self.__right.eval(m)
        elif self.__symbol == MOD:
            return self.__left.eval(m) % self.__right.eval(m)
        elif self.__symbol == EQUALS:
            return self.__left.eval(m) == self.__right.eval(m)
        elif self.__symbol == SMALLER:
            return self.__left.eval(m) < self.__right.eval(m)
        elif self.__symbol == BIGGER:
            return self.__left.eval(m) > self.__right.eval(m)
        elif self.__symbol == OR:
            return self.__left.eval(m) or self.__right.eval(m)
        elif self.__symbol == AND:
            return self.__left.eval(m) and self.__right.eval(m)
        elif self.__symbol == 'in':
            return self.__left.eval(m) in self.__right.eval(m)
        try:
            if self.__symbol == DIV:
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

        x = self.value.eval(m)
        if type(x) == list:
            m[self.name] = [[i for i in x], m.in_function]

        else:
            m[self.name] = [x, m.in_function]


class IndexVar(Program):
    def __init__(self, n, v, i):
        self.name = n
        self.value = v
        self.index = i

    def eval(self, m):
        y = m[self.name]
        self.value=self.value.eval(m)
        for c, i in enumerate(self.index):
            if c == len(self.index) - 1:

                y[i.eval(m)] = self.value
                break
            else:
                self.value = y[0][c][i.eval(m)]

class Input(Program):

    def eval(self, m):
        return input()


class Len(Program):
    def __init__(self, v):
        self.value = v

    def eval(self, m):
        return len(self.value.eval(m))


class Write(Program):
    def __init__(self, v):
        self.var = v

    def eval(self, m):
        x = self.var.eval(m)

        if type(x) == str and x.replace('\n','')=='None':
            print('null',end='')
        elif type(x) == int or type(x) == float or type(x) == str:
            print(x, end='')
        elif x is None:
            print('null', end='')

        else:
            if x.eval(m) == None:
                print('null',end='')
            else:
                print(x.eval(m), end='')


class Composition(Program):
    def __init__(self, r, l):
        self.right = r
        self.left = l
    def eval(self, m):
        r = self.right.eval(m)
        if type(self.right) in (Returned, If, While):
            if r is not None:
                return r
        l = self.left.eval(m)
        if type(self.left) in (Returned, If, While):

            if l is not None:
                return l


class If(Program):
    def __init__(self, c, t, e):
        self.condition = c
        self.b_then = t
        self.b_else = e

    def eval(self, m):
        if self.condition.eval(m):
            x = self.b_then.eval(m)
            return x if type(self.b_then) in (If, While, Returned, Composition) else None
        else:
            x = self.b_else.eval(m)
            return x if type(self.b_else) in (If, While, Returned, Composition) else None


class Str(Program):
    def __init__(self, v):
        self.value = v

    def eval(self, m):
        return str(self.value.eval(m))


class Float(Program):
    def __init__(self, v):
        self.value = v

    def eval(self, m):
        return float(self.value.eval(m))


class Int(Program):
    def __init__(self, v):
        self.value = v

    def eval(self, m):
        return int(self.value.eval(m))


class While(Program):
    def __init__(self, c, b):
        self.condition = c
        self.body = b

    def eval(self, m):
        if self.condition.eval(m):
            x = self.body.eval(m)
            if type(self.body) in (While, Returned, If, Composition):
                return x
            self.eval(m)


class Function(Program):
    def __init__(self, b, p):
        self.body = b
        self.params = p

    def eval(self, m):
        return {"body": self.body, "params": self.params}


class EvalFunction(Program):
    def __init__(self, v, i, p):
        self.value = v
        self.indexes = i
        self.params = p

    def eval(self, m):
        if type(self.value) == str:
            y = m[self.value]
        elif type(self.value) == list:
            y = self.value
        y = y[0]
        m2 = m.copy()
        for i in range(len(self.indexes)):
            y = y[0]
            if type(y) == list:
                y = y[self.indexes[i].eval(m)]

        for i in range(len(y['params'])):
            m[y['params'][i]] = [self.params[i].eval(m), True]
        m.in_function = True
        value = y["body"].eval(m)
        m.in_function = False


        return value


class Append(Program):
    def __init__(self, name, value, indexs):
        self.name = name
        self.value = value
        self.indexs = indexs

    def eval(self, m):
        y = m[self.name]
        if self.indexs:
            for c, i in enumerate(y):
                if c == len(y) - 2:
                    y[self.indexs[c].eval(m)] = self.value.eval(m)
                else:
                    y = i[self.indexs[c].eval(m)]
        y.append(self.value.eval(m))
        m[self.name] = y


class Del(Program):
    def __init__(self, name):
        self.name = name

    def eval(self, m):
        del m[self.name]


class Returned(Program):
    def __init__(self, value):
        self.value = value

    def eval(self, m):
        return self.value.eval(m)
