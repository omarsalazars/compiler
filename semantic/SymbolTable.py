from semantic.SemanticError import SemanticError
from lexer.Rules import TokenType


class SymbolTable(dict):
    def __init__(self):
        super().__init__()
        self.__dict__ = self
        self.loc = 0

    # Allocate a new empty symbol table
    def allocate(self):
        pass

    # Remove all entries and free storage of symbol table
    def free(self):
        pass

    # Search for a name and return pointer to its entry
    def lookup(self, name):
        if name in self:
            return self[name]
        else:
            return None
        pass

    # Insert a name in a symbol table and return a pointer to its entry
    def insert(self, name, type, lineno):
        if name in self:
            # raise SemanticError("Variable already defined")
            pass
        else:
            self[name] = {'type': type, 'lines': [lineno], 'val': 0, 'loc': self.loc}
            self.loc = self.loc + 1
        pass

    def add_line(self, name, line):
        if name in self:
            self[name]['lines'].append(line)

    # Associate an attribute with a given entry
    def set_attribute(self, name, attribute, newVal):
        if name in self:
            if attribute in self[name]:
                self[name][attribute] = newVal
                if attribute == "val":
                    if self[name]["type"]["token"]["type"] == TokenType.INT:
                        self[name]["val"] = int(self[name]["val"])
                    elif self[name]["type"]["token"]["type"] == TokenType.REAL:
                        self[name]["val"] = float(self[name]["val"])
                    else:
                        pass
            else:
                raise SemanticError("Attribute %s not defined" % attribute)
        else:
            # raise SemanticError("Undefined variable %s" % name)
            self.insert(name, )

    # Get an attribute associated with a given entry
    def get_attribute(self, name, attribute):
        if name in self:
            if attribute in self[name]:
                return self[name][attribute]
            else:
                raise SemanticError("Attribute %s not defined" % attribute)
        else:
            raise SemanticError("Undefined variable %s", name)
