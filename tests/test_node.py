import pytest
from src.shared.model import Node, Scalar


def test_leaf_node():
    node = Node(name="age", attrs=None, children=None, value=Scalar(22))
    assert node.is_leaf
    assert isinstance(node.value, Scalar)
    assert node.value.value == 22


def test_to_sexp_leaf():
    node = Node("age", None, None, Scalar(22))
    assert node.to_sexp() == "(age 22)"


def test_to_sexp_with_attrs():
    node = Node("person", {"name": Scalar("Alice"), "age": Scalar(30)}, None, None)
    assert node.to_sexp() == "(person (:name Alice) (:age 30))"


def test_to_sexp_with_children():
    child1 = Node("age", None, None, Scalar(22))
    child2 = Node("name", None, None, Scalar("Bob"))
    parent = Node("person", None, [child1, child2], None)
    assert parent.to_sexp() == "(person (age 22) (name Bob))"
