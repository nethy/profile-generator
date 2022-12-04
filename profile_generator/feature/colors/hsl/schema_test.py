from unittest import TestCase

from profile_generator.profile_params import HueParams, ProfileParams
from profile_generator.schema import (
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import _STEPS, SCHEMA, _parse, process

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
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 6,
                    "magenta": -6,
                },
                "saturation": {
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 6,
                    "magenta": -6,
                },
                "luminance": {
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 6,
                    "magenta": -6,
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
            {"hue": {"blue": -11}},
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

    def test_process_default(self) -> None:
        self.assertEqual(process({}), DEFAULT)

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
            DEFAULT
            | {
                "HhCurve": "1;0.0000000;0.5000000;0.0000000;0.0000000;"
                + "0.1666667;0.3750000;0.0000000;0.0000000;"
                + "0.3333333;0.6250000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.6250000;0.0000000;0.0000000;"
                + "0.8333333;0.3750000;0.0000000;0.0000000;",
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
            DEFAULT
            | {
                "ChCurve": "1;0.0000000;0.6500000;0.0000000;0.0000000;"
                + "0.1666667;0.5000000;0.0000000;0.0000000;"
                + "0.3333333;0.5000000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.5000000;0.0000000;0.0000000;"
                + "0.8333333;0.3500000;0.0000000;0.0000000;",
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
            DEFAULT
            | {
                "LhCurve": "1;0.0000000;0.5350000;0.0000000;0.0000000;"
                + "0.1666667;0.5000000;0.0000000;0.0000000;"
                + "0.3333333;0.5000000;0.0000000;0.0000000;"
                + "0.5000000;0.5000000;0.0000000;0.0000000;"
                + "0.6666667;0.5000000;0.0000000;0.0000000;"
                + "0.8333333;0.4650000;0.0000000;0.0000000;",
            },
        )

    def test_parse(self) -> None:
        profile_params = ProfileParams()

        _parse(
            {
                "hue": {
                    "red": 1,
                    "yellow": 2,
                    "green": 3,
                    "cyan": 4,
                    "blue": 5,
                    "magenta": 6,
                },
                "saturation": {
                    "red": 1,
                    "yellow": 2,
                    "green": 3,
                    "cyan": 4,
                    "blue": 5,
                    "magenta": 6,
                },
                "luminance": {
                    "red": 1,
                    "yellow": 2,
                    "green": 3,
                    "cyan": 4,
                    "blue": 5,
                    "magenta": 6,
                },
            },
            profile_params,
        )

        expected_hue_params = HueParams(1, 2, 3, 4, 5, 6)
        self.assertEqual(profile_params.color.hsl.hue, expected_hue_params)
        self.assertEqual(profile_params.color.hsl.saturation, expected_hue_params)
        self.assertEqual(profile_params.color.hsl.luminance, expected_hue_params)
