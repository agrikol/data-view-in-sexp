from src.shared.parser import Lexer, Parser
from src.sexp_schema.interpreter import Interpreter
from src.sexp_schema.validator import Validator
from src.shared.model import Node
from src.visualizer.cli import TreeRenderer
from src.spath.engine import SPathEngine
from src.spath.ast import SPath
from src.spath.spath_parser import SPathParser
from src.spath.spath_lexer import SPathLexer


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
    >>> validate(Node(name="person", attrs={"name": Scalar("Alice")}), \
        Node(name="schema", attrs={"name": Scalar("person")}))
    # True
    """

    schema = Interpreter(schema_document).interpret()
    return Validator(document, schema).validate()


def tree(document: Node | str) -> None:
    """
    Print document as a tree to stdout. \
    You can put the document as a raw S-exp string or as a Node.

    Parameters
    ----------
    document: Node | str
        Document to print. If it is a string, it is parsed into a Node.

    Returns
    -------
    None

    Example
    --------
    >>> tree(Node(name="person", attrs={"name": Scalar("Alice")}))
    # Print the document as a tree

    >>> tree('(:name "Alice")')
    # Print the document as a tree
    """
    if isinstance(document, str):
        document = loads(document)
    TreeRenderer().render(document)


def path(document: Node | str, path: SPath | str) -> Node:
    """
    Evaluate a path on a document.

    Parameters
    ----------
    document: Node | str
        Document to evaluate the path on. If it is a string, it is parsed into a Node.
    path: SPath | str
        Path to evaluate. If it is a string, it is parsed into a SPath.

    Returns
    -------
    Node
        Result of the evaluation.

    Example
    --------
    >>> path(Node(name="person", attrs={"name": Scalar("Alice")}), \
        '/person')
    # Node(name='person', attrs={'name': Scalar('Alice')}, children=None, value=None)
    """
    if isinstance(document, str):
        document = loads(document)
    if isinstance(path, str):
        path = SPathParser(SPathLexer(path).tokenize()).parse()
    result = SPathEngine().evaluate(document, path)
    return result[0] if len(result) == 1 else result
