from src.shared.model import Node, Scalar
from dataclasses import dataclass
from typing import Literal


class InterpreterError(Exception):
    pass


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
            (max_occurs null)))))))
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


@dataclass
class SchemaNode:
    name: str
    # kind: Literal["element", "attribute", "children", "value"]
    # value: Scalar | None

    value_type = Literal["string", "number", "boolean", "null"] | None = None
    required: bool = True

    min_occurs: int = 1
    max_occurs: int | Literal["unbounded"] = 1

    attrs: dict[str, Scalar]
    children: list["SchemaNode"]


TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


class Interpreter:
    def __init__(self, ast: Node):
        self.ast: Node = ast

    def interpret(self) -> SchemaNode:
        self._check_schema(self.ast.name, self.ast.attrs, self.ast.value)
        if not self.ast.children or len(self.ast.children) != 1:
            raise InterpreterError("Schema must contain exactly one root element")
        return self._interpret_node(self.ast.children[0])

    def _interpret_node(self, node: Node) -> SchemaNode:
        name = node.name
        attrs = node.attrs
        scalar = node.value
        children = node.children

        if name != "element":
            raise InterpreterError(f"Expected 'element' node, got '{name}'")
        element_name = attrs.get("name")
        if not isinstance(element_name, Scalar):
            raise InterpreterError("Schema element must have name attribute")

        schema = SchemaNode(
          name=element_name,
        )

        for child in children:
            match child.name:
                case "type":
                    schema.value_type = child.value
                case "required":
                    schema.required = bool(child.value)
                case "min_occurs":
                    schema.min_occurs = int(child.value)
                case "max_occurs":
                    schema.max_occurs = (
                        "unbounded" if child.value is None else int(child.value))
                case "attrs":
                    self._collect_attrs(child, schema)
                
                case "children":
                    self._collect_children(child, schema)
                    
        return schema
    

    def _collect_children(self, node: Node, schema: SchemaNode):
        for element in node.children:
            if element.name != "element":
                raise InterpreterError("children can only contain element")

            schema.children.append(
                self._interpret_node(element)
            )
    
    def _collect_attrs(self, node: Node, schema: SchemaNode):
        for attr in node.children:
            if attr.name != "attr":
                raise InterpreterError("Attrs can only contain attr")
            attr_name = attr.attrs.get("name")
            if attr_name is None:
                raise InterpreterError(
                    "Attribute must have name attribute"
                )
            
            attr_schema = SchemaNode(name=attr_name)

            for prop in attr.children:
                if prop.name == "type":
                    attr_schema.value_type = prop.value

                elif prop.name == "required":
                    attr_schema.required = bool(prop.value)

            schema.attrs[attr_name] = attr_schema



    def _check_schema(
        self, name: str, attrs: dict[str, Scalar] | None, scalar: Scalar | None
    ) -> None:
        if name != "schema":
            raise InterpreterError(f"Root node must be 'schema', got '{name}'")
        if len(attrs) > 1 or (not attrs.get("version") and len(attrs) == 1):
            raise InterpreterError("Schema node can only have 'version' attribute")
        if scalar is not None:
            raise InterpreterError("Schema node cannot have a scalar value")
