from compiler.compiler import Compiler
import json

compiler = Compiler()
compiler.parse()
file = open("out/parse", "w")
json_str = json.dumps(compiler.ast, indent=4)
file.write(json_str)
file.close()
