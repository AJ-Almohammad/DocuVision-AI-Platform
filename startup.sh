#!/bin/bash
pip install -r requirements.txt
gunicorn --bind=0.0.0.0:8001 --workers=4 --chdir ./src/api simple_main:app