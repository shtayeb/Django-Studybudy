#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

make npm-install
make npm-build

python src/manage.py collectstatic --no-input
python src/manage.py migrate