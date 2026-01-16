from typing import Iterable, List
from .ast import Filter, FilterTarget, SPath, Step, CompareOp, Literal
from ..shared.model import Node


class SPathEngine:
    def evaluate(self, root: Node, spath: SPath) -> list[Node]:
        current = [root]

        for step in spath.steps:
            current = self._apply_step(current, step)

        return current

    def _apply_step(self, nodes: list[Node], step: Step) -> list[Node]:
        result: list[Node] = []

        for node in nodes:
            if step.name is None:
                candidates = [node]

            elif step.recursive:
                candidates = [node] + self._descendants(node)

            else:
                candidates = [node] + node.children

            for cand in candidates:
                if step.name is not None and cand.name != step.name:
                    continue
                if self._apply_filters(cand, step.filters):
                    result.append(cand)

        return result

    def _descendants(self, node: Node) -> list[Node]:
        result = []
        stack = list(node.children)

        while stack:
            cur = stack.pop()
            result.append(cur)
            stack.extend(cur.children)

        return result

    def _apply_filters(self, node: Node, filters: list[Filter]) -> bool:
        return all(self._match_filter(node, f) for f in filters)

    def _match_filter(self, node: Node, flt: Filter) -> bool:
        if flt.target is FilterTarget.ATTRIBUTE:
            if flt.key not in node.attrs:
                return False
            lhs = node.attrs[flt.key].value

        elif flt.target is FilterTarget.FIELD:
            fields = [
                c.scalar.value for c in node.children if c.name == flt.key and c.is_leaf  # type: ignore
            ]
            if not fields:
                return False
            lhs = fields[0]

        else:
            raise ValueError(f"Unknown filter target: {flt.target}")

        return self._compare(lhs, flt.op, flt.value)

    def _compare(self, lhs, op: CompareOp, rhs) -> bool:
        if op is CompareOp.EQ:
            return lhs == rhs
        if op is CompareOp.NEQ:
            return lhs != rhs
        raise ValueError(op)
