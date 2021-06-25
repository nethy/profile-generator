from collections.abc import Sequence

from profile_generator.model import spline
from profile_generator.model.sigmoid import (
    Curve,
    curve,
    find_contrast_gradient,
    find_curve_brightness,
)
from profile_generator.unit import Point, Strength, equals

MAX_GRADIENT = 4
MAX_HL_PROTECTION = 4


def calculate(
    grey: Point,
    strength: Strength,
    hl_protection: Strength = Strength(0.0),
    offsets: tuple[float, float] = (0.0, 1.0),
) -> Sequence[Point]:
    gradient = _as_gradient(strength)
    contrast = _calculate_contrast(gradient, offsets)
    brightness = find_curve_brightness(grey, contrast)
    protection = _as_multiplication(hl_protection, MAX_HL_PROTECTION)
    _curve = _apply_offsets(curve(brightness, contrast, protection), offsets)
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _as_gradient(strength: Strength) -> float:
    gradient = _as_multiplication(strength, MAX_GRADIENT)
    if strength.value < 0:
        return 1 / -gradient
    return gradient


def _calculate_contrast(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    corrigated_gradient = gradient
    if not equals(1, highlight - shadow):
        corrigated_gradient = gradient / (highlight - shadow)
    return find_contrast_gradient(corrigated_gradient)


def _as_multiplication(strength: Strength, max_value: float) -> float:
    return strength.value * (max_value - 1) + 1


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]
