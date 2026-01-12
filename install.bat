@echo off
REM ArXiv Paper Collector - Installation Script for Windows

echo ==================================
echo ArXiv Paper Collector Installer
echo ==================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Check pip
echo.
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip not found, attempting to install...
    python -m ensurepip --upgrade
)

REM Check LaTeX
echo.
echo Checking LaTeX installation...
pdflatex --version >nul 2>&1
if errorlevel 1 (
    xelatex --version >nul 2>&1
    if errorlevel 1 (
        echo Warning: LaTeX not found!
        echo.
        echo LaTeX is required for PDF generation.
        echo Please install MiKTeX from https://miktex.org/download
        echo.
        set /p CONTINUE="Continue anyway? (y/N): "
        if /i not "%CONTINUE%"=="y" exit /b 1
    ) else (
        echo Found LaTeX (xelatex)
    )
) else (
    echo Found LaTeX (pdflatex)
)

REM Create virtual environment
echo.
set /p CREATE_VENV="Create virtual environment? (recommended) [Y/n]: "
if /i not "%CREATE_VENV%"=="n" (
    if not exist "venv" (
        echo Creating virtual environment...
        python -m venv venv
    )
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Install dependencies
echo.
echo Installing Python dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

REM Create output directories
echo.
echo Creating output directories...
if not exist "output\papers" mkdir output\papers
if not exist "output\latex" mkdir output\latex

REM Test installation
echo.
echo Testing installation...
python main.py --help >nul 2>&1
if errorlevel 1 (
    echo Warning: Installation test failed
) else (
    echo Installation successful!
)

echo.
echo ==================================
echo Installation Complete!
echo ==================================
echo.
echo Usage:
if /i not "%CREATE_VENV%"=="n" (
    echo   1. Activate virtual environment:
    echo      venv\Scripts\activate
)
echo   2. Run the collector:
echo      python main.py --run
echo.
echo   3. Edit keywords:
echo      python main.py --edit-keywords
echo.
echo   4. Start scheduled daemon:
echo      python main.py --daemon
echo.
echo For more information, see README.md
echo.
pause
