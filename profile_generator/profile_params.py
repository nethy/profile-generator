from abc import ABC
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any


class NoneSafe(ABC):
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __value is not None:
            super().__setattr__(__name, __value)


@dataclass
class Camera(NoneSafe):
    resolution_mp: float = 16.0


@dataclass
class Hcl(NoneSafe):
    hue: float = 0.0
    chromacity: float = 0.0
    luminance: float = 0.0


@dataclass
class Grading:
    base: Hcl = Hcl()
    shadow: Hcl = Hcl()
    midtone: Hcl = Hcl()
    highlight: Hcl = Hcl()


@dataclass
class HueParams(NoneSafe):
    red: float = 0.0
    yellow: float = 0.0
    green: float = 0.0
    cyan: float = 0.0
    blue: float = 0.0
    magenta: float = 0.0


@dataclass
class Hsl:
    hue: HueParams = HueParams()
    saturation: HueParams = HueParams()
    luminance: HueParams = HueParams()


@unique
class ColorProfile(Enum):
    ACES_P0 = "ACESp0"
    ACES_P1 = "ACESp1"
    PRO_PHOTO = "ProPhoto"
    REC_2020 = "Rec2020"
    SRGB = "sRGB"


@dataclass
class Color(NoneSafe):
    vibrance: float = 0.0
    chrome: float = 0.0
    grading: Grading = Grading()
    hsl: Hsl = Hsl()
    profile: ColorProfile = ColorProfile.PRO_PHOTO


@unique
class NoiseReductionMode(Enum):
    AGGRESSIVE = "shalbi"
    CONSERVATIVE = "shal"


@dataclass
class NoiseReduction(NoneSafe):
    mode: NoiseReductionMode = NoiseReductionMode.CONSERVATIVE
    luminance: float = 0.0
    chrominance: float = 0.0


@dataclass
class CaptureSharpening(NoneSafe):
    radius: float = 0.0
    threshold: int = 10


@dataclass
class OutputSharpening(NoneSafe):
    radius: float = 0.75
    threshold: int = 20
    amount: int = 100
    damping: int = 0
    iterations: int = 30


@dataclass
class Sharpening:
    capture: CaptureSharpening = CaptureSharpening()
    output: OutputSharpening = OutputSharpening()


@unique
class DemosaicMethod(Enum):
    AMAZE = "amaze"
    AMAZE_VNG4 = "amazevng4"
    DCB_VNG4 = "dcbvng4"
    RCD_VNG4 = "rcdvng4"
    LMMSE = "lmmse"


@dataclass
class Demosaic(NoneSafe):
    method: DemosaicMethod = DemosaicMethod.AMAZE
    auto_threshold: bool = True
    threshold: int = 20


@dataclass
class Contrast(NoneSafe):
    grey18: float = 90.0
    strength: float = 1.6
    linear_profile: bool = True
    local: float = 0.0


@dataclass
class ProfileParams:
    camera: Camera = Camera()
    color: Color = Color()
    noise_reduction: NoiseReduction = NoiseReduction()
    sharpening: Sharpening = Sharpening()
    demosaic: Demosaic = Demosaic()
    contrast: Contrast = Contrast()
