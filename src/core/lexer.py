from dataclasses import dataclass
from errors.sexp_erros import ParserError
from typing import List


@dataclass
class Token:
    type: str
    value: str
    pos: int


class BaseLexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def tokenize(self) -> List[Token]:
        raise NotImplementedError

    def _peek(self, offset: int = 0) -> str:
        if self.pos + offset < len(self.text):
            return self.text[self.pos + offset]
        return None  # type: ignore

    def _eof(self) -> bool:
        return self.pos >= len(self.text)

    def _skip_whitespace(self) -> None:
        while not self._eof() and self.text[self.pos].isspace():
            self.pos += 1

    def _advance(self) -> str:
        self.pos += 1
        return self.text[self.pos - 1]

    def _string(self, token_type) -> Token:
        start_pos = self.pos
        self._advance()
        value = ""
        while not self._eof():
            ch = self._peek()
            if ch == '"':
                self._advance()
                return Token(token_type, value, start_pos)
            if ch is not None:
                value += ch
            self._advance()
        raise SyntaxError("Unterminated string literal")

    def _number(self, token_type) -> Token:
        start_pos = self.pos
        value = ""
        if self._peek() == "-":
            value += self._advance()
        while not self._eof() and self._peek().isdigit():  # type: ignore
            value += self._advance()
        if not self._eof() and self._peek() == ".":
            try:
                self._peek(1).isdigit()  # type: ignore
            except Exception:
                raise ParserError("Invalid number format")
            else:
                value += self._advance()
                while not self._eof() and self._peek().isdigit():  # type: ignore
                    value += self._advance()
        return Token(token_type, value, start_pos)

    def _symbol(self) -> Token:
        raise NotImplementedError
