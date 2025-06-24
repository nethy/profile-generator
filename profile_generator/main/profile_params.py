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


E = TypeVar("E", bound=Enum)


class ProfileParamEnum(Enum):
    @classmethod
    def parse(cls: type[E], data: Any) -> E | None:
        if data is None:
            return None
        for member in cls:
            if member.name.casefold() == data.casefold():
                return member
        return None


T = TypeVar("T", str, int, float, bool)


class ProfileParamTuple(Generic[T], ProfileParamParser):
    def parse(self, data: Any) -> None:
        if data is None:
            return
        for i, value in enumerate(self.__dict__.values()):
            parser = cast(ProfileParamParser, value)
            parser.parse(data[i])

    def as_list(self) -> list[T]:
        return [cast(Value, value).value for value in self.__dict__.values()]


V = TypeVar("V", str, int, float, bool, tuple, list, ProfileParamEnum)


class Value(Generic[V], ProfileParamParser):
    def __init__(self, value: V):
        self._value: V = value
        self._is_set = False

    @property
    def value(self) -> V:
        return self._value

    @property
    def is_set(self) -> bool:
        return self._is_set

    def parse(self, data: Any) -> None:
        if isinstance(self._value, ProfileParamEnum):
            data = cast(ProfileParamEnum, self._value).parse(data)

        if data is None:
            return

        self._value = data
        self._is_set = True


class Camera(ProfileParamParser):
    def __init__(self) -> None:
        self.resolution_mp: Final = Value[float](16)


class LchValue(ProfileParamTuple[float]):
    def __init__(self) -> None:
        self.luminance: Final = Value[float](0)
        self.chroma: Final = Value[float](0)
        self.hue: Final = Value[float](0)


@unique
class ColorToningChannel(ProfileParamEnum):
    ONE = 1
    TWO = 2
    THREE = 3


class ColorToning(ProfileParamParser):
    def __init__(self) -> None:
        self.channels = Value[ColorToningChannel](ColorToningChannel.TWO)
        self.black = LchValue()
        self.shadow = LchValue()
        self.midtone = LchValue()
        self.highlight = LchValue()
        self.white = LchValue()


class Matte(ProfileParamParser):
    def __init__(self) -> None:
        self.black: Final = Value[float](0)
        self.white: Final = Value[float](100)


class LchAdjustment(ProfileParamParser):  # pylint: disable=too-many-instance-attributes
    def __init__(self) -> None:
        self.magenta = Value[float](0)
        self.orange = Value[float](0)
        self.yellow = Value[float](0)
        self.green = Value[float](0)
        self.aqua = Value[float](0)
        self.teal = Value[float](0)
        self.blue = Value[float](0)
        self.purple = Value[float](0)
        self.skin_tone_protection = Value[float](0)


class Lch(ProfileParamParser):
    def __init__(self) -> None:
        self.luminance: Final = LchAdjustment()
        self.chroma: Final = LchAdjustment()
        self.hue: Final = LchAdjustment()


class Grading(ProfileParamParser):
    def __init__(self) -> None:
        self.toning: Final = ColorToning()
        self.matte: Final = Matte()
        self.lch: Final = Lch()


class WhiteBalance(ProfileParamParser):
    def __init__(self) -> None:
        self.temperature: Final = Value[int](6504)
        self.tint: Final = Value[float](1)


class Colors(ProfileParamParser):
    def __init__(self) -> None:
        self.vibrance: Final = Value[float](0)
        self.chrome: Final = Value[float](0)
        self.grading: Grading = Grading()
        self.white_balance: Final = WhiteBalance()


class Grain(ProfileParamParser):
    def __init__(self) -> None:
        self.strength: Final = Value[int](0)


@unique
class NoiseReductionMode(ProfileParamEnum):
    AGGRESSIVE = "shalbi"
    CONSERVATIVE = "shal"


class NoiseReduction(ProfileParamParser):
    def __init__(self) -> None:
        self.mode: Final = Value[NoiseReductionMode](NoiseReductionMode.CONSERVATIVE)
        self.luminance: Final = Value[float](0)
        self.detail: Final = Value[float](100.0)
        self.chrominance: Final = Value[float](0)


class CaptureSharpening(ProfileParamParser):
    def __init__(self) -> None:
        self.radius: Final = Value[float](0)
        self.threshold: Final = Value[int](10)


class OutputSharpening(ProfileParamParser):
    def __init__(self) -> None:
        self.radius: Final = Value[float](0.75)
        self.threshold: Final = Value[int](20)
        self.amount: Final = Value[int](100)
        self.damping: Final = Value[int](0)
        self.iterations: Final = Value[int](30)


class Sharpening(ProfileParamParser):
    def __init__(self) -> None:
        self.capture: Final = CaptureSharpening()
        self.output: Final = OutputSharpening()


@unique
class DemosaicMethod(ProfileParamEnum):
    AMAZE = "amaze"
    AMAZE_BILINEAR = "amazebilinear"
    AMAZE_VNG4 = "amazevng4"
    RCD_BILINEAR = "rcdbilinear"
    RCD_VNG4 = "rcdvng4"
    DCB_BILINEAR = "dcbbilinear"
    DCB_VNG4 = "dcbvng4"
    LMMSE = "lmmse"


class Demosaic(ProfileParamParser):
    def __init__(self) -> None:
        self.algorithm: Final = Value[DemosaicMethod](DemosaicMethod.AMAZE)
        self.auto_threshold: Final = Value[bool](True)
        self.threshold: Final = Value[int](20)


class Contrast(ProfileParamParser):
    def __init__(self) -> None:
        self.local: Final = Value[float](0.0)


class Raw(ProfileParamParser):
    def __init__(self) -> None:
        self.demosaic: Final = Demosaic()
        self.black_points: Final = Value[tuple[int, int, int]]((0, 0, 0))


class Sigmoid(ProfileParamParser):
    def __init__(self) -> None:
        self.linear_grey18: Final = Value[float](0.1)
        self.slope: Final = Value[float](1.6)


class Curve(ProfileParamParser):
    def __init__(self) -> None:
        self.sigmoid: Final = Sigmoid()


class Tone(ProfileParamParser):
    def __init__(self) -> None:
        self.curve: Final = Curve()
        self.contrast: Final = Contrast()


class Details(ProfileParamParser):
    def __init__(self) -> None:
        self.sharpening: Final = Sharpening()
        self.noise_reduction: Final = NoiseReduction()
        self.grain: Final = Grain()


class ProfileParams(ProfileParamParser):
    def __init__(self) -> None:
        self.camera: Final = Camera()
        self.raw: Final = Raw()
        self.tone: Final = Tone()
        self.details: Final = Details()
        self.colors: Final = Colors()
