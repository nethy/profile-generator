from unittest import TestCase


class ColorspaceTest(TestCase):
    def assert_color_equal(
        self, left: list[float], right: list[float], places: int = 7
    ) -> None:
        self.assertEqual(
            len(left), len(right), "length incorrect: left is {0}, but right is {1}"
        )
        for a, b in zip(left, right):
            diff = abs(a - b)
            if round(diff, places) != 0:
                message = (
                    f"{[round(x, places) for x in left]} != "
                    + f"{[round(x, places) for x in right]}"
                )
                raise self.failureException(message)
