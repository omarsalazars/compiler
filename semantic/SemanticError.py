class SemanticError(Exception):
    def __init__(self, error, *pos):
        self.error = error

    def __str__(self):
        return self.error
