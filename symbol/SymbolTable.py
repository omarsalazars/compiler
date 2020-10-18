from .Node import Node

class SymbolTable(dict):
    def __init__(self):
        
    #Allocate a new empty symbol table
    def allocate():

    #Remove all entries and free storage of symbol table
    def free():

    #Search for a name and return pointer to its entry
    def lookup():

    #Insert a name in a symbol table and return a pointer to its entry
    def insert(self, name, type, lineno):
        self[name] = Node(name, type, lineno, )

    #Associate an attribute with a given entry
    def set_attribute():

    #Get an attribute associated with a given entry
    def get_attribute():
