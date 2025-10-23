import math

DECIMALS = 7

PRECISION = 1e-13
PRECISION_DECIMALS = 13


def equals(a: float, b: float, tolerance: float = PRECISION) -> bool:
    return math.isclose(a, b, rel_tol=tolerance, abs_tol=tolerance)


def round_float(value: float) -> float:
    return round(value, DECIMALS)
