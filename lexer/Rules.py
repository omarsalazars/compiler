from enum import Enum
class TokenType(str, Enum):
    MAIN = "main"
    IF = "if"
    THEN = "then"
    ELSE = "else"
    END = "end"
    DO = "do"
    WHILE = "while"
    UNTIL = "until"
    REAL = "real"
    INT = "int"
    BOOLEAN = "boolean"
    READ = "cin"
    PRINT = "cout"
    SFLOAT = "signed float"
    FLOAT = "float"
    SNUMBER = "signed number"
    NUMBER = "number"
    IDENTIFIER = "identifier"
    INC = "++"
    DEC = "--"
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
    EQUALS = ":="
    SEMICOLON = ";"
    LB = "{"
    RB = "}"
    COMMA = ","
    COMMENT = "comment"


rules = [
    #Reserved Words
    ('\/\/[^\n\r]*?(?:\*\)|[\n\r])', TokenType.COMMENT),
    ('main', TokenType.MAIN),
    ('if', TokenType.IF),
    ('then', TokenType.THEN),
    ('else', TokenType.ELSE),
    ('end', TokenType.END),
    ('while', TokenType.WHILE),
    ('do', TokenType.DO),
    ('until', TokenType.UNTIL),
    ('real', TokenType.REAL),
    ('int', TokenType.INT),
    ('boolean', TokenType.BOOLEAN),
    ('cin', TokenType.READ),
    ('cout', TokenType.PRINT),
    #Floats
    ('-\d+\.\d+', TokenType.SFLOAT),
    ('\d+\.\d+', TokenType.FLOAT),
    #Integers
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
    (':=', TokenType.EQUALS),
    #Semicolon
    (';', TokenType.SEMICOLON),
    #Comma
    (',', TokenType.COMMA),
]

