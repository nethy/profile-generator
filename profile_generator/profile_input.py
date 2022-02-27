from dataclasses import dataclass
from enum import Enum, unique


@dataclass
class Camera:
    resolution: float = 16.0


@dataclass
class HCL:
    hue: float = 0.0
    chromacity: float = 0.0
    luminance: float = 0.0


@dataclass
class Grading:
    base: HCL = HCL()
    shadow: HCL = HCL()
    midtone: HCL = HCL()
    highlight: HCL = HCL()


@dataclass
class HueInput:
    red: float = 0.0
    yellow: float = 0.0
    green: float = 0.0
    cyan: float = 0.0
    blue: float = 0.0
    magenta: float = 0.0


@dataclass
class HSL:
    hue: HueInput = HueInput()
    saturation: HueInput = HueInput()
    luminance: HueInput = HueInput()


@unique
class ColorProfile(Enum):
    ACES_P0 = "ACESp0"
    ACES_P1 = "ACESp1"
    PRO_PHOTO = "ProPhoto"
    REC_2020 = "Rec2020"
    SRGB = "sRGB"


@dataclass
class Color:
    vibrance: float = 0.0
    chrome: float = 0.0
    grading: Grading = Grading()
    hsl: HSL = HSL()
    profile: ColorProfile = ColorProfile.PRO_PHOTO


@unique
class NoiseReductionMode(Enum):
    AGGRESSIVE = "shalbi"
    CONSERVATIVE = "shal"


@dataclass
class NoiseReduction:
    mode: NoiseReductionMode = NoiseReductionMode.CONSERVATIVE
    luminance: float = 0.0
    chrominance: float = 0.0


@dataclass
class CaptureSharpening:
    radius: float = 0.0
    threshold: int = 10


@dataclass
class OutputSharpening:
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
class Demosaic:
    method: DemosaicMethod = DemosaicMethod.AMAZE
    auto_threshold: bool = True
    threshold: int = 20


@dataclass
class Contrast:
    grey18: float = 90.0
    strength: float = 1.6
    linear_profile: bool = True
    local: float = 0.0


@dataclass
class ProfileInput:
    camera: Camera = Camera()
    color: Color = Color()
    noise_reduction: NoiseReduction = NoiseReduction()
    demosaic: Demosaic = Demosaic()
    contrast: Contrast = Contrast()
