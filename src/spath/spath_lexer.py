from typing import List
from ..core.lexer import BaseLexer, Token
from ..enum.spath_types import SPathTypes
from ..errors.sexp_erros import ParserError


class SPathLexer(BaseLexer):
    def tokenize(self) -> List[Token]:  # type: ignore
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
                    tokens.append(Token(SPathTypes.DOT.name, ch, self.pos))
                    self._advance()
                case "=":
                    tokens.append(Token(SPathTypes.EQ.name, ch, self.pos))
                    self._advance()
                case ":":
                    tokens.append(Token(SPathTypes.COLON.name, ch, self.pos))
                    self._advance()
                case "!":
                    tokens.append(self._non_eq())
                    self._advance()
                case "[":
                    tokens.append(Token(SPathTypes.LBRACKET.name, ch, self.pos))
                    self._advance()
                case "]":
                    tokens.append(Token(SPathTypes.RBRACKET.name, ch, self.pos))
                    self._advance()
                case '"':
                    tokens.append(self._string(token_type=SPathTypes.STRING.name))
                case _ if ch.isdigit() or (ch == "-" and self._peek(1).isdigit()):
                    tokens.append(self._number(token_type=SPathTypes.NUMBER.name))
                case _:
                    tokens.append(self._symbol())
        tokens.append(Token(SPathTypes.EOF.name, "", self.pos))
        return tokens

    def _symbol(self) -> Token:
        start_pos = self.pos
        value = ""
        while not self._eof():
            ch = self._peek()
            if ch.isalnum() or ch == "_":
                value += ch
                self._advance()
            else:
                break

        if value in ("true", "false"):
            return Token(SPathTypes.BOOLEAN.name, value, start_pos)
        elif value == "null":
            return Token(SPathTypes.NULL.name, value, start_pos)
        return Token(SPathTypes.IDENT.name, value, start_pos)

    def _slash(self) -> Token:
        if self._peek(1) == "/":
            self._advance()
            return Token(SPathTypes.DOUBLE_SLASH.name, "//", self.pos)
        return Token(SPathTypes.SLASH.name, "/", self.pos)

    def _non_eq(self) -> Token:
        if self._peek(1) == "=":
            self._advance()
            return Token(SPathTypes.NEQ.name, "!=", self.pos)
        raise ParserError(f"Expected '!=' got '!{self._peek(1)} in position {self.pos}")
