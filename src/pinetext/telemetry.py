from __future__ import annotations

from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


try:
    import wandb
    import weave
except ImportError:
    wandb = None
    weave = None


def op(*dargs: Any, **dkwargs: Any):
    if weave is None:
        if dargs and callable(dargs[0]) and len(dargs) == 1 and not dkwargs:
            return dargs[0]

        def _decorator(fn: F) -> F:
            return fn

        return _decorator
    return weave.op(*dargs, **dkwargs)


def init(project: str, api_key: str | None = None) -> None:
    if wandb is not None and api_key:
        wandb.login(key=api_key)
    if weave is not None:
        weave.init(project)
