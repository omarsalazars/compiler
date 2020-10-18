from .Rules import TokenType

class Token(dict):
    def __init__(self, type, val, pos):
        super().__init__()
        self.__dict__ = self
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s( %s ) at %s' % (self.type, repr(self.val), self.pos)
