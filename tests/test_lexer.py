import pytest
from src.shared.parser import Lexer, TokenTypes, Token, ParserError


def test_lexer_simple_expression():
    text = "(define x 42)"
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    expected_types = [
        TokenTypes.LPAREN.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.NUMBER.name,
        TokenTypes.RPAREN.name,
        TokenTypes.EOF.name,
    ]

    assert [token.type for token in tokens] == expected_types


def test_lexer_string_and_bool():
    text = '(set name "Alice" active true)'
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    expected_types = [
        TokenTypes.LPAREN.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.STRING.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.BOOLEAN.name,
        TokenTypes.RPAREN.name,
        TokenTypes.EOF.name,
    ]

    assert [token.type for token in tokens] == expected_types


def test_lexer_nested_expression():
    text = '(person (:age 22) (child "Ivan"))'
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    expected_types = [
        TokenTypes.LPAREN.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.LPAREN.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.NUMBER.name,
        TokenTypes.RPAREN.name,
        TokenTypes.LPAREN.name,
        TokenTypes.SYMBOL.name,
        TokenTypes.STRING.name,
        TokenTypes.RPAREN.name,
        TokenTypes.RPAREN.name,
        TokenTypes.EOF.name,
    ]

    assert [token.type for token in tokens] == expected_types
    assert [
        token.value for token in tokens if token.type == TokenTypes.STRING.name
    ] == ["Ivan"]
    assert [
        token.value for token in tokens if token.type == TokenTypes.NUMBER.name
    ] == ["22"]


def test_lexer_empty_input():
    text = ""
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == TokenTypes.EOF.name


def test_lexer_only_whitespace():
    text = "   \n\t  "
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    assert len(tokens) == 1
    assert tokens[0].type == TokenTypes.EOF.name


def test_lexer_number_formats():
    number1 = "-123"
    number2 = "45.67"
    number3 = "-45.67"
    number4 = "0"
    number5 = "-0."
    number6 = "12.34.56"
    lexer1 = Lexer(number1).tokenize()
    lexer2 = Lexer(number2).tokenize()
    lexer3 = Lexer(number3).tokenize()
    lexer4 = Lexer(number4).tokenize()
    assert lexer1[0].type == TokenTypes.NUMBER.name
    assert lexer1[0].value == number1
    assert lexer2[0].type == TokenTypes.NUMBER.name
    assert lexer2[0].value == number2
    assert lexer3[0].type == TokenTypes.NUMBER.name
    assert lexer3[0].value == number3
    assert lexer4[0].type == TokenTypes.NUMBER.name
    assert lexer4[0].value == number4
    with pytest.raises(ParserError):
        Lexer(number5).tokenize()
    assert Lexer(number6).tokenize()[0].type == TokenTypes.NUMBER.name
    assert Lexer(number6).tokenize()[0].value == "12.34"
