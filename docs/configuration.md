# Configuration

### Table of content
* [Overview](#overview)
* [Templates](#templates)
* [Tone](#tone)
    * [Curve](#curve)
        * [Bezier](#bezier)
* [Raw](#raw)

## Overview

Configuration is a JSON object.
Every specified field is optional, but it is forbidden to use any other
to avoid typos.

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

The middle grey point, center of the S-curve.

<br/>

`strength`
|               |         |
| ---           | ---     |
| Type          | integer |
| Value range   | 0 - 100 |
| Default value | 0       |

Amount of contrast. 0 will produce a linear tone curve, while 100 results in a near
horizontal line around the middle grey point.

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
