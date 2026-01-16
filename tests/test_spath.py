import pytest
from sexp_repr import path, loads, dumps

sexp = dumps(
    loads(
        '(book (:lang "ru") (title "Война и мир") (author (:born 1828) "Лев Толстой")\
      (year 1869) (tags (tag "classic") (tag "novel")))'
    )
)
node = loads(sexp)


def test_basic_path():
    p1 = path(sexp, "book")
    assert dumps(p1) == sexp
    p2 = path(sexp, "/book")
    assert dumps(p2) == sexp
    p3 = path(sexp, ".")
    assert dumps(p3) == sexp


def test_children():
    p1 = path(sexp, "book/title")
    title = node.children[0]
    assert dumps(p1) == dumps(title)
    author = node.children[1]
    p2 = path(sexp, "book/author")
    assert dumps(p2) == dumps(author)


def test_absolute_path():
    p1 = path(sexp, "//author")
    author = node.children[1]
    assert dumps(p1) == dumps(author)
    p2 = path(sexp, "//tag")
    tag = node.children[3].children[1]
    assert dumps(p2) == dumps(tag)


def test_attribute():
    p1 = path(sexp, 'book[:lang="ru"]')
    assert p1.attrs["lang"].value == "ru"
    p2 = path(sexp, "book/author[:born=1828]")
    assert p2.attrs["born"].value == 1828
