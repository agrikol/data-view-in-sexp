from typing import List, Tuple, Dict
from ..shared.model import Node, Scalar
from ..core.lexer import BaseLexer, Token
from ..enum.spath_types import SPathTokens


class SPathLexer(BaseLexer):
    def tokenize(self) -> List[SPathToken]:  # type: ignore
        tokens: List[Token] = []
        while not self._eof():
            self._skip_whitespace()
            ch = self._peek()

            match ch:
                case None:
                    break
                case "/":
                    tokens.append(self._slash())
                    self._advance()
                case ".":
                    tokens.append(Token(SPathTokens.DOT.name, ch, self.pos))
                    self._advance()
                case "=":
                    tokens.append(Token(SPathTokens.EQ.name, ch, self.pos))
                    self._advance()
                case "!":
                    tokens.append(self._non_eq())
                    self._advance()
                case "[":
                    tokens.append(Token(SPathTokens.LBRACKET.name, ch, self.pos))
                    self._advance()
                case "]":
                    tokens.append(Token(SPathTokens.RBRACKET.name, ch, self.pos))
                    self._advance()
                case '"':
                    tokens.append(self._string())
                case _ if ch.isdigit() or (ch == "-" and self._peek(1).isdigit()):  # type: ignore
                    tokens.append(self._number())
                # case _ if ch.isalpha():
                #     tokens.append(self._ident())
                case _:
                    tokens.append(self._symbol())

    def _string(self) -> Token | None: ...

    def _number(self) -> Token | None: ...

    def _symbol(self) -> Token | None: ...

    def _slash(self) -> Token | None: ...

    def _non_eq(self) -> Token | None: ...
