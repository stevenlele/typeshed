# `ruamel.yaml` stub refresh report

## Scope

The original rebase request was not replayed because the local implementation
commits were lost. This refresh was replayed directly onto the working branch,
which was clean at `b24c3c5` (`Remove unused type ignore comments`); no unrelated
rebase or history rewrite was performed.

The latest upstream release available during the refresh was `ruamel.yaml
0.19.1`. Its supported Python versions include the versions supported by the
current typeshed layout, so the metadata was updated from `0.18.*` to `0.19.*`.
The current metadata validator requires the keys `upstream_repository` and
`stubtest_requirements`.

## Maintainer feedback and stub-writing guidance

PR [python/typeshed#12584](https://github.com/python/typeshed/pull/12584) had
three unresolved maintainer suggestions:

* Package constants (`version_info`, `__version__`, and `__with_libyaml__`)
  are now marked `Final`.
* `_BufferDecoder` is a typing-only protocol and is marked
  `@type_check_only`.
* `_RepresenterFunction` is a typing-only protocol and is marked
  `@type_check_only`.

The current
[writing stubs guide](https://typing.python.org/en/latest/guides/writing_stubs.html)
was consulted before making these changes. The replay follows its emphasis on
matching runtime behavior, using precise types where practical, keeping
implementation details private, and documenting justified uses of `Any`.
`MergeValue` retains `Any` for its dynamically shaped merge data because the
upstream object accepts and stores values whose shape depends on the YAML input.

## Upstream API changes reflected in the stubs

The 0.19.1 source comparison identified these changes:

* Added `ruamel.yaml.mergevalue.MergeValue` and updated round-trip merge
  handling in `CommentedMap` and `RoundTripConstructor`.
* Added `YAML.max_depth`, `Composer.depth`, and
  `MaxDepthExceededError`.
* Changed safe-constructor mapping flattening to mutate the node and return
  `None`.
* Added `Serializer.templated_id`.
* Added keyword forwarding to `load_yaml_guess_indent`.
* Added the `_ruamel_yaml_clibz` compatibility path through `cyaml.__yaml_lib`
  and updated C-loader argument types.
* Updated Pyright suppressions for the untyped `configobj` dependency.

The `ruamel.yaml` stubtest remains disabled because mypy cannot parse the
upstream package's `main.py`.

## Validation history and limitations

Before the local commits were lost, the replayed implementation passed
typeshed structure validation, targeted mypy validation, targeted Pyright
validation, and targeted pre-commit checks. The same checks are being rerun
after replay where the required tools are available.

In this environment, the initial rerun attempts were blocked by missing
`tomli` (structure validation) and missing `pre-commit`. `ty` and `pyrefly`
were unavailable. CodeQL previously timed out twice against the large rebased
diff; the replay will be checked again against the smaller change set.
