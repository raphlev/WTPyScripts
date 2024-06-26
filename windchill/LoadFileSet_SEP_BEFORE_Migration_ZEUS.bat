@echo off
setlocal enabledelayedexpansion
cls
:: Execute this bat file in Windchill shell admin console opened as Administrator

:: Set the Windchill installation directory variable
set WINDCHILL_DIR=D:\ptc\Windchill_12.1\Windchill

echo ************************************************************
echo ** Starting deployment of the Windchill Migration Package **
echo ************************************************************

:: Navigate to the Windchill directory
cd /d %WINDCHILL_DIR%

:: Compiling and deploying new class in codebase\ext\lps\common\utils\ReassignLCAgainstIterationNote.class
echo ************************************************************
echo ** Compiling new Java class ReassignLCAgainstIterationNote**
echo ************************************************************
echo call ant -f bin/tools.xml class -Dclass.source=%WINDCHILL_DIR%\src\ext\lps\common\utils -Dclass.includes=ReassignLCAgainstIterationNote.java
call ant -f bin/tools.xml class -Dclass.source=%WINDCHILL_DIR%\src\ext\lps\common\utils -Dclass.includes=ReassignLCAgainstIterationNote.java
if !errorlevel! neq 0 (
    echo Compilation failed. Exiting script.
    exit /b !errorlevel!
)

:: Load new configuration files into Windchill
echo ****************************************************
echo ** Loading new configuration files into Windchill **
echo ****************************************************
echo call .\bin\windchill --javaargs=-Dwt.auth.trustedAuth.username=wcadmin wt.load.LoadFileSet -file "%WINDCHILL_DIR%\loadFiles\ext\LoadFileSet_SEP_BEFORE_Migration_ZEUS.xml" -UNATTENDED -NOSERVERSTOP
call .\bin\windchill --javaargs=-Dwt.auth.trustedAuth.username=wcadmin wt.load.LoadFileSet -file "%WINDCHILL_DIR%\loadFiles\ext\LoadFileSet_SEP_BEFORE_Migration_ZEUS.xml" -UNATTENDED -NOSERVERSTOP
if !errorlevel! neq 0 (
	echo.
	echo **************************************************************
    echo ** Failed to load new configuration files. Exiting script ! **
	echo **************************************************************
    exit /b !errorlevel!
)

:: Restarting Windchill server
echo *****************************************************
echo ** Windchill server may need to be restarted (Y/N) **
echo *****************************************************

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
