import pytest
from sexp_repr import path, loads

sexp = '(book (:lang "ru") (title "Война и мир") (author (:born 1828) "Лев Толстой")\
      (year 1869) (tags (tag "classic") (tag "novel")))'


def test_basic_path():
    p1 = path(sexp, "book")
    # print(p1)
    # p2 = path(sexp, ".")
    # p3 = path(sexp, "/book")
    assert p1 == sexp
