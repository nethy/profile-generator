# mypy: ignore-errors
# pylint: skip-file
from functools import cache
from pprint import pprint

from profile_generator.model import sigmoid, spline
from profile_generator.util import search


def find_coeff(gradient):
    return search.jump_search(0, 100, sigmoid.contrast_gradient, gradient)


if __name__ == "__main__":
    pprint(spline.fit(find_coeff, 1.0, 5.0, 1e-7))
