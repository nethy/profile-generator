from collections.abc import Callable, Sequence

from profile_generator.model import spline
from profile_generator.model.sigmoid import (
    Curve,
    curve,
    curve_with_hl_protection,
    find_contrast_gradient,
    find_curve_brightness,
)
from profile_generator.unit import Point, Strength, equals

MAX_CONTRAST = 4


def calculate(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
) -> Sequence[Point]:
    return _calculate(grey, strength, offsets, curve)


def calculate_with_hl_protection(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
) -> Sequence[Point]:
    return _calculate(grey, strength, offsets, curve_with_hl_protection)


def _calculate(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float],
    fn: Callable[[float, float], Curve],
) -> Sequence[Point]:
    gradient = _calculate_gradient(strength.value)
    contrast = _calculate_contrast(gradient, offsets)
    brightness = find_curve_brightness(grey, contrast)
    _curve = _apply_offsets(fn(brightness, contrast), offsets)
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _calculate_gradient(strength: float) -> float:
    gradient = 1 + strength * (MAX_CONTRAST - 1)
    if strength < 0:
        return 1 / -gradient
    return gradient


def _calculate_contrast(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    corrigated_gradient = gradient
    if not equals(1, highlight - shadow):
        corrigated_gradient = gradient / (highlight - shadow)
    return find_contrast_gradient(corrigated_gradient)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]
