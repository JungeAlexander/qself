qself
================

> Tools to extract personal, quantitative data from various sources.

[![Documentation Status](https://readthedocs.org/projects/qself/badge/?version=latest)](https://qself.readthedocs.io/en/latest/?badge=latest)

## Install

``` sh
pip install qself
```

## How to use

``` python
import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from qself.oura import OuraAPIClient

load_dotenv(find_dotenv()) # or similar
client = OuraAPIClient(os.environ["OURA_PERSONAL_ACCESS_TOKEN"])
da = client("daily_activity", "2023-07-01", "2023-07-08")
wo = client("workout", "2023-07-01", "2023-07-08")

with open("wo.json", "w") as fh:
    fh.write(wo.json(indent=2))

with open("wo_schema.json", "w") as fh:
    fh.write(wo.schema_json(indent=2))
```

Note that this assumes that the `OURA_PERSONAL_ACCESS_TOKEN` environment
variable contains a personal access token which you can create
[here](https://cloud.ouraring.com/personal-access-tokens).

## Contributing

Installing `qself` and all development dependencies:

```console
poetry install
```

Running tests:

```console
pytest tests
```

To build the documentation:

```console
poetry install --with docs
cd docs
rm -rf _build/html
make html
```
