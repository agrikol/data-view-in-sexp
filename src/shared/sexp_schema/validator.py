from src.shared.sexp_schema.interpreter import SchemaNode
from src.shared.model import Node
from src.errors.sexp_erros import ValidationError
from collections import defaultdict


TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


class Validator:
    def __init__(self, document: Node, schema: SchemaNode):
        self.document: Node = document
        self.schema: SchemaNode = schema

    def validate(self) -> bool:
        self._validate_node(self.document, self.schema)
        return True

    def _validate_node(self, document: Node, schema: SchemaNode) -> None:
        self._check_name(document.name, schema.name)
        self._check_value(document, schema)
        self._check_attrs(document, schema)
        self._check_children(document, schema)

    def _check_name(self, document_name: str, schema_name: str) -> None:
        if document_name != schema_name:
            raise ValidationError(
                f"Document name {document_name} does not match schema name {schema_name}"
            )

    def _check_value(self, document: Node, schema: SchemaNode) -> None:
        if schema.value_type is None:
            if document.scalar is not None:
                raise ValidationError(f"Element '{schema.name}' must not have a value")
            return

        if document.scalar is None:
            raise ValidationError(f"Element '{schema.name}' must have a value")

        py_type = TYPE_MAP.get(schema.value_type.value)
        if not isinstance(document.scalar.value, py_type):
            raise ValidationError(
                f"Element '{schema.name}' must have a value of type {schema.value_type}"
            )

    def _check_attrs(self, document: Node, schema: SchemaNode) -> None:
        for name, attr_schema in schema.attrs.items():
            if attr_schema.required and name not in document.attrs:
                raise ValidationError(
                    f"Attribute '{name}' is required in element '{schema.name}'"
                )
        for name, value in document.attrs.items():
            if name not in schema.attrs:
                raise ValidationError(
                    f"Attribute '{name}' is not allowed in element '{schema.name}'"
                )
            attr_schema: SchemaNode = schema.attrs[name]
            py_type = TYPE_MAP.get(attr_schema.value_type.value)
            if not isinstance(value.value, py_type):
                raise ValidationError(
                    f"Attribute '{name}' must have a value of type {attr_schema.value_type}"
                )

    def _check_children(self, document: Node, schema: SchemaNode) -> None:
        doc_children = defaultdict(list)
        schema_child_names = set()
        for child in document.children:
            doc_children[child.name].append(child)

        for child_schema in schema.children:
            schema_child_names.add(child_schema.name)
            occurrences = len(doc_children.get(child_schema.name, []))

            self._check_min_occurs(child_schema, occurrences)
            self._check_max_occurs(child_schema, occurrences)

            for child in doc_children.get(child_schema.name, []):
                self._validate_node(child, child_schema)

        self._check_unexpected(doc_children.keys(), schema_child_names, schema.name)

    def _check_min_occurs(self, child_schema: SchemaNode, occurrences: int) -> None:
        if occurrences < child_schema.min_occurs:
            raise ValidationError(
                f"Element '{child_schema.name}' occurs {occurrences} times, "
                f"minimum is {child_schema.min_occurs} (parent '{child_schema.name}')"
            )

    def _check_max_occurs(self, child_schema: SchemaNode, occurrences: int) -> None:
        if (
            child_schema.max_occurs != "unbounded"
            and occurrences > child_schema.max_occurs
        ):
            raise ValidationError(
                f"Element '{child_schema.name}' occurs {occurrences} times, "
                f"maximum is {child_schema.max_occurs} (parent '{child_schema.name}')"
            )

    def _check_unexpected(
        self, doc_children: list[str], schema_child_names: set[str], schema_name: str
    ):
        for name in doc_children:
            if name not in schema_child_names:
                raise ValidationError(
                    f"Unexpected child element '{name}' in element '{schema_name}'"
                )
