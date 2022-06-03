#!/bin/bash

cd /code

rm -rf /code/static/react_components
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --ws-ping-interval 120 --ws-ping-timeout 120