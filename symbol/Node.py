class Node():
    def __init__(self, identifier, value, type, lineno, attributes, next):
        self.identifier = identifier
        self.scope = value
        self.type = type
        self.lineno = lineno
        self.next = None
        self.attributes = attributes

    def __str__(self):
        return ''


