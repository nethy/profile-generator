import math
from collections.abc import Sequence

from profile_generator.model import gamma, spline
from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.sigmoid import Curve, tone_curve_sqrt
from profile_generator.unit import Point


def calculate(
    grey18: float,
    gradient: float,
    offsets: tuple[float, float] = (0.0, 1.0),
) -> Sequence[Point]:
    middle = _get_middle(grey18)
    middle = _corrigate_middle(middle, offsets)
    _gradient = _corrigate_gamma(gradient, offsets)
    _curve = _apply_offsets(
        tone_curve_sqrt(middle, _gradient),
        offsets,
    )
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _get_middle(grey18: float) -> Point:
    in_lum = rgb.normalize_value(grey18)
    out_lum = constants.MIDDLE_GREY_LUMINANCE_SRGB
    return Point(in_lum, out_lum)


def _corrigate_middle(middle: Point, offsets: tuple[float, float]) -> Point:
    shadow, highlight = offsets
    return Point(middle.x, (middle.y - shadow) / (highlight - shadow))


def _corrigate_gamma(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    return gradient / (highlight - shadow)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]


def base_controls(neutral5: float, ev_comp: float = 0.0) -> Sequence[Point]:
    middle_grey = _get_middle(neutral5)
    middle_grey.y = _adjust(middle_grey.x, ev_comp)
    if math.isclose(*middle_grey):
        shadow_control = middle_grey / 2
        highlight_control = Point(middle_grey.x + 1, middle_grey.y + 1) / 2
        return [
            Point(0, 0),
            shadow_control,
            middle_grey,
            highlight_control,
            Point(1, 1),
        ]
    else:
        base_curve, _ = gamma.gamma_linear(*middle_grey)
        return [Point(x, y) for x, y in spline.fit(base_curve)]


def _adjust(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))
