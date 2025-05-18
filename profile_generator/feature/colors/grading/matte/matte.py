import bisect
import math
from collections.abc import Callable
from operator import itemgetter

from profile_generator.main.profile_params import Matte, Toning
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space.srgb import SRGB


def get_matte_curve(matte_param: Matte) -> Callable[[float], float]:
    shadow_offset = matte_param.shadow.value / 255
    highlight_offset = matte_param.highlight.value / 255
    shadow_boundary = 2 * shadow_offset
    highlight_boundary = 1 - 2 * (1 - highlight_offset)

    shadow_curve = _get_shadow_curve(shadow_offset, shadow_boundary)
    highlight_curve = _get_highlight_curve(highlight_offset, highlight_boundary)

    def _curve(x: float) -> float:
        if x < shadow_boundary:
            return shadow_curve(x)
        elif x < highlight_boundary:
            return x
        else:
            return highlight_curve(x)

    return _curve


def _get_shadow_curve(offset: float, boundary: float) -> Callable[[float], float]:
    if math.isclose(offset, 0):
        return lambda x: x

    a = offset / math.pow(boundary, 2)
    b = 1 - 2 * offset / boundary
    c = offset

    return lambda x: a * x * x + b * x + c


def _get_highlight_curve(offset: float, boundary: float) -> Callable[[float], float]:
    if math.isclose(offset, 1):
        return lambda x: x

    a = (offset - 1) / math.pow(boundary - 1, 2)
    b = (boundary - a * math.pow(boundary, 2) + a - offset) / (boundary - 1)
    c = offset - a - b

    return lambda x: a * x * x + b * x + c


def get_lightness_curve(toning: Toning) -> Callable[[float], float]:
    global_l = toning.global_lch.as_list()[0]
    shadow_l = toning.shadow_lch.as_list()[0]
    midtone_l = toning.midtone_lch.as_list()[0]
    highlight_l = toning.highlight_lch.as_list()[0]

    lightnesses: list[list[float]] = [
        [0, 0],
        [25, 25 + shadow_l + global_l],
        [50, 50 + midtone_l + global_l],
        [75, 75 + highlight_l + global_l],
        [100, 100],
    ]

    def _curve(x: float) -> float:
        i = bisect.bisect(lightnesses, x, key=itemgetter(0))
        if i == 0:
            return 0
        elif i < len(lightnesses):
            begin = lightnesses[i - 1]
            end = lightnesses[i]
            length = end[0] - begin[0]
            return (end[0] - x) / length * begin[1] + (x - begin[0]) / length * end[1]
        else:
            return 100

    return lambda x: _to_rgb_from_lab(_curve(_to_lab_from_rgb(x)))


def _to_lab_from_rgb(x: float) -> float:
    return lab.from_xyz(xyz.from_rgb([x] * 3, SRGB))[0]


def _to_rgb_from_lab(x: float) -> float:
    return xyz.to_rgb(lab.to_xyz([x, 0, 0]), SRGB)[0]
