from email.mime import text
import pytest
from src.shared.parser import Lexer, TokenTypes, ParserError, Parser, Token
from src.api.api import loads


def test_parser_simple_node():
    text = "(age 22)"
    node = loads(text)
    assert node.name == "age"
    assert node.is_leaf
    assert node.value.value == 22


def test_parser_empty_node():
    text = "()"
    with pytest.raises(ParserError):
        node = loads(text)


def test_node_with_name():
    text = "(person)"
    node = loads(text)
    assert node.name == "person"
    assert not node.is_leaf
    assert len(node.children) == 0
    assert len(node.attrs) == 0


def test_parser_node_with_attrs():
    text = '(person (:name "Alice") (:age 30))'
    node = loads(text)
    assert node.name == "person"
    assert not node.is_leaf
    assert node.attrs["name"].value == "Alice"
    assert node.attrs["age"].value == 30


def test_parser_node_with_children():
    text = '(person (:name "Alice") (:age 30) (child (:name "Ivan") 10))'
    node = loads(text)
    assert node.name == "person"
    assert not node.is_leaf
    assert len(node.children) == 1
    child = node.children[0]
    assert child.name == "child"
    assert child.attrs["name"].value == "Ivan"
    assert child.value.value == 10


def test_parser_invalid_syntax():
    text1 = '(person (:name "Alice" (:age 30))'
    text2 = '(person (:name "Alice") (:age 30) (child (:name "Ivan") 10)))'
    text3 = '(person (:name "Alice") (:age thirty)'
    text4 = 'person (:name "Alice" (:age 30))'
    with pytest.raises(ParserError):
        loads(text1)
    with pytest.raises(ParserError):
        loads(text2)
    with pytest.raises(ParserError):
        loads(text3)
    with pytest.raises(ParserError):
        loads(text4)
