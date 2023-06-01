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

from qself.oura import OuraAPIClient
```

``` python
client = OuraAPIClient(os.environ["OURA_PERSONAL_ACCESS_TOKEN"])
```

Note that this assumes that the `OURA_PERSONAL_ACCESS_TOKEN` environment
variable contains a personal access token which you can create
[here](https://cloud.ouraring.com/personal-access-tokens).
