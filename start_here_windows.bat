@echo off
echo ==================================================
echo MetaOpenCoach - One-Click Starter (Windows)
echo ==================================================
echo 1. Checking/Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo 2. Launching Generation UI...
python src_python\app_builder_ui.py
pause
