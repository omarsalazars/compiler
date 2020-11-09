import sys
from lexer.Lexer import Lexer
from lexer.LexerError import LexerError
from lexer.Rules import rules
from parser.Parser import Parser
from semantic.Semantic import Semantic


class Compiler:

    def __init__(self):
        self.lx = None
        self.tokens = None
        self.parser = None
        self.ast = None
        self.semantics = None
        if len(sys.argv) < 2:
            raise Exception('File not provided', 'Must provide filename as first argument')
        try:
            self.file = open(sys.argv[1], "r")
        except Exception as inst:
            print("Error {%s}" % inst)

    def lex(self):
        self.lx = Lexer(rules, skip_whitespace=True)
        self.lx.input(self.file.read())
        self.tokens = []

        try:
            for tok in self.lx.tokens():
                self.tokens.append(tok)
        except LexerError as err:
            raise err
        return self.tokens

    def parse(self):
        self.lex()
        self.parser = Parser(self.tokens)
        self.ast = self.parser.parse()
        return self.ast

    def semantic(self):
        self.parse()
        self.semantics = Semantic(self.ast)
        return self.semantics.root
