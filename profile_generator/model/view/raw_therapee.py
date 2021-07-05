from collections.abc import Callable, Iterable
from typing import TypeVar

from profile_generator.unit import DECIMALS, Point

_T = TypeVar("_T")
_Presenter = Callable[[_T], str]

_EQ_STRENGTH = f"{(1 / 3 * 1 / 4) ** (1 / 2):.{DECIMALS}f}"


class CurveType:
    LINEAR = "0;"
    STANDARD = "1;"
    FLEXIBLE = "4;"


class WbSetting:
    CAMERA = "Camera"
    CUSTOM = "Custom"


def _present_point(point: Point) -> str:
    return f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};"


def present_curve(points: Iterable[Point]) -> str:
    return "".join((_present_point(p) for p in points))


def _present_eq_point(point: Point) -> str:
    return (
        f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};"
        + f"{_EQ_STRENGTH};{_EQ_STRENGTH};"
    )


def _present_linear_eq_point(point: Point) -> str:
    return f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};0;0;"


def present_equalizer(points: Iterable[Point]) -> str:
    return _present(_present_eq_point, points)


def present_linear_equalizer(points: Iterable[Point]) -> str:
    return _present(_present_linear_eq_point, points)


def _present(presenter: _Presenter, items: Iterable[_T]) -> str:
    return "".join((presenter(i) for i in items))
