@echo off
setlocal

where pyw >nul 2>nul
if not errorlevel 1 (
    start "" pyw "%~dp0main.py"
    exit /b 0
)

where pythonw >nul 2>nul
if not errorlevel 1 (
    start "" pythonw "%~dp0main.py"
    exit /b 0
)

echo Python with Tkinter was not found. Install Python and try again.
pause
