@echo off
echo ==================================================
echo   STARTING DRIVER SLEEP ALARM SYSTEM
echo   By Navvardhan Singh
echo ==================================================
echo.
echo [1/2] Checking and Installing Libraries...
pip install opencv-python face_recognition numpy
echo.
echo [2/2] Launching Drowsiness Detector...
python drowsy_detector.py
echo.
pause