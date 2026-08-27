from _typeshed import SupportsWrite
from typing import Literal
from typing_extensions import Self

from .anchor import Anchor
from .scalarint import _Underscore

__all__ = ["ScalarFloat", "ExponentialFloat", "ExponentialCapsFloat"]

class ScalarFloat(float):
    # copilot: scalarfloat.py initializes width and precision from optional keyword metadata.
    _width: int | None
    _prec: int | None
    _m_sign: Literal[False, "+", "-"] | None
    _m_lead0: int
    _exp: Literal["e", "E"] | None
    _e_width: int | None
    _e_sign: bool | None
    _underscore: _Underscore | None
    def __new__(
        cls,
        value: float,
        /,
        width: int | None = None,
        prec: int | None = None,
        m_sign: Literal[False, "+", "-"] | None = None,
        m_lead0: int = 0,
        exp: Literal["e", "E"] | None = None,
        e_width: int | None = None,
        e_sign: bool | None = None,
        underscore: _Underscore | None = None,
        anchor: str | None = None,
    ) -> Self: ...
    # The following methods explicitly return floats
    def __iadd__(self, a: float, /) -> float: ...  # noqa: Y034
    def __ifloordiv__(self, a: float, /) -> float: ...  # noqa: Y034
    def __imul__(self, a: float, /) -> float: ...  # noqa: Y034
    def __ipow__(self, a: float, /) -> float: ...  # type: ignore[override, misc]  # noqa: Y034
    def __isub__(self, a: float, /) -> float: ...  # noqa: Y034
    @property
    def anchor(self) -> Anchor: ...
    # copilot: scalarfloat.py returns None until an anchor is set and accepts its any flag positionally.
    def yaml_anchor(self, any: bool = False) -> Anchor | None: ...
    def yaml_set_anchor(self, value: str, /, *, always_dump: bool = False) -> None: ...
    def dump(self, out: SupportsWrite[str] = ...) -> None: ...

class ExponentialFloat(ScalarFloat):
    # copilot: scalarfloat.py declares width and underscore as ordinary optional parameters on this subclass.
    def __new__(cls, value: float, width: int | None = None, underscore: _Underscore | None = None) -> Self: ...

class ExponentialCapsFloat(ScalarFloat):
    # copilot: scalarfloat.py uses the same positional constructor shape for the capitalized exponent variant.
    def __new__(cls, value: float, width: int | None = None, underscore: _Underscore | None = None) -> Self: ...
