import httpx

_HEADERS = {
    "content-type": "application/x-www-form-urlencoded",
    "cache-control": "max-age=0",
    "origin": "https://meine.zeit.de",
    # For some reason, I need to use this user-agent when making requests, otherwise
    # zeit.de thinks I'm a bot...
    "user-agent": "python-requests/2.32.3",
}


def get_client() -> httpx.Client:
    """Create an httpx client with the required headers."""
    return httpx.Client(follow_redirects=True, headers=_HEADERS)
