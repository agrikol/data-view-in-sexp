from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union


Literal = Union[str, int, float, bool, None]


class CompareOp(Enum):
    EQ = "="
    NEQ = "!="


class FilterTarget(Enum):
    FIELD = "field"
    ATTRIBUTE = "attribute"


@dataclass
class Filter:
    target: FilterTarget
    key: str
    op: CompareOp
    value: Literal


@dataclass
class Step:
    name: Optional[str]
    recursive: bool
    filters: List[Filter]


@dataclass
class SPath:
    absolute: bool
    steps: List[Step]
