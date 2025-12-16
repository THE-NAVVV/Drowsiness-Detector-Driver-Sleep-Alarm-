@echo off
echo ==================================================
echo   STARTING SIGN LANGUAGE DETECTOR
echo   By Navvardhan Singh
echo ==================================================
echo.
echo [1/2] Checking and Installing Libraries...
pip install -r requirements.txt
echo.
echo [2/2] Launching Camera...
python sign_language_project.py
echo.
pause