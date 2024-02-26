@echo off
:: set absolute paths
set "BASE_DIR=D:\WTPyScripts\windchill\enums"
set "PYTHON_SCRIPT=%BASE_DIR%\merge_xml_enumerated_values_with_new_entries.py"
set "INPUT_XML=..\..\..\inputSEP\Enums\POWERAircraft.xml"
set "TEST_DIR=%BASE_DIR%\test"
:: delete and create test directory
rd /s /q "%TEST_DIR%"
mkdir "%TEST_DIR%"
cd /d "%TEST_DIR%"
if not exist "%TEST_DIR%" (
    echo Failed to create or access the test directory.
    exit /b
)
:: csvInput input file creation
echo name~displayName~csvlocale_fr>csvInput.csv
echo RLU1~Value1 RLU~Valeur1 RLU>>csvInput.csv
echo BLU2~Value2 RLU~Valeur2 RLU>>csvInput.csv
:: Execute Python scripts
REM sort by name all entries (existing and new)
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "csvInput.csv" -o "output_merged_name.txt"
REM preserve existing sorting at begininng - and sort by name new entries at the end
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "csvInput.csv" -o "output_merged_name_p.txt" -p
REM sort by displayName all entries (existing and new)
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "csvInput.csv" -o "output_merged_displayName.txt" -s displayName
REM preserve existing sorting at begininng - and sort by displayName new entries at the end
python.exe "%PYTHON_SCRIPT%" -i "%INPUT_XML%" -n "csvInput.csv" -o "output_merged_displayName_p.txt" -s displayName -p
