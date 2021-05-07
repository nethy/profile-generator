import math

from profile_generator.unit import PRECISION, Point


def brightness(b: float, x: float) -> float:
    if b == 0:
        return x
    else:
        return (1 - math.exp(-b * x)) / (1 - math.exp(-b))


def contrast(c: float, x: float) -> float:
    if c == 0:
        return x
    elif c > 0:
        return (1 / (1 + math.exp(c * (0.5 - x))) - 1 / (1 + math.exp(c / 2))) / (
            1 / (1 + math.exp(c * (-0.5))) - 1 / (1 + math.exp(c / 2))
        )
    else:
        n_c = 2 - 1 / (math.exp((-c - math.sqrt(-c + 2)) / 2))
        return (
            math.log((n_c * (x - 0.5) + 1) / (1 - n_c * (x - 0.5)))
            - math.log((-n_c / 2 + 1) / (1 + n_c / 2))
        ) / (
            math.log((n_c / 2 + 1) / (1 - n_c / 2))
            - math.log((-n_c / 2 + 1) / (1 + n_c / 2))
        )


def contrast_slope(c: float) -> float:
    return (c * (math.exp(c / 2) + 1)) / (4 * (math.exp(c / 2) - 1))


def curve(c: float, b: float, x: float) -> float:
    return contrast(c, brightness(b, x))


_ITERATION_LIMIT = 100


def approximate_brightness(grey: Point, c: float) -> float:
    low = -100.0
    high = 100.0
    b = 0.0
    y = curve(c, b, grey.x)
    for _ in range(_ITERATION_LIMIT):
        if abs(grey.y - y) < PRECISION:
            break

        if y < grey.y:
            low = b
        else:
            high = b

        b = (low + high) / 2
        y = curve(c, b, grey.x)
    return b
