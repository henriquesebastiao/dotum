#!/bin/sh

alembic upgrade head
fastapi run app/main.py --host 0.0.0.0 --port 8000 --workers 4