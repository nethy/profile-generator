import math

DECIMALS = 7
_PRECISION = 1e-7


def equals(a: float, b: float) -> bool:
    return math.isclose(a, b, abs_tol=_PRECISION)


def round_float(value: float) -> float:
    return round(value, DECIMALS)
