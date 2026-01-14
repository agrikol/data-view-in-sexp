from enum import Enum


class SPathTokens(Enum):
    IDENT = "IDENT"
    SLASH = "/"
    DOUBLE_SLASH = "//"
    DOT = "."
    EQ = "="
    NEQ = "!="
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    NULL = "null"
    AT = "@"
    LBRACKET = "["
    RBRACKET = "]"
    EOF = "EOF"
