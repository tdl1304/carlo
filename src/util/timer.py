from collections import defaultdict
from typing import Optional
from .stopwatch import Stopwatch
from .ema import ExponentialMovingAverage


class Timer:
    def __init__(self) -> None:
        self._sw = Stopwatch()
        self._ema = ExponentialMovingAverage(mixing=0.2, initial=1)

    def restart(self) -> None:
        """Restarts the timer."""
        self._sw.restart()

    def tick(self, fmt: Optional[str] = None):
        """Measures the elapsed time and updates the EMA. Optionally prints the timer status with the given format."""
        dt = self._sw.elapsed_seconds
        self._sw.restart()
        self._ema.update(dt)
        if fmt is not None:
            self.print(fmt, dt)
    
    def print(self, fmt: str, dt: Optional[float] = None) -> None:
        """Prints the timer status with the given format."""
        if dt is None:
            dt = self._sw.elapsed_seconds

        variables = {
            'dt': dt,
            'avg': self._ema.value,
            'fps': 1 / self._ema.value,
        }
        text = fmt.format(**variables)
        print(text)

    def ctx(self, fmt: Optional[str] = None) -> 'TimerCtx':
        """Returns a context manager that measures the elapsed time and updates the EMA. Optionally prints the timer status with the given format."""
        return TimerCtx(self, fmt)


class TimerCtx:
    def __init__(self, timer: Timer, fmt: Optional[str] = None):
        self._timer = timer
        self._fmt = fmt

    def __enter__(self):
        self._timer.restart()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._timer.tick(fmt=self._fmt)
