from errors.sexp_erros import ParserError
from .lexer import Token
from typing import List


class BaseParser:
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    def parse(self):
        raise NotImplementedError

    def _peek(self, offset: int = 0) -> Token:  # type: ignore
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]

    def _expect_eof(self, token_type) -> None:
        if self._peek() == token_type:
            raise ParserError("Expected end of input (EOF)")

    def _expect(self, token_type: str) -> Token:
        token = self._peek()
        if token is None or token.type != token_type:
            raise ParserError(
                f"Expected token of type {token_type}, got {token} at position {self.pos}"
            )
        self.pos += 1
        return token

    def _advance(self) -> Token:
        token = self._peek()
        if token is None:
            raise ParserError("Unexpected end of input")
        self.pos += 1
        return token

    def _peek_type(self) -> str | None:
        token = self._peek()
        if token:
            return token.type
