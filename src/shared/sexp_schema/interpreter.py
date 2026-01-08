from src.shared.model import Node, Scalar
from dataclasses import dataclass, field
from typing import Literal
from src.errors.sexp_erros import InterpreterError


@dataclass
class SchemaNode:
    name: str
    value_type: Literal["string", "number", "boolean", "null"] | None = None

    required: bool = False
    min_occurs: int = 1
    max_occurs: int | Literal["unbounded"] = "unbounded"

    attrs: dict[str, "SchemaNode"] = field(default_factory=dict)
    children: list["SchemaNode"] = field(default_factory=list)


class Interpreter:
    def __init__(self, ast: Node):
        self.ast: Node = ast

    def interpret(self) -> SchemaNode:
        self._check_schema(self.ast.name, self.ast.attrs, self.ast.scalar)
        if not self.ast.children or len(self.ast.children) != 1:
            raise InterpreterError("Schema must contain exactly one root element")
        return self._interpret_node(self.ast.children[0])

    def _interpret_node(self, node: Node) -> SchemaNode:
        name = node.name
        attr = node.attrs
        children = node.children

        if name != "element":
            raise InterpreterError(f"Expected 'element' node, got '{name}'")
        element_name = attr.get("name")
        if not isinstance(element_name, Scalar):
            raise InterpreterError("Schema element must have name attribute")

        schema = SchemaNode(
            name=element_name.value,
        )

        for child in children:
            match child.name:
                case "type":
                    self._check_type_correctness(child.scalar.value)
                    schema.value_type = child.scalar
                case "required":
                    self._check_required_correctness(child.scalar.value)
                    schema.required = child.scalar == Scalar(True)
                case "min_occurs":
                    self._check_min_occurs_correctness(child.scalar.value, schema)
                    schema.min_occurs = int(child.scalar)
                case "max_occurs":
                    self._check_max_occurs_correctness(child.scalar.value, schema)
                    schema.max_occurs = (
                        int(child.scalar)
                        if child.scalar.value is not None
                        and child.scalar.value != "unbounded"
                        else "unbounded"
                    )

                case "attrs":
                    self._collect_attrs(child, schema)
                case "children":
                    self._collect_children(child, schema)
        return schema

    def _collect_attrs(self, node: Node, schema: SchemaNode):
        for attr in node.children:
            if attr.name != "attr":
                raise InterpreterError("Attrs can only contain attr")
            attr_name = attr.attrs.get("name")
            if attr_name.value == "" or attr_name is None:
                raise InterpreterError("Attribute must have name attribute")

            attr_schema = SchemaNode(name=attr_name)

            for prop in attr.children:
                match prop.name:
                    case "type":
                        self._check_type_correctness(prop.scalar.value)
                        attr_schema.value_type = prop.scalar
                    case "required":
                        self._check_required_correctness(prop.scalar.value)
                        attr_schema.required = prop.scalar == "true"

            schema.attrs[attr_name.value] = attr_schema

    def _collect_children(self, node: Node, schema: SchemaNode):
        for element in node.children:
            schema.children.append(self._interpret_node(element))

    def _check_max_occurs_correctness(self, value, schema: SchemaNode):
        if value != "unbounded" and value < schema.min_occurs:
            raise InterpreterError("Max_occurs cannot be less than min_occurs")

    def _check_min_occurs_correctness(self, value: int, schema: SchemaNode):
        if value < 1 and schema.required:
            raise InterpreterError("Min_occurs cannot be with required attribute")
        if value < 0:
            raise InterpreterError("Min_occurs cannot be negative")

    def _check_required_correctness(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise InterpreterError("Required must be true or false")

    def _check_type_correctness(self, value: str) -> None:
        if value not in ("string", "number", "boolean", "null"):
            raise InterpreterError(
                f"Type must be string, number, boolean or null, got {value}"
            )

    def _check_schema(
        self, name: str, attrs: dict[str, Scalar] | None, scalar: Scalar | None
    ) -> None:
        if name != "schema":
            raise InterpreterError(f"Root node must be 'schema', got '{name}'")
        if len(attrs) > 1 or (not attrs.get("version") and len(attrs) == 1):
            raise InterpreterError("Schema node can only have 'version' attribute")
        if scalar is not None:
            raise InterpreterError("Schema node cannot have a scalar value")
