from enum import Enum, auto
from dataclasses import dataclass


@dataclass(frozen=True)
class TreeStyle:
    leaf: str
    branch: str
    trunk: str
    space: str


UNICODE_STYLE = TreeStyle(
    branch="├── ",
    leaf="└── ",
    trunk="│   ",
    space="    ",
)

ASCII_STYLE = TreeStyle(
    branch="|-- ",
    leaf="`-- ",
    trunk="|   ",
    space="    ",
)
