# Configuration

### Table of content
* [Overview](#overview)
* [Templates](#templates)
* [Tone](#tone)
    * [Contrast](#contrast)
        * [Local](#local)
    * [Curve](#curve)
        * [Bezier](#bezier)
        * [Sigmoid](#sigmoid)
* [Details](#details)
    * [Sharpening](#sharpening)
        * [Capture](#capture)
        * [Output](#output)
    * [Noise reduction](#noise-reduction)
* [Raw](#raw)
* [Colors](#colors)
    * [HSL](#hsl)

## Overview

Configuration is a JSON object.
Every specified field is optional, but it is forbidden to use any other
to avoid typos.

Dot notation also supported, so you can write something like `tone.curve.bezier`
instead of nesting each object. It is very useful for setting only one parameter.

## Templates

```json
{
    "variables": {
        ...
    },
    "defaults": <configuration>,
    "templates": [
        {
            "optional": true,
            "directory": true,
            "settings": {
                <template_name>: <configuration>,
                ...
            }
        },
        ...
    ]
}
```

`variables`: variables, that can be referenced rest of the template as `$<variable_name>`.

`settings`: template names and it's configuration

`optional`: if a template is optional, then profiles will be created with and
without it. Example: `T1` and `T2` are templates and `T2` is optional, then
`T1` and `T1_T2` profiles will be created.
Default value is `false`.

`directory`: template will be a sub-directory instead. Each template represents
a directory level.

Configuration templates are described in the `templates` field. Each template will be
combined with predecessing ones.

*Example:*
```json
{
    "templates": [
        {
            "I": { ... },
            "II": { ... }
        },
        {
            "A": { ... },
            "B": { ... }
        },
        {
            "1": { ... },
            "2": { ... }
        }
    ]
}
```

Above configuration will produce the following profiles:
* I-A-1
* I-A-2
* I-B-1
* I-B-2
* II-A-1
* II-A-2
* II-B-1
* II-B-2

Templates will be merged recusively, and same parameters will be overwritten.
By the `defaults` field, you can provide a configuration which will serve as a
base template.
If `templates` is not provided or empty, a single **Default** profile will be created.

Content of the configurations are specified in their own chapters.

## Tone

Field name: `tone`

These parameters are related to the image tone, like exposure or contrast.

### Contrast

Field name: `contrast`

**Parameters**

|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 0       |

Increase the local contrast.

### Curve

Field name: `curve`

#### Bezier

Field name: `bezier`

Creates an S-cruve around the middle grey point with the given strength.

**Parameters**

`grey.x`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 255 |
| Default value | 92      |

x coordinate of the middle grey point, center of the S-curve.

`grey.y`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 255 |
| Default value | 119      |

y coordinate of the middle grey point, center of the S-curve.

`strength`
|               |             |
| ---           | ---         |
| Type          | float       |
| Value range   | 0.0 - 100.0 |
| Default value | 0           |

Amount of contrast. 0 will produce a linear tone curve, while 100 results in a near
vertical line around the middle grey point.

`weights`
|               |                |
| ---           | ---            |
| Type          | [float, float] |
| Value range   | 0.0 - 5.0      |
| Default value | [1.0, 1.0]     |

Shadow and the highlight point weights of the tone curve. Determines how gradual or
steep the curve is. Smaller value provides flatter, while larger value provides more
steeper curve.
Using higher weight for shadow helps to increase the contrast of the image, while
highlights can be preserved as much as possible.

#### Sigmoid

Field name: `sigmoid`

Creates an S-cruve around the middle grey point with the given strength.

**Parameters**

`neutral5`
|               |                             |
| ---           | ---                         |
| Type          | [integer, integer, integer] |
| Value range   | 16 - 240                    |
| Default value | [90, 90, 90]                |

RGB value of the `Neutral5` patch of a color checker card.

`exposure_compensation`
|               |            |
| ---           | ---        |
| Type          | float      |
| Value range   | -2.0 - 2.0 |
| Default value | 0.0        |

Middle grey adjustment via expsure values.

`gamma`
|               |             |
| ---           | ---         |
| Type          | float       |
| Value range   | 1.0 - 5.0   |
| Default value | 0           |

Amount of contrast. 1.0 will produce a linear tone curve.
For portraits use 1.7-1.8, and landscapes around 2.0-2.2.

`matte_effect`
|               |             |
| ---           | ---         |
| Type          | boolean     |
| Value range   | true, false |
| Default value | false       |

Shrinks the dynamic range of the tone curve, to simulate faded look.


## Detials

Field name: `details`

### Sharpening

Field name: `sharpening`

#### Capture

Field name: `capture`

Enhance image details via caputre sharpening.

**Parameters**

`enabled`
|               |             |
| ---           | ---         |
| Type          | boolean     |
| Value range   | true, false |
| Default value | false       |

#### Output

Field name: `output`

Applies sharpening on the image using RL-Deconvolution algorithm.

**Parameters**

`enabled`
|               |             |
| ---           | ---         |
| Type          | boolean     |
| Value range   | true, false |
| Default value | false       |

`threshold`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 200 |
| Default value | 20      |

`radius`
|               |           |
| ---           | ---       |
| Type          | float     |
| Value range   | 0.4 - 2.5 |
| Default value | 0.75      |

`amount`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 100     |

`damping`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 0       |

`iterations`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 5 - 100 |
| Default value | 30      |


### Noise reduction

Field name: `noise_reduction`

Reduce noise.

**Parameters**

`enabled`
|               |             |
|---------------|-------------|
| Type          | boolean     |
| Value range   | true, false |
| Default value | false       |

Enables noise reduction - it will automatically reduce chorminance noise.

`strength`
|               |         |
|---------------|---------|
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 10      |

Strength of the luminance noise reduction.

`median`
|               |             |
|---------------|-------------|
| Type          | boolean     |
| Value range   | true, false |
| Default value | false       |

Applies median fitler to clean up noise pattern, at the cost of softening
the whole image.

## Raw

Field name: `raw`

Raw conversion details.

**Parameters**

`demosaic`
|               |                     |
|---------------|---------------------|
| Type          | string              |
| Value range   | "DCB+VNG4", "LMMSE" |
| Default value | "DCB+VNG4"          |

Demosaicing algorithm.


## Colors

Field name: `colors`

Colors related adjustments.

**Parameters**

`vibrance`
|               |            |
|---------------|------------|
| Type          | integer    |
| Value range   | -100 - 100 |
| Default value | 0          |

Adjust the vibrance of the image.

`skin_tone_protection`
|               |         |
|---------------|---------|
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 0       |

Dimming the vibrance strength in skin tones.


### HSL

Field name: `hsl`

Hue, saturation and luminance adjustments.

`hue`, `saturation`, `luminance`

`red`, `yellow`, `green`, `cyan`, `blue`, `magenta`
|               |         |
|---------------|---------|
| Type          | integer |
| Value Range   | -7 - 7  |
| Default Value | 0       |
