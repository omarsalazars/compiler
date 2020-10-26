from lexer.Token import Token
from lexer.Lexer import Lexer
from lexer.LexerError import LexerError
from lexer.Rules import rules
import sys

lx = Lexer(rules, skip_whitespace=True)

try:
    if len(sys.argv)<2:
        raise Exception('File not provided', 'Must provide filename as first argument')
    file = open(sys.argv[1], 'r')
except Exception as inst:
    print("Error {%s}" % inst)

lx.input(file.read())
tokens = []

try:
    for tok in lx.tokens():
        tokens.append(tok)
except LexerError as err:
    raise err

for tok in tokens:
    print(tok)
