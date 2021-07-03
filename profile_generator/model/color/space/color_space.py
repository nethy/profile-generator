from collections.abc import Callable
from typing import NamedTuple

from profile_generator.model.linalg import Matrix, Vector


class ColorSpace(NamedTuple):
    xyz_matrix: Matrix
    xyz_inverse_matrix: Matrix
    white_point: Vector
    gamma: Callable[[float], float]
    inverse_gamma: Callable[[float], float]
