from abc import ABC
from enum import Enum, unique
from typing import Any, Final, Generic, TypeVar, cast


class ProfileParamParser(ABC):
    def parse(self, data: Any) -> None:
        if data is None:
            return

        for name, value in self.__dict__.items():
            parser = cast(ProfileParamParser, value)
            parser.parse(data.get(name))


A = TypeVar("A", bound=Enum)


class ProfileParamEnum(Enum):
    @classmethod
    def parse(cls: type[A], data: Any) -> A | None:
        if data is None:
            return None
        for member in cls:
            if member.value.casefold() == data.casefold():
                return member
        return None


B = TypeVar("B", str, int, float, bool, ProfileParamEnum)


class Value(Generic[B], ProfileParamParser):
    def __init__(self, value: B):
        self._value: B = value

    @property
    def value(self) -> B:
        return self._value

    def parse(self, data: Any) -> None:
        if isinstance(self._value, ProfileParamEnum):
            data = cast(ProfileParamEnum, self._value).parse(data)

        if data is None:
            return

        self._value = data


class Camera:
    RESOLUTION_MP: Final = Value[float](16)


class Hcl:
    HUE: Final = Value[float](0)
    CHROMACITY: Final = Value[float](0)
    LUMINANCE: Final = Value[float](0)


class Grading:
    BASE: Final = Hcl()
    SHADOW: Final = Hcl()
    MIDTONE: Final = Hcl()
    HIGHLIGHT: Final = Hcl()


class HueParams:
    RED: Final = Value[float](0)
    YELLOW: Final = Value[float](0)
    GREEN: Final = Value[float](0)
    CYAN: Final = Value[float](0)
    BLUE: Final = Value[float](0)
    MAGENTA: Final = Value[float](0)


class Hsl:
    HUE: Final = HueParams()
    SATURATION: Final = HueParams()
    LUMINANCE: Final = HueParams()


@unique
class ColorSpace(ProfileParamEnum):
    ACES_P0 = "ACESp0"
    ACES_P1 = "ACESp1"
    PRO_PHOTO = "ProPhoto"
    REC_2020 = "Rec2020"
    SRGB = "sRGB"


class WhiteBalance:
    TEMPERATURE: Final = Value[int](6504)
    TINT: Final = Value[float](1)


class Color:
    VIBRANCE: Final = Value[float](0)
    CHROME: Final = Value[float](0)
    grading: Grading = Grading()
    HSL: Final = Hsl()
    PROFILE: Final = Value[ColorSpace](ColorSpace.PRO_PHOTO)
    WHITE_BALANCE: Final = WhiteBalance()


@unique
class NoiseReductionMode(ProfileParamEnum):
    AGGRESSIVE = "shalbi"
    CONSERVATIVE = "shal"


class NoiseReduction:
    MODE: Final = Value[NoiseReductionMode](NoiseReductionMode.CONSERVATIVE)
    LUMINANCE: Final = Value[float](0)
    CHROMINANCE: Final = Value[float](0)


class CaptureSharpening:
    RADIUS: Final = Value[float](0)
    THRESHOLD: Final = Value[int](10)


class OutputSharpening:
    RADIUS: Final = Value[float](0.75)
    THRESHOLD: Final = Value[int](20)
    AMOUNT: Final = Value[int](100)
    DAMPING: Final = Value[int](0)
    ITERATIONS: Final = Value[int](30)


class Sharpening:
    CAPTURE: Final = CaptureSharpening()
    OUTPUT: Final = OutputSharpening()


@unique
class DemosaicMethod(ProfileParamEnum):
    AMAZE = "amaze"
    AMAZE_VNG4 = "amazevng4"
    DCB_VNG4 = "dcbvng4"
    RCD_VNG4 = "rcdvng4"
    LMMSE = "lmmse"


class Demosaic:
    METHOD: Final = Value[DemosaicMethod](DemosaicMethod.AMAZE)
    AUTO_THRESHOLD: Final = Value[bool](True)
    THRESHOLD: Final = Value[int](20)


class Contrast:
    GREY18: Final = Value[float](90.0)
    STRENGTH: Final = Value[float](1.6)
    LINEAR_PROFILE: Final = Value[bool](True)
    LOCAL: Final = Value[float](0.0)


class ProfileParams:
    CAMERA: Final = Camera()
    COLOR: Final = Color()
    NOISE_REDUCTION: Final = NoiseReduction()
    SHARPENING: Final = Sharpening()
    DEMOSAIC: Final = Demosaic()
    CONTRAST: Final = Contrast()
