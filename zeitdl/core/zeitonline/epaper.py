import re
from urllib.parse import urljoin

import httpx
import structlog
from bs4 import BeautifulSoup

from zeitdl.core.zeitonline.constants import BASE_URL_EPAPER
from zeitdl.exceptions import IssueNotFoundError
from zeitdl.types import Issue

logger = structlog.get_logger()


def get_issue_page_url(client: httpx.Client, issue: Issue) -> str:
    """Each issue has a page from which it can be read/downloaded.

    This function finds the URL of this page.

    For this, we make a query the `abo/diezeit` search page with the number and year of
    the issue we want. We then need to parse the response. That's because the
    response contains a few recent issues in addition to the result of the search.

    Args:
        client: `httpx.Client` object that must contain login cookies
        issue: `Issue` metadata

    Returns:
        URL of the issue page

    Raises:
        IssueNotFoundError: if the issue page URL could not unambiguously be determined
    """
    url = urljoin(BASE_URL_EPAPER, "abo/diezeit")
    # The issue needs to be a 0 padded number with 2 digits.
    params = {"issue": f"{issue.number:02d}", "year": issue.year, "title": "diezeit"}

    logger.debug("Getting issue page url", issue=issue, url=url, params=params)
    res = client.get(url, params=params)

    # There will be many 'results'. Each result has an img with the alternative text
    # being the issue number and year. We'll use that to find the link to the
    # correct issue page.
    alt_text = f"DIE ZEIT {issue.number:02d}/{issue.year:04d}"
    soup = BeautifulSoup(res.content, "html.parser")

    logger.debug("Searching img element", alt_text=alt_text)
    results = soup.find_all("img", alt=alt_text)

    if len(results) > 1:
        msg = (
            f"More than one result found in page "
            f"for img element with attribute {alt_text=}."
        )
        raise IssueNotFoundError(msg)
    if not results:
        msg = f"No result found in page for img element with attribute {alt_text=}."
        raise IssueNotFoundError(
            msg,
        )
    issue_page_url = results[0].parent.attrs["href"]
    logger.debug("Found issue page url", issue_page_url=issue_page_url)
    return urljoin(BASE_URL_EPAPER, issue_page_url)


def get_download_url(client: httpx.Client, issue_page_url: str) -> str:
    """Find the issue download URL.

    This is done by parsing the content of the issue page.

    Args:
    ----
        client: `httpx.Client` object that must contain login cookies
        issue_page_url: URL of the issue page

    Returns:
    -------
        issue download URL
    """
    res = client.get(issue_page_url)

    soup = BeautifulSoup(res.content, "html.parser")

    # The download URL is the href of the button that says 'GESAMT PDF-LADEN'.
    # For some reason, this finds multiple elements. As far as I can see,
    # they all contain the same
    # download URL, so I'm just going to take the first match.
    element = soup.find_all(text=re.compile("GESAMT"))[0].parent
    href = element.attrs["href"]
    logger.debug("Found download url", download_url=href)
    return urljoin(BASE_URL_EPAPER, href)
