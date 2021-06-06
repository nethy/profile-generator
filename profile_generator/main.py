import concurrent.futures
import logging
import sys
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import Future
from typing import Any

from profile_generator import configuration, generator, integration, log
from profile_generator.configuration.configuration import Configuration
from profile_generator.generator import (
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


def process_config_file(cfg_file_name: str, template: str, output_dir: str) -> None:
    logger = logging.getLogger(__name__)
    console_logger = log.get_console_logger()
    try:
        cfg_template = generator.load_configuration_file(
            cfg_file_name, integration.SCHEMA
        )
        cfg = configuration.create_from_template(cfg_template)
        creators = _execute_creators(cfg, template)
        persisters = _execute_persisters(creators, output_dir)
        concurrent.futures.wait(persisters)
    except ConfigFileReadError:
        console_logger.error("%s: file read failure", cfg_file_name)
    except InvalidConfigFileError as exc:
        console_logger.error("%s: invalid configuration", cfg_file_name)
        logger.error(exc.errors)


def _execute_creators(cfg: Configuration, template: str) -> Iterable[Future]:
    with concurrent.futures.ProcessPoolExecutor() as process_pool:
        return [
            process_pool.submit(
                _create_profile_content,
                name,
                template,
                body,
                integration.CONFIGURATION_SCHEMA.process,
            )
            for name, body in cfg.items()
        ]


def _create_profile_content(
    name: str,
    template: str,
    cfg: Mapping[str, Any],
    marshall: Callable[[Any], Mapping[str, str]],
) -> tuple[str, str]:
    logger = logging.getLogger(__name__)
    logger.info("Creating profile: %s", name)
    return generator.create_profile_content(name, template, cfg, marshall)


def _execute_persisters(
    creators: Iterable[Future], output_dir: str
) -> Iterable[Future]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as thread_pool:
        return [
            thread_pool.submit(
                _persist_profile,
                *creator.result(),
                output_dir,
            )
            for creator in concurrent.futures.as_completed(creators)
        ]


def _persist_profile(name: str, content: str, output_dir: str) -> None:
    console_logger = log.get_console_logger()
    try:
        generator.persist_profile(name, content, output_dir)
        console_logger.info("Profile has been created: %s", name)
    except ProfileWriteError as exc:
        console_logger.error("%s: file write failure", exc.filename)
