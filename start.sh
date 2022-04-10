#!/bin/bash

# start fastapi server using uvicorn
if [ "$FASTAPI_DEBUG" = "True" ]; then
    uvicorn \
        --reload \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 2 \
        --log-level "debug" \
        main:app

else
    uvicorn \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 2 \
        --log-level "debug" \
        main:app
fi