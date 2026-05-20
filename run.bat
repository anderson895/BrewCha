@echo off
REM Launch BrewCha local dev server.
REM No venv needed — serve.py uses only the Python standard library.
cd /d "%~dp0"
python serve.py
