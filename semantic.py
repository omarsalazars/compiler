from compiler.compiler import Compiler
from lexer.Encoder import TableEncoder
from lexer.Rules import TokenType
import json

compiler = Compiler()
compiler.semantic()

#AST
file = open("out/ast", "w")
tree = compiler.semantics.root.to_dict(compiler.semantics.symbol)
json_str = json.dumps(tree, indent=4)
file.write(json_str)
file.close()

def add_lines(symtable, tokens):
    for tok in tokens:
        if tok.type == TokenType.IDENTIFIER:
            if symtable.lookup(tok.val) is not None:
                symtable.add_l(tok.val, tok.pos)

#add_lines(compiler.semantics.symbol, compiler.tokens)
#SymTable
file = open("out/sym", "w")
json_str = json.dumps(compiler.semantics.symbol, indent=4, cls=TableEncoder)
file.write(json_str)
file.close()



