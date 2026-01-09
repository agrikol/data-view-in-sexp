import pytest
from src.api.core import loads, validate, dumps
from src.errors.sexp_erros import ValidationError
from src.shared.model import Node, Scalar

test_schema_sexp = """
(schema
  (element
    (:name "book")
    (attrs
      (attr (:name "lang") (type "string") (required false)))
    (children
      (element
        (:name "title")
        (type "string")
        (required true))

      (element
        (:name "author")
        (type "string")
        (required true)
        (attrs
          (attr (:name "born") (type "number") (required false))))

      (element
        (:name "year")
        (type "number")
        (required true))

      (element
        (:name "tags")
        (children
          (element
            (:name "tag")
            (type "string")
            (min_occurs 0)
            (max_occurs "unbounded")))))))
"""

test_sexp = """
(book
  (:lang "ru")
  (title "Война и мир")
  (author (:born 1828) "Лев Толстой")
  (year 1869)
  (tags
    (tag "classic")
    (tag "novel")))
"""


def test_validate_1():
    document = loads('(person (:name "Alice"))')
    schema = loads(
        '(schema (element (:name "person") (attrs (attr (:name "name") (type "string") (required true)))))'
    )
    assert validate(document, schema)


def test_validate_2():
    document = loads('(person (:name "Alice") (:age 30))')
    schema_1 = loads(
        '(schema (element (:name "person") (attrs (attr (:name "name") (type "string") (required true)))))'
    )
    with pytest.raises(ValidationError):
        validate(document, schema_1)
    schema_2 = loads(
        '(schema (element (:name "person") (attrs (attr (:name "name") (type "string") (required true)) (attr (:name "age") (type "number") (required true)))))'
    )
    assert validate(document, schema_2)


def test_validate_3():
    document: Node = loads(test_sexp)
    schema: Node = loads(test_schema_sexp)
    assert validate(document, schema)
    document.attrs = {}
    assert validate(document, schema)
