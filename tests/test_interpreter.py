import pytest
from src.shared.sexp_schema.interpreter import Interpreter, SchemaNode
from src.shared.model import Scalar
from src.api.api import loads, dumps
from src.errors.sexp_erros import InterpreterError


def test_simple_1():
    ast = loads('(schema (element (:name "book")))')
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"


def test_value_type_1():
    ast = loads('(schema (element (:name "book") (type "string")))')
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"
    assert schema.value_type == Scalar("string")


def test_value_type_2():
    ast = loads('(schema (element (:name "book") (type "number")))')
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"
    assert schema.value_type == Scalar("number")


def test_value_type_3():
    ast = loads('(schema (element (:name "book") (type "boolean")))')
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"
    assert schema.value_type == Scalar("boolean")


def test_value_type_4():
    ast = loads('(schema (element (:name "book") (type "null")))')
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"
    assert schema.value_type == Scalar("null")


def test_required():
    ast = loads('(schema (element (:name "book") (type "string") (required true)))')
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"
    assert schema.value_type == Scalar("string")
    assert schema.required == True


def test_occurs_1():
    ast = loads(
        '(schema (element (:name "book") (type "string") (min_occurs 2) (max_occurs 3)))'
    )
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.name == "book"
    assert schema.value_type == Scalar("string")
    assert schema.min_occurs == 2
    assert schema.max_occurs == 3


def test_occurs_2():
    ast = loads(
        '(schema (element (:name "book") (type "string") (min_occurs 2) (max_occurs "unbounded")))'
    )
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.min_occurs == 2
    assert schema.max_occurs == "unbounded"


def test_wrong_occurs_1():
    ast = loads(
        '(schema (element (:name "book") (type "string") (min_occurs 3) (max_occurs 2)))'
    )
    interpreter = Interpreter(ast)
    with pytest.raises(InterpreterError):
        interpreter.interpret()


def test_wrong_occurs_2():
    ast = loads(
        '(schema (element (:name "book") (type "string") (required true) (max_occurs 0)))'
    )
    interpreter = Interpreter(ast)
    with pytest.raises(InterpreterError):
        interpreter.interpret()


def test_wrong_occurs_3():
    ast = loads('(schema (element (:name "book") (type "string") (min_occurs -1)))')
    interpreter = Interpreter(ast)
    with pytest.raises(InterpreterError):
        interpreter.interpret()


def test_attrs_1():
    ast = loads(
        '(schema (element (:name "book") (attrs (atr (:name "lang") (type "string") (required false)))))'
    )
    interpreter = Interpreter(ast)
    with pytest.raises(InterpreterError):
        interpreter.interpret()


def test_attrs_2():
    ast = loads(
        '(schema (element (:name "book") (attrs (attr (:name "lang") (type "string")))))'
    )
    interpreter = Interpreter(ast)
    schema: SchemaNode = interpreter.interpret()
    assert schema.attrs["lang"].name == Scalar("lang")
    assert schema.attrs["lang"].value_type == Scalar("string")


def test_attrs_3():
    ast = loads(
        '(schema (element (:name "book") (attrs (attr (:name "") (type "string") (required true)))))'
    )
    interpreter = Interpreter(ast)
    with pytest.raises(InterpreterError):
        interpreter.interpret()


def test_one_children():
    ast = loads(
        '(schema (element (:name "book") (children (element (:name "chapter")))))'
    )
    interpreter = Interpreter(ast)
    schema = interpreter.interpret()
    assert len(schema.children) == 1


def test_children():
    ast = loads(
        '(schema (element (:name "book") (children (element (:name "chapter") (type "string")))))'
    )
    interpreter = Interpreter(ast)
    schema = interpreter.interpret()
    assert schema.children[0].value_type == Scalar("string")

    ast = loads(
        '(schema (element (:name "book") (children (element (:name "chapter") (type "number")))))'
    )
    interpreter = Interpreter(ast)
    schema = interpreter.interpret()
    assert schema.children[0].value_type == Scalar("number")


def test_two_children():
    ast = loads(
        '(schema (element (:name "book") (children (element (:name "chapter")) (element (:name "chapter")))))'
    )
    interpreter = Interpreter(ast)
    schema = interpreter.interpret()
    assert len(schema.children) == 2


def test_wrong_children():
    ast = loads(
        '(schema (element (:name "book") (children (elem (:name "chapter") (type "string") (required true)))))'
    )
    interpreter = Interpreter(ast)
    with pytest.raises(InterpreterError):
        interpreter.interpret()
