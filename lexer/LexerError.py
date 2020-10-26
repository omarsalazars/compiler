class LexerError(Exception):
    def __init__(self, pos, sym):
        self.pos = pos
        self.sym = sym
    def __str__(self):
        return 'LexerError at position %s: Symbol "%s" not recognized' % (self.pos, self.sym)
