import math

from profile_generator.model import linalg
from profile_generator.model.color.xyz import (
    D50_TO_D65_ADAPTATION,
    D65_TO_D50_ADAPTATION,
)
from profile_generator.model.linalg import Vector

from .white_point import D50_XYZ, D65_XYZ


def from_xyz(xyz_d65: Vector) -> Vector:
    xyz_d50 = linalg.multiply_matrix_vector(D65_TO_D50_ADAPTATION, xyz_d65)
    x_ratio, y_ratio, z_ratio = [value / ref for value, ref in zip(xyz_d50, D50_XYZ)]
    l = 116 * _lab_f(y_ratio) - 16
    a = 500 * (_lab_f(x_ratio) - _lab_f(y_ratio))
    b = 200 * (_lab_f(y_ratio) - _lab_f(z_ratio))
    return [l, a, b]


def to_xyz(lab: Vector) -> Vector:
    l, a, b = lab
    x_ref, y_ref, z_ref = D50_XYZ
    l_ref = (l + 16) / 116
    x = x_ref * _lab_f_inverse(l_ref + a / 500)
    y = y_ref * _lab_f_inverse(l_ref)
    z = z_ref * _lab_f_inverse(l_ref - b / 200)
    xyz_d50 = [x, y, z]
    xyz_d65 = linalg.multiply_matrix_vector(D50_TO_D65_ADAPTATION, xyz_d50)
    return xyz_d65


def to_lch(lab: Vector) -> Vector:
    l, a, b = lab
    c = math.sqrt(a * a + b * b)
    h = math.degrees(math.atan2(b, a))
    if h < 0:
        h += 360
    return [l, c, h]


def from_lch(lch: Vector) -> Vector:
    l, c, h = lch
    a = c * math.cos(math.radians(h))
    b = c * math.sin(math.radians(h))
    return [l, a, b]


def to_bsh(lab: Vector) -> Vector:
    """
    Brilliance, Saturation, Hue
    """
    l, c, h = to_lch(lab)
    b = math.sqrt(l * l + c * c)
    s = (1 - math.atan2(l, c) / math.pi * 2) * 100 if l > 0 or c > 0 else 0
    return [b, s, h]


def from_bsh(bsh: Vector) -> Vector:
    b, s, h = bsh
    s_radians = (1 - s / 100) * math.pi / 2
    l = b * math.sin(s_radians)
    c = b * math.cos(s_radians)
    return from_lch([l, c, h])


def from_xyz_lum(y_d65: float) -> float:
    return 116 * _lab_f(y_d65 / D65_XYZ[1]) - 16


def to_xyz_lum(lum: float) -> float:
    return D65_XYZ[1] * _lab_f_inverse((lum + 16) / 116)


SIGMA = 6.0 / 29.0
SIGMA_2 = 36.0 / 841.0
SIGMA_3 = 216.0 / 24389.0


def _lab_f(x: float) -> float:
    if x > SIGMA_3:
        return math.pow(x, 1 / 3)
    else:
        return x / (3 * SIGMA_2) + 4 / 29


def _lab_f_inverse(x: float) -> float:
    if x > SIGMA:
        return math.pow(x, 3)
    else:
        return 3 * SIGMA_2 * (x - 4 / 29)
