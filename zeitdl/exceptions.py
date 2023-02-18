class ZeitDownloadException(Exception):
    """Base exception for any exception raised by the `zeitdl` package."""


class ZeitOnlineLoginError(ZeitDownloadException):
    """
    Raised if login to Zeit Online (https://meine.zeit.de/) failed.
    """


class IssueNotFoundError(ZeitDownloadException):
    """Raised if an issue could not be found, i.e. the issue page for a certain issue
    number and year could not be determined."""
