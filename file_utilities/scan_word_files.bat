@echo off
REM Navigate to the script's directory
cd /d "D:\WTPyScripts\file_utilities"

REM Open PowerShell in a new window to monitor the log
start "" powershell.exe -NoExit -Command "Get-Content doc_processing.log -Wait"

REM Execute the Python script
python scan_word_files.py

REM Inform the user
echo.
echo -----------------------------------------------
echo Python script has completed execution.
echo -----------------------------------------------
echo.

REM Prompt the user to delete the log file
set /p userinput=Do you want to delete the log file? (Y/N): 

if /I "%userinput%"=="Y" (
    REM Close the PowerShell window before deleting the log
    taskkill /IM powershell.exe /F >nul 2>&1
    del /f /q doc_processing.log
    echo Log file deleted successfully.
) else (
    echo Log file retained.
)

REM Pause to keep the CMD window open after execution
pause
