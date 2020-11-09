from compiler.compiler import Compiler

compiler = Compiler()
file = open("out/tokens", "w")
compiler.lex()
for tok in compiler.tokens:
    file.write(str(tok)+"\n")
file.close()
