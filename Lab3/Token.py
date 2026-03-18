from enum import Enum, auto

class TokenType(Enum):
    # Data Types
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()

    # Keywords & Built-ins
    LET = auto()
    PRINT = auto()
    SIN = auto()
    COS = auto()
    IF = auto()
    ELSE = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()
    EQUALS = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    # File / Error control
    EOF = auto()
    ILLEGAL = auto()

# Map string keywords to TokenType
KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "sin": TokenType.SIN,
    "cos": TokenType.COS,
    "if": TokenType.IF,
    "else": TokenType.ELSE
}

class Token:
    def __init__(self, type_: TokenType, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"Token(type={self.type.name}, value='{self.value}', line={self.line}, col={self.column})"
    
    def __str__(self):
        return self.__repr__()
