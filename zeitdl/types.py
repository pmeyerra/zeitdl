import dataclasses

@dataclasses.dataclass(frozen=True)
class ZeitOnlineCredentials:
    """
    The credentials required to authenticate to Zeit Online.
    """

    email: str
    # do not include in repr because it's a secret
    password: str = dataclasses.field(repr=False)


@dataclasses.dataclass(frozen=True)
class Issue:
    """
    One Zeit Epaper issue is identified by the number and the year it was issued.
    """

    number: int
    year: int
