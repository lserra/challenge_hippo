#!/bin/bash

# Create folders
mkdir -p analisys database input output
echo ">> Folders 'analisys', 'database', 'input', and 'output' created successfully."

# Create a virtual environment
python3 -m venv .venv
echo ">> Virtual environment '.venv' created successfully."

# Activate the virtual environment
source .venv/bin/activate
echo ">> Virtual environment '.venv' activated."

# Install necessary packages (if any)
pip install -r requirements.txt
echo ">> Packages installed successfully."
