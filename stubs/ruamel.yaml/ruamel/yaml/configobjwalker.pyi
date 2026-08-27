from collections.abc import Iterator
from typing_extensions import deprecated

# copilot: configobj is an optional runtime dependency listed for stubtest, not a typing dependency.
from configobj import (
    ConfigObj,  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]  # ty:ignore[unresolved-import]  # pyrefly: ignore [missing-import]
)

@deprecated("configobj_walker has moved to ruamel.yaml.util")
def configobj_walker(cfg: ConfigObj, /) -> Iterator[str]: ...
