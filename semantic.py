from compiler.compiler import Compiler
import json

compiler = Compiler()
compiler.semantic()

#AST
file = open("out/ast", "w")
json_str = json.dumps(compiler.semantics.root, indent=4)
file.write(json_str)
file.close()

#SymTable
file = open("out/sym", "w")
json_str = json.dumps(compiler.semantics.symbol, indent=4)
file.write(json_str)
file.close()
