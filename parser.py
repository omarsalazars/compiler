from compiler.compiler import Compiler
from lexer.Encoder import Encoder
import json

compiler = Compiler()
compiler.parse()
file = open("out/parse", "w")
json_str = json.dumps(compiler.ast, indent=4, cls=Encoder)
file.write(json_str)
file.close()
