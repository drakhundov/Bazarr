#!/bin/bash
set -e

if ! [[ -f "data.db" ]]; then
    echo "Creating database from schema..."
    sqlite3 data.db < schema.sql
fi
if ! [[ -d "env" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi
if [[ -f "initenv.sh" ]]; then
    source initenv.sh
else
    echo "error: initenv.sh not found"
    exit 1
fi
echo "Activating Python virtual environment..."
source ./env/bin/activate
echo "Installing requirements..."
pip3 install -r requirements.txt
echo "Running the application..."
python3 main.py
