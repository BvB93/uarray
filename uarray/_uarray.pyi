"""Annotations for the ``uarray._uarray`` extension module."""

import types
from collections.abc import Callable, Iterable
from typing import Any, final, overload, Generic

# TODO: Import from `typing` once `uarray` requires Python >= 3.10
from typing_extensions import ParamSpec

import uarray
from uarray._typing import (
    _PyGlobalDict,
    _PyLocalDict,
    _ReplacerFunc,
    _SupportsUAConvert,
    _SupportsUADomain,
)

_P = ParamSpec("_P")

class BackendNotImplementedError(NotImplementedError): ...

@final
class _SkipBackendContext:
    def __init__(self, backend: _SupportsUADomain) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
        /,
    ) -> None: ...
    def _pickle(self) -> tuple[_SupportsUADomain]: ...

@final
class _SetBackendContext:
    def __init__(
        self,
        backend: _SupportsUADomain,
        coerce: bool = ...,
        only: bool = ...,
    ) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
        /,
    ) -> None: ...
    def _pickle(self) -> tuple[_SupportsUADomain, bool, bool]: ...

# NOTE: Parametrize w.r.t. `__ua_domain__` when returning, but use `Any`
# when used as argument type. Due to lists being invariant the `__ua_domain__`
# protocol will likelly be disruptivelly strict in the latter case, hence the
# usage of `Any` as an escape hatch.
@final
class _BackendState:
    def _pickle(self) -> tuple[
        _PyGlobalDict[_SupportsUADomain],
        _PyLocalDict[_SupportsUADomain],
        bool,
    ]: ...
    @classmethod
    def _unpickle(
        cls,
        py_global: _PyGlobalDict[Any],
        py_locals: _PyLocalDict[Any],
        use_thread_local_globals: bool,
        /,
    ) -> _BackendState: ...

# TODO: Remove the `type: ignore` once python/mypy#12033 has been bug fixed
@final  # type: ignore[arg-type]
class _Function(Generic[_P]):
    def __init__(
        self,
        extractor: Callable[_P, tuple[uarray.Dispatchable, ...]],
        replacer: None | _ReplacerFunc,
        domain: str,
        def_args: tuple[Any, ...],
        def_kwargs: dict[str, Any],
        def_impl: None | Callable[..., Any],
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> Any: ...
    @overload
    def __get__(self, obj: None, type: type[Any]) -> _Function: ...
    @overload
    def __get__(
        self, obj: object, type: None | type[Any] = ...
    ) -> types.MethodType: ...
    @property
    def arg_extractor(self) -> Callable[_P, tuple[uarray.Dispatchable, ...]]: ...
    @property
    def arg_replacer(self) -> None | _ReplacerFunc: ...
    @property
    def default(self) -> None | Callable[..., Any]: ...
    @property
    def domain(self) -> str: ...
    # NOTE: These attributes are dynamically inserted by
    # `uarray.generate_multimethod` via a `functools.update_wrapper` call
    __module__: str
    __name__: str
    __qualname__: str
    __doc__: None | str
    __wrapped__: Callable[_P, tuple[uarray.Dispatchable, ...]]
    __annotations__: dict[str, Any]

def set_global_backend(
    backend: _SupportsUADomain,
    coerce: bool = ...,
    only: bool = ...,
    try_last: bool = ...,
    /,
) -> None: ...
def clear_backends(
    domain: None | str,
    registered: bool = ...,
    global_: bool = ...,
    /,
) -> None: ...
def determine_backend(
    domain_object: str,
    dispatchables: Iterable[uarray.Dispatchable],
    coerce: bool,
    /,
) -> _SupportsUAConvert: ...
def register_backend(backend: _SupportsUADomain, /) -> None: ...
def get_state() -> _BackendState: ...
def set_state(arg: _BackendState, reset_allowed: bool = ..., /) -> None: ...
