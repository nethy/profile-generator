import math
from collections.abc import Sequence

from profile_generator.model import gamma, spline
from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.sigmoid import Curve, tone_curve_filmic, tone_curve_hlp
from profile_generator.unit import Point


def calculate(
    grey18: float,
    gradient: float,
    offsets: tuple[float, float] = (0.0, 1.0),
    highlight_protection: bool = False,
    ev_comp: float = 0.0,
) -> Sequence[Point]:
    middle = _get_middle(grey18)
    middle = _corrigate_middle(middle, offsets)
    _gradient = _corrigate_gamma(gradient, offsets)
    _curve = (
        tone_curve_filmic(middle, _gradient)
        if not highlight_protection
        else tone_curve_hlp(middle, _gradient)
    )
    _curve = _apply_offsets(
        _curve,
        offsets,
    )
    _comp_curve, _ = gamma.gamma_sqrt(
        rgb.normalize_value(grey18),
        _adjust_ev(rgb.normalize_value(grey18), ev_comp),
    )
    return [Point(x, y) for x, y in spline.fit(lambda x: _curve(_comp_curve(x)))]


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


def _adjust_ev(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))
