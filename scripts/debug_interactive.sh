#!/bin/bash

# Launch interactive debugger

set -e

echo "======================================"
echo "Launching Interactive Debugger"
echo "======================================"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run interactive debugger
python3 debug/interactive_debug.py
