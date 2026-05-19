@echo off
REM Launch BrewCha local server using the venv Python
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo Creating venv...
    python -m venv venv
)
"venv\Scripts\python.exe" serve.py
