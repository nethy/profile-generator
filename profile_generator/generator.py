import json
import os
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Any

from profile_generator.configuration.preprocessor import dot_notation, variable
from profile_generator.configuration.schema import Schema
from profile_generator.util import file

_PROFILES_DIR = "profiles"

_TEMPLATES_DIR = "templates"

_RAW_THERAPEE_TEMPLATE = "raw_therapee.pp3"


class NoConfigFileError(Exception):
    ...


def get_config_files() -> Sequence[str]:
    if len(sys.argv) < 2:
        raise NoConfigFileError

    return sys.argv[1:]


class OutputDirCreationFailure(Exception):
    ...


def create_output_dir() -> str:
    try:
        return file.create_dir(_PROFILES_DIR)
    except OSError as exc:
        raise OutputDirCreationFailure from exc


class TemplateFileReadError(Exception):
    ...


def get_profile_template() -> str:
    try:
        path = file.get_full_path(_TEMPLATES_DIR, _RAW_THERAPEE_TEMPLATE)
        return file.read_file(path)
    except OSError as exc:
        raise TemplateFileReadError from exc


class ConfigFileReadError(Exception):
    ...


class InvalidConfigFileError(Exception):
    def __init__(self, errors: Iterable[Exception]):
        super().__init__()
        self.errors = errors


def load_configuration_file(file_name: str, schema: Schema) -> dict[str, Any]:
    try:
        raw_config = file.read_file(file_name)
        cfg_template = json.loads(raw_config)
        cfg_template, variable_errors = variable.replace(cfg_template)
        if len(variable_errors) > 0:
            raise InvalidConfigFileError(variable_errors)
        cfg_template = dot_notation.expand(cfg_template)
        error = schema.validate(cfg_template)
        if error is not None:
            raise InvalidConfigFileError([error])
        return cfg_template
    except OSError as exc:
        raise ConfigFileReadError from exc
    except JSONDecodeError as exc:
        raise InvalidConfigFileError([]) from exc


@dataclass
class ProfileWriteError(Exception):
    filename: str


def generate_profile(
    name: str,
    config: Mapping[str, Any],
    marshall: Callable[[Mapping[str, Any]], Mapping[str, str]],
    template: str,
    output_dir: str,
) -> None:
    try:
        output_filename = f"{name}.pp3"
        template_args = marshall(config)
        output = template.format(**template_args)
        file.write_file(output, output_dir, output_filename)
    except Exception as exc:
        filename = os.path.normpath(os.path.join(output_dir, output_filename))
        raise ProfileWriteError(filename) from exc
