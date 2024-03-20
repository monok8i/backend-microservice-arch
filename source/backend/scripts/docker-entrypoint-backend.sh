#!/bin/bash
set -e

alembic upgrade head

sh ./scripts/format-code.sh

exec python main.py