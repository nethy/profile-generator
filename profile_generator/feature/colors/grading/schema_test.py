from unittest import TestCase

from profile_generator.schema import (
    InvalidListError,
    InvalidListSizeError,
    InvalidObjectError,
    InvalidRangeError,
    InvalidTypeError,
    SchemaValidator,
)

from .schema import SCHEMA, process

DEFAULT = {
    "RGBCurvesEnabled": "false",
    "RGBCurvesRCurve": "0;",
    "RGBCurvesGCurve": "0;",
    "RGBCurvesBCurve": "0;",
}


class SchemaTest(TestCase):
    def setUp(self) -> None:
        self.validator = SchemaValidator(self, SCHEMA)

    def test_validate_valid_config(self) -> None:
        self.validator.assert_valid(
            {"shadow": [30, 5, -5], "midtone": [120, 2, 0], "highlight": [320, 8, 5]}
        )

    def test_validate_invalid_shadow(self) -> None:
        self.validator.assert_error(
            {"shadow": False},
            InvalidObjectError({"shadow": InvalidTypeError(tuple)}),
        )

    def test_validate_invalid_midtone(self) -> None:
        self.validator.assert_error(
            {"midtone": False},
            InvalidObjectError({"midtone": InvalidTypeError(tuple)}),
        )

    def test_validate_invalid_highlight(self) -> None:
        self.validator.assert_error(
            {"highlight": False},
            InvalidObjectError({"highlight": InvalidTypeError(tuple)}),
        )

    def test_validate_invalid_tint_value(self) -> None:
        self.validator.assert_error(
            {"shadow": False}, InvalidObjectError({"shadow": InvalidTypeError(tuple)})
        )

        self.validator.assert_error(
            {"shadow": [0]},
            InvalidObjectError({"shadow": InvalidListSizeError(3)}),
        )

        self.validator.assert_error(
            {"shadow": [False, 0, 0]},
            InvalidObjectError(
                {"shadow": InvalidListError({1: InvalidRangeError(0.0, 360.0)})}
            ),
        )

    def test_process_default(self) -> None:
        self.assertEqual(process({}), DEFAULT)

    def test_process(self) -> None:
        self.assertEqual(
            process(
                {
                    "shadow": [30, 5, -5],
                    "midtone": [120, 2, 0],
                    "highlight": [320, 8, 5],
                }
            ),
            {
                "RGBCurvesEnabled": "true",
                "RGBCurvesRCurve": "1;0.0000000;0.0000000;"
                + "0.1077034;0.1212422;"
                + "0.1893757;0.2182220;"
                + "0.3226963;0.3376571;"
                + "0.4663266;0.4633724;"
                + "0.6184204;0.6328111;"
                + "0.7777584;0.8106199;"
                + "0.8875672;0.9045831;"
                + "1.0000000;1.0000000;",
                "RGBCurvesGCurve": "1;0.0000000;0.0000000;"
                + "0.1077034;0.1037024;"
                + "0.1893757;0.1805566;"
                + "0.3226963;0.3189638;"
                + "0.4663266;0.4682064;"
                + "0.6184204;0.6127973;"
                + "0.7777584;0.7637486"
                + ";0.8875672;0.8804867;"
                + "1.0000000;1.0000000;",
                "RGBCurvesBCurve": "1;0.0000000;0.0000000;"
                + "0.1077034;0.1014174;"
                + "0.1893757;0.1757557;"
                + "0.3226963;0.3097780;"
                + "0.4663266;0.4546580;"
                + "0.6184204;0.6307581;"
                + "0.7777584;0.8162691"
                + ";0.8875672;0.9073216;"
                + "1.0000000;1.0000000;",
            },
        )
