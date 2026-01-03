import pytest
from src.shared.model import Scalar


def test_scalar_int():
    s = Scalar(10)
    assert s.value == 10
    assert s.type == "int"
    assert int(s) == 10
    assert float(s) == 10.0
    assert bool(s) is True
    assert str(s) == "10"


def test_scalar_float():
    s = Scalar(3.14)
    assert s.value == 3.14
    assert s.type == "float"
    assert int(s) == 3
    assert float(s) == 3.14
    assert bool(s) is True
    assert str(s) == "3.14"


def test_scalar_str():
    s = Scalar("hello")
    assert s.value == "hello"
    assert s.type == "str"
    assert str(s) == "hello"
    assert bool(s) is True


def test_scalar_bool():
    s = Scalar(True)
    assert s.value is True
    assert s.type == "bool"
    assert bool(s) is True
    assert str(s) == "True"


def test_scalar_none():
    s = Scalar(None)
    assert s.value is None
    assert s.type == "NoneType"
    assert bool(s) is False
    assert str(s) == "None"


def test_scalar_invalid_type():
    with pytest.raises(ValueError):
        Scalar([1, 2, 3])  # type: ignore
    with pytest.raises(ValueError):
        Scalar({"key": "value"})  # type: ignore


def test_scalar_equality():
    s1 = Scalar(10)
    s2 = Scalar(10)
    s3 = Scalar(20)
    assert s1 == s2
    assert s1 != s3


def test_scalar_comparison():
    s1 = Scalar(10)
    s2 = Scalar(20)
    s3 = Scalar("hello")
    assert s1 < s2
    assert s2 > s1
    with pytest.raises(TypeError):
        s1 < s3  # type: ignore
    with pytest.raises(TypeError):
        s1 > s3  # type: ignore
