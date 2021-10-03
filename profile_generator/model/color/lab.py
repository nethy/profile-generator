import math

from profile_generator.model import linalg
from profile_generator.model.color.xyz import (
    D50_TO_D65_ADAPTATION,
    D65_TO_D50_ADAPTATION,
)
from profile_generator.model.linalg import Vector

from .white_point import D50_XYZ

LAB_F_SIGMA = 6 / 29
LAB_F_SIGMA_2 = 36 / 841
LAB_F_SIGMA_3 = 216 / 24389


def from_xyz(xyz_d65: Vector) -> Vector:
    xyz_d50 = linalg.multiply_matrix_vector(D65_TO_D50_ADAPTATION, xyz_d65)
    x_ratio, y_ratio, z_ratio = [value / ref for value, ref in zip(xyz_d50, D50_XYZ)]
    l = 116 * lab_f(y_ratio) - 16
    a = 500 * (lab_f(x_ratio) - lab_f(y_ratio))
    b = 200 * (lab_f(y_ratio) - lab_f(z_ratio))
    return [l, a, b]


def to_xyz(lab: Vector) -> Vector:
    l, a, b = lab
    x_ref, y_ref, z_ref = D50_XYZ
    l_ref = (l + 16) / 116
    x = x_ref * lab_f_inverse(l_ref + a / 500)
    y = y_ref * lab_f_inverse(l_ref)
    z = z_ref * lab_f_inverse(l_ref - b / 200)
    xyz_d50 = [x, y, z]
    xyz_d65 = linalg.multiply_matrix_vector(D50_TO_D65_ADAPTATION, xyz_d50)
    return xyz_d65


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
