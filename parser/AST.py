from semantic.SemanticError import SemanticError
from lexer.Rules import TokenType
from lexer.Token import Token

class AST(dict):
    def __init__(self):
        super().__init__()
        self.__dict__ = self

class MainNode(AST):
    def __init__(self, name, declarations, statements):
        super().__init__()
        self.declarations = declarations
        self.statements = statements

    def __str__(self):
        return "MainNode(%s, %s)" % (self.declarations, self.statements)

    def interpret(self, symtable):
        for decl in self.declarations:
            decl.interpret(symtable)
        for stmt in self.statements:
            stmt.interpret(symtable)
        return self;
        pass

class BlockNode(AST):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def interpret(self, symtable):
        for stmt in self.statements:
            stmt.interpret(symtable)

class DeclarationNode(AST):
    def __init__(self, type, var):
        super().__init__()
        self.type = type
        if isinstance(var, list):
            self.vars = var
        else:
            self.var = var

    def __str__(self):
        return "Declaration"

    def interpret(self, symtable):
        if self.vars is not None:
            for var in self.vars:
                var.type = self.type
                var.interpret(symtable)
        else:
            self.var.type = self.type
            self.var.interpret(symtable)
        return self

class TypeNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token

class VarNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token

    def interpret(self, symtable):
        symtable.insert(self.token.val, self.type, self.token.pos)

class IfNode(AST):
    def __init__(self, relationalExpression, block, elseNode = None):
        super().__init__()
        self.prod = "if statement"
        if isinstance(relationalExpression, RelationalExpressionNode):
            self.relationalExpression = relationalExpression
        else:
            self.expression = relationalExpression
        self.block = block
        if elseNode != None:
            self.elseNode = elseNode
    def __str__(self):
        return "IfNode"
    
    def interpret(self, symtable):
        self.relationalExpression.interpret(symtable)
        if self.relationalExpression.type != TokenType.BOOLEAN:
            raise SemanticError("Expression is not boolean.")

class DoUntilNode(AST):
    def __init__(self, statements, relationalExpression):
        super().__init__()
        self.prod = "do-until statement"
        self.relationalExpression = relationalExpression
        self.statements = statements

    def interpret(self, symtable):
        if hasattr(self.relationalExpression, "interpret"):
            self.relationalExpression.interpret(symtable)
        for stmt in self.statements:
            if hasattr(stmt, "interpret"):
                stmt.interpret(symtable)

class WhileNode(AST):
    def __init__(self, relationalExpression, block):
        super().__init__()
        self.prod = "while statement"
        if isinstance(relationalExpression, RelationalExpressionNode):
            self.relationalExpression = relationalExpression
        else:
            self.expression = relationalExpression
        self.block = block
    def __str__(self):
        return "WhileNode"

    def interpret(self, symtable):
        self.relationalExpression.interpret(symtable)
        if self.relationalExpression.type != TokenType.BOOLEAN:
            raise SemanticError("Expression is not boolean.")

class ReadNode(AST):
    def __init__(self, token):
        super().__init__()
        self.prod = "read statement"
        self.token = token
    def __str__(self):
        return "ReadNode"

    def interpret(self, symtable):
        if symtable.lookup(self.token.val) == None:
            raise SemanticError("Variable no declarada.")
        symtable.set_attribute(self.token.val, 'val', None)

class PrintNode(AST):
    def __init__(self, relationalExpression):
        super().__init__()
        self.prod = "print statement"
        self.relationalExpression = relationalExpression
    def __str__(self):
        return "PrintNode"

    def interpret(self, symtable):
        self.relationalExpression.interpret(symtable)
        self.val = self.relationalExpression.val

class BinaryOperationNode(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right


    def interpret(self, symtable):
        # Interpret operation sides
        if hasattr(self.left, "interpret"):
            self.left.interpret(symtable)
        if hasattr(self.right, "interpret"):
            self.right.interpret(symtable)

        #Set Left Operation type: float | int
        if isinstance(self.left, Token):
            if self.left.type == TokenType.IDENTIFIER:
                leftType = symtable.lookup(self.left.val)
                if leftType is None:
                    pass
                else:
                    leftType = symtable.get_attribute(self.left.val, 'type')
                    leftVal = symtable.get_attribute(self.left.val, 'val')
        elif isinstance(self.left, NumNode):
            leftType = self.left.type
            leftVal = self.left.val
        elif isinstance(self.left, BinaryOperationNode):
            leftType = self.left.type
            leftVal = self.left.val
        else:
            print(self.left)
            raise SemanticError("Tipo indefinido")

        #Set right operation type: int | float
        if isinstance(self.right, Token):
            if self.right.type == TokenType.IDENTIFIER:
                rightType = symtable.lookup(self.right.val)
                if rightType is None:
                    pass
                else:
                    rightType = symtable.get_attribute(self.right.val, 'type')
                    rightVal = symtable.get_attribute(self.right.val, 'val')
        elif isinstance(self.right, NumNode):
            rightType = self.right.type
            rightVal = self.right.val
        elif isinstance(self.right, BinaryOperationNode):
            rightType = self.right.type
            rightVal = self.right.val
        else:
            print(self.right)
            raise SemanticError("Tipo indefinido")

        #Set self type
        if leftType is None and rightType is None:
            self.type = None
        elif leftType == TokenType.INT and rightType == TokenType.INT:
            self.type = TokenType.INT
        else:
            self.type = TokenType.FLOAT

        #Set self value
        if leftVal is None or rightVal is None:
            self.val = None
        else:
            self.val = self.operacionBinaria(leftVal, self.op, rightVal)


    def operacionBinaria(self, leftVal, op, rightVal):
        if op.type == TokenType.PLUS:
            return leftVal + rightVal
        elif op.type == TokenType.MINUS:
            return leftVal - rightVal
        elif op.type == TokenType.MULTIPLY:
            return leftVal * rightVal
        elif op.type == TokenType.DIVIDE:
            return leftVal / rightVal
        else:
            raise SemanticError("Unrecognized operator type "+op)

class NumNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
    
    def interpret(self, symtable):
        if self.token.type == TokenType.IDENTIFIER:
            self.val = symtable.lookup(self.token.val)["val"]
            self.type = symtable.lookup(self.token.val)["type"]
        elif self.token.type == TokenType.NUMBER:
            try:
                self.val = int(self.token.val)
                self.type = TokenType.INT
            except ValueError:
                raise SemanticError("Invalid type "+self.token)
        elif self.token.type == TokenType.FLOAT:
            try:
                self.val = float(self.token.val)
                self.type = TokenType.FLOAT
            except ValueError:
                raise SemanticError("Invalid type "+self.token)
        else:
            print(self.token)
            raise SemanticError("Error inesperado.")

class AssignNode(AST):
    def __init__(self, left, relationalExpression):
        super().__init__()
        self.prod = "assign statement"
        self.left = left
        if isinstance(relationalExpression, RelationalExpressionNode):
            self.relationalExpression = relationalExpression
        else:
            self.expression = relationalExpression

    def interpret(self, symtable):
        if hasattr(self, "relationalExpression"):
            self.relationalExpression.interpret(symtable)
            if self.relationalExpression.type != symtable.lookup(self.left).type:
                raise SemanticError("Tipos incompatibles.")
            elif hasattr(self.relationalExpression, "val"):
                    symtable.set_attribute(self.left.val, "val", self.relationalExpression.val)
        elif hasattr(self, "expression"):
            self.expression.interpret(symtable)
            if hasattr(self.expression, "val"):
                if symtable.lookup(self.left.val) is None:
                    #raise SemanticError("Undefined Variable")
                    symtable.insert(self.left.val, self.expression.type, self.left.pos)
                symtable.set_attribute(self.left.val, "val", self.expression.val)
                #Update symtable with new value?

class RelationalExpressionNode(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def interpret(self, symtable):
        if hasattr(self.left, "interpret"):
            self.left.interpret(symtable)
        if hasattr(self.right, "interpret"):
            self.right.interpret(symtable)
        self.type = TokenType.BOOLEAN
        if self.left.val is None or self.right.val is None:
            self.val = None
        else:
            self.val = self.operacionRelacional(self.left, self.op, self.right)

    def operacionRelacional(self, left, op, right):
        if op.type == TokenType.LT:
            return left.val < right.val
        if op.type == TokenType.GT:
            return left.val > right.val
        if op.type == TokenType.GET:
            return left.val >= right.val
        if op.type == TokenType.LET:
            return left.val <= right.val
        if op.type == TokenType.ET:
            return left.val == right.val
        if op.type == TokenType.NE:
            return left.val != right.val
        raise SemanticError("Invalid operator.")

class NoOperationNode(AST):
    def __init__(self):
        super().__init__()
