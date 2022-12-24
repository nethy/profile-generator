# mypy: ignore-errors
# pylint: skip-file


from functools import partial
from timeit import Timer

from profile_generator.model import bezier
from profile_generator.unit import Point, curve


def run_benchmark():
    bench(
        bench_bezier_curve_2,
        bench_bezier_curve_4,
        bench_bezier_curve_8,
        bench_bezier_curve_16,
        bench_bezier_curve_32,
        bench_bezier_curve_64,
        bench_bezier_curve_128,
        bench_bezier_curve_256,
    )


def bench_bezier_curve_2():
    bench_bezier_curve(2)


def bench_bezier_curve_4():
    bench_bezier_curve(4)


def bench_bezier_curve_8():
    bench_bezier_curve(8)


def bench_bezier_curve_16():
    bench_bezier_curve(16)


def bench_bezier_curve_32():
    bench_bezier_curve(32)


def bench_bezier_curve_64():
    bench_bezier_curve(64)


def bench_bezier_curve_128():
    bench_bezier_curve(128)


def bench_bezier_curve_256():
    bench_bezier_curve(256)


def bench_bezier_curve(table_size):
    points = [
        (Point(0, 0), 1),
        (Point(0.15, 0), 1),
        (Point(0.25, 1), 1),
        (Point(1, 1), 1),
    ]
    curve.as_points(bezier.curve(points, table_size))


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
