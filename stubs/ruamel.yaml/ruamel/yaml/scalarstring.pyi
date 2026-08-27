from collections.abc import Callable, Mapping
from typing import Any, Final, SupportsIndex
from typing_extensions import Self

from .anchor import Anchor
from .comments import CommentedMap, CommentedSeq
from .tokens import _ScalarStyle

__all__ = [
    "ScalarString",
    "LiteralScalarString",
    "FoldedScalarString",
    "SingleQuotedScalarString",
    "DoubleQuotedScalarString",
    "PlainScalarString",
    "PreservedScalarString",
]

class ScalarString(str):
    def __new__(cls, value: str, /, *, anchor: str | None = None) -> Self: ...
    def replace(self, old: str, new: str, maxreplace: SupportsIndex = -1, /) -> Self: ...
    @property
    def anchor(self) -> Anchor: ...
    # copilot: scalarstring.py returns None before an anchor is attached and accepts any positionally.
    def yaml_anchor(self, any: bool = False) -> Anchor | None: ...
    def yaml_set_anchor(self, value: str, /, *, always_dump: bool = False) -> None: ...

class LiteralScalarString(ScalarString):
    style: Final[_ScalarStyle] = "|"
    comment: str
    # copilot: scalarstring.py defines subclass __new__ methods with an ordinary optional anchor parameter.
    def __new__(cls, value: str, anchor: str | None = None) -> Self: ...

PreservedScalarString = LiteralScalarString

class FoldedScalarString(ScalarString):
    style: Final[_ScalarStyle] = ">"
    fold_pos: list[int]
    comment: str
    def __new__(cls, value: str, anchor: str | None = None) -> Self: ...

class SingleQuotedScalarString(ScalarString):
    style: Final[_ScalarStyle] = "'"
    def __new__(cls, value: str, anchor: str | None = None) -> Self: ...

class DoubleQuotedScalarString(ScalarString):
    style: Final[_ScalarStyle] = '"'
    def __new__(cls, value: str, anchor: str | None = None) -> Self: ...

class PlainScalarString(ScalarString):
    style: Final[_ScalarStyle] = ""
    def __new__(cls, value: str, anchor: str | None = None) -> Self: ...

def preserve_literal(s: str, /) -> str: ...
def walk_tree(
    base: CommentedMap[Any, Any] | CommentedSeq[Any], map: Mapping[str, Callable[[str], str]] | None = None
) -> None: ...
