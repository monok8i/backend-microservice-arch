#!/bin/bash
set -x

black --config pyproject.toml .
isort --profile black .


