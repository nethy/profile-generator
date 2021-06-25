import math
from typing import Optional

from profile_generator.model import linalg
from profile_generator.model.linalg import Matrix, Vector

from .colorspace_constants import (
    BRADFORD,
    BRADFORD_INVERSE,
    D50_XYZ,
    D65_XYZ,
    SRGB_TO_XYZ,
    XYZ_TO_PROPHOTO,
    XYZ_TO_SRGB,
)

LAB_F_SIGMA = 6 / 29
LAB_F_SIGMA_2 = 36 / 841
LAB_F_SIGMA_3 = 216 / 24389


def normalize(srgb: Vector) -> Vector:
    return list(map(lambda x: x / 255, srgb))


def ev_comp_srgb(srgb: Vector, compensation: float) -> Vector:
    if math.isclose(compensation, 0):
        return srgb
    linear = map(srgb_gamma_inverse, srgb)
    linear = map(lambda x: x * 2 ** compensation, linear)
    return list(map(srgb_gamma, linear))


def srgb_to_xyz(srgb: Vector) -> Vector:
    linear = list(map(srgb_gamma_inverse, srgb))
    return linalg.transform(SRGB_TO_XYZ, linear)


def xyz_to_srgb(xyz: Vector) -> Vector:
    linear = linalg.transform(XYZ_TO_SRGB, xyz)
    return list(map(srgb_gamma, linear))


def xyz_to_prophoto(xyz: Vector) -> Vector:
    linear = linalg.transform(XYZ_TO_PROPHOTO, xyz)
    return list(map(prophoto_gamma, linear))


def srgb_to_prophoto(srgb: Vector) -> Vector:
    xyz = srgb_to_xyz(srgb)
    return xyz_to_prophoto(xyz)


def xyy_to_xyz(xyy: Vector) -> Vector:
    x, y, big_y = xyy
    if math.isclose(y, 0):
        return [0.0, 0.0, 0.0]
    return [x * big_y / y, big_y, (1 - x - y) * big_y / y]


def xyz_to_xyy(xyz: Vector, white_point: Optional[Vector] = None) -> Vector:
    white_point = white_point or D65_XYZ
    x, y, z = xyz
    summary = x + y + z
    if math.isclose(summary, 0):
        return white_point[:2] + [0.0]
    return [x / summary, y / summary, y]


def xyz_to_lab(xyz: Vector, white_point: Optional[Vector] = None) -> Vector:
    white_point = white_point or D65_XYZ
    x_ratio, y_ratio, z_ratio = [value / ref for value, ref in zip(xyz, white_point)]
    l = 116 * lab_f(y_ratio) - 16
    a = 500 * (lab_f(x_ratio) - lab_f(y_ratio))
    b = 200 * (lab_f(y_ratio) - lab_f(z_ratio))
    return [l, a, b]


def lab_to_xyz(lab: Vector, white_point: Optional[Vector] = None) -> Vector:
    white_point = white_point or D65_XYZ
    l, a, b = lab
    x_ref, y_ref, z_ref = white_point
    l_ref = (l + 16) / 116
    x = x_ref * lab_f_inverse(l_ref + a / 500)
    y = y_ref * lab_f_inverse(l_ref)
    z = z_ref * lab_f_inverse(l_ref - b / 200)
    return [x, y, z]


def lab_to_lch(lab: Vector) -> Vector:
    l, a, b = lab
    c = math.sqrt(a ** 2 + b ** 2)
    h = math.degrees(math.atan2(b, a))
    if h < 0:
        h += 360
    return [l, c, h]


def lch_to_lab(lch: Vector) -> Vector:
    l, c, h = lch
    a = c * math.cos(math.radians(h))
    b = c * math.sin(math.radians(h))
    return [l, a, b]


def lab_f(x: float) -> float:
    if x > LAB_F_SIGMA_3:
        return x ** (1 / 3)
    else:
        return x / (3 * LAB_F_SIGMA_2) + 4 / 29


def lab_f_inverse(x: float) -> float:
    if x > LAB_F_SIGMA:
        return x ** 3
    else:
        return 3 * LAB_F_SIGMA_2 * (x - 4 / 29)


def srgb_gamma_inverse(x: float) -> float:
    if x <= 0.040449936:
        return max(0.0, x / 12.92)
    else:
        return min(1.0, ((x + 0.055) / 1.055) ** 2.4)


def srgb_gamma(x: float) -> float:
    if x <= 0.0031308:
        return max(0.0, 12.92 * x)
    else:
        return min(1.0, 1.055 * x ** (1 / 2.4) - 0.055)


def prophoto_gamma(x: float) -> float:
    if x < 0.001953125:
        return max(0.0, 16 * x)
    else:
        return min(1.0, x ** (1 / 1.8))


def prophoto_gamma_inverse(x: float) -> float:
    if x < 0.03125:
        return max(0.0, x / 16)
    else:
        return min(1.0, x ** 1.8)


def chromatic_adaptation(xyz_source: Vector, xyz_target: Vector) -> Matrix:
    source = linalg.transform(BRADFORD, xyz_source)
    target = linalg.transform(BRADFORD, xyz_target)
    scale = [[0.0, 0.0, 0.0] for _ in range(3)]
    for i in range(3):
        scale[i][i] = target[i] / source[i]
    return linalg.multiply(BRADFORD_INVERSE, linalg.multiply(scale, BRADFORD))


def get_conversion_matrix(refs: Matrix, white_point: Vector) -> Matrix:
    r, g, b = refs
    matrix = [
        [r[0] / r[1], g[0] / g[1], b[0] / b[1]],
        [1.0, 1.0, 1.0],
        [(1 - r[0] - r[1]) / r[1], (1 - g[0] - g[1]) / g[1], (1 - b[0] - b[1]) / b[1]],
    ]
    inverse = linalg.inverse(list(matrix))
    coeffs = linalg.transform(inverse, white_point)
    return [[coeff * value for coeff, value in zip(coeffs, row)] for row in matrix]


D65_TO_D50_ADAPTATION = chromatic_adaptation(D65_XYZ, D50_XYZ)
