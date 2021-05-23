import os
from functools import reduce
from typing import Any

Configuration = dict[str, dict[str, Any]]

_DEFAULT_NAME = "Default"


def create_from_template(template: dict[str, Any]) -> Configuration:
    defaults = template.get("defaults", {})
    templates = template.get("templates", [])

    return reduce(_merge_template, templates, {_DEFAULT_NAME: defaults})


def _merge_template(
    configuration: Configuration, template: Configuration
) -> Configuration:
    settings = _get_settings(template)
    if len(settings) == 0:
        return configuration

    is_directory = _is_directory(template)

    merged = {
        _merge_name(cfg_name, template_name, is_directory): _merge_dicts(
            cfg_body, template_body
        )
        for cfg_name, cfg_body in configuration.items()
        for template_name, template_body in settings.items()
    }
    if _is_optional(template) and _DEFAULT_NAME not in configuration:
        merged = {**configuration, **merged}
    return merged


def _merge_name(cfg_name: str, template_name: str, is_directory: bool) -> str:
    directory, name = os.path.dirname(cfg_name), os.path.basename(cfg_name)
    if is_directory:
        directory = "/".join(filter(None, (directory, template_name)))
    else:
        if name == _DEFAULT_NAME:
            name = template_name
        else:
            name = name + "_" + template_name
    return "/".join(filter(None, (directory, name)))


def _merge_dicts(base: dict[str, Any], overrider: dict[str, Any]) -> dict[str, Any]:
    merged = base.copy()
    for key, value in overrider.items():
        if isinstance(value, dict):
            default_value = merged.get(key, {})
            merged[key] = _merge_dicts(default_value, value)
        else:
            merged[key] = value
    return merged


def _get_settings(template: dict[str, Any]) -> dict[str, Any]:
    return template.get("settings", {})


def _is_optional(template: dict[str, Any]) -> bool:
    return template.get("optional", False)


def _is_directory(template: dict[str, Any]) -> bool:
    return template.get("directory", False)
