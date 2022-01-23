import math

from profile_generator.unit import Curve


def algebraic(gradient: float, exponent: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    elif gradient < 1 and not math.isclose(exponent, 1):
        raise ValueError(
            f"Gradient must be greater than equal to 1. Actual value is {gradient}"
        )
    c = 2 * math.pow(math.pow(gradient, exponent) - 1, 1 / exponent)
    acc = c * 0.5 / math.pow(1 + math.pow(c * 0.5, exponent), 1 / exponent)
    return lambda x: (
        (
            c
            * (x - 0.5)
            / math.pow(1 + math.pow(c * abs(x - 0.5), exponent), 1 / exponent)
            + acc
        )
        / (2 * acc)
    )
