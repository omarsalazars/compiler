from semantic.SymbolTable import SymbolTable
from semantic.SemanticError import SemanticError
from lexer.Rules import TokenType

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
        self.statements = statements
        self.relationalExpression = relationalExpression

    def interpret(self, symtable):
        pass

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
        self.relationalExpression.interpret()
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
        self.left.interpret()
        self.right.interpret()
        self.val = self.operacionBinaria(self.left, self.op, self.right)
    
    def operacionBinaria(left, op, right):
        if op == TokenType.PLUS: return left.val + right.val
        if op == TokenType.MINUS: return left.val - right.val
        if op == TokenType.MULTIPLY: return left.val * right.val
        if op == TokenType.DIVIDE: return left.val / right.val
        raise SemanticError("Unrecognized operator type. %s" % (op))

class NumNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
    
    def interpret(self, symtable):
        if self.token.type == TokenType.IDENTIFIER:
            self.val = symtable.lookup(self.token.val)["val"]
        elif self.token.type == TokenType.NUMBER:
            self.val = int(self.token.val)
        else:
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
        self.relationalExpression.interpret(symtable)
        if symtable.lookup(self.left):
            raise SemanticError("Variable no declarada")
        elif self.relationalExpression.type != symtable.lookup(self.left).type:
            raise SemanticError("Tipos incompatibles.")
        elif self.relationalExpression.val is not None:
            symtable.set_attribute(self.left.val, "val", self.relationalExpression.val)
        #Update symtable with new value?

class RelationalExpressionNode(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def interpret(self, symtable):
        self.left.interpret(symtable)
        self.right.interpret(symtable)
        self.type = TokenType.BOOLEAN
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
