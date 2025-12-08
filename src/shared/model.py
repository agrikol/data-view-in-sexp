from typing import Any, Dict, List, Union


class Node:
    pass


class Element(Node):
    def __init__(
        self,
        name: str,
        attrs: Dict[str, Any] | None = None,
        children: List[Union["Element", "Atom"]] | None = None,
    ):
        self.name = name
        self.attrs = attrs or {}
        self.children = children or []

    def __repr__(self):
        return f"Element({self.name}, attrs={self.attrs}, children={self.children})"


class Atom(Node):
    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f"Atom({self.value})"


class Document:
    def __init__(self, root: Element):
        self.root = root

    def find(self, path: str) -> List[Node]:
        raise NotImplementedError("К реализации. @Игорь")

    def modify(self, path: str, new_value: Any):
        raise NotImplementedError("К реализации. @Игорь")


def parse_sexp(sexp: str) -> Document:
    raise NotImplementedError("К реализации. @Дима")
