from lexer.Rules import TokenType
from .ParseError import ParseError
from .TreeNode import TreeNode

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
        self.Declarations()
        self.Statements()
        self.expect(TokenType.RB)

    #DECLARATIONS -> DECLARATION DECLARATIONS | E
    def Declarations(self):
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        while self.match(first):
            self.Declaration()

    #DECLARATION -> TYPE VARS ;
    def Declaration(self):
        self.Type()
        self.Vars()
        self.expect(TokenType.SEMICOLON)
    
    #TYPE -> int | real | boolean
    def Type(self):
        first = [TokenType.INT, TokenType.REAL, TokenType.BOOLEAN]
        self.expect(first)

    #VARS -> identifier { , identifier }
    def Vars(self):
        self.expect(TokenType.IDENTIFIER)
        while self.accept(TokenType.COMMA):
            self.expect(TokenType.IDENTIFIER)

    #STATEMENTS -> STATEMENT STATEMENTS | E
    def Statements(self):
        first = [ 
            TokenType.IF, TokenType.WHILE, TokenType.READ,
            TokenType.PRINT, TokenType.LB, TokenType.IDENTIFIER 
        ]
        while self.match(first):
            self.Statement()
            

    #STATEMENT -> IF_STMT | WHILE_STMT | READ_STMT | PRINT_STMT | BLOCK_STMT | ASSIGN_STMT
    def Statement(self):
        if self.match(TokenType.IF):
            self.If()
        elif self.match(TokenType.WHILE):
            self.While()
        elif self.match(TokenType.READ):
            self.Read()
        elif self.match(TokenType.PRINT):
            self.Print()
        elif self.match(TokenType.LB):
            self.Block()
        elif self.match(TokenType.IDENTIFIER):
            self.Assign()
        else:
            raise ParseError(self.current.pos, "Unexpected token")

    #IF_STMT -> if ( RELATIONAL_EXPRESSION ) BLOCK_STMT { ELSE_STMT }
    def If(self):
        self.expect(TokenType.IF)
        self.expect(TokenType.LP)
        self.RelationalExpression()
        self.expect(TokenType.RP)
        self.Block()
        if self.match(TokenType.ELSE):
            Else()

    #WHILE_STMT -> while ( RELATIONAL_EXPRESSION ) BLOCK_STMT
    def While(self):
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LP)
        self.RelationalExpression()
        self.expect(TokenType.RP)
        Block()

    #READ_STMT -> read id ;
    def Read(self):
        self.expect(TokenType.READ)
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.SEMICOLON)

    #PRINT_STMT -> print RELATIONAL_EXPESSION ;
    def Print(self):
        self.expect(TokenType.PRINT)
        self.RelationalExpression()
        self.expect(TokenType.SEMICOLON)

    #BLOCK_STMT -> { STATEMENTS }
    def Block(self):
        self.expect(TokenType.LB)
        self.Statements()
        self.expect(TokenType.RB)

    #ASSIGN_STMT -> id = RELATIONAL_EXPRESSION ;
    def Assign(self):
        self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQUALS)
        self.RelationalExpression()
        self.expect(TokenType.SEMICOLON)
    
    #RELATIONAL_EXPRESSION -> EXPRESSION { RELOP EXPRESSION }
    def RelationalExpression(self):
        RELOP = [
            TokenType.LT, TokenType.GT, TokenType.GET, TokenType.LET,
            TokenType.ET, TokenType.NE
        ]
        self.Expression()
        if self.accept(RELOP):
            self.Expression()

    #EXPRESSION -> TERM { ADDOP TERM }
    def Expression(self):
        ADDOP = [ TokenType.PLUS, TokenType.MINUS ]
        self.Term()
        while self.accept(ADDOP):
            self.Term()
    
    #TERM -> FACTOR { MULOP FACTOR }
    def Term(self):
        MULOP = [ TokenType.MULTIPLY, TokenType.DIVIDE ]
        self.Factor()
        while self.accept(MULOP):
            self.Factor()

    #FACTOR -> id | number | (EXPRESSION)
    def Factor(self):
        LITERAL = [
            TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.SNUMBER,
            TokenType.FLOAT, TokenType.SFLOAT, TokenType.BOOLEAN
        ]
        if self.accept(TokenType.LP):
            self.Expression()
            self.expect(TokenType.RP)
        else:
            self.expect(LITERAL)
            #Good production

    def parse(self):
       self.Main() 
