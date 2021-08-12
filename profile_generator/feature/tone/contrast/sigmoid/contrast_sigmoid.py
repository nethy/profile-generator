import math
from collections.abc import Sequence

from profile_generator.model import spline
from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.linalg import Vector
from profile_generator.model.sigmoid import Curve, tone_curve_sqrt
from profile_generator.unit import Point


def calculate(
    neutral5: float,
    gamma: float,
    offsets: tuple[float, float] = (0.0, 1.0),
) -> Sequence[Point]:
    middle_grey = _get_middle_grey(neutral5)
    middle_grey = _corrigate_middle_grey(middle_grey, offsets)
    gradient = _corrigate_gamma(gamma, offsets)
    _curve = _apply_offsets(
        tone_curve_sqrt(middle_grey, gradient),
        offsets,
    )
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _get_middle_grey(neutral5: float) -> Point:
    in_lum = neutral5 / 255
    patch_lum = _srgb_to_luminance(ColorChart.NEUTRAL50)
    out_lum = constants.SRGB_MIDDLE_GREY_LUMINANCE
    in_lum *= out_lum / patch_lum
    return Point(in_lum, out_lum)


def _srgb_to_luminance(color: Vector) -> float:
    return rgb.luminance(rgb.normalize(color), SRGB)


def _corrigate_middle_grey(middle: Point, offsets: tuple[float, float]) -> Point:
    shadow, highlight = offsets
    return Point(middle.x, (middle.y - shadow) / (highlight - shadow))


def _corrigate_gamma(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    return gradient / (highlight - shadow)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]


def base_controls(
    neutral5: float, ev_corr: float = 0.0, ev_comp: float = 0.0
) -> Sequence[Point]:
    middle_grey = _get_middle_grey(neutral5)
    middle_grey.y = adjust(middle_grey.x, ev_comp)
    middle_grey.x = adjust(middle_grey.x, -ev_corr)
    if math.isclose(middle_grey.x, middle_grey.y):
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
        return [
            Point(0, 0),
            middle_grey,
            Point(1 - middle_grey.y, 1 - middle_grey.x),
            Point(1, 1),
        ]


def adjust(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))
