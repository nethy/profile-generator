# Configuration

### Table of content
* [Overview](#overview)
* [Templates](#templates)
* [Tone](#tone)
    * [Curve](#curve)
        * [Bezier](#bezier)
* [Details](#details)
    * [Sharpening](#sharpening)
        * [Capture](#capture)
        * [Output](#output)
    * [Noise reduction](#noise-reduction)
* [Raw](#raw)

## Overview

Configuration is a JSON object.
Every specified field is optional, but it is forbidden to use any other
to avoid typos.

Dot notation also supported, so you can write something like `tone.curve.bezier.`
instead of nesting each object. It is very useful for setting only one parameter.

## Templates

```json
{
    "defaults": <configuration>,
    "templates": [
        {
            <template_name>: <configuration>,
            ...
        },
        ...
    ]
}
```

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

### Curve

#### Bezier

Field name: `bezier`

Creates an S-cruve around the middle grey point with the given strength.

**Parameters**

`middle_grey`
|               |                    |
| ---           | ---                |
| Type          | [integer, integer] |
| Value range   | 0 - 255            |
| Default value | [92, 119]          |

x, y coordinates of the middle grey point, center of the S-curve.

`strength`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 0       |

Amount of contrast. 0 will produce a linear tone curve, while 100 results in a near
horizontal line around the middle grey point.

`weights`
|               |                |
| ---           | ---            |
| Type          | [float, float] |
| Value range   | 0.0 - 5.0      |
| Default value | [2.0, 1.0]     |

Shadow and the highlight point weights of the tone curve. Determines how gradual or
steep the curve is. Smaller value provides flatter, while larger value provides more
steeper curve.
Using higher weight for shadow helps to increase the contrast of the image, while
highlights can be preserved as much as possible.

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
| ---           | ---         |
| Type          | boolean     |
| Value range   | true, false |
| Default value | false       |

Enables noise reduction - it will automatically reduce chorminance noise.

`strength`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 10      |

Strength of the luminance noise reduction.

`median`
|               |             |
| ---           | ---         |
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
| ---           | ---                 |
| Type          | [string]            |
| Value range   | "RCD+VNG4", "LMMSE" |
| Default value | "RCD+VNG4"          |

Demosaicing algorithm.
