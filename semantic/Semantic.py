from .SymbolTable import SymbolTable

class Semantic():
    def __init__(self, root):
        self.symbol = SymbolTable()
        self.root = root
        self.root.interpret(self.symbol)

    def semantic(self):
        pass

    def traverse(self, node):
        pass
