@echo off
cd /d "c:\Users\ANN\dyad-apps\Recursive-Intelligence-Expansion-1"
uvicorn app:app --reload --host 0.0.0.0 --port 8080
pause
