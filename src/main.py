import Parser
import sys
filename=sys.argv[1]
file = open(filename)
s = ''
for i in file.readlines():
    s += i
m=Parser.Memory()

parser=Parser.Parser(s)

if __name__=='__main__':
    evals=parser.parse_Program()
    evals.eval(m)