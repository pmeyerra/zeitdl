from datetime import datetime
from pathlib import Path

import click

from zeitdl.core import tasks
from zeitdl.types import Issue


@click.command()
@click.option(
    "--year",
    default=datetime.now().year,  # noqa: DTZ005
    type=int,
    help="Year of the issues to download.",
    show_default=True,
)
@click.option("--start-issue", required=True, type=int, help="Starting issue number.")
@click.option("--end-issue", required=True, type=int, help="Ending issue number.")
@click.option(
    "--credentials",
    default=Path("credentials.json"),
    type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    help="Path to the credentials file.",
    show_default=True,
)
@click.option(
    "--destination",
    default=Path("credentials.json").resolve(),
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Destination folder for downloaded files.",
    show_default=True,
)
def main(
    year: int,
    start_issue: int,
    end_issue: int,
    credentials: Path,
    destination: Path,
) -> None:
    """Download issues of Die Zeit."""
    issue_numbers = list(range(start_issue, end_issue + 1))
    issues = [Issue(num, year) for num in issue_numbers]

    credential_file = Path(credentials)

    destination_path = Path(destination).resolve()

    client = tasks.initialize_session(credential_file)

    for issue in issues:
        tasks.download_issue(client, issue, destination_path)
