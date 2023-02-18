from pathlib import Path

import requests

from zeitdl import service
from zeitdl.core import zeitonline


def initialize_session(credential_file: Path) -> requests.Session:
    """
    Initialize a session. This includes login to Zeit Online.

    Args:
        credential_file: path to a JSON file containing the credentials to log in to
            Zeit Online. See `zeitdl.service.credentials.load_credentials_from_file`.

    Returns:
        session that has been logged into Zeit Online
    """
    # Prepare session. We need to be login.
    credentials = service.load_credentials_from_file(credential_file)
    sess = requests.Session()
    zeitonline.login(sess, credentials)
    return sess
