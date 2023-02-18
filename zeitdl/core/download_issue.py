import logging
from pathlib import Path

import requests

from zeitdl import service
from zeitdl.core import zeitonline
from zeitdl.types import Issue

logger = logging.getLogger(__name__)


def download_issue(sess: requests.Session, issue: Issue, destination: Path):
    """
    Download one Zeit issue to from Zeit Online and save it to disk.

    Args:
        sess: `requests.Session` to use for the download. Must be logged into
            Zeit Online.
        issue: issue (number and year) to download
        destination: destination folder where the PDF file will be saved

    Returns:
        path to the downloaded file
    """
    logger.info(f"Downloading {issue=} with {destination=}.")
    issue_page_url = zeitonline.get_issue_page_url(sess, issue)
    download_url = zeitonline.get_download_url(sess, issue_page_url)
    return service.download_file(sess, download_url, destination, overwrite=False)
