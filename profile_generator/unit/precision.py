import math

DECIMALS = 6
_PRECISION = 1e-6


def equals(a: float, b: float) -> bool:
    return math.isclose(a, b, abs_tol=_PRECISION)
