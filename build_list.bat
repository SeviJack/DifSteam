@echo off
setlocal

:: --- Configuration ---
set "SCRIPT=list.py"
set "NAME=%~1"
set "OUTDIR=C:\Tools\folders"


if "%NAME%"=="" (
    echo Usage: build.bat ^<icon_path.ico^>
    exit /b 1
)

echo Building %NAME%.exe with icon "%NAME%.ico" ...

:: Clean previous build artifacts
rmdir /s /q build dist >nul 2>&1

:: Compile with PyInstaller
pyinstaller --onefile --noconsole --icon "C:\PersonalProjects\DifSteam\resources\%NAME%.ico" "%SCRIPT%" --name "%NAME%" --add-data "resources;resources"

:: Create install directory if missing
if not exist "%OUTDIR%" mkdir "%OUTDIR%"

:: Move built exe to output
move /Y "dist\%NAME%.exe" "%OUTDIR%\" >nul

echo Done. Output: %OUTDIR%\%NAME%.exe
pause
endlocal
