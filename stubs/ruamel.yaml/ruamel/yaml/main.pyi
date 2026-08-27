from _typeshed import Unused
from collections.abc import Callable, Iterable, Iterator, Sequence
from pathlib import Path
from re import Pattern
from types import ModuleType, TracebackType
from typing import Any, ClassVar, Final, Literal, NoReturn, Protocol, TypeVar, overload, type_check_only
from typing_extensions import Self, TypeAlias, deprecated

from _ruamel_yaml import CEmitter, CParser

from .comments import CommentedMap, CommentedSeq
from .compat import VersionType, _ReadStream, _WriteStream
from .composer import Composer
from .constructor import BaseConstructor, Constructor, RoundTripConstructor, _ConstructorFunction, _MultiConstructorFunction
from .docinfo import DocInfo
from .dumper import BaseDumper, RoundTripDumper
from .emitter import Emitter, RoundTripEmitter, _Inf, _LineBreak
from .events import Event
from .loader import BaseLoader
from .nodes import Node
from .parser import Parser, RoundTripParser
from .reader import Reader
from .representer import BaseRepresenter, Representer, RoundTripRepresenter, _RepresenterFunction
from .resolver import BaseResolver
from .scanner import RoundTripScanner, Scanner
from .serializer import Serializer
from .tag import Tag, _TagHandleToPrefix
from .tokens import Token, _ScalarStyle, _VersionTuple

_T = TypeVar("_T")
_Constructor = TypeVar("_Constructor", bound=BaseConstructor)
_Representer = TypeVar("_Representer", bound=BaseRepresenter)

_YAMLType: TypeAlias = str | Literal["rt", "safe", "unsafe", "full", "base"]  # noqa: Y051

# type aliases to avoid name clashes and make mypy happy
_Reader: TypeAlias = Reader
_Scanner: TypeAlias = Scanner
_Parser: TypeAlias = Parser
_Composer: TypeAlias = Composer
_Emitter: TypeAlias = Emitter
_Serializer: TypeAlias = Serializer

class YAML:
    typ: list[_YAMLType]
    pure: Final[bool]
    plug_ins: list[ModuleType]
    Resolver: type[BaseResolver]
    allow_unicode: bool
    Reader: type[Reader] | None
    Representer: type[BaseRepresenter]
    Constructor: type[BaseConstructor]
    Scanner: type[Scanner] | None
    Serializer: type[Serializer] | None
    default_flow_style: bool | None
    comment_handling: int | None
    # copilot: main.py initializes max_depth to zero and Composer uses it to limit nested composition.
    max_depth: int
    Emitter: type[Emitter | CEmitter]
    Parser: type[Parser | CParser]
    Composer: type[Composer]
    stream: None
    canonical: bool | None
    old_indent: int | None
    width: int | _Inf | None
    line_break: _LineBreak | None
    map_indent: int | None
    sequence_indent: int | None
    sequence_dash_offset: int
    compact_seq_seq: bool | None
    compact_seq_map: bool | None
    sort_base_mapping_type_on_output: bool | None
    top_level_colon_align: int | Literal[True] | None
    prefix_colon: str | None
    preserve_quotes: bool | None
    allow_duplicate_keys: bool
    encoding: str
    explicit_start: bool | None
    explicit_end: bool | None
    doc_infos: list[DocInfo]
    default_style: _ScalarStyle | None
    top_level_block_style_scalar_no_indent_error_1_1: bool
    scalar_after_indicator: bool | None
    brace_single_entry_mapping_in_flow_sequence: bool
    boolean_representation: Sequence[str]
    @overload
    def __new__(
        cls,
        *,
        typ: Literal["rt"] | list[Literal["rt"]] | None = None,
        pure: bool = False,
        output: Path | _WriteStream | None = None,
        plug_ins: list[str] | None = None,
    ) -> _RoundTripYAML: ...
    @overload
    def __new__(
        cls,
        *,
        typ: Literal["full"] | list[Literal["full"]],
        pure: bool = False,
        output: Path | _WriteStream | None = None,
        plug_ins: list[str] | None = None,
    ) -> _FullYAML: ...
    @overload
    def __new__(
        cls,
        *,
        typ: _YAMLType | list[_YAMLType],
        pure: bool = False,
        output: Path | _WriteStream | None = None,
        plug_ins: list[str] | None = None,
    ) -> Self: ...
    # This redundant overload prevents type checkers from matching the deprecated "unsafe" overload
    # when users are typing `YAML(typ=)`.
    @overload
    def __init__(
        self,
        *,
        typ: Literal["rt"] | list[Literal["rt"]] | None = None,
        pure: bool = False,
        output: Path | _WriteStream | None = None,
        plug_ins: list[str] | None = None,
    ) -> None: ...
    @overload
    @deprecated("For **dumping only** use YAML(typ='full')", category=PendingDeprecationWarning)
    def __init__(
        self,
        *,
        typ: Literal["unsafe"] | list[Literal["unsafe"]],
        pure: bool = False,
        output: Path | _WriteStream | None = None,
        plug_ins: list[str] | None = None,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        typ: _YAMLType | list[_YAMLType],
        pure: bool = False,
        output: Path | _WriteStream | None = None,
        plug_ins: list[str] | None = None,
    ) -> None: ...
    @property
    def reader(self) -> _Reader: ...
    @property
    def scanner(self) -> _Scanner: ...
    @property
    def parser(self) -> _Parser | CParser | None: ...
    @property
    def composer(self) -> _Composer: ...
    @property
    def constructor(self) -> BaseConstructor: ...
    @property
    def resolver(self) -> BaseResolver: ...
    @property
    def emitter(self) -> _Emitter | CEmitter | None: ...
    @property
    def serializer(self) -> _Serializer: ...
    @property
    def representer(self) -> BaseRepresenter: ...
    def scan(self, stream: _ReadStream) -> Iterator[Token]: ...
    def parse(self, stream: _ReadStream) -> Iterator[Event]: ...
    def compose(self, stream: Path | _ReadStream) -> Node: ...
    def compose_all(self, stream: _ReadStream) -> Iterator[Node]: ...
    def load(self, stream: Path | _ReadStream) -> Any: ...
    def load_all(self, stream: Path | _ReadStream) -> Iterator[Any]: ...
    def get_constructor_parser(self, stream: _ReadStream) -> tuple[BaseConstructor, _Parser | CParser]: ...
    def emit(self, events: Iterable[Event], stream: _WriteStream) -> None: ...
    # copilot: main.py permits stream=None for serialize APIs and for context-managed dump(), while dump_all still requires a stream.
    def serialize(self, node: Node, stream: _WriteStream | None = None) -> None: ...
    def serialize_all(self, nodes: Iterable[Node], stream: _WriteStream | None = None) -> None: ...
    def dump(
        self, data: Any, stream: Path | _WriteStream | None = None, *, transform: Callable[[str], str] | None = None
    ) -> None: ...
    def dump_all(
        self, documents: Iterable[Any], stream: Path | _WriteStream, *, transform: Callable[[str], str] | None = None
    ) -> None: ...
    def Xdump_all(
        self, documents: Iterable[Any], stream: Path | _WriteStream, *, transform: Callable[[str], str] | None = None
    ) -> None: ...
    def get_serializer_representer_emitter(
        self, stream: _WriteStream, tlca: int | None
    ) -> tuple[_Serializer, BaseRepresenter, _Emitter | CEmitter]: ...
    @overload
    def map(self) -> dict[Any, Any]: ...
    @overload
    def map(self, **kw: _T) -> dict[str, _T]: ...
    @overload
    def seq(self) -> list[Any]: ...
    @overload
    def seq(self, iterable: Iterable[_T], /) -> list[_T]: ...
    def official_plug_ins(self) -> list[str]: ...
    def register_class(self, cls: _RegistrableClass) -> _RegistrableClass: ...
    def __enter__(self) -> _YAMLContext: ...
    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None: ...
    @property
    def version(self) -> _VersionTuple | None: ...
    @version.setter
    def version(self, val: VersionType) -> None: ...
    @property
    def tags(self) -> _TagHandleToPrefix | None: ...
    @tags.setter
    def tags(self, val: _TagHandleToPrefix | None) -> None: ...
    @property
    def indent(self) -> _IndentSetter: ...
    @indent.setter
    def indent(self, val: int | None) -> None: ...
    @property
    def block_seq_indent(self) -> int: ...
    @block_seq_indent.setter
    def block_seq_indent(self, val: int) -> None: ...
    def compact(self, seq_seq: bool | None = None, seq_map: bool | None = None) -> None: ...

# copilot: _IndentSetter describes the callable property implemented by YAML._indent and is not a runtime class.
@type_check_only
class _IndentSetter(Protocol):
    def __call__(self, mapping: int | None = None, sequence: int | None = None, offset: int | None = None) -> None: ...

# copilot: these pseudo-subclasses express YAML.__new__'s typ-dependent return types and do not exist at runtime.
@type_check_only
class _RoundTripYAML(YAML):
    Representer: type[RoundTripRepresenter]
    Constructor: type[RoundTripConstructor]
    Scanner: type[RoundTripScanner]
    Emitter: type[RoundTripEmitter]
    Parser: type[RoundTripParser]
    @overload
    def map(self) -> CommentedMap[Any, Any]: ...
    @overload
    def map(self, **kw: _T) -> CommentedMap[str, _T]: ...
    @overload
    def seq(self) -> CommentedSeq[Any]: ...
    @overload
    def seq(self, iterable: Iterable[_T], /) -> CommentedSeq[_T]: ...
    def __enter__(self) -> _RoundTripYAMLContext: ...

@type_check_only
class _FullYAML(YAML):
    @property
    def composer(self) -> NoReturn: ...
    @property
    def constructor(self) -> NoReturn: ...
    # copilot: main.py raises for every loading API when typ="full", so preserve their concrete stream parameters with NoReturn.
    @deprecated("You can only use YAML(typ='full') for dumping")
    def scan(self, stream: _ReadStream) -> NoReturn: ...
    @deprecated("You can only use YAML(typ='full') for dumping")
    def parse(self, stream: _ReadStream) -> NoReturn: ...
    @deprecated("You can only use YAML(typ='full') for dumping")
    def compose(self, stream: Path | _ReadStream) -> NoReturn: ...
    @deprecated("You can only use YAML(typ='full') for dumping")
    def compose_all(self, stream: Path | _ReadStream) -> NoReturn: ...
    @deprecated("You can only use YAML(typ='full') for dumping")
    def load(self, stream: Path | _ReadStream) -> NoReturn: ...
    @deprecated("You can only use YAML(typ='full') for dumping")
    def load_all(self, stream: Path | _ReadStream) -> NoReturn: ...
    def get_constructor_parser(self, stream: _ReadStream) -> NoReturn: ...
    def __enter__(self) -> _FullYAMLContext: ...

@type_check_only
class _YAMLContext(YAML):
    def dump(self, data: Any, stream: Unused = None, *, transform: None = None) -> None: ...  # type: ignore[override]
    def dump_all(
        self, documents: Iterable[Any], stream: Unused = None, *, transform: None = None
    ) -> None: ...  # type: ignore[override]

@type_check_only
class _RoundTripYAMLContext(_YAMLContext, _RoundTripYAML): ...

@type_check_only
class _FullYAMLContext(_YAMLContext, _FullYAML): ...

class YAMLContextManager:
    def __init__(self, yaml: YAML, transform: Callable[[str], str] | None = None) -> None: ...
    def teardown_output(self) -> None: ...
    def init_output(self, first_data: Any) -> None: ...
    def dump(self, data: Any) -> None: ...

# This is because we can't mark protocol fields as not required
# See https://github.com/python/typing/issues/601
_RegistrableClass: TypeAlias = type[_RegistrableObject | object]

@type_check_only
class _RegistrableObject(Protocol):
    yaml_tag: str
    @classmethod
    def to_yaml(cls, representer: BaseRepresenter, data: Self, /) -> Node: ...
    @classmethod
    def from_yaml(cls, constructor: BaseConstructor, node: Node, /) -> Self: ...

def yaml_object(yml: YAML) -> Callable[[_RegistrableClass], _RegistrableClass]: ...
def warn_deprecation(fun: str, method: str, arg: str = "") -> None: ...
def error_deprecation(fun: str, method: str, arg: str = "", comment: str = "instead of") -> NoReturn: ...
@deprecated("Use YAML().scan() instead")
def scan(stream: _ReadStream, Loader: type[BaseLoader] = ...) -> NoReturn: ...
@deprecated("Use YAML().parse() instead")
def parse(stream: _ReadStream, Loader: type[BaseLoader] = ...) -> NoReturn: ...
@deprecated("Use YAML().compose() instead")
def compose(stream: Path | _ReadStream, Loader: type[BaseLoader] = ...) -> NoReturn: ...
@deprecated("Use YAML().compose_all() instead")
def compose_all(stream: Path | _ReadStream, Loader: type[BaseLoader] = ...) -> NoReturn: ...
@deprecated("Use YAML().load() instead")
def load(
    stream: Path | _ReadStream,
    Loader: type[BaseLoader] | None = None,
    version: VersionType = None,
    preserve_quotes: bool | None = None,
) -> NoReturn: ...
@deprecated("Use YAML().load_all() instead")
def load_all(
    stream: Path | _ReadStream,
    Loader: type[BaseLoader] | None = None,
    version: VersionType = None,
    preserve_quotes: bool | None = None,
) -> NoReturn: ...
@deprecated("Use YAML(typ='safe', pure=True).load() instead")
def safe_load(stream: _ReadStream, version: VersionType = None) -> NoReturn: ...
@deprecated("Use YAML(typ='safe', pure=True).load_all() instead")
def safe_load_all(stream: _ReadStream, version: VersionType = None) -> NoReturn: ...
@deprecated("Use YAML().load() instead")
def round_trip_load(
    stream: _ReadStream, version: VersionType = None, preserve_quotes: bool | None = None
) -> NoReturn: ...
@deprecated("Use YAML().load_all() instead")
def round_trip_load_all(
    stream: _ReadStream, version: VersionType = None, preserve_quotes: bool | None = None
) -> NoReturn: ...
@deprecated("Use YAML(typ='safe', pure=True).emit() instead")
def emit(
    events: Iterable[Event],
    stream: _WriteStream | None = None,
    Dumper: type[BaseDumper] = ...,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | None = None,
    allow_unicode: bool | None = None,
    line_break: _LineBreak | None = None,
) -> NoReturn: ...
@deprecated("Use YAML(typ='safe', pure=True).serialize_all() instead")
def serialize_all(
    nodes: Iterable[Node],
    stream: _WriteStream | None = None,
    Dumper: type[BaseDumper] = ...,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | None = None,
    allow_unicode: bool | None = None,
    line_break: _LineBreak | None = None,
    encoding: str | None = ...,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: VersionType = None,
    tags: _TagHandleToPrefix | None = None,
) -> NoReturn: ...
@deprecated("Use YAML(typ='safe', pure=True).serialize() instead")
def serialize(
    node: Node, stream: _WriteStream | None = None, Dumper: type[BaseDumper] = ..., **kwds: object
) -> NoReturn: ...
@deprecated("Use YAML(typ='unsafe', pure=True).dump_all() instead")
def dump_all(
    documents: Iterable[Any],
    stream: _WriteStream | None = None,
    Dumper: type[BaseDumper] = ...,
    default_style: _ScalarStyle | None = None,
    default_flow_style: bool | None = None,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | None = None,
    allow_unicode: bool | None = None,
    line_break: _LineBreak | None = None,
    encoding: str | None = ...,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: VersionType = None,
    tags: _TagHandleToPrefix | None = None,
    block_seq_indent: int | None = None,
    top_level_colon_align: int | bool | None = None,
    prefix_colon: str | None = None,
) -> NoReturn: ...
@deprecated("Use YAML(typ='unsafe', pure=True).dump() instead")
def dump(
    data: Any,
    stream: _WriteStream | None = None,
    Dumper: type[BaseDumper] = ...,
    default_style: _ScalarStyle | None = None,
    default_flow_style: bool | None = None,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | None = None,
    allow_unicode: bool | None = None,
    line_break: _LineBreak | None = None,
    encoding: str | None = ...,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: VersionType = None,
    tags: _TagHandleToPrefix | None = None,
    block_seq_indent: int | None = None,
) -> NoReturn: ...
@deprecated("Use YAML(typ='safe', pure=True).dump() instead")
def safe_dump(data: Any, stream: _WriteStream | None = None, **kwds: object) -> NoReturn: ...
@deprecated("Use YAML().dump() instead")
def round_trip_dump(
    data: Any,
    stream: _WriteStream | None = None,
    Dumper: type[RoundTripDumper] = ...,
    default_style: _ScalarStyle | None = None,
    default_flow_style: bool | None = None,
    canonical: bool | None = None,
    indent: int | None = None,
    width: int | None = None,
    allow_unicode: bool | None = None,
    line_break: _LineBreak | None = None,
    encoding: str | None = ...,
    explicit_start: bool | None = None,
    explicit_end: bool | None = None,
    version: VersionType = None,
    tags: _TagHandleToPrefix | None = None,
    block_seq_indent: int | None = None,
    top_level_colon_align: int | bool | None = None,
    prefix_colon: str | None = None,
) -> NoReturn: ...
def add_implicit_resolver(
    tag: str,
    regexp: Pattern[str],
    first: list[str] | None = None,
    Loader: type[BaseResolver] | None = None,
    Dumper: type[BaseResolver] | None = None,
    resolver: type[BaseResolver] = ...,
) -> None: ...
def add_path_resolver(
    tag: str,
    path: Iterable[Any],
    kind: type | None = None,
    Loader: type[BaseResolver] | None = None,
    Dumper: type[BaseResolver] | None = None,
    resolver: type[BaseResolver] = ...,
) -> None: ...
@overload
def add_constructor(
    tag: Tag | str | None, object_constructor: _ConstructorFunction[_Constructor], *, constructor: type[_Constructor]
) -> None: ...
@overload
def add_constructor(
    tag: Tag | str | None, object_constructor: _ConstructorFunction[_Constructor], Loader: type[_Constructor]
) -> None: ...
@overload
def add_constructor(tag: Tag | str | None, object_constructor: _ConstructorFunction[Constructor]) -> None: ...
@overload
def add_multi_constructor(
    tag_prefix: str | None, multi_constructor: _MultiConstructorFunction[_Constructor], *, constructor: type[_Constructor]
) -> None: ...
@overload
def add_multi_constructor(
    tag_prefix: str | None, multi_constructor: _MultiConstructorFunction[_Constructor], Loader: type[_Constructor]
) -> None: ...
@overload
def add_multi_constructor(tag_prefix: str | None, multi_constructor: _MultiConstructorFunction[Constructor]) -> None: ...
@overload
def add_representer(
    data_type: type[_T] | None, object_representer: _RepresenterFunction[_Representer, _T], *, representer: type[_Representer]
) -> None: ...
@overload
def add_representer(
    data_type: type[_T] | None, object_representer: _RepresenterFunction[_Representer, _T], Dumper: type[_Representer]
) -> None: ...
@overload
def add_representer(data_type: type[_T] | None, object_representer: _RepresenterFunction[Representer, _T]) -> None: ...
@overload
def add_multi_representer(
    data_type: type[_T] | None, multi_representer: _RepresenterFunction[_Representer, _T], *, representer: type[_Representer]
) -> None: ...
@overload
def add_multi_representer(
    data_type: type[_T] | None, multi_representer: _RepresenterFunction[_Representer, _T], Dumper: type[_Representer]
) -> None: ...
@overload
def add_multi_representer(data_type: type[_T] | None, multi_representer: _RepresenterFunction[Representer, _T]) -> None: ...

class YAMLObjectMetaclass(type):
    def __init__(cls, name: str, bases: tuple[type, ...], kwds: dict[str, Any], /) -> None: ...

class YAMLObject(metaclass=YAMLObjectMetaclass):
    yaml_constructor: ClassVar[type[BaseConstructor]]
    yaml_representer: ClassVar[type[BaseRepresenter]]
    yaml_tag: Tag | str | None
    yaml_flow_style: bool | None
    @classmethod
    def from_yaml(cls, constructor: BaseConstructor, node: Node) -> Self: ...
    @classmethod
    def to_yaml(cls, representer: BaseRepresenter, data: Self) -> Node: ...
