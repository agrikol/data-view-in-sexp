from src.shared.parser import Lexer, Parser
from src.shared.sexp_schema.interpreter import Interpreter, SchemaNode
from src.shared.sexp_schema.validator import Validator
from src.shared.model import Node


def loads(text: str) -> Node:
    """
    Parse an S-expression string into an AST.

    Parameters
    ----------
    text: str
        Input string containing an S-expression.

    Returns
    -------
    Node
        Root node of the parsed AST.

    Example
    --------
    >>> loads('(person (:name "Alice") (:age 30) (child (:name "Ivan") 10))')
    Node(
        name='person',
        attrs={'name': Scalar('Alice'), 'age': Scalar(30)},
        children=[
            Node(
                name='child',
                attrs={'name': Scalar('Ivan')},
                children=None,
                value=10
            )
        ],
        value=None
    )
    """
    return Parser(Lexer(text).tokenize()).parse()


def dumps(node: Node) -> str:
    """
    Serialize an AST node into an S-expression string.

    Parameters
    ----------
    node: Node
        AST node to serialize.

    Returns
    -------
    str
        S-expression representation of the AST.

    Example
    --------
    >>> dumps(Node(
    ...     name='person',
    ...     attrs={'name': Scalar('Alice'), 'age': Scalar(30)},
    ...     children=[
    ...         Node(
    ...             name='child',
    ...             attrs={'name': Scalar('Ivan')},
    ...             children=None,
    ...             value=10
    ...         )
    ...     ],
    ...     value=None
    ... ))
    (person (:name "Alice") (:age 30) (child (:name "Ivan") 10))'
    """
    return node.to_sexp()


def validate(document: Node, schema_document: Node) -> bool:
    """
    Validate a document against a schema.

    Parameters
    ----------
    document: Node
        Document to validate.
    schema_document: Node
        Schema to validate against.

    Returns
    -------
    bool
        True if the document is valid against the schema or Exception otherwise.

    Example
    --------
    >>> validate(Node(name="person", attrs={"name": Scalar("Alice")}), Node(name="schema", attrs={"name": Scalar("person")}))
    # True
    """

    schema = Interpreter(schema_document).interpret()
    return Validator(document, schema).validate()
