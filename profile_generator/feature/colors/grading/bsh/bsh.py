import math
import pprint
from collections.abc import Sequence
from typing import Final

from profile_generator.main.profile_params import Bsh
from profile_generator.model.color import lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Vector


class ReferenceColorLch:
    RED: Final = [50.0, 20.0, 30.0]
    YELLOW: Final = [50.0, 20.0, 90.0]
    GREEN: Final = [50.0, 20.0, 150.0]
    CYAN: Final = [50.0, 20.0, 210.0]
    BLUE: Final = [50.0, 20.0, 270.0]
    MAGENTA: Final = [50.0, 20.0, 330.0]


def get_hsvs(bsh: Bsh) -> Sequence[tuple[Vector, Vector]]:
    """
    Returns hsv color tuples; first is the reference value, the second is the modified.
    """
    params_by_lch: list[tuple[Vector, Vector]] = [
        (ReferenceColorLch.RED, bsh.red.as_list()),
        (ReferenceColorLch.YELLOW, bsh.yellow.as_list()),
        (ReferenceColorLch.GREEN, bsh.green.as_list()),
        (ReferenceColorLch.CYAN, bsh.cyan.as_list()),
        (ReferenceColorLch.BLUE, bsh.blue.as_list()),
        (ReferenceColorLch.MAGENTA, bsh.magenta.as_list()),
    ]
    result = [
        (_to_hsv_from_lch(lch), _apply(lch, bsh))
        for lch, bsh in params_by_lch
    ]
    pprint.pp(result)
    return result


def _apply(lch: Vector, bsh: Vector) -> Vector:
    if all(math.isclose(value, 0, rel_tol=1e-2) for value in bsh):
        return _to_hsv_from_lch(lch)
    ref_b, ref_s, ref_h = _to_bsh_from_lch(lch)
    b, s, h = bsh
    new_b = ref_b * math.pow(1.5, b / 10.0)
    new_s = ref_s * math.pow(1.5, s / 10.0)
    new_h = ref_h + 60 * (h / 10.0)
    return _to_hsv_from_bsh([new_b, new_s, new_h])


def _to_bsh_from_lch(lch: Vector) -> Vector:
    return lab.to_bsh(lab.from_lch(lch))


def _to_hsv_from_bsh(bsh: Vector) -> Vector:
    return rgb.to_hsv(xyz.to_rgb(lab.to_xyz(lab.from_bsh(bsh)), SRGB))


def _to_hsv_from_lch(lch: Vector) -> Vector:
    return rgb.to_hsv(xyz.to_rgb(lab.to_xyz(lab.from_lch(lch)), SRGB))
