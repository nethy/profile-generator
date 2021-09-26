import math

from .type import Curve


def curve(offset: float, slope: float) -> Curve:
    fade_end = 3 * offset / (2 - 2 * slope)
    a = (1 - offset / fade_end - slope) / math.pow(fade_end, 2)
    b = 0
    c = slope
    d = offset

    def _curve(x: float) -> float:
        if x < fade_end:
            return a * math.pow(x, 3) + b * math.pow(x, 2) + c * x + d
        else:
            return x

    return _curve
