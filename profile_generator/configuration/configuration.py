from functools import reduce
from typing import Any

Configuration = dict[str, dict[str, Any]]


def create_from_template(template: dict[str, Any]) -> Configuration:
    defaults = template.get("defaults", {})
    templates = template.get("templates", [])

    if len(templates) == 0:
        return {"Default": defaults}

    first_template, *rest_templates = templates
    first_cfg = _merge_first_template(defaults, first_template)
    return reduce(_merge_template, rest_templates, first_cfg)


def _merge_first_template(
    defaults: dict[str, Any], template: Configuration
) -> Configuration:
    return {
        name: _merge_dicts(defaults, body)
        for name, body in _get_settings(template).items()
    }


def _merge_template(
    configuration: Configuration, template: Configuration
) -> Configuration:
    merged = {
        cfg_name + "_" + template_name: _merge_dicts(cfg_body, template_body)
        for cfg_name, cfg_body in configuration.items()
        for template_name, template_body in _get_settings(template).items()
    }
    if _get_optional(template):
        merged = {**configuration, **merged}
    return merged


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
    return template["settings"]


def _get_optional(template: dict[str, Any]) -> bool:
    return template["optional"]
