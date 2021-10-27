import math

from profile_generator.unit import Curve


def curve(threshold: float, limit: float) -> Curve:
    """
    Args:
        threshold: boundary of the linear and roll-off part of the curve
        limit: maximal value
    """
    a = (1 - limit) / (
        -2 * math.pow(threshold, 3) + 6 * math.pow(threshold, 2) - 6 * threshold + 2
    )
    b = -3 * a
    c = 1 + 3 * a * (2 * threshold - math.pow(threshold, 2))
    d = limit - a - b - c

    def _curve(x: float) -> float:
        if x < threshold:
            return x
        else:
            return a * math.pow(x, 3) + b * math.pow(x, 2) + c * x + d

    return _curve
