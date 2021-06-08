# mypy: ignore-errors
# pylint: skip-file

#   Report
# find_curve_brightness     1760ms
# spline_fitting            1243ms
# find_contrast_gradient      27ms
# curve_with_hl_protection    21ms
# curve                        9ms

from timeit import Timer

from profile_generator.model import sigmoid, spline
from profile_generator.unit import Point


def run_benchmark():
    bench(
        bench_find_contrast_gradient,
        bench_find_curve_brightness,
        bench_curve,
        bench_curve_with_hl_protection,
        bench_spline_fitting,
    )


def bench_find_curve_brightness():
    for x in range(48, 128 + 1, 8):
        for y in range(92, 164 + 1, 8):
            grey = Point(x / 255, y / 255)
            test_over(-20, 20, 100, lambda c: sigmoid.find_curve_brightness(grey, c))


def bench_find_contrast_gradient():
    test_over(0.1, 10, 1000, sigmoid.find_contrast_gradient)


def bench_curve():
    for b in test_range(-10, 10, 20):
        curve = sigmoid.curve(b, 12)
        for x in test_range(0, 1, 50):
            curve(x)


def bench_curve_with_hl_protection():
    for b in test_range(-10, 10, 20):
        curve = sigmoid.curve_with_hl_protection(b, 12)
        for x in test_range(0, 1, 50):
            curve(x)


def bench_spline_fitting():
    for b in test_range(1, 3, 8):
        for c in test_range(2, 12, 8):
            spline.fit(sigmoid.curve(b, c))


def test_over(start, stop, step, fn):
    for next in test_range(start, stop, step):
        fn(next)


def test_range(begin, end, sample_size):
    return (begin + x / (sample_size - 1) * (end - begin) for x in range(sample_size))


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
    return Timer(fn).timeit(3)


if __name__ == "__main__":
    run_benchmark()