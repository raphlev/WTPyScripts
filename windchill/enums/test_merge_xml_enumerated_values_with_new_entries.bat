@echo off
:: Batch command to test tmerge_xml_enumerated_values_with_new_entries.py with 4 scenarios. It creates 4 Test* folders with resulted files.
:: <ROOT> .\windchill\enums\test_merge_xml_enumerated_values_with_new_entries.bat

:: set absolute paths
set "BASE_DIR=D:\WTPyScripts\windchill\enums"
set "PYTHON_SCRIPT=%BASE_DIR%\merge_xml_enumerated_values_with_new_entries.py"
set "INPUT_XML=D:\WTPyScripts\inputSEP\Enums\POWERAircraft.xml"

:: Scenario 1: Test sort by name all entries (existing and new)
set "TEST_DIR=%BASE_DIR%\test"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
:: delete and create test directory
rd /s /q "%TEST_DIR%"
mkdir "%TEST_DIR%"
if not exist "%TEST_DIR%" (
    echo Failed to create or access the test directory.
    exit /b
)
:: csvInput input file creation
echo name~displayName~csvlocale_fr>"%INPUT_CSV%"
echo RLU1~Value1 RLU~Valeur1 RLU>>"%INPUT_CSV%"
echo BLU2~Value2 RLU~Valeur2 RLU>>"%INPUT_CSV%"
:: Execute Python scripts
REM sort by name all entries (existing and new)
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%"

:: Scenario 2: Test preserve existing sorting at begininng - and sort by name new entries at the end
set "TEST_DIR=%BASE_DIR%\testName_p"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
:: delete and create test directory
rd /s /q "%TEST_DIR%"
mkdir "%TEST_DIR%"
if not exist "%TEST_DIR%" (
    echo Failed to create or access the test directory.
    exit /b
)
:: csvInput input file creation
echo name~displayName~csvlocale_fr>"%INPUT_CSV%"
echo RLU1~Value1 RLU~Valeur1 RLU>>"%INPUT_CSV%"
echo BLU2~Value2 RLU~Valeur2 RLU>>"%INPUT_CSV%"
:: Execute Python scripts
REM preserve existing sorting at begininng - and sort by name new entries at the end
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -p

:: Scenario 3: Test sort by displayName all entries (existing and new)
set "TEST_DIR=%BASE_DIR%\testDisplayName"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
:: delete and create test directory
rd /s /q "%TEST_DIR%"
mkdir "%TEST_DIR%"
if not exist "%TEST_DIR%" (
    echo Failed to create or access the test directory.
    exit /b
)
:: csvInput input file creation
echo name~displayName~csvlocale_fr>"%INPUT_CSV%"
echo RLU1~Value1 RLU~Valeur1 RLU>>"%INPUT_CSV%"
echo BLU2~Value2 RLU~Valeur2 RLU>>"%INPUT_CSV%"
:: Execute Python scripts
REM sort by displayName all entries (existing and new)
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -s displayName

:: Scenario 4: Test preserve existing sorting at begininng - and sort by displayName new entries at the end
set "TEST_DIR=%BASE_DIR%\testDisplayName_p"
set "INPUT_CSV=%TEST_DIR%\csvInput.csv"
:: delete and create test directory
rd /s /q "%TEST_DIR%"
mkdir "%TEST_DIR%"
if not exist "%TEST_DIR%" (
    echo Failed to create or access the test directory.
    exit /b
)
:: csvInput input file creation
echo name~displayName~csvlocale_fr>"%INPUT_CSV%"
echo RLU1~Value1 RLU~Valeur1 RLU>>"%INPUT_CSV%"
echo BLU2~Value2 RLU~Valeur2 RLU>>"%INPUT_CSV%"
:: Execute Python scripts
REM preserve existing sorting at begininng - and sort by displayName new entries at the end
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "%INPUT_CSV%" -o "%TEST_DIR%" -p -s displayName
