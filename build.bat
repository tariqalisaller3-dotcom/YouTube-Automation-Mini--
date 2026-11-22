
@echo off
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --windowed --name YouTubeAutomationMini app.py
pause
