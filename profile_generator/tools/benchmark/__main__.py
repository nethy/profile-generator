# mypy: ignore-errors
# pylint: skip-file


from timeit import Timer

from profile_generator.model import sigmoid, spline
from profile_generator.unit import Point


def run_benchmark():
    bench(
        bench_tone_curve_exp_fitting_1200,
    )


def bench_tone_curve_exp_fitting_1200():
    for x in test_range(48, 104, 15):
        for y in test_range(100, 140, 4):
            middle = Point(x / 255, y / 255)
            for c in test_range(1, 3, 5):
                spline.fit(sigmoid.tone_curve_exp(middle, c))


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
