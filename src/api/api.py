from src.shared.parser import Lexer, Parser
from src.shared.model import Node


def loads(text: str) -> Node:
    """Метод для преобразования S-выражения в формате строки в объектное AST-дерево.

    Args:
        text (str): Входная строка в формате S-выражения.
    >>> loads('(person (:name "Alice") (:age 30) (child (:name "Ivan") 10))')
        Node(name='person', attrs={'name': Scalar(value='Alice'), 'age': Scalar(value=30)}, children=[Node(name='child', attrs={'name': Scalar(value='Ivan')}, children=None, value=10)], value=None)

    Returns:
        Node: Объектное AST-дерево.
    """
    return Parser(Lexer(text).tokenize()).parse()


def dumps(node: Node) -> str:
    """Метод для преобразования объектного AST-дерева в строковое S-выражение.

    Args:
        node (Node): Входное объектное AST-дерево.
    >>> dumps(Node(name='person', attrs={'name': Scalar(value='Alice'), 'age': Scalar(value=30)}, children=[Node(name='child', attrs={'name': Scalar(value='Ivan')}, children=None, value=10)], value=None))
        '(person (:name "Alice") (:age 30) (child (:name "Ivan") 10))'

    Returns:
        str: Строковое S-выражение.
    """
    return node.to_sexp()
