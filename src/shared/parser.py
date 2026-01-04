import re
from typing import List, Tuple, Dict, Any
from src.shared.model import Node, Scalar
import logging
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.DEBUG)


class ParserError(Exception):
    pass


@dataclass
class Token:
    type: str
    value: str
    pos: int


class TokenTypes(Enum):
    LPAREN: str = "LPAREN"
    RPAREN: str = "RPAREN"
    STRING: str = "STRING"
    NUMBER: str = "NUMBER"
    BOOL: str = "BOOL"
    NULL: str = "NULL"
    KEY: str = "KEY"
    SYMBOL: str = "SYMBOL"
    WHITESPACE: str = "WHITESPACE"
    EOF: str = "EOF"


class Lexer:
    """Лексер для разбора входного текста на токены.
    Поддерживает скобки, строки, числа, булевы значения, null и символы.
    >>> Lexer(text: str).tokenize() -> List[Token] - возвращает список токенов.
    """

    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def tokenize(self) -> List[Token]:
        tokens = []
        while not self._eof():
            self._skip_whitespace()
            ch = self._peek()

            logging.debug(f"Current char: {str(ch)} at pos {self.pos}")
            if ch is None:
                break
            if ch == "(":
                tokens.append(Token(TokenTypes.LPAREN.name, ch, self.pos))
                self._advance()
            elif ch == ")":
                tokens.append(Token(TokenTypes.RPAREN.name, ch, self.pos))
                self._advance()
            elif ch == '"':
                tokens.append(self._string())
            elif ch.isdigit() or (ch == "-" and self._peek(1).isdigit()):
                tokens.append(self._number())
            else:
                tokens.append(self._symbol())
        tokens.append(Token(TokenTypes.EOF.name, "", self.pos))
        return tokens

    def _peek(self, offset: int = 0) -> str | None:
        if self.pos + offset < len(self.text):
            return self.text[self.pos + offset]

    def _eof(self) -> bool:
        return self.pos >= len(self.text)

    def _skip_whitespace(self) -> None:
        while not self._eof() and self.text[self.pos].isspace():
            self.pos += 1

    def _advance(self) -> None:
        self.pos += 1
        return self.text[self.pos - 1]

    def _string(self) -> Token:
        start_pos = self.pos
        self._advance()
        value = ""
        print(value)
        while not self._eof():
            ch = self._peek()
            if ch == '"':
                self._advance()
                return Token(TokenTypes.STRING.name, value, start_pos)
            value += ch
            self._advance()
        raise SyntaxError("Unterminated string literal")

    def _number(self) -> Token:
        start_pos = self.pos
        value = ""
        if self._peek() == "-":
            value += self._advance()
        while not self._eof() and self._peek().isdigit():
            value += self._advance()
        if not self._eof() and self._peek() == ".":
            try:
                self._peek(1).isdigit()
            except Exception:
                raise ParserError("Invalid number format")
            value += self._advance()
            while not self._eof() and self._peek().isdigit():
                value += self._advance()
        return Token(TokenTypes.NUMBER.name, value, start_pos)

    def _symbol(self) -> Token:
        start_pos = self.pos
        value = ""
        while not self._eof():
            ch = self._peek()
            if ch.isspace() or ch in "()":
                break
            value += ch
            self._advance()

        if value in ("true", "false"):
            return Token(TokenTypes.BOOL.name, value, start_pos)
        elif value == "null":
            return Token(TokenTypes.NULL.name, value, start_pos)
        return Token(TokenTypes.SYMBOL.name, value, start_pos)
