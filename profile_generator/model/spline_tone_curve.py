import math

from profile_generator.unit import Point
from profile_generator.util import validation

from .gamma import Curve


def curve(
    middle: Point, gamma: float, offsets: tuple[float, float] = (0.0, 1.0)
) -> Curve:
    """
    p0, p1, p2

    x0 = 0, x2 = 1

    y0, y2 - offsets

    fi(x) = aix^3+bix^2+cix+di, i = 0, 1
    fi'(x) = 3*aix^2+2*bix+ci
    fi''(x) = 6*aix+2*bi

    f0(x0) = y0
    f0(x1) = y1
    f1(x1) = y1
    f1(x2) = y2

    f0'(x1) = gamma
    f1'(x1) = gamma
    f0'(x0) = shadow_strength = 1/gamma
    f1''(x2) = 0

    --------

    d0 = y0
    a0x1^3+b0x1^2+c0x1+d0 = y1
    a1x1^3+b1x1^2+c1x1+d1 = y1
    a1+b1+c1+d1 = y2

    3a0x1^2+2b0x1+c0 = gamma
    3a1x1^2+2b1x1+c1 = gamma
    c0 = shadow_strength
    6a1+2b1 = 0

    --------

    a0x1^3+b0x1^2 = y1-d0-c0x1
    a0x1 + b0 = (y1-d0-c0x1)/x1^2
    b0 = (y1-d0-c0x1)/x1^2-a0x1

    3a0x1^2+2b0x1 = gamma-c0
    3a0x1+2b0 = (gamma-c0)/x1
    a0x1+(2y1-2d0-2c0x1)/x1^2 = (gamma-c0)/x1
    a0 = (gamma-c0)/x1^2 - 2(y1-d0-c0x1)/x1^3


    6a1+2b1 = 0
    3a1 + b1 = 0
    b1 = -3a1

    3a1x1^2+2b1x1+c1 = gamma
    c1 = gamma - 3a1x1^2 - 2b1x1
    c1 = gamma - 3a1x1^2 - 2(-3a1)x1
    c1 = gamma - 3a1x1^2 + 6a1x1
    c1 = gamma - 3a1x1(x1-2)

    a1+b1+c1+d1 = y2
    d1 = y2 - a1 - b1 - c1
    d1 = y2 - gamma + 2a1 + 3a1x1(x1-2)

    a1x1^3+b1x1^2+c1x1+d1 = y1
    a1x1^3 + (-3a1)x1^2 + (gamma-3a1x1(x1-2))x1 + y2 - gamma + 2a1 + 3a1x1(x1-2) = y1
    a1x1^3 + (-3a1)x1^2 + (gamma-3a1x1(x1-2))x1 + 2a1 + 3a1x1(x1-2) = y1 - y2 + gamma
    a1x1^3 - 3a1x1^2 - 3a1x1^2(x1-2) + 2a1 + 3a1x1(x1-2) = y1 - y2 + gamma - gamma*x1
    a1x1^3 - 3a1x1^2 - 3a1x1^3 + 6a1x1^2 + 2a1 + 3a1x1^2 - 6a1x1 = y1 - y2 + gamma(1-x1)
    -2a1x1^3 + 6a1x1^2 - 6a1x1 + 2a1 = y1 - y2 + gamma(1-x1)
    2a1(-x1^3 + 3x1^2 - 3x1 + 1) = y1 - y2 + gamma(1-x1)
    a1 = (y1 - y2 + gamma(1-x1))/2(-x1^3 + 3x1^2 - 3x1 + 1)
    """
    if gamma < 0 or math.isclose(gamma, 0):
        raise ValueError("Gamma must be greater than zero.")
    validation.is_in_closed_interval(offsets[0], 0, 1)
    validation.is_in_closed_interval(offsets[1], 0, 1)

    x, y = middle
    shadow_gradient = middle.y / middle.x / math.pow(gamma, 2)

    c = shadow_gradient
    d = offsets[0]
    a = (gamma - c) / math.pow(x, 2) - 2 * (y - d - c * x) / math.pow(x, 3)
    b = (y - d - c * x) / math.pow(x, 2) - a * x

    e = (
        (y - offsets[1] + gamma * (1 - x))
        / 2
        / (-math.pow(x, 3) + 3 * math.pow(x, 2) - 3 * x + 1)
    )
    f = -3 * e
    g = gamma - 3 * e * x * (x - 2)
    h = offsets[1] + 2 * e - g

    def _curve(x: float) -> float:
        if x < middle.x:
            return a * math.pow(x, 3) + b * math.pow(x, 2) + c * x + d
        else:
            return e * math.pow(x, 3) + f * math.pow(x, 2) + g * x + h

    return _curve
