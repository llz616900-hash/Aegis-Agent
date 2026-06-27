#!/bin/bash
# Start the Aegis-Agent FastAPI backend
cd "$(dirname "$0")/.."
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
