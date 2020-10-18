class AST(dict):
    def __init__(self):
        super().__init__()
        self.__dict__ = self
    pass

class MainNode(AST):
    def __init__(self, name, declarations, statements):
        super().__init__()
        self.name = name
        self.declarations = declarations
        self.statements = statements
    def __str__(self):
        return "MainNode(%s, %s)" % (self.declarations, self.statements)

class BlockNode(AST):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

class DeclarationNode(AST):
    def __init__(self, type, var):
        super().__init__()
        self.type = type
        self.var = var
    def __str__(self):
        return "Declaration"

class TypeNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.val = token.val

class VarNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.val = token.val

class IfNode(AST):
    def __init__(self, relationalExpression, block, elseNode = None):
        super().__init__()
        if isinstance(relationalExpression, RelationalExpressionNode):
            self.relationalExpression = relationalExpression
        else:
            self.expression = relationalExpression
        self.block = block
        if elseNode != None:
            self.elseNode = elseNode
    def __str__(self):
        return "IfNode"

class WhileNode(AST):
    def __init__(self, relationalExpression, block):
        super().__init__()
        if isinstance(relationalExpression, RelationalExpressionNode):
            self.relationalExpression = relationalExpression
        else:
            self.expression = relationalExpression
        self.block = block
    def __str__(self):
        return "WhileNode"

class ReadNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
    def __str__(self):
        return "ReadNode"

class PrintNode(AST):
    def __init__(self, relationalExpression):
        super().__init__()
        self.relationalExpression = relationalExpression
    def __str__(self):
        return "PrintNode"

class BinaryOperationNode(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

class NumNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token

class AssignNode(AST):
    def __init__(self, left, relationalExpression):
        super().__init__()
        self.left = left
        if isinstance(relationalExpression, RelationalExpressionNode):
            self.relationalExpression = relationalExpression
        else:
            self.expression = relationalExpression

class RelationalExpressionNode(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

class NoOperationNode(AST):
    def __init__(self):
        super().__init__()
