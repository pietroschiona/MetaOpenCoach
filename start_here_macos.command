#!/bin/bash
cd "$(dirname "$0")"
echo "=================================================="
echo "MetaOpenCoach - One-Click Starter (macOS)"
echo "=================================================="
echo "1. Checking/Installing dependencies..."
python3 -m pip install -r requirements.txt
echo ""
echo "2. Launching Generation UI..."
python3 src_python/app_builder_ui.py
