from urllib.parse import urljoin

import httpx
import structlog
from bs4 import BeautifulSoup

from zeitdl.core.zeitonline.constants import BASE_URL_EPAPER, LOGIN_URL
from zeitdl.exceptions import ZeitOnlineLoginError
from zeitdl.types import ZeitOnlineCredentials

logger = structlog.get_logger()


def login(
    client: httpx.Client,
    credentials: ZeitOnlineCredentials,
) -> httpx.Client:
    """Log into Zeit Online.

    The login procedure involves making a GET request to the login URL. The CSRF token
    is extracted from the response and included in the payload to the login POST
    request.

    Args:
        client: stateful ``httpx`` client to use for the login
        credentials: credentials used for authentication
    """
    logger.debug("Making GET request to login URL to retrieve CSRF Token")
    res = client.get(LOGIN_URL)
    soup = BeautifulSoup(res.content, "html.parser")
    csrf_token = soup.find("input", attrs={"name": "csrf_token"})["value"]

    payload = {
        "email": credentials.email,
        "pass": credentials.password,
        "csrf_token": csrf_token,
    }
    res = client.post(LOGIN_URL, data=payload)
    res.raise_for_status()

    # Now, make on more request to the epaper diezeit page.
    # It seems that this is necessary to be fully logged into epaper.zeit.de...
    # Not sure what's going on here...
    epaper_diezeit_url = urljoin(BASE_URL_EPAPER, "abo/diezeit")
    res = client.get(epaper_diezeit_url)

    # Login succeeded if the response URL is the same as the request URL.
    # This means we have successfully accessed the epaper page we want.
    if res.url != epaper_diezeit_url:
        msg = (
            f"Login to Zeit Online seems to have failed. "
            f"The response URL was '{res.url}', "
            f"which does not match the expected url '{epaper_diezeit_url}'."
        )
        raise ZeitOnlineLoginError(msg)
    logger.debug("Successfully logged into Zeit Online", response_url=res.url)

    return client
