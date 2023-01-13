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

    def parse(self, data: Any):
        if isinstance(self._value, ProfileParamEnum):
            data = cast(ProfileParamEnum, self._value).parse(data)

        if data is None:
            return

        self._value = data


class Camera(ProfileParamParser):
    def __init__(self):
        self.resolution_mp: Final = Value[float](16)


class Hcl(ProfileParamParser):
    def __init__(self):
        self.hue: Final = Value[float](0)
        self.chromacity: Final = Value[float](0)
        self.luminance: Final = Value[float](0)


class Grading(ProfileParamParser):
    def __init__(self):
        self.base: Final = Hcl()
        self.shadow: Final = Hcl()
        self.midtone: Final = Hcl()
        self.highlight: Final = Hcl()


class HueParams(ProfileParamParser):
    def __init__(self):
        self.red: Final = Value[float](0)
        self.yellow: Final = Value[float](0)
        self.green: Final = Value[float](0)
        self.cyan: Final = Value[float](0)
        self.blue: Final = Value[float](0)
        self.magenta: Final = Value[float](0)


class Hsl(ProfileParamParser):
    def __init__(self):
        self.hue: Final = HueParams()
        self.saturation: Final = HueParams()
        self.luminance: Final = HueParams()


@unique
class ColorSpace(ProfileParamEnum):
    ACES_P0 = "ACESp0"
    ACES_P1 = "ACESp1"
    PRO_PHOTO = "ProPhoto"
    REC_2020 = "Rec2020"
    SRGB = "sRGB"


class WhiteBalance(ProfileParamParser):
    def __init__(self):
        self.temperature: Final = Value[int](6504)
        self.tint: Final = Value[float](1)


class ColorProfile(ProfileParamParser):
    def __init__(self) -> None:
        self.working: Final = Value[ColorSpace](ColorSpace.PRO_PHOTO)


class Colors(ProfileParamParser):
    def __init__(self):
        self.vibrance: Final = Value[float](0)
        self.chrome: Final = Value[float](0)
        self.grading: Grading = Grading()
        self.hsl: Final = Hsl()
        self.profile: Final = ColorProfile()
        self.white_balance: Final = WhiteBalance()


@unique
class NoiseReductionMode(ProfileParamEnum):
    AGGRESSIVE = "shalbi"
    CONSERVATIVE = "shal"


class NoiseReduction(ProfileParamParser):
    def __init__(self):
        self.mode: Final = Value[NoiseReductionMode](NoiseReductionMode.CONSERVATIVE)
        self.luminance: Final = Value[float](0)
        self.chrominance: Final = Value[float](0)


class CaptureSharpening(ProfileParamParser):
    def __init__(self):
        self.radius: Final = Value[float](0)
        self.threshold: Final = Value[int](10)


class OutputSharpening(ProfileParamParser):
    def __init__(self):
        self.radius: Final = Value[float](0.75)
        self.threshold: Final = Value[int](20)
        self.amount: Final = Value[int](100)
        self.damping: Final = Value[int](0)
        self.iterations: Final = Value[int](30)


class Sharpening(ProfileParamParser):
    def __init__(self):
        self.capture: Final = CaptureSharpening()
        self.output: Final = OutputSharpening()


@unique
class DemosaicMethod(ProfileParamEnum):
    AMAZE = "amaze"
    AMAZE_VNG4 = "amazevng4"
    DCB_VNG4 = "dcbvng4"
    RCD_VNG4 = "rcdvng4"
    LMMSE = "lmmse"


class Demosaic(ProfileParamParser):
    def __init__(self):
        self.algorithm: Final = Value[DemosaicMethod](DemosaicMethod.AMAZE)
        self.auto_threshold: Final = Value[bool](True)
        self.threshold: Final = Value[int](20)


class Contrast(ProfileParamParser):
    def __init__(self):
        self.local: Final = Value[float](0.0)


class Raw(ProfileParamParser):
    def __init__(self):
        self.demosaic: Final = Demosaic()
        self.black_points: Final = Value[tuple[int, int, int]]((0, 0, 0))


class Sigmoid(ProfileParamParser):
    def __init__(self):
        self.grey18: Final = Value[float](90.0)
        self.slope: Final = Value[float](1.6)


class Curve(ProfileParamParser):
    def __init__(self):
        self.sigmoid: Final = Sigmoid()


class Tone(ProfileParamParser):
    def __init__(self):
        self.curve: Final = Curve()
        self.contrast: Final = Contrast()


class Details(ProfileParamParser):
    def __init__(self):
        self.sharpening: Final = Sharpening()


class ProfileParams(ProfileParamParser):
    def __init__(self):
        self.camera: Final = Camera()
        self.raw: Final = Raw()
        self.tone: Final = Tone()
        self.details: Final = Details()
        self.colors: Final = Colors()
