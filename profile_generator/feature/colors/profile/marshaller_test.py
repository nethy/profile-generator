from unittest import TestCase

from .marshaller import get_profile_args

_DEFAULT = {
    "LabEnabled": "false",
    "LabaCurve": "0;",
    "LabbCurve": "0;",
}


class MarshallerTest(TestCase):
    def test_default(self) -> None:
        self.assertEqual(_DEFAULT, get_profile_args({}))

    def test_vibrance(self) -> None:
        self.assertEqual(
            {
                "LabEnabled": "true",
                "LabaCurve": "1;0.000000;0.000000;0.125490;0.083398;0.305882;0.257195;"
                + "0.768627;0.822289;0.909804;0.943055;1.000000;1.000000;",
                "LabbCurve": "1;0.000000;0.000000;0.125490;0.083398;0.305882;0.257195;"
                + "0.768627;0.822289;0.909804;0.943055;1.000000;1.000000;",
            },
            get_profile_args({"vibrance": 50}),
        )

        self.assertEqual(
            {
                "LabEnabled": "true",
                "LabaCurve": "1;0.000000;0.119203;1.000000;0.880797;",
                "LabbCurve": "1;0.000000;0.119203;1.000000;0.880797;",
            },
            get_profile_args({"vibrance": -50}),
        )
