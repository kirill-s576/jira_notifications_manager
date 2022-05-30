#!/bin/bash

cd /code

uvicorn main:app --host 0.0.0.0 --port 8000 --reload --ws-ping-interval 120 --ws-ping-timeout 120