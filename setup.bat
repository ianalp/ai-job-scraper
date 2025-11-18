@echo off
REM AI Job Scraper - Quick Start Script for Windows

echo ========================================
echo    AI Job Scraper - Quick Start
echo ========================================
echo.

REM Check Python version
echo [*] Checking Python version...
python --version
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt
echo.

REM Install Playwright browsers
echo [*] Installing Playwright browsers...
playwright install chromium
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo [*] Creating .env file from template...
    copy .env.example .env
    echo [!] Please edit .env file with your email credentials!
) else (
    echo [*] .env file already exists
)

echo.
echo ========================================
echo           Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your email settings
echo 2. Run scraper: python scraper.py
echo 3. Launch dashboard: streamlit run dashboard.py
echo.
echo Happy job hunting! 💼
echo.
pause
