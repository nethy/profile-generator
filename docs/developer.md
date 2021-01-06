# Developer guide

Table of content
* [Requirements](#requirements)
* [Development tools](#development-tools)
* [Project structure](#project-structure)
* [Architecture](#architecture)
* [Development environment setup](#development-environment-setup)
    - [Visual Studio Code](#visual-studio-code)


## Requirements

There is no runtime dependency.
For development you can install the tools by the requirements file.

1. Create your virtual environment and/or activate
    ```
    python -m venv venv
    . venv/bin/activate (or venv/Scripts/activate)
    ```

1. Install development depencencies
    ````
    pip install -r requirements-dev.txt
    ````

## Development tools

Under the `ci` folder, there is couple of scripts to help run linters and formatters.

`ci/check_all.sh` will check everything which is necessary to keep the code as good
shape as possible. Make sure it does not report any issue.

If a linter reports false-positive, feel free to modify it's configuration, but please
exmplain later in the pull request what was the reason behind that.

## Project structure

| Directory         | Description              |
| ---               | ---                      |
| profile_generator | main python package      |
| ci                | tools for code checks    |
| docs              | documentations           |
| templates         | output profile templates |
| log               | logs                     |

## Architecture

### Domain elements
* **profile configuration template** - input artifact, this will be converted to
  profile configurations
* **profile configuration** - set of parameters, mapped to a name
* **profile template** - template for the profiles
* **profile template arguments** - profile template specific parameters,
  synthetized from the profile configurations
* **profile** - output artifact, each profile configuration produces a profile
* **feature** - computational logic, which process a part of profile configuration,
  but their implementation is independent from the domain language

### Configuration

Creates profile configurations form profile configuration template and validates.

### Profile

Handle profile configurations over to features and combines results in to single
set of profile template arguments.

### Feature

Strutured place of features. APIs must be independent from domain elements,
integration with the configuration and profile packages is done by shims.

### Integration

As each feature defines it's own profile configuration schema and profile template
arguments, this package is combines features together so they can treated like a
single entity.

## Development environment setup

### Visual Studio Code

#### .env file
````
PYTHONPATH="profile_generator"
MYPYPATH="profile_generator"
````

#### workspace settings
```json
{
  "python.pythonPath": "venv\\Scripts\\python.exe",
  "python.testing.unittestEnabled": true,
  "python.testing.unittestArgs": [
    "-v",
    "-s",
    "${env:PYTHONPATH}",
    "-p",
    "*_test.py"
  ],
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackPath": "black",
  "python.formatting.blackArgs": [],
  "python.sortImports.path": "isort",
  "python.sortImports.args": [
    "--profile",
    "black",
    "--src",
    "${env:PYTHONPATH}"
  ],
  "python.linting.enabled": true,
  "python.linting.pylintPath": "pylint",
  "python.linting.pylintEnabled": true,
  "python.linting.mypyPath": "mypy",
  "python.linting.mypyEnabled": true,
  "python.linting.mypyArgs": [
    "--disallow-untyped-defs",
    "--disallow-incomplete-defs",
    "--show-column-numbers",
    "--package ${env:PYTHONPATH}"
  ],
  "[python]": {
    "editor.tabSize": 4,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true,
    }
  }
}
```

