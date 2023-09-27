import json
from pathlib import Path

import structlog

from zeitdl.types import ZeitOnlineCredentials

logger = structlog.get_logger()


def load_credentials_from_file(file: Path) -> ZeitOnlineCredentials:
    """Load Zeit Online credentials from a JSON file.

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
    logger.debug("Loading ZeitOnline credentials", file=file)
    with file.open(encoding="utf-8") as f:
        data = json.load(f)
    return ZeitOnlineCredentials(**data)
