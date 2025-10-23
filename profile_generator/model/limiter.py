import math

from profile_generator.unit import PRECISION, Curve
from profile_generator.util import validation


def log_limiter(threshold: float) -> Curve:
    validation.is_greater_or_equal(threshold, 0.0)
    if threshold < PRECISION:
        return lambda x: math.log(x + 1.0)
    else:
        return lambda x: threshold * (math.log(x / threshold) + 1)
