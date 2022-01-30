from collections.abc import Callable

from .line import Line
from .point import Point
from .precision import *
from .strength import Strength

Curve = Callable[[float], float]
Vector = list[float]
Matrix = list[list[float]]
