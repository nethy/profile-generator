from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline, tone_curve
from profile_generator.model.color import rgb
from profile_generator.unit import Point


@cache
def calculate(
    grey18: float,
    slope: float,
) -> tuple[Sequence[Point], ...]:
    adjusted_grey18 = rgb.normalize_value(grey18)
    filmic_curves = tone_curve.filmic(adjusted_grey18, slope)
    return tuple(map(spline.fit, filmic_curves))
