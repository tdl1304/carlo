import time
from datetime import timedelta


class Stopwatch:
    _start: int

    def __init__(self):
        self.restart()

    def restart(self):
        self._start = time.monotonic_ns()

    @property
    def elapsed_ns(self) -> int:
        return time.monotonic_ns() - self._start

    @property
    def elapsed_seconds(self) -> float:
        return self.elapsed_ns / 1e9

    @property
    def elapsed(self) -> timedelta:
        return timedelta(microseconds=self.elapsed_ns / 1000)
