import math
from typing import Optional

from profile_generator.model import linalg
from profile_generator.model.linalg import Matrix, Vector

SRGB_XY = [[0.64, 0.33], [0.3, 0.6], [0.15, 0.06]]
PROPHOTO_XY = [[0.7347, 0.2653], [0.29, 0.6], [0.15, 0.06]]

XYZ_TO_SRGB = [
    [3.240454162114103, -1.5371385127977157, -0.49853140955601577],
    [-0.9692660305051869, 1.8760108454466944, 0.041556017530349834],
    [0.05564343095911475, -0.20402591351675384, 1.057225188223179],
]

SRGB_TO_XYZ = [
    [0.41245643908969243, 0.357576077643909, 0.18043748326639894],
    [0.21267285140562264, 0.715152155287818, 0.07217499330655958],
    [0.01933389558232931, 0.11919202588130297, 0.9503040785363679],
]

XYZ_TO_PROPHOTO = [
    [2.6233934787916144, -1.1932679794417997, -0.40748473804080276],
    [-0.559215782890511, 1.548646195588611, -0.011438486457898737],
    [0.11786266946348113, -0.3263991830185436, 1.4696303242428785],
]

PROPHOTO_TO_XYZ = [
    [0.4560993669437902, 0.3787102635615131, 0.12941036949469678],
    [0.16469737586795635, 0.7835384763341651, 0.05176414779787871],
    [0.0, 0.14364872066126358, 0.6815612793387364],
]

D65_XYZ = [0.95047, 1.0, 1.08883]
D50_XYZ = [0.96422, 1.0, 0.82521]

BRADFORD = [
    [0.8951, 0.2664, -0.1614],
    [-0.7502, 1.7135, 0.0367],
    [0.0389, -0.0685, 1.0296],
]
BRADFORD_INVERSE = [
    [0.9869929, -0.1470543, 0.1599627],
    [0.4323053, 0.5183603, 0.0492912],
    [-0.0085287, 0.0400428, 0.9684867],
]


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
D50_TO_D65_ADAPTATION = chromatic_adaptation(D50_XYZ, D65_XYZ)
