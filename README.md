# zeitdl

It's possible to download a PDF version of each issue of the german
newspaper *Die Zeit*.

With the code in this repo, you can do so programmatically.

## Installation

Clone this repository and install it using [`uv`](https://docs.astral.sh/uv/#uv).

```shell
uv sync
```

## Usage

Below is an example of how to use this package to download issues of *Die Zeit* as PDF.

```shell
zeitdl \
  --year 2025 \
  --start-issue 1 \
  --end-issue 10 \
  --credentials "credentials.json" \
  --destination "DieZeit2025/"
```

## Authentication

Valid credentials for [Zeit Online](https://meine.zeit.de/) are required.

They must be saved in a JSON file and provided to the `zeitdl` script.
An example of what the JSON file must look like is shown below.

```json
{
  "email": "myname@mydomain.com",
  "password": "my-strong-password"
}
```
