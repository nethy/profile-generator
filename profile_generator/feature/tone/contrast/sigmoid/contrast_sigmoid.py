from collections.abc import Sequence

from profile_generator.model import spline
from profile_generator.model.sigmoid import (
    Curve,
    curve,
    find_contrast_gradient,
    find_curve_brightness,
)
from profile_generator.unit import Point, equals


def calculate(
    grey: Point,
    gamma: float,
    highlight_protection: float = 1.0,
    offsets: tuple[float, float] = (0.0, 1.0),
) -> Sequence[Point]:
    contrast = _corrigate_gamma(gamma, offsets)
    brightness = find_curve_brightness(grey, contrast)
    _curve = _apply_offsets(curve(brightness, contrast, highlight_protection), offsets)
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _corrigate_gamma(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    corrigated_gradient = gradient
    if not equals(1, highlight - shadow):
        corrigated_gradient = gradient / (highlight - shadow)
    return find_contrast_gradient(corrigated_gradient)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]
