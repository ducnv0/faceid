#!/bin/bash
cd "$(dirname $0)"
cd ..
uvicorn src.main:app --host 0.0.0.0 --port 8080
