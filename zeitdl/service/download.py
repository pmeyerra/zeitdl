import re
from pathlib import Path

import httpx
import structlog

logger = structlog.get_logger()


def download_file(
    sess: httpx.Client,
    url: str,
    destination: Path,
    overwrite: bool = False,
) -> Path:
    """Download a file from the internet.

    If the file already exists and `overwrite` is false, skip download. If the
    `destination` directory does not exist, it will be created.

    Args:
        sess: ``httpx.Client`` session to use
        url: download URL
        destination: destination folder into which the downloaded content will be saved.
            The filename will be extracted from the response headers.
        overwrite: if True and the output file already exists, it will be overwritten.
            Otherwise, do not overwrite the existing file and skip download.

    Returns:
        path to the downloaded file
    """
    with sess.stream("GET", url) as res:
        res.raise_for_status()

        # Extract filename from headers.
        matches = re.findall("filename=(.+)", res.headers["Content-Disposition"])

        if not matches:
            msg = "Could not extract filename from response headers."
            raise RuntimeError(msg)

        filename = matches[0].strip('"')

        path = destination / filename

        if not destination.is_dir():
            logger.debug("Creating destination directory", destination=destination)
            destination.mkdir(parents=False)

        if path.is_file():
            if overwrite:
                logger.warning(f"Overwriting file {path}.")
            else:
                logger.info(f"File {path} already exists, skipping download.")
                return path

        logger.debug("Downloading content", url=url, path=path)

        with path.open("wb") as f:
            for chunk in res.iter_bytes(chunk_size=8192):
                f.write(chunk)
    return path
