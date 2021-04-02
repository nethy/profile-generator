from unittest import TestCase

from .marshaller import get_profile_args

_DEFAULT = {
    "LabEnabled": "false",
    "LabChromaticity": "0",
    "HsvEnabled": "false",
    "HsvSCurve": "0;",
}


class MarshallerTest(TestCase):
    def test_default(self) -> None:
        self.assertEqual(_DEFAULT, get_profile_args({}))

    def test_vibrance_positive(self) -> None:
        self.assertEqual(
            {
                **_DEFAULT,
                "HsvEnabled": "true",
                "HsvSCurve": "1;0;0.750000;0;0;1;0.750000;0;0;",
            },
            get_profile_args({"vibrance": 50}),
        )

    def test_vibrance_negative(self) -> None:
        self.assertEqual(
            {**_DEFAULT, "LabEnabled": "true", "LabChromaticity": "-36"},
            get_profile_args({"vibrance": -73}),
        )
