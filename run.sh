#!/bin/bash
# Quick launcher script for subtitles-auto-correct
# This script activates the virtual environment and runs the application

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating it now..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing subtitles-auto-correct..."
    pip install -e .
else
    source venv/bin/activate
fi

# Run the application
python -m subtitles_auto_correct
