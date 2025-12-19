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

===============================

Cubic interpolation

o: offset
t: threshold, where the curve meet the linear tone

The curve is defined in a isoscele triangle, so
t = (1+sqrt(2)/2) * o

maximum:
t = 0.5
o = 1/(2+sqrt(2)) ~0.2929

f(x) = ax^3+bx^2+cx+d

For shadows:
f(0) = o
f(t) = t
f'(0) = 0
f'(t) = 1

d = o
c = 0
b = (2t-3o)/t^2
a = (1-2bt)/t^2

For highlights:
f(0) = o
f(t) = t
f'(t) = 1
f''(0) = 0

d = o
c = (1-3o)/2t
b = 0
a = (1-c)/3t^2

t = 0.5
"""

import math
from collections.abc import Callable, Mapping

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Curve, curve, equals
from profile_generator.util import validation

SQRT_8 = math.sqrt(8)

OFFSET_MAXIMUM = 1 / (2 + math.sqrt(2))


def generate(profile_params: ProfileParams, exclude_defult: bool) -> Mapping[str, str]:
    matte_strength = profile_params.colors.grading.matte
    if exclude_defult and not matte_strength.is_set:
        return {}

    normalized_strength = matte_strength.value / 10.0
    offset = 0.0 * (1.0 - normalized_strength) + OFFSET_MAXIMUM * normalized_strength
    matte_curve = get_matte_curve(offset)
    return {
        "LCurve": (
            raw_therapee.present_curve(
                raw_therapee.CurveType.FLEXIBLE, curve.as_points(matte_curve)
            )
            if normalized_strength > 0.0
            else raw_therapee.present_linear_curve()
        )
    }


def get_matte_curve(offset: float) -> Curve:
    validation.is_in_closed_interval(offset, 0.0, OFFSET_MAXIMUM)
    if equals(offset, 0.0):
        return lambda x: x

    shadow_threshold = (1 + math.sqrt(2) / 2) * offset
    highlight_threshold = 0.5  # [0.5, 1-offset)
    shadow_fade = _get_fade(offset, shadow_threshold)
    highlight_fade = _get_fade(offset, 1 - highlight_threshold)

    def _curve(x: float) -> float:
        if x < shadow_threshold:
            return shadow_fade(x)
        elif x <= highlight_threshold:
            return x
        else:
            return 1 - highlight_fade(1 - x)

    return _curve


def _get_fade(offset: float, threshold: float) -> Callable[[float], float]:
    c = 1 - 3 * offset / (2 * threshold)
    a = (1 - c) / (3 * math.pow(threshold, 2))
    return lambda x: a * math.pow(x, 3) + c * x + offset
