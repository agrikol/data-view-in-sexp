from typing import List, Tuple, Dict
from ..shared.model import Node, Scalar
from ..enums.parser_enums import TokenTypes, SCALAR_TYPES
import logging
from dataclasses import dataclass
from ..errors.sexp_erros import ParserError
from ..core.parser import BaseParser
from ..core.lexer import BaseLexer

logging.basicConfig(level=logging.DEBUG)


@dataclass
class Token:
    type: str
    value: str
    pos: int


class Lexer(BaseLexer):
    """Лексер для разбора входного текста на токены.
    Поддерживает скобки, строки, числа, булевы значения, null и символы.
    >>> Lexer(text: str).tokenize() -> List[Token] - возвращает список токенов.
    """

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while not self._eof():
            self._skip_whitespace()
            ch = self._peek()

            if ch is None:
                break
            if ch == "(":
                tokens.append(Token(TokenTypes.LPAREN.name, ch, self.pos))
                self._advance()
            elif ch == ")":
                tokens.append(Token(TokenTypes.RPAREN.name, ch, self.pos))
                self._advance()
            elif ch == '"':
                tokens.append(self._string(TokenTypes.STRING.name))
            elif ch.isdigit() or (ch == "-" and self._peek(1).isdigit()):
                tokens.append(self._number(TokenTypes.NUMBER.name))
            else:
                tokens.append(self._symbol())
        tokens.append(Token(TokenTypes.EOF.name, "", self.pos))
        return tokens

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
            return Token(TokenTypes.BOOLEAN.name, value, start_pos)
        elif value == "null":
            return Token(TokenTypes.NULL.name, value, start_pos)
        return Token(TokenTypes.SYMBOL.name, value, start_pos)


class Parser(BaseParser):
    def parse(self) -> Node:
        node = self._parse_node()
        self._expect_eof(TokenTypes.EOF.name)
        return node

    def _is_attr(self) -> bool:
        t1 = self._peek()
        t2 = self._peek(1)
        return (
            t1 is not None
            and t2 is not None
            and t1.type == TokenTypes.LPAREN.name
            and t2.type == TokenTypes.SYMBOL.name
            and t2.value.startswith(":")
        )

    def _parse_attr(self) -> Tuple[str, Scalar]:
        self._expect(TokenTypes.LPAREN.name)
        key_token = self._expect(TokenTypes.SYMBOL.name)
        if not key_token.value.startswith(":"):
            raise ParserError("Attribute key must start with ':'")
        value = self._parse_scalar()
        self._expect(TokenTypes.RPAREN.name)
        return key_token.value[1:], value

    def _parse_scalar(self) -> Scalar:
        token = self._advance()

        if token.type not in SCALAR_TYPES:
            raise ParserError(f"Expected scalar type, got {token}")
        if token.type == TokenTypes.STRING.name:
            return Scalar(token.value)
        elif token.type == TokenTypes.NUMBER.name:
            if "." in token.value:
                return Scalar(float(token.value))
            else:
                return Scalar(int(token.value))
        elif token.type == TokenTypes.BOOLEAN.name:
            return Scalar(token.value == "true")
        elif token.type == TokenTypes.NULL.name:
            return Scalar(None)

        raise ParserError(f"Expected scalar type, got {token}")

    def _parse_node(self) -> Node:
        self._expect(TokenTypes.LPAREN.name)

        name: str = self._expect(TokenTypes.SYMBOL.name).value
        attrs: Dict[str, Scalar] = {}
        children: List[Node] | None = []
        leaf_value: Scalar | None = None

        while self._is_attr():
            k, v = self._parse_attr()
            attrs[k] = v
        if self._peek().type in SCALAR_TYPES:
            leaf_value = self._parse_scalar()
        else:
            while self._peek().type == TokenTypes.LPAREN.name:
                children.append(self._parse_node())
        self._expect(TokenTypes.RPAREN.name)

        return Node(name=name, attrs=attrs, children=children, scalar=leaf_value)
