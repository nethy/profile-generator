import math
from typing import Optional

from profile_generator.model.linalg import Vector

from .white_point import D65_XYZ

LAB_F_SIGMA = 6 / 29
LAB_F_SIGMA_2 = 36 / 841
LAB_F_SIGMA_3 = 216 / 24389


def from_xyz(xyz: Vector, white_point: Optional[Vector] = None) -> Vector:
    white_point = white_point or D65_XYZ
    x_ratio, y_ratio, z_ratio = [value / ref for value, ref in zip(xyz, white_point)]
    l = 116 * lab_f(y_ratio) - 16
    a = 500 * (lab_f(x_ratio) - lab_f(y_ratio))
    b = 200 * (lab_f(y_ratio) - lab_f(z_ratio))
    return [l, a, b]


def to_xyz(lab: Vector, white_point: Optional[Vector] = None) -> Vector:
    white_point = white_point or D65_XYZ
    l, a, b = lab
    x_ref, y_ref, z_ref = white_point
    l_ref = (l + 16) / 116
    x = x_ref * lab_f_inverse(l_ref + a / 500)
    y = y_ref * lab_f_inverse(l_ref)
    z = z_ref * lab_f_inverse(l_ref - b / 200)
    return [x, y, z]


def to_lch(lab: Vector) -> Vector:
    l, a, b = lab
    c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
    h = math.degrees(math.atan2(b, a))
    if h < 0:
        h += 360
    return [l, c, h]


def from_lch(lch: Vector) -> Vector:
    l, c, h = lch
    a = c * math.cos(math.radians(h))
    b = c * math.sin(math.radians(h))
    return [l, a, b]


def lab_f(x: float) -> float:
    if x > LAB_F_SIGMA_3:
        return math.pow(x, 1 / 3)
    else:
        return x / (3 * LAB_F_SIGMA_2) + 4 / 29


def lab_f_inverse(x: float) -> float:
    if x > LAB_F_SIGMA:
        return math.pow(x, 3)
    else:
        return 3 * LAB_F_SIGMA_2 * (x - 4 / 29)
