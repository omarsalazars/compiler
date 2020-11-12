from compiler.compiler import Compiler
from lexer.Encoder import TableEncoder
import json

compiler = Compiler()
compiler.semantic()

#AST
file = open("out/ast", "w")
tree = compiler.semantics.root.to_dict(compiler.semantics.symbol)
json_str = json.dumps(tree, indent=4)
file.write(json_str)
file.close()

#SymTable
file = open("out/sym", "w")
json_str = json.dumps(compiler.semantics.symbol, indent=4, cls=TableEncoder)
file.write(json_str)
file.close()



