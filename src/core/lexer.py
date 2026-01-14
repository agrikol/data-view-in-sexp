from dataclasses import dataclass
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

    def _peek(self, offset: int = 0) -> str | None:
        if self.pos + offset < len(self.text):
            return self.text[self.pos + offset]

    def _eof(self) -> bool:
        return self.pos >= len(self.text)

    def _skip_whitespace(self) -> None:
        while not self._eof() and self.text[self.pos].isspace():
            self.pos += 1

    def _advance(self) -> str:
        self.pos += 1
        return self.text[self.pos - 1]
