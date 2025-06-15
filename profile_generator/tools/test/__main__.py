# mypy: ignore-errors
# pylint: skip-file

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _GREY18,
    _SLOPE,
)


def print_calculation(name, fn, *args, **kwargs):
    print(name)
    result = fn(*args, **kwargs)
    if isinstance(result, list):
        print("[")
        for item in result:
            print(f"  {item},")
        print("]")
    else:
        print(result)
    print()


if __name__ == "__main__":
    print_calculation(
        "test_flat",
        contrast_sigmoid.get_flat,
        _GREY18,
    )
    print_calculation("test_contrast", contrast_sigmoid.get_contrast, _SLOPE)
