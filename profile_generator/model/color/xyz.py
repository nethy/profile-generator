import math
from typing import Optional

from profile_generator.model import linalg
from profile_generator.model.color.space.color_space import ColorSpace
from profile_generator.model.color.white_point import D50_XYZ, D65_XYZ
from profile_generator.model.linalg import Matrix, Vector

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


def from_rgb(rgb: Vector, color_space: ColorSpace) -> Vector:
    linear = [color_space.inverse_gamma(x) for x in rgb]
    return linalg.transform(color_space.xyz_matrix, linear)


def to_rgb(xyz: Vector, color_space: ColorSpace) -> Vector:
    linear = linalg.transform(color_space.xyz_inverse_matrix, xyz)
    return [color_space.gamma(x) for x in linear]


def from_xyy(xyy: Vector) -> Vector:
    x, y, big_y = xyy
    if math.isclose(y, 0):
        return [0.0, 0.0, 0.0]
    return [x * big_y / y, big_y, (1 - x - y) * big_y / y]


def to_xyy(xyz: Vector, white_point: Optional[Vector] = None) -> Vector:
    white_point = white_point or D65_XYZ
    x, y, z = xyz
    summary = x + y + z
    if math.isclose(summary, 0):
        return white_point[:2] + [0.0]
    return [x / summary, y / summary, y]


def chromatic_adaptation(xyz_source: Vector, xyz_target: Vector) -> Matrix:
    source = linalg.transform(BRADFORD, xyz_source)
    target = linalg.transform(BRADFORD, xyz_target)
    scale = [t / s for t, s in zip(target, source)]
    return linalg.multiply_matrix_matrix(
        BRADFORD_INVERSE, linalg.scale_matrix(scale, BRADFORD)
    )


def conversion_matrix_of(refs: Matrix, white_point: Vector) -> Matrix:
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
