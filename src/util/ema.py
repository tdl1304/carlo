

class ExponentialMovingAverage:
    _mixing: float
    _value: float

    def __init__(self, mixing: float = 0.9, initial: float = 0.0):
        self._mixing = mixing
        self._value = initial

    def set(self, value: float):
        self._value = value
    
    def update(self, value: float) -> float:
        self._value = self._mixing * value + (1 - self._mixing) * self._value
        return self._value
    
    @property
    def value(self) -> float:
        return self._value
