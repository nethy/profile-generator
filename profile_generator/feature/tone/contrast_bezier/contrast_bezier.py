import logging
from typing import List, Tuple

from unit import Line, Point, Strength

from .bezier import bezier

_logger = logging.getLogger(__name__)

_BLACK_POINT = Point(0, 0)
_WHITE_POINT = Point(1, 1)

_SHADOW_LIMIT = 8 / 255
_HIGHLIGHT_LIMIT = 240 / 255

_POINTS_COUNT = 8


def calculate(grey: Point, strength: Strength) -> List[Point]:
    _logger.info("Calculating contrast curve: {grey} {strength}")
    (shadow, highlight) = _get_control_points(grey, strength)
    toe = _get_bezier_curve([(_BLACK_POINT, 1), (shadow, 2), (grey, 1)])
    shoulder = _get_bezier_curve([(grey, 1), (highlight, 1), (_WHITE_POINT, 1)])
    return toe + shoulder[1:]


def _get_control_points(grey: Point, strength: Strength) -> Tuple[Point, Point]:
    if strength.value < 1:
        contrast_line = _get_contrast_line(grey, strength)
        shadow = Point(contrast_line.get_x(_SHADOW_LIMIT), _SHADOW_LIMIT)
        highlight = Point(contrast_line.get_x(_HIGHLIGHT_LIMIT), _HIGHLIGHT_LIMIT)
        return (shadow, highlight)
    else:
        shadow = Point(grey.x, _SHADOW_LIMIT)
        highlight = Point(grey.x, _HIGHLIGHT_LIMIT)
        return (shadow, highlight)


def _get_contrast_line(grey: Point, strength: Strength) -> Line:
    gradient = grey.y / (grey.x * (1 - strength.value))
    offset = grey.y - gradient * grey.x
    return Line(gradient, offset)


def _get_bezier_curve(points: bezier.WeightedPoints) -> List[Point]:
    return [
        bezier.get_point_at(points, 1 / (_POINTS_COUNT - 1) * i)
        for i in range(_POINTS_COUNT)
    ]
