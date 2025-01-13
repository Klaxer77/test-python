#!/bin/bash

pytest --maxfail=1 --disable-warnings

if [ $? -ne 0 ]; then
  echo "Testing failed"
  exit 1 
fi

gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000