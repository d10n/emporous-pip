# emporous-pip


Wrap pip for Emporous

Setup:

* Install poetry
* poetry install
* poetry shell

Prepare:

* ./workdata/bare/pypi.org/build-collection.sh
* ./workdata/bare/pypi.org/push-collection.sh

Use:

* `PIP_INDEX_URL='http://127.0.0.1:8089' pip install bottle`
* `PIP_EXTRA_INDEX_URL='http://127.0.0.1:8089' pip install pymetronome`
* `PIP_INDEX_URL='http://127.0.0.1:8089' pip index versions pymetronome`
