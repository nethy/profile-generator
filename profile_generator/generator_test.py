from unittest import TestCase
from unittest.mock import Mock, patch

from profile_generator import generator
from profile_generator.generator import (
    ConfigFileReadError,
    InvalidConfigFileError,
    NoConfigFileError,
    OutputDirCreationFailure,
    ProfileWriteError,
    TemplateFileReadError,
)
from profile_generator.schema import object_of, type_of


class ProfileGeneratorTest(TestCase):
    @patch("sys.argv", ["app.py", "one.json", "two.json"])
    def test_get_config_files_returns_config_files(self) -> None:
        self.assertEqual(["one.json", "two.json"], generator.get_config_files())

    @patch("sys.argv", ["app.py"])
    def test_get_config_files_raises_error_when_arguments_are_missing(self) -> None:
        self.assertRaises(NoConfigFileError, generator.get_config_files)

    @patch(
        "profile_generator.util.file.create_dir", lambda *xs: "/root/" + "/".join(xs)
    )
    def test_create_output_dir_raises_returns_created_dir_path(self) -> None:
        self.assertEqual("/root/profiles", generator.create_output_dir())

    @patch("profile_generator.util.file.create_dir")
    def test_create_output_dir_raises_error_when_cannot_create_dir(
        self, create_dir: Mock
    ) -> None:
        create_dir.side_effect = OSError

        self.assertRaises(OutputDirCreationFailure, generator.create_output_dir)

    @patch("profile_generator.util.file.read_file")
    @patch(
        "profile_generator.util.file.get_full_path", lambda *xs: "/root/" + "/".join(xs)
    )
    def test_get_profile_template_returns_template_file_content(
        self, read_file: Mock
    ) -> None:
        read_file.return_value = "file content"

        self.assertEqual("file content", generator.get_profile_template())
        read_file.assert_called_once_with("/root/templates/raw_therapee.pp3")

    @patch("profile_generator.util.file.read_file")
    def test_get_profile_template_raises_error_when_cannot_read_template_file(
        self, read_file: Mock
    ) -> None:
        read_file.side_effect = OSError

        self.assertRaises(TemplateFileReadError, generator.get_profile_template)

    @patch("profile_generator.util.file.read_file")
    def test_load_configuration_file_loads_configuration_files(
        self, read_file: Mock
    ) -> None:
        read_file.return_value = '{"a": 2}'
        schema = object_of(a=type_of(int))

        config = generator.load_configuration_file("config.json", schema)

        self.assertEqual({"a": 2}, config)
        read_file.assert_called_once_with("config.json")

    @patch("profile_generator.util.file.read_file")
    def test_load_configuration_file_raises_error_when_config_file_cannot_be_read(
        self, read_file: Mock
    ) -> None:
        schema = object_of(a=type_of(int))
        read_file.side_effect = OSError

        self.assertRaises(
            ConfigFileReadError,
            generator.load_configuration_file,
            "config.json",
            schema,
        )

    @patch("profile_generator.util.file.read_file")
    def test_load_configuration_file_raises_error_when_contains_variable_error(
        self, read_file: Mock
    ) -> None:
        read_file.return_value = '{"a": "$a"}'
        schema = object_of(a=type_of(str))

        self.assertRaises(
            InvalidConfigFileError,
            generator.load_configuration_file,
            "config.json",
            schema,
        )

    @patch("profile_generator.util.file.read_file")
    def test_load_configuration_file_raises_error_when_config_file_is_invalid(
        self, read_file: Mock
    ) -> None:
        read_file.return_value = '{"a": false}'
        schema = object_of(a=type_of(int))

        self.assertRaises(
            InvalidConfigFileError,
            generator.load_configuration_file,
            "config.json",
            schema,
        )

    @patch("profile_generator.util.file.read_file")
    def test_load_configuration_file_raises_error_when_config_file_is_invalid_json(
        self, read_file: Mock
    ) -> None:
        read_file.return_value = '{"a": false'
        schema = object_of(a=type_of(int))

        self.assertRaises(
            InvalidConfigFileError,
            generator.load_configuration_file,
            "config.json",
            schema,
        )

    @classmethod
    @patch("profile_generator.util.file.write_file")
    def test_generate_profile_writes_profile_into_file(cls, write_file: Mock) -> None:
        name = "profile_name"
        config = {"a": "1"}
        template = "{a}"
        output_dir = "dir"

        generator.generate_profile(name, config, lambda x: x, template, output_dir)

        write_file.assert_called_once_with("1", output_dir, name + ".pp3")

    @patch("profile_generator.util.file.write_file")
    def test_generate_profile_raises_error_when_write_failed(
        self, write_file: Mock
    ) -> None:
        name = "profile_name"
        config = {"a": "1"}
        template = "{a}"
        output_dir = "dir"
        write_file.side_effect = OSError

        self.assertRaises(
            ProfileWriteError,
            generator.generate_profile,
            name,
            config,
            lambda x: x,
            template,
            output_dir,
        )
