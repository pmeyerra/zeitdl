import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from zeitdl.core.zeitonline.constants import BASE_URL_EPAPER, HEADERS, LOGIN_URL
from zeitdl.exceptions import ZeitOnlineLoginError
from zeitdl.types import ZeitOnlineCredentials

logger = logging.getLogger(__name__)


def login(
    sess: requests.Session, credentials: ZeitOnlineCredentials
) -> requests.Session:
    """
    Log into Zeit Online.

    The login procedure involved making a GET request to the login URL.
    The CSRF token will be extracted from the response and included in the payload to
    the login POST request.

    Args:
        sess: stateful `requests.Session` object which will be logged in
        credentials: credentials used for authentication
    """
    logger.debug("Making GET request to login URL to retrieve CSRF Token.")
    res = sess.get(LOGIN_URL)
    soup = BeautifulSoup(res.content, "html.parser")
    csrf_token = soup.find("input", attrs={"name": "csrf_token"})["value"]

    payload = {
        "email": credentials.email,
        "pass": credentials.password,
        "csrf_token": csrf_token,
    }
    logger.debug(
        "CSRF token extracted from response. "
        "Now POSTing to login URL with login credentials."
    )
    res = sess.post(LOGIN_URL, data=payload, headers=HEADERS)
    res.raise_for_status()

    # Now, make on more request to the epaper diezeit page.
    # It seems that this is necessary to be fully logged into epaper.zeit.de...
    # Not sure what's going on here...
    epaper_diezeit_url = urljoin(BASE_URL_EPAPER, "abo/diezeit")
    res = sess.get(epaper_diezeit_url)

    # Login succeeded if the response URL is the same as the request URL.
    # This means we have successfully accessed the epaper page we want.
    if res.url != epaper_diezeit_url:
        raise ZeitOnlineLoginError(
            f"Login to Zeit Online seems to have failed. The response URL "
            f"was '{res.url}', which does not match the expected "
            f"url '{epaper_diezeit_url}'."
        )
    logger.debug(f"Successfully logged into Zeit Online. Response URL is '{res.url}'.")

    return sess
