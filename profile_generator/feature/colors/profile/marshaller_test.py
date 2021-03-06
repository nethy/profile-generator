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
                **_DEFAULT,
                "LabEnabled": "true",
                "LabaCurve": "1;0.00000;0.00000;0.06250;0.03787;0.12500;0.08301;"
                + "0.18750;0.13590;0.25000;0.19661;0.31250;0.26473;"
                + "0.37500;0.33921;0.43750;0.41836;0.50000;0.50000;"
                + "0.56250;0.58164;0.62500;0.66079;0.68750;0.73527;"
                + "0.75000;0.80339;0.81250;0.86410;0.87500;0.91699;"
                + "0.93750;0.96213;1.00000;1.00000;",
                "LabbCurve": "1;0.00000;0.00000;0.06250;0.03787;0.12500;0.08301;"
                + "0.18750;0.13590;0.25000;0.19661;0.31250;0.26473;"
                + "0.37500;0.33921;0.43750;0.41836;0.50000;0.50000;"
                + "0.56250;0.58164;0.62500;0.66079;0.68750;0.73527;"
                + "0.75000;0.80339;0.81250;0.86410;0.87500;0.91699;"
                + "0.93750;0.96213;1.00000;1.00000;",
            },
            get_profile_args({"vibrance": 50}),
        )

        self.assertEqual(
            {
                **_DEFAULT,
                "LabEnabled": "true",
                "LabaCurve": "1;0.00000;0.11920;1.00000;0.88080;",
                "LabbCurve": "1;0.00000;0.11920;1.00000;0.88080;",
            },
            get_profile_args({"vibrance": -50}),
        )
