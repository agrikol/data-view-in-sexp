from typing import Any, Dict, List, Union


class Scalar:
    """Представление скаляров (int, float, str, bool, None).
    Позволяет хранить значение, получать его тип, делать сравнения и приведения к другим типам.
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

    def to_sexp(self) -> str:
        if isinstance(self.value, str):
            return f'"{self.value}"'
        if self.value is None:
            return "null"
        if isinstance(self.value, bool):
            return "true" if self.value else "false"
        return str(self.value)


class Node:
    """Представление узла дерева.
    Узел может иметь имя, атрибуты (словарь скаляров), дочерние узлы и значение (скаляр).
    Узел не может иметь одновременно значение и дочерние узлы.
    >>> is_leaf() -> bool: возвращает True, если узел является листом (имеет значение).
    >>> add_child(child: Node): добавляет дочерний узел.
    >>> get_childs(name: str) -> List[Node]: возвращает список дочерних узлов с заданным именем.
    >>> to_sexp() -> str: возвращает строковое представление узла в формате S-expr.
    """

    def __init__(
        self,
        name: str,
        attrs: Dict[str, Scalar] | None = None,
        children: List["Node"] | None = None,
        scalar: Scalar | None = None,
    ):
        if scalar and children:
            raise ValueError("A node cannot have both value and children")
        self.name = name
        self.attrs = attrs or {}
        self.children = children or []
        self.scalar = scalar

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        if not isinstance(new_name, str) or not new_name:
            raise ValueError("Node name must be a non-empty string")
        if " " in new_name or "(" in new_name or ")" in new_name:
            raise ValueError("Node name cannot contain spaces or parentheses")
        if new_name.startswith(":"):
            raise ValueError("Node name cannot start with a colon")
        self._name = new_name

    @property
    def is_leaf(self) -> bool:
        return self.scalar is not None

    def add_child(self, child: "Node"):
        if self.is_leaf:
            raise ValueError("Cannot add children to a leaf node")
        self.children.append(child)

    def get_childs_by_name(self, name: str) -> List["Node"]:
        childs: List["Node"] = self.children
        return [child for child in childs if child.name == name]

    @property
    def get_childs(self) -> List["Node"]:
        return self.children

    def to_sexp(self) -> str:  # TODO: indent
        attrs: str = " ".join([f"(:{k} {v.to_sexp()})" for k, v in self.attrs.items()])
        if self.is_leaf:
            assert self.scalar is not None
            return (
                f"({" ".join(filter(None, [self.name, attrs, self.scalar.to_sexp()]))})"
            )
        else:
            children: str = " ".join(child.to_sexp() for child in self.children)
            return f"({" ".join(filter(None, [self.name, attrs, children]))})"

    def __repr__(self):
        return (
            f"Node(name={self.name!r}, attrs={self.attrs!r}, "
            f"children={self.children!r}, value={self.scalar!r})"
        )

    def __str__(self):
        return self.to_sexp()
