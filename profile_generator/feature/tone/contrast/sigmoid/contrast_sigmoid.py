from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline
from profile_generator.model.sigmoid import Curve, curve, curve_sqrt
from profile_generator.unit import Point


@cache
def calculate(
    middle: Point,
    gamma: float,
    highlight_protection: float = 1.0,
    offsets: tuple[float, float] = (0.0, 1.0),
) -> Sequence[Point]:
    gradient = _corrigate_gamma(gamma, offsets)
    _curve = _apply_offsets(
        curve_sqrt(middle, gradient, 1.0, 1 / highlight_protection),
        offsets,
    )
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _corrigate_gamma(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    return gradient / (highlight - shadow)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]
