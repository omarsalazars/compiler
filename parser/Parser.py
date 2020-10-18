from lexer.Rules import TokenType
from .ParseError import ParseError
from .AST import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenPos = 0
        self.current = self.tokens[self.tokenPos]

    def nextSym(self):
        if self.tokenPos < len(self.tokens)-1:
            self.tokenPos = self.tokenPos+1
            self.current = self.tokens[self.tokenPos]

    def accept(self, token):
        if isinstance(token, list):
            if self.current.type in token:
                self.nextSym()
                return True
            else:
                return False
        if self.current.type == token:
            self.nextSym()
            return True
        return False

    def match(self, token):
        if isinstance(token, list):
            if self.current.type in token:
                return True
            else:
                return False
        return self.current.type == token

    def expect(self, token):
        if self.accept(token):
            return True
        error = "Expected token: "
        if isinstance(token, list):
            for t in token:
                error = error + repr(t.type) + '\n'
        else:
            error = error + repr(token) + '\n'
        raise ParseError(self.current.pos, "Unexpected token: %s. %s" % (repr(self.current.type), error))
        return False

    #Start of Grammar Rules

    #MAIN -> main{ DECLARATIONS STATEMENTS }
    def Main(self):
        self.expect(TokenType.MAIN)
        self.expect(TokenType.LB)
        declarations = self.Declarations()
        statements = self.Statements()
        self.expect(TokenType.RB)
        return MainNode("main", declarations, statements)

    #DECLARATIONS -> DECLARATION DECLARATIONS | E
    def Declarations(self):
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        declarations = []
        while self.match(first):
            declarations.append(self.Declaration())
        return declarations

    #DECLARATION -> TYPE VARS ;
    def Declaration(self):
        type = self.Type()
        var = self.Vars()
        self.expect(TokenType.SEMICOLON)
        return DeclarationNode(type, var)
    
    #TYPE -> int | real | boolean
    def Type(self):
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.expect(first)
        return TypeNode(self.current)

    #VARS -> identifier { , identifier }
    def Vars(self):
        vars = []
        vars.append(VarNode(self.current))
        self.expect(TokenType.IDENTIFIER)
        while self.accept(TokenType.COMMA):
            vars.append(VarNode(self.current))
            self.expect(TokenType.IDENTIFIER)
        return vars

    #STATEMENTS -> STATEMENT STATEMENTS | E
    def Statements(self):
        first = [ 
            TokenType.IF, TokenType.WHILE, TokenType.READ,
            TokenType.PRINT, TokenType.LB, TokenType.IDENTIFIER 
        ]
        statements = []
        while self.match(first):
            statements.append(self.Statement())
        return statements
            

    #STATEMENT -> IF_STMT | WHILE_STMT | READ_STMT | PRINT_STMT | BLOCK_STMT | ASSIGN_STMT
    def Statement(self):
        if self.match(TokenType.IF):
            statement = self.If()
        elif self.match(TokenType.WHILE):
            statement = self.While()
        elif self.match(TokenType.READ):
            statement = self.Read()
        elif self.match(TokenType.PRINT):
            statement = self.Print()
        elif self.match(TokenType.LB):
            statement = self.Block()
        elif self.match(TokenType.IDENTIFIER):
            statement = self.Assign()
        else:
            raise ParseError(self.current.pos, "Unexpected token")
        return statement

    #IF_STMT -> if ( RELATIONAL_EXPRESSION ) BLOCK_STMT { ELSE_STMT }
    def If(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LP)
        relationalExpression = self.RelationalExpression()
        self.expect(TokenType.RP)
        block = self.Block()
        if self.match(TokenType.ELSE):
            elseNode = self.Else()
            return IfNode(relationalExpression, block, elseNode)
        return IfNode(relationalExpression, block)

    def Else(self):
        self.expect(TokenType.ELSE)
        if self.match(TokenType.IF):
            return self.If()
        elif self.match(TokenType.LB):
            return self.Block()
        raise ParseError(self.current.pos, "Unexpected token")

    #WHILE_STMT -> while ( RELATIONAL_EXPRESSION ) BLOCK_STMT
    def While(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LP)
        relationalExpression = self.RelationalExpression()
        self.expect(TokenType.RP)
        block = self.Block()
        return WhileNode(relationalExpression, block)

    #READ_STMT -> read id ;
    def Read(self):
        self.expect(TokenType.READ)
        var = self.current
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.SEMICOLON)
        return ReadNode(var)

    #PRINT_STMT -> print RELATIONAL_EXPESSION ;
    def Print(self):
        self.expect(TokenType.PRINT)
        relationalExpression = self.RelationalExpression()
        self.expect(TokenType.SEMICOLON)
        return PrintNode(relationalExpression)

    #BLOCK_STMT -> { STATEMENTS }
    def Block(self):
        self.expect(TokenType.LB)
        statements = self.Statements()
        self.expect(TokenType.RB)
        return BlockNode(statements)

    #ASSIGN_STMT -> id = RELATIONAL_EXPRESSION ;
    def Assign(self):
        left = self.current
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUALS)
        relationalExpression = self.RelationalExpression()
        self.expect(TokenType.SEMICOLON)
        return AssignNode(left, relationalExpression)
    
    #RELATIONAL_EXPRESSION -> EXPRESSION { RELOP EXPRESSION }*
    def RelationalExpression(self):
        RELOP = [
            TokenType.LT, TokenType.GT, TokenType.GET, TokenType.LET,
            TokenType.ET, TokenType.NE
        ]
        relationalExpression = self.Expression()
        relop = self.current
        if self.accept(RELOP):
            rightExpression = self.Expression()
            relationalExpression = RelationalExpressionNode(relationalExpression, relop, rightExpression)
        return relationalExpression

    #EXPRESSION -> TERM { ADDOP TERM }
    def Expression(self):
        ADDOP = [ TokenType.PLUS, TokenType.MINUS ]
        node = self.Term()
        op = self.current
        while self.accept(ADDOP):
            right = self.Term()
            node = BinaryOperationNode(node, op, right)
            op = self.current
        return node

    #TERM -> FACTOR { MULOP FACTOR }
    def Term(self):
        MULOP = [ TokenType.MULTIPLY, TokenType.DIVIDE ]
        node = self.Factor()
        op = self.current
        while self.accept(MULOP):
            right = self.Factor()
            node = BinaryOperationNode(node, op, right)
            op = self.current
        return node

    #FACTOR -> id | number | (EXPRESSION)
    def Factor(self):
        LITERAL = [
            TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.SNUMBER,
            TokenType.FLOAT, TokenType.SFLOAT, TokenType.BOOLEAN
        ]
        if self.accept(TokenType.LP):
            node = self.Expression()
            self.expect(TokenType.RP)
        else:
            node = NumNode(self.current)
            self.expect(LITERAL)
            #Good production
        return node

    def parse(self):
       return self.Main()
