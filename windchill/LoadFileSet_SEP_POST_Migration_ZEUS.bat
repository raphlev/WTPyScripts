@echo off
setlocal enabledelayedexpansion
cls

:: Execute this bat file in Windchill shell admin console opened as Administrator

:: Set the Windchill installation directory variable
set WINDCHILL_DIR=D:\ptc\Windchill_12.1\Windchill
echo **********************************************************************************************
echo ** Starting post deployment of the Windchill Migration Package after migration was executed **
echo **********************************************************************************************

:: Navigate to the Windchill directory
cd /d %WINDCHILL_DIR%

:: Prepare the special argument
set "SPECIAL_ARG=Migration-Zeus"

:: Execute LC Reassignment : POWERStandardComponentDocument
echo **************************************************************************************************************************
echo ** Execute LC Reassignment : site administrator password must be set manually in this file before launching this script **
echo **************************************************************************************************************************
echo call .\bin\windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERStandardComponentDocument %SPECIAL_ARG%
call .\bin\windchill ext.lps.common.utils.ReassignLCAgainstIterationNote wcadmin ***** RUN BULK ext.lps.power.POWERStandardComponentDocument %SPECIAL_ARG%

if %errorlevel% neq 0 (
    echo LC Reassignment failed. See error in MethodServer log. Exiting script.
    exit /b %errorlevel%
)

:: Load sep configuration files into Windchill as default : POWERStandardComponentDocumentOIR
echo ****************************************************
echo ** Loading new configuration files into Windchill **
echo ****************************************************
echo call .\bin\windchill --javaargs=-Dwt.auth.trustedAuth.username=wcadmin wt.load.LoadFileSet -file "%WINDCHILL_DIR%\loadFiles\ext\LoadFileSet_SEP_POST_Migration_ZEUS.xml" -UNATTENDED -NOSERVERSTOP
call .\bin\windchill --javaargs=-Dwt.auth.trustedAuth.username=wcadmin wt.load.LoadFileSet -file "%WINDCHILL_DIR%\loadFiles\ext\LoadFileSet_SEP_POST_Migration_ZEUS.xml" -UNATTENDED -NOSERVERSTOP
if %errorlevel% neq 0 (
	echo.
	echo **************************************************************
    echo ** Failed to load new configuration files. Exiting script ! **
	echo **************************************************************
    exit /b %errorlevel%
)

:: Restarting Windchill server
echo ****************************************************************************
echo ** Restart Windchill server ? (you will have option to clean cached)      **
echo ****************************************************************************

set /p restartChoice="Restart Windchill server (Y/N)? "
if /i "!restartChoice!"=="Y" (
	echo call .\bin\windchill stop
    call .\bin\windchill stop
    if !errorlevel! neq 0 (
		echo ****************************************
		echo ** Failed to stop Windchill server ! **
		echo ****************************************
        exit /b !errorlevel!
    )
	echo *******************************************
	echo ** Windchill server stopped successfully **
	echo *******************************************

	:: Start Windchill server
	echo ******************************
	echo ** Start Windchill server : **
	echo ******************************
	echo ******************************************************************************
	echo ** Do you want to execute these cache cleansing commands before ?           **
	echo ** N: start Windchill without cache cleansing                               **
	echo ** Y: Execute below commands and then start Windchill                       **
	echo ******************************************************************************
	echo ** del /Q/F/S D:\ptc\Windchill_12.1\Windchill\logs\*                        **
	echo ** del /Q/F/S D:\ptc\Windchill_12.1\Windchill\temp\*                        **
	echo ** del /Q/F/S D:\ptc\Windchill_12.1\Windchill\tasks\codebase\*              **
	echo ** del /Q/F/S D:\ptc\Windchill_12.1\Windchill\tomcat\instances\*            **
	echo ** del /Q/F/S D:\ptc\Windchill_12.1\Windchill\codebase\wt\workflow\expr\*   **
	echo ******************************************************************************
	set /p cleanseChoice="Do you want to execute these cache cleansing commands before (Y/N)? "
	if /i "!cleanseChoice!"=="Y" (
		echo del /Q/F/S D:\ptc\Windchill_12.1\Windchill\logs\*
		call del /Q/F/S D:\ptc\Windchill_12.1\Windchill\logs\*
		echo del /Q/F/S D:\ptc\Windchill_12.1\Windchill\temp\*
		call del /Q/F/S D:\ptc\Windchill_12.1\Windchill\temp\*
		echo del /Q/F/S D:\ptc\Windchill_12.1\Windchill\tasks\codebase\*
		call del /Q/F/S D:\ptc\Windchill_12.1\Windchill\tasks\codebase\*
		echo del /Q/F/S D:\ptc\Windchill_12.1\Windchill\tomcat\instances\*
		call del /Q/F/S D:\ptc\Windchill_12.1\Windchill\tomcat\instances\*
		echo del /Q/F/S D:\ptc\Windchill_12.1\Windchill\codebase\wt\workflow\expr\*
		call del /Q/F/S D:\ptc\Windchill_12.1\Windchill\codebase\wt\workflow\expr\*
	)
	echo call .\bin\windchill start
	call .\bin\windchill start
	if !errorlevel! neq 0 (
		echo ****************************************
		echo ** Failed to start Windchill server ! **
		echo ****************************************
		exit /b !errorlevel!
	)
	echo *******************************************
	echo ** Windchill server started successfully **
	echo *******************************************
) else (
	echo *****************************************************************************
	echo ** Windchill server restart was cancelled - You can restart manually later **
	echo *****************************************************************************
)
echo ********************************
echo ** Deployment script finished **
echo ********************************

endlocal