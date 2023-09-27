# zeitdl

It's possible to download a PDF version of each issue of the german
newspaper *Die Zeit*.

With the code in this repo, you can do so programmatically.

## Usage

Below is an example of how to use this package to download issues of *Die Zeit* as PDF.

```python
from pathlib import Path

from zeitdl.core import download_issue, initialize_session
from zeitdl.types import Issue


if __name__ == "__main__":
    # Generate list of issues to download. Download issues 1 through 20 from year 2022.
    year = 2023
    issue_numbers = list(range(1, 21))
    issues = [Issue(num, year) for num in issue_numbers]

    # A credential file containing the credentials to log into Zeit Online must
    # be created.
    credential_file = Path("/path/to/credentials.json")
    assert credential_file.is_file(), f"Credential file {credential_file} not found."

    # Save the downloaded files here.
    destination = Path("/path/to/destination/2022")

    # Initialize session, this will perform login to Zeit Online.
    sess = initialize_session(credential_file)

    # Download all the issues you want :)
    for issue in issues:
        download_issue(sess, issue, destination)
```

## Authentication

Valid credentials for [Zeit Online](https://meine.zeit.de/) are required.

They must be saved in a JSON file and provided to the `initialize_session` function.
An example of what the JSOn file must look like is shown below.

```json
{
  "email": "myname@mydomain.com",
  "password": "my-strong-password"
}
```
