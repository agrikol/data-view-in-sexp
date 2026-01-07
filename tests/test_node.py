import pytest
from src.shared.model import Node, Scalar


def test_leaf_node():
    node = Node(name="age", attrs=None, children=None, scalar=Scalar(22))
    assert node.is_leaf
    assert isinstance(node.scalar, Scalar)
    assert node.scalar.value == 22


def test_to_sexp_leaf():
    node = Node("age", None, None, Scalar(22))
    assert node.to_sexp() == "(age 22)"


def test_to_sexp_with_attrs():
    node = Node("person", {"name": Scalar("Alice"), "age": Scalar(30)}, None, None)
    assert node.to_sexp() == '(person (:name "Alice") (:age 30))'


def test_to_sexp_boolean_and_null_attrs():
    node = Node(
        "settings", {"active": Scalar(True), "value": Scalar(None)}, scalar=Scalar(None)
    )
    assert node.to_sexp() == "(settings (:active true) (:value null) null)"


def test_to_sexp_with_children():
    child1 = Node("age", None, None, Scalar(22))
    child2 = Node("name", None, None, Scalar("Bob"))
    parent = Node("person", None, [child1, child2], None)
    assert parent.to_sexp() == '(person (age 22) (name "Bob"))'


def test_invalid_node_name():
    with pytest.raises(ValueError):
        Node("", None, None, Scalar(10))
    with pytest.raises(ValueError):
        Node("invalid name")
    with pytest.raises(ValueError):
        Node("(invalid)")
    with pytest.raises(ValueError):
        Node(":invalid")
    assert Node("valid_name").name == "valid_name"


# def test_non_scalar_value():
#     with pytest.raises(ValueError):
#         Node("test", None, None, "not a scalar")
#     with pytest.raises(ValueError):
#         Node("test", None, None, [1, 2, 3])
#     with pytest.raises(ValueError):
#         Node("test", {"key": "value"})
