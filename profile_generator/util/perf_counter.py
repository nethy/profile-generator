import logging
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from types import TracebackType
from typing import Any, ContextManager, Optional, Type


def perf_counter(fn: Callable[..., Any]) -> Any:
    log = logging.getLogger(__name__)

    def _log_perf(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = start - time.perf_counter()
        log.info("Execution time of %s: %5.3f", fn.__name__, elapsed)
        return result

    return _log_perf


@contextmanager
def log_perf(name: str, logger: logging.Logger) -> Generator[None, None, None]:
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    logger.info("Execution time of %s: %5.3f", name, elapsed)


class LogPerf(ContextManager[None]):
    def __init__(self, name: str, logger: logging.Logger) -> None:
        self._name = name
        self._logger = logger
        self._start = 0.0

    def __enter__(self) -> None:
        self._start = time.perf_counter()

    def __exit__(
        self,
        __exc_type: Optional[Type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        elapsed = time.perf_counter() - self._start
        self._logger.info("Execution time of %s: %5.3f", self._name, elapsed)
