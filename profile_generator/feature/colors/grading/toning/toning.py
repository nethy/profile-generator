import bisect
import math
from collections.abc import Callable

from profile_generator.main.profile_params import ColorTone
from profile_generator.model.color import lab
from profile_generator.unit import Vector
from profile_generator.util import validation

COLOR_TONE = tuple[float, Vector]


def get_lab_curve(color_tones: list[ColorTone]) -> Callable[[float], Vector]:
    sorted_tones = sorted(color_tones, key=lambda item: item.l.value)
    _validate(sorted_tones)
    lab_tones = _to_lab(sorted_tones)

    def lab_curve(x: float) -> Vector:
        i = bisect.bisect(lab_tones, x, key=lambda item: item[0])
        if i == 0:
            lab = lab_tones[0][1]
        elif i == len(lab_tones):
            lab = lab_tones[-1][1]
        else:
            lab = _interpolate(x, lab_tones[i-1], lab_tones[i])
        return [a + b for a, b in zip(lab, [x, 0, 0])]

    if len(lab_tones) > 0:
        return lab_curve
    else:
        return lambda x: [x, 0, 0]


def _validate(color_tones: list[ColorTone]) -> None:
    for i in range(len(color_tones) - 1):
        current = color_tones[i].l.value
        next = color_tones[i+1].l.value
        validation.is_greater_or_equal(next - current, 0.1)


def _to_lab(color_tones: list[ColorTone]) -> list[COLOR_TONE]:
    return [
        (l, lab.from_lch(lch))
        for l, *lch in map(ColorTone.as_list, color_tones)
    ]


def _interpolate(x: float, left: COLOR_TONE, right: COLOR_TONE) -> Vector:
    weight = _weight((x - left[0]) / (right[0] - left[0]))
    return [
        weight * a + (1 - weight) * b
        for a, b in zip(left[1], right[1])
    ]

def _weight(x: float) -> float:
    return 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1
