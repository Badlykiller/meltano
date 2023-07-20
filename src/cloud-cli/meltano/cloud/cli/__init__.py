"""Meltano Cloud CLI."""

from __future__ import annotations

import click
from structlog import get_logger

from meltano.cloud.api import MeltanoCloudError
from meltano.cloud.cli import (  # noqa: WPS235
    config,
    deployment,
    docs,
    history,
    job,
    login,
    logs,
    project,
    run,
    schedule,
)
from meltano.cloud.cli.base import cloud

logger = get_logger()

cloud.add_command(config.config)  # type: ignore[attr-defined]
cloud.add_command(docs.docs)  # type: ignore[attr-defined]
cloud.add_command(deployment.deployment_group)  # type: ignore[attr-defined]
cloud.add_command(history.history)  # type: ignore[attr-defined]
cloud.add_command(job.job_group)  # type: ignore[attr-defined]
cloud.add_command(login.login)  # type: ignore[attr-defined]
cloud.add_command(login.logout)  # type: ignore[attr-defined]
cloud.add_command(logs.logs)  # type: ignore[attr-defined]
cloud.add_command(project.project_group)  # type: ignore[attr-defined]
cloud.add_command(run.run)  # type: ignore[attr-defined]
cloud.add_command(schedule.schedule_group)  # type: ignore[attr-defined]


def main() -> int:
    """Run the Meltano Cloud CLI.

    Returns:
        The CLI exit code.
    """
    try:
        cloud()  # type: ignore[misc]
    except MeltanoCloudError as e:
        click.secho(e.response.reason, fg="red")
        return 1
    except Exception as e:
        logger.error("An unexpected error occurred.", exc_info=e)
        return 1
    return 0