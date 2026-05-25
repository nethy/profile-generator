import logging
import os
import sys
from collections.abc import Callable, Mapping
from typing import Any

from profile_generator import configuration, integration, log

from . import generator
from .generator import (
    ConfigFileReadError,
    InvalidConfigFileError,
    NoConfigFileError,
    OutputDirCreationFailure,
    ProfileWriteError,
    TemplateFileReadError,
)


def main() -> None:
    log.init()
    console_logger = log.get_console_logger()

    try:
        output_dir = generator.create_output_dir()
        template = generator.get_profile_template()
        for cfg_file_name in generator.get_config_files():
            logging.info("processing configuration file: %s", cfg_file_name)
            process_config_file(cfg_file_name, template, output_dir)
    except NoConfigFileError:
        console_logger.error("No config file provided.")
        sys.exit(1)
    except OutputDirCreationFailure:
        console_logger.error("Target directory creation failure", exc_info=True)
        sys.exit(1)
    except TemplateFileReadError:
        console_logger.error("Template file read failure", exc_info=True)
        sys.exit(1)


def process_config_file(cfg_path: str, template: str, output_dir: str) -> None:
    logger = logging.getLogger(__name__)
    console_logger = log.get_console_logger()
    try:
        cfg_name = os.path.splitext(os.path.basename(cfg_path))[0]
        cfg_template = generator.load_configuration_file(cfg_path, integration.SCHEMA)
        is_partial = cfg_template.get("partial", False)
        cfg = configuration.create_from_template(cfg_template)
        create_profile_content = generator.get_create_profile_content(
            template, integration.GENERATOR
        )
        _persist_profiles(cfg_name, cfg, create_profile_content, is_partial, output_dir)
    except ConfigFileReadError:
        console_logger.error("%s: file read failure", cfg_path)
    except InvalidConfigFileError as exc:
        console_logger.error("%s: invalid configuration", cfg_path)
        logger.error(exc.errors)


def _persist_profiles(
    cfg_name: str,
    cfg: configuration.Configuration,
    create_profile_content: Callable[[Mapping[str, Any], bool], str],
    is_partial: bool,
    output_dir: str,
) -> None:
    is_single = len(cfg) == 1
    for name, body in cfg.items():
        content = create_profile_content(body, is_partial)
        if is_single:
            name = cfg_name
            cfg_output_dir = output_dir
        else:
            cfg_output_dir = os.path.join(output_dir, cfg_name)
        _persist_profile(cfg_name, name, content, cfg_output_dir)


def _persist_profile(
    filename: str, cfg_name: str, content: str, output_dir: str
) -> None:
    logger = log.get_console_logger()
    try:
        generator.persist_profile(cfg_name, content, output_dir)
        if logger.isEnabledFor(logging.INFO):
            log_name = f"{filename} / {cfg_name}"
            if filename == cfg_name:
                log_name = cfg_name
            logger.info("Profile has been created: %s", log_name)
    except ProfileWriteError as exc:
        logger.error("%s: file write failure", exc.filename)
