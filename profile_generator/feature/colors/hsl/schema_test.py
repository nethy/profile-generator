from unittest import TestCase

from profile_generator.schema import InvalidObjectError, SchemaValidator
from profile_generator.schema.range_schema import InvalidRangeError
from profile_generator.schema.type_schema import InvalidTypeError

from .schema import _STEPS, SCHEMA, process

DEFAULT = {
    "HhCurve": "0;",
    "ChCurve": "0;",
    "LhCurve": "0;",
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "hue": {
                    "magenta": -6,
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 6,
                },
                "saturation": {
                    "magenta": -6,
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 6,
                },
                "luminance": {
                    "magenta": -6,
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 6,
                },
            }
        )

    def test_validate_invalid_hue(self) -> None:
        self.validator.assert_error(
            {"hue": False}, InvalidObjectError({"hue": InvalidTypeError(dict)})
        )

    def test_validate_invalid_saturation(self) -> None:
        self.validator.assert_error(
            {"saturation": False},
            InvalidObjectError({"saturation": InvalidTypeError(dict)}),
        )

    def test_validate_invalid_luminance(self) -> None:
        self.validator.assert_error(
            {"luminance": False},
            InvalidObjectError({"luminance": InvalidTypeError(dict)}),
        )

    def test_validate_invalid_color_value(self) -> None:
        self.validator.assert_error(
            {"hue": {"blue": 1.2}},
            InvalidObjectError(
                {
                    "hue": InvalidObjectError(
                        {"blue": InvalidRangeError(-_STEPS, _STEPS)}
                    )
                }
            ),
        )
        self.validator.assert_error(
            {"hue": {"blue": -8}},
            InvalidObjectError(
                {
                    "hue": InvalidObjectError(
                        {"blue": InvalidRangeError(-_STEPS, _STEPS)}
                    )
                }
            ),
        )
        self.validator.assert_error(
            {"hue": {"blue": False}},
            InvalidObjectError(
                {
                    "hue": InvalidObjectError(
                        {"blue": InvalidRangeError(-_STEPS, _STEPS)}
                    )
                }
            ),
        )

    def test_process_hue(self) -> None:
        data = {
            "hue": {
                "yellow": -5,
                "green": 5,
                "cyan": 0,
                "blue": 5,
                "magenta": -5,
            }
        }
        self.assertEqual(
            process(data),
            {
                **DEFAULT,
                "LabEnabled": "true",
                "HhCurve": "1;0.000000;0.500000;0;0;"
                + "0.166667;0.321429;0;0;"
                + "0.333333;0.678571;0;0;"
                + "0.500000;0.500000;0;0;"
                + "0.666667;0.678571;0;0;"
                + "0.833333;0.321429;0;0;",
            },
        )

    def test_process_saturation(self) -> None:
        data = {
            "saturation": {
                "red": 5,
                "magenta": -5,
            }
        }
        self.assertEqual(
            process(data),
            {
                **DEFAULT,
                "LabEnabled": "true",
                "ChCurve": "1;0.000000;0.714286;0;0;"
                + "0.166667;0.500000;0;0;"
                + "0.333333;0.500000;0;0;"
                + "0.500000;0.500000;0;0;"
                + "0.666667;0.500000;0;0;"
                + "0.833333;0.285714;0;0;",
            },
        )

    def test_process_luminances(self) -> None:
        data = {
            "luminance": {
                "red": 5,
                "magenta": -5,
            }
        }
        self.assertEqual(
            process(data),
            {
                **DEFAULT,
                "LabEnabled": "true",
                "LhCurve": "1;0.000000;0.550000;0;0;"
                + "0.166667;0.500000;0;0;"
                + "0.333333;0.500000;0;0;"
                + "0.500000;0.500000;0;0;"
                + "0.666667;0.500000;0;0;"
                + "0.833333;0.450000;0;0;",
            },
        )
