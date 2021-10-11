from collections.abc import Iterable

from profile_generator.unit import DECIMALS, Point

_EQ_STRENGTH = 0.25
_ONE_SIDE_EQ_STRENGTH = 0.5


class CurveType:
    LINEAR = "0;"
    STANDARD = "1;"
    CONTROL_CAGE = "3;"
    FLEXIBLE = "4;"


class WbSetting:
    CAMERA = "Camera"
    CUSTOM = "Custom"


class EqPoint(Point):
    def present(self) -> str:
        return self._present(_EQ_STRENGTH, _EQ_STRENGTH)

    def _present(self, left: float, right: float) -> str:
        return (
            f"{self.x:.{DECIMALS}f};{self.y:.{DECIMALS}f};"
            + f"{left:.{DECIMALS}f};{right:.{DECIMALS}f};"
        )


class LinearEqPoint(EqPoint):
    def present(self) -> str:
        return self._present(0, 0)


class LeftLinearEqPoint(EqPoint):
    def present(self) -> str:
        return self._present(0, _ONE_SIDE_EQ_STRENGTH)


class RightLinearEqPoint(EqPoint):
    def present(self) -> str:
        return self._present(_ONE_SIDE_EQ_STRENGTH, 0)


def present_curve(points: Iterable[Point]) -> str:
    return "".join((_present_point(p) for p in points))


def _present_point(point: Point) -> str:
    return f"{point.x:.{DECIMALS}f};{point.y:.{DECIMALS}f};"


def present_equalizer(points: Iterable[EqPoint]) -> str:
    return "".join(p.present() for p in points)
