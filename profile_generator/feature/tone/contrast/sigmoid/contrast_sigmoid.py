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
    neutral5: Vector,
    gamma: float,
    ev_comp: float = 0.0,
    offsets: tuple[float, float] = (0.0, 1.0),
) -> Sequence[Point]:
    middle_grey = _get_middle_grey(neutral5, ev_comp)
    middle_grey = _corrigate_middle_grey(middle_grey, offsets)
    gradient = _corrigate_gamma(gamma, offsets)
    _curve = _apply_offsets(
        tone_curve_sqrt(middle_grey, gradient),
        offsets,
    )
    return [Point(x, y) for x, y in spline.fit(_curve)]


def _get_middle_grey(neutral5: Vector, ev_comp: float) -> Point:
    in_lum = _srgb_to_luminance(neutral5)
    patch_lum = _srgb_to_luminance(ColorChart.NEUTRAL50)
    in_lum = in_lum * constants.SRGB_MIDDLE_GREY_LUMINANCE / patch_lum
    out_lum = constants.SRGB_MIDDLE_GREY_LUMINANCE * math.pow(2, ev_comp)
    return Point(SRGB.gamma(in_lum), SRGB.gamma(out_lum))


def _srgb_to_luminance(color: Vector) -> float:
    color = [SRGB.inverse_gamma(x) for x in rgb.normalize(color)]
    return rgb.luminance(color, SRGB)


def _corrigate_middle_grey(middle: Point, offsets: tuple[float, float]) -> Point:
    shadow, highlight = offsets
    return Point(middle.x, (middle.y - shadow) / (highlight - shadow))


def _corrigate_gamma(gradient: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    return gradient / (highlight - shadow)


def _apply_offsets(fn: Curve, offsets: tuple[float, float]) -> Curve:
    return lambda x: fn(x) * (offsets[1] - offsets[0]) + offsets[0]


def base_controls(neutral5: Vector) -> Sequence[Point]:
    middle_grey = _get_middle_grey(neutral5, 0)
    shadow_control = middle_grey / 2
    highlight_control = Point(middle_grey.x + 1, middle_grey.y + 1) / 2
    return [shadow_control, middle_grey, highlight_control]
