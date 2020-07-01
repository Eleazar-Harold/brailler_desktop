
#!/usr/bin/env bash

set -x

mypy src
black --check src
isort --recursive --check-only src
flake8 src --max-line-length=88