from enum import Enum
class TokenType(str, Enum):
    MAIN = "main"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    REAL = "real"
    INT = "int"
    BOOLEAN = "boolean"
    READ = "read"
    PRINT = "print"
    SFLOAT = "signed float"
    FLOAT = "float"
    SNUMBER = "signed number"
    NUMBER = "number"
    IDENTIFIER = "identifier"
    INC = "++"
    DEC =  "--"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULUS = "%"
    LP = "("
    RP = ")"
    LT = "<"
    GT = ">"
    GET = ">="
    LET = "<="
    ET = "=="
    NE = "!="
    EQUALS = "="
    SEMICOLON = ";"
    LB = "{"
    RB = "}"
    COMMA = ","


rules = [
    #Reserved Words
    ('main', TokenType.MAIN),
    ('if', TokenType.IF),
    ('else', TokenType.ELSE),
    ('while', TokenType.WHILE),
    ('real', TokenType.REAL),
    ('int', TokenType.INT),
    ('boolean', TokenType.BOOLEAN),
    ('read', TokenType.READ),
    ('print', TokenType.PRINT),
    #Floats
    ('-\d+\.\d+', TokenType.SFLOAT),
    ('\d+\.\d+', TokenType.FLOAT),
    #Integers
    ('-\d+', TokenType.SNUMBER),
    ('\d+', TokenType.NUMBER),
    #Identifiers
    ('[a-zA-Z_]\w*', TokenType.IDENTIFIER),
    #Arithmetic
    ('\+\+', TokenType.INC),
    ('\-\-', TokenType.DEC),
    ('\+', TokenType.PLUS),
    ('\-', TokenType.MINUS),
    ('\*', TokenType.MULTIPLY),
    ('\/', TokenType.DIVIDE),
    ('%', TokenType.MODULUS),
    #Parenthesis
    ('\(', TokenType.LP),
    ('\)', TokenType.RP),
    #Brackets
    ('\{', TokenType.LB),
    ('\}', TokenType.RB),
    #Relops
    ('\<', TokenType.LT),
    ('\>', TokenType.GT),
    ('\>=', TokenType.GET),
    ('\<=', TokenType.LET),
    ('==', TokenType.ET),
    ('!=', TokenType.NE),
    #Equals
    ('=', TokenType.EQUALS),
    #Semicolon
    (';', TokenType.SEMICOLON),
    #Comma
    (',', TokenType.COMMA),
]

