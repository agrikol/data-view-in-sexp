from enum import Enum, auto


class TokenTypes(Enum):
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    KEY = "KEY"
    SYMBOL = "SYMBOL"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"


SCALAR_TYPES: set = {"STRING", "NUMBER", "BOOLEAN", "NULL"}
