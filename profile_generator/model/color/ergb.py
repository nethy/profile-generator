import math

from profile_generator.unit import Vector


def length(a: Vector) -> float:
    return math.sqrt(dot_product(a, a))


def dot_product(a: Vector, b: Vector) -> float:
    return sum(ai * bi for ai, bi in zip(a, b))


def angle(a: Vector, b: Vector) -> float:
    return math.degrees(math.acos(dot_product(a, b) / (length(a) * length(b))))


def hue(rgb: Vector) -> tuple[float, float]:
    l = sum(a * b for a, b in zip([0.2126, 0.7152, 0.0722], rgb))
    r, g, b = [c - l for c in rgb]
    alpha = r - g / 2 - b / 2
    beta = math.sqrt(3) / 2 * (g - b)
    return (
        math.degrees(math.atan2(beta, alpha)),
        math.sqrt(alpha * alpha + beta * beta),
    )
