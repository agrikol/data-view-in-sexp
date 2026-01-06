from src.shared.sexp_schema.interpreter import SchemaNode
from src.shared.model import Node


class ValidationError(Exception):
    pass


class Validator:
    def __init__(self, document: Node, schema: SchemaNode):
        self.document: Node = document
        self.schema: SchemaNode = schema

    def validate(self) -> bool:
        return True
