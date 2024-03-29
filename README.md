
# Dff DB Connector

[Dff DB Connector](https://github.com/ruthenian8/dff-db-connector) is an extension to the [Dialogflow Framework](https://github.com/deepmipt/dialog_flow_engine), a minimalistic open-source engine for conversational services.

[Dff DB Connector](https://github.com/ruthenian8/dff-db-connector) allows you to to save and retrieve user dialogue states (in the form of a `Context` object) using various database backends. 

Currently, the supported options are: 
* [Redis](https://redis.io/)
* [MongoDB](https://www.mongodb.com/)
* [Postgresql](https://www.postgresql.org/)
* [MySQL](https://www.mysql.com/)
* [Sqlite](https://www.sqlite.org/index.html)

Aside from this, we offer some interfaces for saving data to your local file system. These are not meant to be used in production, but can be helpful for prototyping your application.

<!-- [![Documentation Status](https://dff-db-connector.readthedocs.io/en/stable/?badge=stable)](https://readthedocs.org/projects/dff-db-connector/badge/?version=stable) -->
<!-- [![Coverage Status](https://coveralls.io/repos/github/ruthenian8/dff-db-connector/badge.svg?branch=main)](https://coveralls.io/github/ruthenian8/dff-db-connector?branch=main) -->
[![Codestyle](https://github.com/ruthenian8/dff-db-connector/workflows/codestyle/badge.svg)](https://github.com/ruthenian8/dff-db-connector)
[![Tests](https://github.com/ruthenian8/dff-db-connector/workflows/test_coverage/badge.svg)](https://github.com/ruthenian8/dff-db-connector)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ruthenian8/dff-db-connector/blob/main/LICENSE)
![Python 3.6, 3.7, 3.8, 3.9](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-green.svg)
<!-- [![PyPI](https://img.shields.io/pypi/v/dff-db-connector)](https://pypi.org/project/dff-db-connector/)
[![Downloads](https://pepy.tech/badge/dff-db-connector)](https://pepy.tech/project/dff-db-connector) -->

# Quick Start
## Installation
```bash
pip install dff-db-connector
```

Please, note that if you are going to use one of the database backends, you will have to specify an extra or install the corresponding requirements yourself.
```bash
pip install dff-db-connector[redis]
pip install dff-db-connector[mongodb]
pip install dff-db-connector[mysql]
pip install dff-db-connector[postgresql]
pip install dff-db-connector[sqlite]
```

## Basic example
```python
from df_engine.core import Context, Actor
from dff_db_connector import SqlConnector
from .plot import some_dff_plot

db = SqlConnector("postgresql://user:password@host:port/dbname")

actor = Actor(some_dff_plot, start_label=("root", "start"), fallback_label=("root", "fallback"))


def handle_request(request):
    user_id = request.args["user_id"]
    if user_id not in db:
        context = Context(id=user_id)
    else:
        context = db[user_id]
    new_context = actor(context)
    db[user_id] = new_context
    assert user_id in db
    return new_context.last_response

```

To get more advanced examples, take a look at [examples](https://github.com/ruthenian8/dff-db-connector/tree/main/examples) on GitHub.

# Contributing to the Dff DB Connector

Please refer to [CONTRIBUTING.md](https://github.com/ruthenian8/dff-db-connector/blob/main/CONTRIBUTING.md).