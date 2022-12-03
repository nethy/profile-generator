import math
from functools import cache

from profile_generator.unit import Curve
from profile_generator.util import search, validation

from . import spline


def algebraic(gradient: float, exponent: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    elif gradient < 1 and not math.isclose(exponent, 1):
        raise ValueError(
            f"Gradient must be greater than equal to 1. Actual value is {gradient}"
        )

    c = 2 * math.pow(math.pow(gradient, exponent) - 1, 1 / exponent)
    return _generic_algebraic(c, exponent, 0, 1)


def _generic_algebraic(c: float, k: float, a: float, b: float) -> Curve:
    if math.isclose(c, 0):
        return lambda x: x
    o = (a + b) / 2
    offset = c * (a - o) / math.pow(1 + math.pow(c * abs(a - o), k), 1 / k)
    return lambda x: (
        (c * (x - o) / math.pow(1 + math.pow(c * abs(x - o), k), 1 / k) - offset)
        / (c * (b - o) / math.pow(1 + math.pow(c * abs(b - o), k), 1 / k) - offset)
    )


def brightness_curve(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda x: x
    else:
        return lambda x: (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def brightness_gradient(b: float) -> Curve:
    if math.isclose(b, 0):
        return lambda x: 1
    else:
        return lambda x: b * math.exp(b - b * x) / (math.exp(b) - 1)


@cache
def brightness_at(x: float, y: float) -> Curve:
    validation.is_positive(x)
    validation.is_positive(y)
    validation.is_greater_or_equal(y, x)
    test_curve = lambda b: brightness_curve(b)(x)
    coeff = search.jump_search(0, 100, test_curve, y)
    return brightness_curve(coeff)


def contrast_curve(c: float) -> Curve:
    validation.is_greater_or_equal(c, 0)
    if math.isclose(c, 0):
        return lambda x: x
    return lambda x: (1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))) / (
        1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2))
    )


def contrast_gradient(c: float) -> float:
    if math.isclose(c, 0):
        return 1
    gradient = (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))
    if c > 0:
        return gradient
    else:
        return 1 / gradient


_COEFF_CACHE = spline.interpolate(
    [
        (1.0, 0.0),
        (1.0173160173160174, 0.913265040386706),
        (1.0346320346320346, 1.293791811056),
        (1.051948051948052, 1.5873143510703696),
        (1.0692640692640694, 1.8360544584686307),
        (1.0865800865800865, 2.0563362530200764),
        (1.103896103896104, 2.256517089108517),
        (1.1385281385281385, 2.6146683562588926),
        (1.155844155844156, 2.7780981545128265),
        (1.1904761904761905, 3.0820015064328934),
        (1.2424242424242424, 3.4951630468615256),
        (1.2943722943722944, 3.8716533146260477),
        (1.3463203463203464, 4.221403463972836),
        (1.4155844155844157, 4.656668413416579),
        (1.4848484848484849, 5.064974246928736),
        (1.5714285714285714, 5.546773831109896),
        (1.6406926406926408, 5.914405782271811),
        (1.70995670995671, 6.269410015445069),
        (1.8484848484848486, 6.9497833160761),
        (1.987012987012987, 7.60027110608227),
        (2.142857142857143, 8.306184296920957),
        (2.2813852813852815, 8.916573977814389),
        (2.41991341991342, 9.514814531522017),
        (2.5584415584415585, 10.103654910166036),
        (2.7142857142857144, 10.757418148469784),
        (2.9913419913419914, 11.903271761955136),
        (3.2857142857142856, 13.105420671965792),
        (3.5627705627705626, 14.22790972971995),
        (3.857142857142857, 15.414707081223808),
        (4.428571428571429, 17.709230015099905),
        (4.774891774891775, 19.09684316726051),
        (5.0, 19.998182433206498),
    ]
)


def exponential(gradient: float) -> Curve:
    validation.is_greater_or_equal(gradient, 1)
    coeff = _COEFF_CACHE(gradient)
    return contrast_curve(coeff)
