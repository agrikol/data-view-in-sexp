from typing import Any, Dict, List, Union


class Scalar:
    """Представление скаляров (int, float, str, bool, None).
    Позволяет хранить значение и получать его тип.
    """

    def __init__(self, value: int | float | str | bool | None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: int | float | str | bool | None):
        if not isinstance(new_value, (int, float, str, bool)) and new_value is not None:
            raise ValueError("Scalar value must be int, float, str, bool, or None")
        self._value = new_value

    @property
    def type(self) -> str:
        return type(self.value).__name__

    def __repr__(self):
        return f"Scalar({self.value})"

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        if not isinstance(self.value, (int, float)):
            raise TypeError("Cannot convert non-int scalar to int")
        return int(self.value)

    def __float__(self):
        if not isinstance(self.value, (float, int)):
            raise TypeError("Cannot convert non-float scalar to float")
        return float(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Scalar):
            return self.value == other.value
        return False

    def __gt__(self, other: Any) -> bool:
        if (
            isinstance(other, Scalar)
            and isinstance(self.value, (int, float))
            and isinstance(other.value, (int, float))
        ):
            return self.value > other.value
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if (
            isinstance(other, Scalar)
            and isinstance(self.value, (int, float))
            and isinstance(other.value, (int, float))
        ):
            return self.value < other.value
        return NotImplemented


class Node:
    """Представление узла дерева.
    Узел может иметь имя, атрибуты (словарь скаляров), дочерние узлы и значение (скаляр).
    Узел не может иметь одновременно значение и дочерние узлы.
    - is_leaf() -> bool: возвращает True, если узел является листом (имеет значение).
    - add_child(child: Node): добавляет дочерний узел.
    - get_childs(name: str) -> List[Node]: возвращает список дочерних узлов с заданным именем.
    - to_sexp() -> str: возвращает строковое представление узла в формате S-expr.
    """

    def __init__(
        self,
        name: str,
        attrs: Dict[str, Scalar] | None = None,
        children: List["Node"] | None = None,
        value: Scalar | None = None,
    ):
        if value and children:
            raise ValueError("A node cannot have both value and children")
        self.name = name
        self.attrs = attrs or {}
        self.children = children or []
        self.value = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not isinstance(new_name, str) or not new_name:
            raise ValueError("Node name must be a non-empty string")
        self._name = new_name

    @property
    def is_leaf(self) -> bool:
        return self.value is not None

    def add_child(self, child: "Node"):
        if self.is_leaf:
            raise ValueError("Cannot add children to a leaf node")
        self.children.append(child)

    def get_childs(self, name: str) -> List["Node"]:
        childs: List["Node"] = self.children
        return [child for child in childs if child.name == name]

    def to_sexp(self) -> str:  # TODO: indent
        attrs: str = " ".join(f"(:{k} {v})" for k, v in self.attrs.items())
        if self.is_leaf:
            return f"({" ".join(filter(None, [self.name, attrs, str(self.value)]))})"
        else:
            children: str = " ".join(child.to_sexp() for child in self.children)
            return f"({" ".join(filter(None, [self.name, attrs, children]))})"


# class Element(Node):
#     def __init__(
#         self,
#         name: str,
#         attrs: Dict[str, Any] | None = None,
#         children: List[Union["Element", "Atom"]] | None = None,
#     ):
#         self.name = name
#         self.attrs = attrs or {}
#         self.children = children or []

#     def __repr__(self):
#         return f"Element({self.name}, attrs={self.attrs}, children={self.children})"


# class Document:
#     def __init__(self, root: Element):
#         self.root = root

#     def find(self, path: str) -> List[Node]:
#         raise NotImplementedError("К реализации. @Игорь")

#     def modify(self, path: str, new_value: Any):
#         raise NotImplementedError("К реализации. @Игорь")
