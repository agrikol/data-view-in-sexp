from enum import Enum, auto


class TokenTypes(Enum):
    LPAREN: str = "LPAREN"
    RPAREN: str = "RPAREN"
    STRING: str = "STRING"
    NUMBER: str = "NUMBER"
    BOOLEAN: str = "BOOLEAN"
    NULL: str = "NULL"
    KEY: str = "KEY"
    SYMBOL: str = "SYMBOL"
    WHITESPACE: str = "WHITESPACE"
    EOF: str = "EOF"


SCALAR_TYPES: set = {"STRING", "NUMBER", "BOOLEAN", "NULL"}
