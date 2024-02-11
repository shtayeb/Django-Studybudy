#!/usr/bin/env bash

make install
python3.9 manage.py collectstatic --noinput