import Lexer
import sys

m = Lexer.Memory()

if len(sys.argv) == 2:
    file = open(sys.argv[1])
    program = Lexer.run(file.read())[2]

    program.eval(m)
else:
    while True:
        _input = input("g>")
        tokens, errors, program, errors2 = Lexer.run(_input)
        if errors is None and errors2 == []:
            p = program.eval(m)
            if p is not None:
                print(p)
        else:
            for i in range(len(errors2)):
                print(errors2[i].as_string())
            if errors != None:
                print(errors.as_string())
