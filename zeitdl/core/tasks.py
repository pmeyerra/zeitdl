from pathlib import Path

import httpx
import structlog

from zeitdl import service
from zeitdl.core import zeitonline
from zeitdl.types import Issue

logger = structlog.get_logger()


def download_issue(client: httpx.Client, issue: Issue, destination: Path) -> Path:
    """Download one Zeit issue to from Zeit Online and save it to disk.

    Args:
        client: ``httpx.Client`` to use for the download. Must be logged into
            Zeit Online.
        issue: issue (number and year) to download
        destination: destination folder where the PDF file will be saved

    Returns:
        path to the downloaded file
    """
    logger.info("Downloading issue", issue=issue, destination=destination)
    issue_page_url = zeitonline.get_issue_page_url(client, issue)
    download_url = zeitonline.get_download_url(client, issue_page_url)
    return service.download_file(client, download_url, destination, overwrite=False)


def initialize_session(credential_file: Path) -> httpx.Client:
    """Initialize a session to Zeit Online and authenticate.

    Args:
        credential_file: path to the JSON file containing the credentials

    Returns:
        initialized ``httpx.Client`` session
    """
    logger.debug("Initializing session", credential_file=credential_file)
    credentials = service.load_credentials_from_file(credential_file)
    client = service.get_client()
    return zeitonline.login(client, credentials)
