#!/bin/bash

export FLASK_APP=./clg/db.py

pipenv run flask --debug run -h 0.0.0.0