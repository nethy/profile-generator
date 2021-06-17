import math

Color = list[float]
ColorMatrix = list[list[float]]

XYZ_TO_RGB = [
    [3.240969942, -1.537383178, -0.498610760],
    [-0.969243636, 1.875967502, 0.041555057],
    [0.055630080, -0.203976959, 1.056971514],
]

RGB_TO_XYZ = [
    [0.412390799, 0.357584339, 0.180480788],
    [0.212639006, 0.715168679, 0.072192315],
    [0.019330819, 0.119194780, 0.950532152],
]

D65_XYZ = [0.9504700, 1, 1.0888300]

LAB_F_SIGMA = 6 / 29
LAB_F_SIGMA_2 = 36 / 841
LAB_F_SIGMA_3 = 216 / 24389


def srgb_to_rgb(srgb: Color) -> Color:
    return list(map(gamma_inverse, srgb))


def rgb_to_srgb(rgb: Color) -> Color:
    return list(map(gamma, rgb))


def rgb_to_xyz(rgb: Color) -> Color:
    return multiply(RGB_TO_XYZ, rgb)


def xyz_to_rgb(xyz: Color) -> Color:
    return multiply(XYZ_TO_RGB, xyz)


def xyz_to_lab(xyz: Color) -> Color:
    x_ratio, y_ratio, z_ratio = [value / ref for value, ref in zip(xyz, D65_XYZ)]
    l = 116 * lab_f(y_ratio) - 16
    a = 500 * (lab_f(x_ratio) - lab_f(y_ratio))
    b = 200 * (lab_f(y_ratio) - lab_f(z_ratio))
    return [l, a, b]


def lab_to_xyz(lab: Color) -> Color:
    l, a, b = lab
    x_ref, y_ref, z_ref = D65_XYZ
    l_ref = (l + 16) / 116
    x = x_ref * lab_f_inverse(l_ref + a / 500)
    y = y_ref * lab_f_inverse(l_ref)
    z = z_ref * lab_f_inverse(l_ref - b / 200)
    return [x, y, z]


def lab_to_lch(lab: Color) -> Color:
    l, a, b = lab
    c = math.sqrt(a ** 2 + b ** 2)
    h = math.degrees(math.atan2(b, a))
    if h < 0:
        h += 360
    return [l, c, h]


def lch_to_lab(lch: Color) -> Color:
    l, c, h = lch
    a = c * math.cos(math.radians(h))
    b = c * math.sin(math.radians(h))
    return [l, a, b]


def lab_f(x: float) -> float:
    if x > LAB_F_SIGMA_3:
        return x ** (1 / 3)
    else:
        return x / (3 * LAB_F_SIGMA_2) + 4 / 29


def lab_f_inverse(x: float) -> float:
    if x > LAB_F_SIGMA:
        return x ** 3
    else:
        return 3 * LAB_F_SIGMA_2 * (x - 4 / 29)


def gamma_inverse(x: float) -> float:
    if x <= 0.04045:
        return max(0.0, x / 12.92)
    else:
        return min(1.0, ((x + 0.055) / 1.055) ** 2.4)


def gamma(x: float) -> float:
    if x <= 0.0031308:
        return max(0.0, 12.92 * x)
    else:
        return min(1.0, 1.055 * x ** (1 / 2.4) - 0.055)


def multiply(matrix: ColorMatrix, color: Color) -> Color:
    result = [0.0, 0.0, 0.0]
    for i in range(3):
        for j in range(3):
            result[i] += matrix[i][j] * color[j]
    return result
