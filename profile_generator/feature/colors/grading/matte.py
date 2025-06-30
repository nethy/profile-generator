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
    shadow_threshold = shadow_offset * SQRT_8 / (SQRT_8 - 1)
    highlight_threshold = 1 - (1 - highlight_offset) * SQRT_8 / (SQRT_8 - 1)

    shadow_curve = _get_shadow_curve(shadow_offset, shadow_threshold)
    highlight_curve = _get_highlight_curve(highlight_offset, highlight_threshold)

    def _curve(x: float) -> float:
        if x < shadow_threshold:
            return shadow_curve(x)
        elif x < highlight_threshold:
            return x
        else:
            return highlight_curve(x)

    return _curve


def _get_shadow_curve(offset: float, threshold: float) -> Callable[[float], float]:
    if math.isclose(offset, 0):
        return lambda x: x

    c = offset
    b = threshold / (threshold - offset)
    a = (threshold - offset) / math.pow(threshold, b)

    return lambda x: a * math.pow(x, b) + c


def _get_highlight_curve(offset: float, threshold: float) -> Callable[[float], float]:
    if math.isclose(offset, 1):
        return lambda x: x

    c = 1 - offset
    b = (1 - threshold) / (offset - threshold)
    a = (offset - threshold) / math.pow(1 - threshold, b)

    return lambda x: 1 - (a * math.pow(1 - x, b) + c) if x < 1 else 1 - c
