@echo off
python test_deps.py
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
python -m uvicorn app:app --reload --port 8080 --log-level debug
pause
