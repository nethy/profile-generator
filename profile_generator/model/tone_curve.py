from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants
from profile_generator.unit import Curve, Line, Point

_MIDDLE_GREY = constants.LUMINANCE_50_SRGB


def filmic(grey18: float, gradient: float) -> Curve:
    middle = Point(grey18, _MIDDLE_GREY)
    base = _base_hermite(middle)
    contrast = _contrast(gradient)
    return lambda x: contrast(base(x))


def _base_hermite(middle: Point) -> Curve:
    xs = [0, middle.x, 1]
    ys = [0, middle.y, 1]
    ms = [middle.gradient, 1, (1 - middle.y) / (1 - middle.x)]
    hs = [0.0] * 2
    ss = [0.0] * 2
    cs = [0.0] * 2
    ds = [0.0] * 2
    for i in range(2):
        hs[i] = xs[i + 1] - xs[i]
        ss[i] = (ys[i + 1] - ys[i]) / hs[i]
        cs[i] = (3 * ss[i] - 2 * ms[i] - ms[i + 1]) / hs[i]
        ds[i] = (ms[i] + ms[i + 1] - 2 * ss[i]) / (hs[i] * hs[i])

    def interpolate(x: float) -> float:
        i = 0 if x < middle.x else 1
        dx = x - xs[i]
        return ys[i] + ms[i] * dx + cs[i] * dx * dx + ds[i] * dx * dx * dx

    return interpolate


def _contrast(gradient: float) -> Curve:
    shadow = sigmoid.algebraic(gradient, 2.5)
    highlight = sigmoid.algebraic(gradient, 2)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(_MIDDLE_GREY, 0.5))
    shift_y = gamma.power_at(Point(0.5, _MIDDLE_GREY))
    return lambda x: shift_y(curve(shift_x(x)))


def brightness(p: Point) -> Curve:
    base_line = Line(p.gradient, 0)
    threshold = base_line.get_x(_MIDDLE_GREY)
    highlight = gamma.partial_algebraic_at(
        Point(threshold, _MIDDLE_GREY), base_line.gradient
    )
    return lambda x: base_line.get_y(x) if x < threshold else highlight(x)
