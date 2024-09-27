@echo off
REM Navigate to the script's directory
cd /d "D:\WTPyScripts\file_utilities"

REM Open PowerShell in a new window to monitor the log
start powershell.exe -NoExit -Command "Get-Content doc_processing.log -Wait"

REM Execute the Python script
python scan_word_files_new_latest02.py

REM Pause to keep the CMD window open after execution
pause
