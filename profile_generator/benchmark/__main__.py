# mypy: ignore-errors
# pylint: skip-file

from timeit import Timer

from profile_generator.model import sigmoid
from profile_generator.unit import Point


def run_benchmark():
    bench(
        bench_find_contrast_slope,
        bench_find_brightness_midpoint,
        bench_find_curve_brightness,
        bench_curve,
        bench_curve_with_hl_protection,
    )


def bench_find_contrast_slope():
    test_over(-10, 10, sigmoid.find_contrast_gradient)


def bench_find_brightness_midpoint():
    test_over(-10, 10, sigmoid._find_brightness_midpoint)


def bench_find_curve_brightness():
    grey = Point(92 / 255, 122 / 255)
    test_over(-20, 20, lambda c: sigmoid.find_curve_brightness(grey, c))


def bench_curve():
    for b in test_range(-10, 10, 10):
        curve = sigmoid.get_curve(12, b)
        for x in test_range(0, 1, 10):
            curve(x)


def bench_curve_with_hl_protection():
    for b in test_range(-10, 10, 10):
        curve = sigmoid.get_curve_with_hl_protection(12, b)
        for x in test_range(0, 1, 10):
            curve(x)


def test_over(start, stop, fn):
    for next in test_range(start, stop, 100):
        fn(next)


def test_range(start, stop, sample_size):
    return (start + x / sample_size * (stop - start) for x in range(sample_size))


def bench(*fns):
    report = {get_name(fn): measure(fn) for fn in fns}
    width = 0
    for name in report:
        if len(name) > width:
            width = len(name)
    print("  Report")
    for name, time in sorted(report.items(), key=lambda x: x[1], reverse=True):
        print("{}{: 6.0f}ms".format(name.ljust(width), time * 1000))


def get_name(fn):
    return fn.__name__[6:]


def measure(fn):
    print("Benchmarking " + get_name(fn))
    return Timer(fn).timeit(100)


if __name__ == "__main__":
    run_benchmark()
