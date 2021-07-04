from unittest import TestCase

from profile_generator.schema import InvalidObjectError, SchemaValidator
from profile_generator.schema.range_schema import InvalidRangeError
from profile_generator.schema.type_schema import InvalidTypeError

from .schema import SCHEMA, process

_DEFAULT = {
    "HhCurve": "0;",
    "ChCurve": "0;",
    "LhCurve": "0;",
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_empty_config(self) -> None:
        self.validator.assert_valid({})

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {
                "hue": {
                    "magenta": -5,
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 5,
                },
                "saturation": {
                    "magenta": -5,
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 5,
                },
                "luminance": {
                    "magenta": -5,
                    "red": -2,
                    "yellow": 0,
                    "green": 1,
                    "cyan": 2,
                    "blue": 5,
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
                {"hue": InvalidObjectError({"blue": InvalidRangeError(-5, 5)})}
            ),
        )
        self.validator.assert_error(
            {"hue": {"blue": -6}},
            InvalidObjectError(
                {"hue": InvalidObjectError({"blue": InvalidRangeError(-5, 5)})}
            ),
        )
        self.validator.assert_error(
            {"hue": {"blue": False}},
            InvalidObjectError(
                {"hue": InvalidObjectError({"blue": InvalidRangeError(-5, 5)})}
            ),
        )

    def test_process_defaults(self) -> None:
        self.assertEqual(process({}), _DEFAULT)

    def test_process_hue(self) -> None:
        data = {
            "hue": {
                "magenta": -5,
                "yellow": -5,
                "green": 5,
                "cyan": 0,
                "blue": 5,
            }
        }
        self.assertEqual(
            process(data),
            {
                **_DEFAULT,
                "LabEnabled": "true",
                "HhCurve": "1;0.140000;0.000000;0.288675;0.288675;"
                + "0.339744;1.000000;0.288675;0.288675;"
                + "0.530501;0.500000;0.288675;0.288675;"
                + "0.657801;1.000000;0.288675;0.288675;"
                + "0.896040;0.000000;0.288675;0.288675;",
            },
        )

    def test_process_saturation(self) -> None:
        data = {
            "saturation": {
                "magenta": -5,
                "red": 5,
            }
        }
        self.assertEqual(
            process(data),
            {
                **_DEFAULT,
                "LabEnabled": "true",
                "ChCurve": "1;0.896040;0.200000;0.288675;0.288675;"
                + "0.991736;0.800000;0.288675;0.288675;",
            },
        )

    def test_process_luminances(self) -> None:
        data = {
            "luminance": {
                "magenta": -5,
                "red": 5,
            }
        }
        self.assertEqual(
            process(data),
            {
                **_DEFAULT,
                "LabEnabled": "true",
                "LhCurve": "1;0.896040;0.200000;0.288675;0.288675;"
                + "0.991736;0.800000;0.288675;0.288675;",
            },
        )
