# Introduction

This is a tool for defining and combining multiple profiles for
[RawTherapee](http://rawtherapee.com/).
If you want multiple conrast presets (e.g. neutral, vivid) for different cameras -
with different sensor characteristics, you can just set parameters for each
and this tool will combine them into multiple profiles.

*Example*

```json
{
  "templates": [
    { "settings": {
        "Camera1": {
          "tone.contrast.bezier.grey": { "x": 98, "y": 119}
        },
        "Camera2": {
          "tone.contrast.bezier.grey": { "x": 83, "y": 119}
        }
      }
    },
    { "settings": {
        "Soft": {
          "tone.contrast.bezier.strength": 10
        },
        "Medium": {
          "tone.contrast.bezier.strength": 20
        },
        "Strong": {
          "tone.contrast.bezier.strength": 30
        }
      }
    }
  ]
}
```

With the above configuration the generated profiles will be
* Camera1_Soft.pp3
* Camera1_Medium.pp3
* Camera1_Strong.pp3
* Camera2_Soft.pp3
* Camera2_Medium.pp3
* Camera2_Strong.pp3

## Usage

Download and install Python version 3.9 or newer at https://python.org

To execute the tool use `run.sh` or `run.cmd` wrappers and provide
one or more configuration files as arguments.

```
run config.json ...
```

For the available configuration options and format,
read the [configuration documentation](docs/configuration.md).

## Error report

In case of unexpected operation, please open an issue with the following informations:
* description of expected operation
* description of actual operation
* python version - `python --version`
* attach log file - `log/profiles_generator.log`
* attach configuration files

## Feature request & contribution

By opening new issue, you can request new features.
Please, spend some time to search in open and closed issues to avoid duplications.
If you've found a closed issue, you can re-open and share your new ideas that wasn't
discussed.

I'm also happy to accept implementation contributions.
Before sending merge request, please create an issue to discuss it beforehand to avoid
major change requests during code review.

For further informations consult with the [developer documentation](docs/developer.md).
