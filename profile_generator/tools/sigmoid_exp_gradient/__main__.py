# mypy: ignore-errors
# pylint: skip-file

from functools import cache
from pprint import pprint

from profile_generator.model import sigmoid, spline
from profile_generator.util import search


def _get_coeff(gradient):
    return search.jump_search(0, 100, sigmoid.contrast_gradient, gradient)


def _get_fit():
    return spline.fit(_get_coeff, 1, 5, 1e-12)


if __name__ == "__main__":
    pprint(search.get_table(0, 20, 32, sigmoid.contrast_gradient))
