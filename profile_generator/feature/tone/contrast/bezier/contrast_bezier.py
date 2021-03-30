import logging
import math
from typing import List, Tuple

from profile_generator.unit import Line, Point, Strength

from . import bezier_fn
from .bezier_fn import WeightedPoints

_logger = logging.getLogger(__name__)

_BLACK_POINT = Point(0, 0)
_WHITE_POINT = Point(1, 1)

_SHADOW_PROTECTION_SLOPE = 0.13165249758739585347152645740972  # 7.5 degree
_HIGHLIGHT_PROTECTION_SLOPE = 0.26794919243112270647255365849413  # 15 degree

_POINTS_COUNT = 8

_CONTRAST_LIMIT = 4


def calculate(
    gray: Point,
    strength: Strength,
    weights: Tuple[float, float],
) -> List[Point]:
    _logger.info("Calculating contrast curve: {grey} {strength}")
    (shadow, highlight) = _get_control_points(gray, strength)
    toe = _get_bezier_curve(
        [(_BLACK_POINT, weights[0]), (shadow, weights[0]), (gray, 1)]
    )
    shoulder = _get_bezier_curve(
        [(gray, 1), (highlight, weights[1]), (_WHITE_POINT, weights[1])]
    )
    return toe + shoulder[1:]


def _get_control_points(gray: Point, strength: Strength) -> Tuple[Point, Point]:
    contrast_correction = math.sqrt(gray.y / gray.x)
    q = (1 - 1 / (strength.value * (_CONTRAST_LIMIT - 1) + 1)) / contrast_correction
    contrast_line = _get_contrast_line(gray, q)
    shadow_line = Line(-_SHADOW_PROTECTION_SLOPE, 0 + _SHADOW_PROTECTION_SLOPE * gray.x)
    shadow = contrast_line.intersect(shadow_line)
    highlight_line = Line(
        -_HIGHLIGHT_PROTECTION_SLOPE, 1 + _HIGHLIGHT_PROTECTION_SLOPE * gray.x
    )
    highlight = contrast_line.intersect(highlight_line)
    return (shadow, highlight)


def _get_contrast_line(gray: Point, q: float) -> Line:
    gradient = gray.y / (gray.x * (1 - q))
    offset = gray.y - gradient * gray.x
    return Line(gradient, offset)


def _get_bezier_curve(points: WeightedPoints) -> List[Point]:
    return [
        bezier_fn.get_point_at(points, 1 / (_POINTS_COUNT - 1) * i)
        for i in range(_POINTS_COUNT)
    ]
