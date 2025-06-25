import math

from profile_generator.model import linalg
from profile_generator.model.color.xyz import (
    D50_TO_D65_ADAPTATION,
    D65_TO_D50_ADAPTATION,
)
from profile_generator.model.linalg import Vector

from .white_point import D50_XYZ


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


def from_xyz_lum(y: float) -> float:
    return 116 * _lab_f(y) - 16


def to_xyz_lum(l: float) -> float:
    return _lab_f_inverse((l + 16) / 116)


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


def to_rgb_hue(lab_hue: float):
    lab_hue_in_radians = _to_radians(lab_hue)
    rgb_hue = 0.0

    if lab_hue_in_radians >= 0 and lab_hue_in_radians < 0.6:
        rgb_hue = 0.11666 * lab_hue_in_radians + 0.93
    elif lab_hue_in_radians >= 0.6 and lab_hue_in_radians < 1.4:
        rgb_hue = 0.1125 * lab_hue_in_radians - 0.0675
    elif lab_hue_in_radians >= 1.4 and lab_hue_in_radians < 2:
        rgb_hue = 0.2666 * lab_hue_in_radians - 0.2833
    elif lab_hue_in_radians >= 2 and lab_hue_in_radians < 3.14159:
        rgb_hue = 0.1489 * lab_hue_in_radians - 0.04785
    elif lab_hue_in_radians >= -3.14159 and lab_hue_in_radians < -2.8:
        rgb_hue = 0.23419 * lab_hue_in_radians + 1.1557
    elif lab_hue_in_radians >= -2.8 and lab_hue_in_radians < -2.3:
        rgb_hue = 0.16 * lab_hue_in_radians + 0.948
    elif lab_hue_in_radians >= -2.3 and lab_hue_in_radians < -0.9:
        rgb_hue = 0.12143 * lab_hue_in_radians + 0.85928
    elif lab_hue_in_radians >= -0.9 and lab_hue_in_radians < -0.1:
        rgb_hue = 0.2125 * lab_hue_in_radians + 0.94125
    elif lab_hue_in_radians >= -0.1 and lab_hue_in_radians < 0:
        rgb_hue = 0.1 * lab_hue_in_radians + 0.93

    if rgb_hue < 0.0:
        rgb_hue += 1.0
    elif rgb_hue > 1.0:
        rgb_hue -= 1.0

    return rgb_hue


def _to_radians(degree: float):
    """
    0..360 -> -pi..pi
    """
    return round(math.radians(degree if degree < 180 else degree - 360), 5)


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
