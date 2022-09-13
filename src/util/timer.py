from collections import defaultdict
from .stopwatch import Stopwatch
from .ema import ExponentialMovingAverage


_averages = defaultdict(lambda: ExponentialMovingAverage(mixing=0.2, initial=1))


class Timer:
    def __init__(self, fmt):
        self._fmt = fmt
        self._sw = Stopwatch()
        self._ema = _averages[fmt]

    def __enter__(self):
        self._sw.restart()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        dt = self._sw.elapsed_seconds
        self._ema.update(dt)
        print(self._fmt.format(dt=dt, avg=self._ema.value, fps=1 / self._ema.value))
