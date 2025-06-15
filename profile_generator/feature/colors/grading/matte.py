import math
from collections.abc import Callable

from profile_generator.main.profile_params import Matte
from profile_generator.unit import Curve


def get_matte_curve(matte_param: Matte) -> Curve:
    shadow_offset = matte_param.black.value / 100
    highlight_offset = matte_param.white.value / 100
    shadow_boundary = 2.5 * shadow_offset
    highlight_boundary = 1 - 2.5 * (1 - highlight_offset)

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
