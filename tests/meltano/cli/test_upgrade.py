import yaml
import pytest
from unittest.mock import Mock, patch

from asserts import assert_cli_runner
from meltano.cli import cli


class TestCliUpgrade:
    def test_upgrade(self, cli_runner):
        result = cli_runner.invoke(cli, ["upgrade"])
        assert_cli_runner(result)

    def test_upgrade_skip_package(self, cli_runner):
        result = cli_runner.invoke(cli, ["upgrade", "--skip-package"])
        assert_cli_runner(result)

    def test_upgrade_package(self, cli_runner):
        result = cli_runner.invoke(cli, ["upgrade", "package"])
        assert_cli_runner(result)

    def test_upgrade_files(
        self, session, project, cli_runner, config_service, plugin_settings_service
    ):
        result = cli_runner.invoke(cli, ["upgrade", "files"])
        assert_cli_runner(result)

        assert "Nothing to update" in result.output

        result = cli_runner.invoke(cli, ["add", "files", "dbt"])
        assert_cli_runner(result)

        # Don't update file if unchanged
        file_path = project.root_dir("transform/profile/profiles.yml")
        file_content = file_path.read_text()

        result = cli_runner.invoke(cli, ["upgrade", "files"])
        assert_cli_runner(result)

        assert "Updating 'dbt' files in project..." in result.output
        assert "Nothing to update" in result.output
        assert file_path.read_text() == file_content

        # Update file if changed
        file_path.write_text("Overwritten!")

        result = cli_runner.invoke(cli, ["upgrade", "files"])
        assert_cli_runner(result)

        assert "Updated transform/profile/profiles.yml" in result.output
        assert file_path.read_text() == file_content

        # Don't update file if unchanged
        result = cli_runner.invoke(cli, ["upgrade", "files"])
        assert_cli_runner(result)

        assert "Nothing to update" in result.output
        assert file_path.read_text() == file_content

        # Don't update file if automatic updating is disabled
        result = cli_runner.invoke(
            cli,
            [
                "config",
                "--plugin-type",
                "files",
                "dbt",
                "set",
                "update.transform/profile/profiles.yml",
                "false",
            ],
        )
        assert_cli_runner(result)

        file_path.write_text("Overwritten!")

        result = cli_runner.invoke(cli, ["upgrade", "files"])
        assert_cli_runner(result)

        assert "Nothing to update" in result.output
        assert file_path.read_text() != file_content

        # Update file if automatic updating is enabled
        result = cli_runner.invoke(
            cli,
            [
                "config",
                "--plugin-type",
                "files",
                "dbt",
                "set",
                "update.transform/dbt_project.yml",
                "true",
            ],
        )
        assert_cli_runner(result)

        result = cli_runner.invoke(cli, ["upgrade", "files"])
        assert_cli_runner(result)

        assert "Updated transform/dbt_project.yml" in result.output

        file_path = project.root_dir("transform/dbt_project.yml")
        assert "This file is managed by the 'dbt' file bundle" in file_path.read_text()

    def test_upgrade_database(self, cli_runner):
        result = cli_runner.invoke(cli, ["upgrade", "database"])
        assert_cli_runner(result)

    def test_upgrade_models(self, cli_runner):
        result = cli_runner.invoke(cli, ["upgrade", "models"])
        assert_cli_runner(result)