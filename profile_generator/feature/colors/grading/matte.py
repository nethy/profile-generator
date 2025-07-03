"""
(0,s)
(S,S)
(H,H)
(1,h)

s, h: shadow and highlight offsets
S, H: shadow, highlight linear tresholhds

thresholds are calculated by monotonic hermite spline condition.

f(x)  = ax^b+c = e^(b*ln(a)+ln(x))+c
f'(x) = abx^(b-1)

f(0) = s
f(S) = S
f'(S) = 1

c = s

aS^b+c = S
aS^b+s = S
aS^b = (S-s)
a = (S-s)/S^b

abS^(b-1) = 1
aS^b = S/b

S-s = S/b
b = S/(S-s)


"""
import math
from collections.abc import Callable

from profile_generator.main.profile_params import Matte
from profile_generator.unit import Curve

SQRT_8 = math.sqrt(8)


def get_matte_curve(matte_param: Matte) -> Curve:
    shadow_offset = matte_param.black.value / 100
    highlight_offset = matte_param.white.value / 100
    shadow_treshold = shadow_offset * 2
    highlight_treshold = 0.6

    shadow_curve = _get_shadow_curve(shadow_offset, shadow_treshold)
    highlight_curve = _get_highlight_curve(highlight_offset, highlight_treshold)

    def _curve(x: float) -> float:
        if x < shadow_treshold:
            return shadow_curve(x)
        elif x < highlight_treshold:
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
