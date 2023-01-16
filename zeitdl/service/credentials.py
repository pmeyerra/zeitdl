import json
import logging
from pathlib import Path

from zeitdl.types import ZeitOnlineCredentials

logger = logging.getLogger(__name__)


def load_credentials_from_file(file: Path) -> ZeitOnlineCredentials:
    """
    Load Zeit Online credentials from a JSON file.

    The credential file must look like this:

    ```json
    {
      "email": "myname@mydomain.com",
      "password": "my-strong-password"
    }
    ```

    Args:
        file: path to the JSON file containing the credentials

    Returns:
        initialized ZeitOnlineCredentials dataclass
    """
    logger.debug(f"Loading ZeitOnline credentials from file {file}.")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return ZeitOnlineCredentials(**data)
