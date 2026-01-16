from enum import Enum


class SPathTypes(Enum):
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
    COLON = ":"
    LBRACKET = "["
    RBRACKET = "]"
    EOF = "EOF"
