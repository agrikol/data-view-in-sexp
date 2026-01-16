from ..core.parser import BaseParser
from ..enums.spath_types import SPathTypes

from ..errors.sexp_erros import ParserError
from typing import List

from spath.ast import (
    SPath,
    Step,
    Filter,
    FilterTarget,
    CompareOp,
)


TYPES_TO_PYTYPES: dict = {
    "NUMBER": int,
    "STRING": str,
    "BOOLEAN": bool,
    "NULL": None,
}


class SPathParser(BaseParser):
    def parse(self) -> SPath:
        path = self._parse_path()
        self._expect_eof(SPathTypes.EOF.name)
        return path

    def _parse_path(self) -> SPath:
        absolute = False
        steps: List[Step] = []

        if self._peek_type() == SPathTypes.SLASH.name:
            absolute = True
            self._advance()
        elif self._peek_type() == SPathTypes.DOUBLE_SLASH.name:
            absolute = True
            self._advance()
            steps.append(self._parse_step(recursive=True))

        if self._peek_type() in (
            SPathTypes.IDENT.name,
            SPathTypes.DOT.name,
        ):
            steps.append(self._parse_step(recursive=False))

        while self._peek_type() in (
            SPathTypes.SLASH.name,
            SPathTypes.DOUBLE_SLASH.name,
        ):
            recursive = self._peek_type() == SPathTypes.DOUBLE_SLASH.name
            self._advance()
            steps.append(self._parse_step(recursive=recursive))

        if not steps:
            raise ParserError("Empty path")

        return SPath(absolute=absolute, steps=steps)

    def _parse_step(self, recursive: bool) -> Step:
        token = self._peek()

        if token.type == SPathTypes.DOT.name:
            self._advance()
            name = None
        elif token.type == SPathTypes.IDENT.name:
            name = token.value
            self._advance()
        else:
            raise ParserError(f"Expected step, got {token}")

        filters = []
        while self._peek_type() == SPathTypes.LBRACKET.name:
            filters.append(self._parse_filter())

        return Step(
            name=name,
            recursive=recursive,
            filters=filters,
        )

    def _parse_filter(self) -> Filter:
        self._expect(SPathTypes.LBRACKET.name)

        if self._peek_type() == SPathTypes.COLON.name:
            self._advance()
            target = FilterTarget.ATTRIBUTE
        else:
            target = FilterTarget.FIELD

        key_token = self._expect(SPathTypes.IDENT.name)
        key = key_token.value

        op_token = self._advance()
        if op_token.type == SPathTypes.EQ.name:
            op = CompareOp.EQ
        elif op_token.type == SPathTypes.NEQ.name:
            op = CompareOp.NEQ
        else:
            raise ParserError(f"Expected comparison operator, got {op_token}")

        value = self._parse_literal()

        self._expect(SPathTypes.RBRACKET.name)

        return Filter(
            target=target,
            key=key,
            op=op,
            value=value,
        )

    def _parse_literal(self):
        token = self._advance()

        match token.type:
            case "NUMBER" | "STRING":
                return TYPES_TO_PYTYPES[token.type](token.value)
            case "BOOLEAN":
                return TYPES_TO_PYTYPES[token.type](token.value == "true")
            case "NULL":
                return TYPES_TO_PYTYPES[token.type]
            case _:
                raise ParserError(f"Expected literal, got {token}")
