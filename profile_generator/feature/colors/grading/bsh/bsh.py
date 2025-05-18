import math
from collections.abc import Sequence
from typing import Final

from profile_generator.main.profile_params import Bsh
from profile_generator.model.color import lab, rgb, xyz
from profile_generator.model.color.space import srgb
from profile_generator.unit import Vector


class ReferenceColorLch:
    RED: Final = [50.0, 50.0, 30.0]
    YELLOW: Final = [50.0, 50.0, 90.0]
    GREEN: Final = [50.0, 50.0, 150.0]
    CYAN: Final = [50.0, 50.0, 210.0]
    BLUE: Final = [50.0, 50.0, 270.0]
    MAGENTA: Final = [50.0, 50.0, 330.0]


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
    new_lchs_by_lch = {
        (lch[0], lch[1], lch[2]): _apply(lch, bsh) for lch, bsh in params_by_lch
    }
    return [
        (_to_hsv_from_lch(list(lch)), _to_hsv_from_lch(new_lch))
        for lch, new_lch in new_lchs_by_lch.items()
    ]


def _apply(lch: Vector, bsh: Vector) -> Vector:
    ref_b, ref_s, ref_h = lab.to_bsh(lab.from_lch(lch))
    b, s, h = bsh
    new_b = ref_b * math.pow(2, b / 10.0)
    new_s = ref_s * math.pow(2, s / 10.0)
    new_h = ref_h + (60 / 360) * (h / 10.0)
    return lab.to_lch(lab.from_bsh([new_b, new_s, new_h]))


def _to_hsv_from_lch(lch: Vector) -> Vector:
    return rgb.to_hsv(xyz.to_rgb(lab.to_xyz(lab.from_lch(lch)), srgb.SRGB))
