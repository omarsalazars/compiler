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

    def to_dict(self, symtable):
        dec = []
        for decl in self.declarations:
            dec.append(decl.to_dict(symtable))
        stmts = []
        for stmt in self.statements:
            stmts.append(stmt.to_dict(symtable))
        return { 'declarations':dec, 'statements':stmts }

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

    def to_dict(self, symtable):
        stmts = []
        for stmt in self.statements:
            stmts.append(stmt.to_dict(symtable))
        return { 'statements':stmts }

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

    def to_dict(self, symtable):
        if hasattr(self, "var"):
            return { self.type.token.type : self.var.to_dict(symtable) }
        else:
            vars = []
            for var in self.vars:
                vars.append(var.to_dict(symtable))
            return { self.type.token.type : vars }

    def interpret(self, symtable):
        if self.vars is not None:
            newVars = []
            for var in self.vars:
                var.type = self.type
                if var.interpret(symtable)!=True:
                    newVars.append(var)
            self.vars = newVars
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
        if symtable.lookup(self.token.val) is not None:
            self.error = "ERROR: Variable redeclarada"
            print("ERROR linea %s: Variable %s redeclarada." % (self.token.pos, self.token.val))
            return True
        symtable.insert(self.token.val, self.type, self.token.pos)

    def to_dict(self, symtable):
        return self.token.val

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

    def to_dict(self, symtable):
        stmts = []
        for stmt in self.block:
            stmts.append(stmt.to_dict(symtable))
        ret = {
            "prod": "if val="+ str(self.relationalExpression.val),
            "condition" : self.relationalExpression.to_dict(symtable),
            "statements" : {
                "statements": stmts,
                "prod": "statements"
            },
        }
        if hasattr(self, "elseNode"):
            elseStmts = []
            for stmt in self.elseNode:
                elseStmts.append(stmt.to_dict(symtable))
            ret["else"] = {
                "elseNode": elseStmts,
                "prod": "elseNode"
            }
        return ret
    
    def interpret(self, symtable):
        self.relationalExpression.interpret(symtable)
        if self.relationalExpression.type != TokenType.BOOLEAN:
            raise SemanticError("Expression is not boolean.")
        for stmt in self.block:
            if hasattr(stmt, "interpret"):
                stmt.interpret(symtable)
        if hasattr(self, "elseNode"):
            for stmt in self.elseNode:
                if hasattr(stmt, "interpret"):
                    stmt.interpret(symtable)

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

    def to_dict(self, symtable):
        stmts = []
        for stmt in self.statements:
            stmts.append(stmt.to_dict(symtable))
        return {
            "prod" : "do-until val="+str(self.relationalExpression.val),
            "statements" : stmts,
            "relExpression" : self.relationalExpression.to_dict(symtable)
        }

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
        self.block.interpret(symtable)

    def to_dict(self, symtable):
        return {
            "prod" : "while val="+str(self.relationalExpression.val),
            "block" : self.block.to_dict(symtable)
        }

class ReadNode(AST):
    def __init__(self, token):
        super().__init__()
        self.prod = "read statement"
        self.token = token
    def __str__(self):
        return "ReadNode"

    def interpret(self, symtable):
        symtable.add_line(self.token.val, self.token.pos)
        if symtable.lookup(self.token.val) is None:
            #raise SemanticError("Variable no declarada.")
            print("ERROR linea %s: Variable %s no declarada" % (self.token.pos, self.token.val))
        else:
            symtable.set_attribute(self.token.val, 'val', None)

    def to_dict(self, symtable):
        return {
            "prod": "cin "+self.token.val
        }

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

    def to_dict(self, symtable):
        return {
            "prod": "print",
            "expression" : self.relationalExpression.to_dict(symtable)
        }

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
            symtable.add_line(self.left.val, self.left.pos)
            if self.left.type == TokenType.IDENTIFIER:
                leftType = symtable.lookup(self.left.val)
                if leftType is None:
                    pass
                else:
                    leftType = symtable.get_attribute(self.left.val, 'type').token.type
                    leftVal = symtable.get_attribute(self.left.val, 'val')
                    symtable.add_line(self.left.val, self.left.pos)
                    self.left.v = leftVal
        elif isinstance(self.left, NumNode):
            if hasattr(self.left,"type"):
                leftType = self.left.type
            else:
                leftType = None
            if hasattr(self.left, "val"):
                leftVal = self.left.val
            else:
                leftVal = None
        elif isinstance(self.left, BinaryOperationNode):
            leftType = self.left.type
            leftVal = self.left.val
        else:
            print(self.left)
            raise SemanticError("Tipo indefinido")

        #Set right operation type: int | float
        if isinstance(self.right, Token):
            symtable.add_line(self.right.val, self.right.pos)
            if self.right.type == TokenType.IDENTIFIER:
                rightType = symtable.lookup(self.right.val)
                if rightType is None:
                    pass
                else:
                    rightType = symtable.get_attribute(self.right.val, 'type').token.type
                    rightVal = symtable.get_attribute(self.right.val, 'val')
                    symtable.add_line(self.right.val, self.right.pos)
                    self.right.v = rightVal
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
            if self.type == TokenType.INT:
                self.val = int(self.val)

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

    def to_dict(self, symtable):
        key = self.op.type
        if hasattr(self, "val"):
            key = key + " val=" + str(self.val)
        else:
            key = key + " val=ERROR"


        if isinstance(self.left, BinaryOperationNode) and isinstance(self.right, BinaryOperationNode):
            leftkey = self.left.op.type
            if hasattr(self.left, "val"):
                leftkey = leftkey + " val="+str(self.left.val)
            else:
                leftkey = leftkey + " val=ERROR"
            rightkey = self.right.op.type
            if hasattr(self.right, "val"):
                rightkey = rightkey + " val="+str(self.right.val)
            else:
                rightkey = rightkey + "val=ERROR"
            ret = {
                    leftkey: self.left.to_dict(symtable),
                    rightkey: self.right.to_dict(symtable)
            }
        elif isinstance(self.left, BinaryOperationNode):
            leftkey = self.left.op.type
            if hasattr(self.left,"val"):
                leftkey = leftkey + " val="+str(self.left.val)
            else:
                leftkey = leftkey + " val=ERROR"
            ret = {
                    leftkey: self.left.to_dict(symtable),
                    self.right.token.val : self.right.token.val
            }
        elif isinstance(self.right, BinaryOperationNode):
            rightkey = self.right.op.type
            if hasattr(self.right, "val"):
                rightkey = rightkey + " val=" + str(self.right.val)
            else:
                rightkey = rightkey + " val=ERROR"
            ret = {
                    self.left.token.val : self.left.token.val,
                    rightkey: self.right.to_dict(symtable)
            }
        else:
            ret = [
                    self.left.to_dict(symtable),
                    self.right.to_dict(symtable)
            ]
        return ret

class NumNode(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
    
    def interpret(self, symtable):
        if self.token.type == TokenType.IDENTIFIER:
            if symtable.lookup(self.token.val) is not None:
                self.val = symtable.lookup(self.token.val)["val"]
                self.type = symtable.lookup(self.token.val)["type"].token.type
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

    def to_dict(self, symtable):
        if self.token.type == TokenType.IDENTIFIER:
            symtable.add_line(self.token.val, self.token.pos)
        if hasattr(self, "val"):
            return self.token.val + " val="+str(self.val)
        else:
            return self.token.val

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
        symtable.add_line(self.left.val, self.left.pos)
        if hasattr(self, "relationalExpression"):
            self.relationalExpression.interpret(symtable)
            if self.relationalExpression.type != symtable.lookup(self.left)["type"].token.type:
                #raise SemanticError("Tipos incompatibles.")
                print("Error linea %s: Tipos incompatibles" % self.left.pos)
                self.error = "ERROR: tipos incompatibles"
                return
            elif hasattr(self.relationalExpression, "val"):
                    symtable.set_attribute(self.left.val, "val", self.relationalExpression.val)
        elif hasattr(self, "expression"):
            self.expression.interpret(symtable)
            if hasattr(self.expression, "val"):
                if symtable.lookup(self.left.val) is None:
                    #raise SemanticError("Undefined Variable")
                    token = {"token":Token(self.expression.type, self.expression.type, self.left.pos)}
                    print("ERROR linea %s: Variable %s no declarada." % (self.left.pos, self.left.val))
                    self.error = "ERROR: "+self.left.val+" no declarada"
                    return

                tipo = symtable.lookup(self.left.val)["type"].token.type
                if hasattr(self.expression, "type"):
                    if tipo == TokenType.INT:
                        if self.expression.type == TokenType.FLOAT or self.expression.type == TokenType.REAL or self.expression.type == TokenType.BOOLEAN:
                            print("ERROR linea %s: Tipos incompatibles, variable %s" % (self.left.pos, self.left.val))
                            self.error = "ERROR: Tipos incompatibles, variable "+self.left.val
                            return
                    elif tipo == TokenType.FLOAT:
                        pass
                    elif tipo == TokenType.BOOLEAN:
                        pass
                symtable.set_attribute(self.left.val, "val", self.expression.val)
                #Update symtable with new value?

    def to_dict(self, symtable):
        val = ""
        if hasattr(self.expression, "val"):
            val = str(self.expression.val)
        else:
            val = "ERROR"

        if symtable.lookup(self.left.val) is None:
            val = "ERROR: variable indefinida"
        elif hasattr(self.expression, "type"):
            currentType = symtable.get_attribute(self.left.val, "type").token.type
            if currentType == TokenType.REAL and self.expression.type == TokenType.FLOAT:
                pass
            elif currentType != self.expression.type:
                val = "ERROR: Tipos incompatibles"
        else:
            val = "ERROR: Tipos incompatibles"
        ret = {
            "prod" : str(self.left.val) + " := " + val,
            "expr" : self.expression.to_dict(symtable)
        }
        if isinstance(self.expression, BinaryOperationNode):
            key = self.expression.op.type
            if hasattr(self.expression,"val"):
                key = key+ " val="+str(self.expression.val)
            else:
                key = key + " val=ERROR"
            ret = {
                "prod" : str(self.left.val)+ " := "+val,
                "expr" : {
                    key :self.expression.to_dict(symtable)
                }
            }
        if hasattr(self.expression, "type"):
            ret["type"] = self.expression.type
        return ret

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
        if hasattr(self.left, "token"):
            if hasattr(self.left.token, "type"):
                if self.left.token.type == TokenType.IDENTIFIER:
                    symtable.add_line(self.left.token.val, self.left.token.pos)
        if hasattr(self.right, "token"):
            if hasattr(self.right.token,"type"):
                if self.right.token.type == TokenType.IDENTIFIER:
                    symtable.add_line(self.right.token.val, self.right.token.pos)
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

    def to_dict(self, symtable):
        key = "relExp"
        if hasattr(self, "val"):
            key = key + " val="+str(self.val) + " op="+self.op.type
        else:
            key = key + " " + self.op.type
        if hasattr(self.left, "val") and hasattr(self.left, "pos"):
            symtable.add_line(self.left.val, self.left.pos)
        if hasattr(self.right, "val") and hasattr(self.right, "pos"):
            symtable.add_line(self.right.val, self.right.pos)
        return{
            key : {
                "prod" : self.op.type,
                "left" : self.left.to_dict(symtable),
                "right" : self.right.to_dict(symtable),
            }
        }

class NoOperationNode(AST):
    def __init__(self):
        super().__init__()
