@echo off
setlocal
:: Batch command to test tmerge_xml_enumerated_values_with_new_entries.py with 4 scenarios. It creates 4 Test* folders with resulted files.
:: <ROOT> .\windchill\enums\test_merge_xml_enumerated_values_with_new_entries.bat

:: set absolute paths
set "BASE_DIR=D:\WTPyScripts"
set "PYTHON_SCRIPT=%BASE_DIR%\windchill\enums\merge_xml_enumerated_values_with_new_entries.py"
set "INPUT_XML=%BASE_DIR%\inputSEP\Enums\POWERAircraft.xml"
set "PYTHON_EXE=python.exe"

:: In a batch (*.bat) script, the ampersand & character is interpreted as a command separator. 
:: To include an ampersand (&) in a string that you're echoing to a file, you need to escape it by using the ^ character before the ampersand. 

:: Scenario: Test sort by name all entries (existing and new)
:: Preserve the original selectable value of existing entries matching new entries
:: Force selectable value at false for the new entries added to existing entries
set "TEST_DIR=%BASE_DIR%\windchill\enums\testName_pes_f"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
call :CreateTestDir
call :CreateCSV
REM sort by name all entries (existing and new)
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -pes -f

:: Scenario: Test sort by name all entries (existing and new)
set "TEST_DIR=%BASE_DIR%\windchill\enums\testName"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
call :CreateTestDir
call :CreateCSV
REM sort by name all entries (existing and new)
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%"

:: Scenario: Test preserve existing sorting at begininng - and sort by name new entries at the end
set "TEST_DIR=%BASE_DIR%\windchill\enums\testName_po"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
call :CreateTestDir
call :CreateCSV
REM preserve existing sorting at begininng - and sort by name new entries at the end
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -po

:: Scenario: Test sort by displayName all entries (existing and new)
set "TEST_DIR=%BASE_DIR%\windchill\enums\testDisplayName"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
call :CreateTestDir
call :CreateCSV
REM sort by displayName all entries (existing and new)
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -s displayName

:: Scenario: Test preserve existing sorting at begininng - and sort by displayName new entries at the end
set "TEST_DIR=%BASE_DIR%\windchill\enums\testDisplayName_po"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
call :CreateTestDir
call :CreateCSV
REM preserve existing sorting at begininng - and sort by displayName new entries at the end
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -po -s displayName

:: End of the main script
goto :eof

:: Function-like section
:: delete and create test directory
:CreateTestDir
rd /s /q "%TEST_DIR%"
mkdir "%TEST_DIR%"
if not exist "%TEST_DIR%" (
    echo Failed to create or access the test directory.
    exit /b
)
goto :eof

:: create and populate the csvInput.cs
:CreateCSV
:: csvInput input file creation in excel:
:: =CONCATENATE("echo ",C2, "~", D2, "~>>""%INPUT_CSV%""")
echo name~displayName~csvlocale_fr>"%INPUT_CSV%"
echo H0405~A129 (M)~>>"%INPUT_CSV%"
echo T9998~Cars ^& Formula1~>>"%INPUT_CSV%"
goto :eof

:eof  REM End of file
endlocal
