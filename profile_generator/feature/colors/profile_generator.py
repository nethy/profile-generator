import math
from collections.abc import Mapping, Sequence
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

from .grading.profile_generator import generate as generate_grading
from .hsl.profile_generator import generate as generate_hsl
from .space.profile_generator import generate as generate_space
from .white_balance.profile_generator import generate as generate_white_balance


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return {
        **_get_vibrance(profile_params),
        **generate_grading(profile_params),
        **generate_hsl(profile_params),
        **generate_space(profile_params),
        **generate_white_balance(profile_params),
    }


class Template:
    A_CURVE: Final = "LcACurve"
    B_CURVE: Final = "LcBCurve"


_MAX_VIBRANCE: Final = 10.0


def _get_vibrance(profile_params: ProfileParams) -> Mapping[str, str]:
    contrast = profile_params.tone.curve.sigmoid.slope.value
    vibrance = profile_params.colors.vibrance.value
    base = math.pow(contrast, 0.605)
    multiplier = 1 + vibrance / _MAX_VIBRANCE
    points = _control_cage_points(base * multiplier)
    curve = raw_therapee.present_curve(raw_therapee.CurveType.CONTROL_CAGE, points)
    return {Template.A_CURVE: curve, Template.B_CURVE: curve}


_DAMPING_THRESHOLD = 0.05


def _control_cage_points(value: float) -> Sequence[Point]:
    x = 0.5 * value / (1 + value)
    y = 0.5 - x
    dx = 0.5 * (1 - _DAMPING_THRESHOLD)
    return [
        Point(0, 0),
        Point(x, y),
        Point(dx, dx),
        Point(1 - dx, 1 - dx),
        Point(1 - x, 1 - y),
        Point(1, 1),
    ]
