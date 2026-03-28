@echo off
cd /d "%~dp0"
start "" "http://localhost:5050"
python app.py
pause
