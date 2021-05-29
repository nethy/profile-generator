from profile_generator.model import spline
from profile_generator.model.sigmoid import (
    Curve,
    contrast_gradient,
    curve,
    curve_with_hl_protection,
    find_contrast_gradient,
    find_curve_brightness,
)
from profile_generator.unit import Point, Strength, equals

MAX_CONTRAST = 16


def calculate(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    contrast = _corrigate_contrast(contrast, offsets)
    brightness = find_curve_brightness(grey, contrast)
    _curve = _apply_offsets(curve(brightness, contrast), offsets)
    return [Point(x, y) for x, y in spline.fit(_curve)]


def calculate_with_hl_protection(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    contrast = _corrigate_contrast(contrast, offsets)
    brightness = find_curve_brightness(grey, contrast)
    _curve = _apply_offsets(curve_with_hl_protection(brightness, contrast), offsets)
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _corrigate_contrast(c: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    if equals(1, highlight - shadow):
        return c
    gradient = contrast_gradient(c) / (highlight - shadow)
    return find_contrast_gradient(gradient)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]
