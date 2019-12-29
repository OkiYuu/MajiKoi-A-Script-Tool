@echo off
:start
cls
echo ****************************
echo *  MajiKoi A Script Tool   *
echo ****************************
echo *  Select from options:    *
echo *                          *
echo *  1. Unpack script        *
echo *  2. Pack script          *
echo *  3. Unpack ALL from IN   *
echo *  4. Pack ALL from EDIT   *
echo *  5. Quit                 *
echo *                          *
echo ****************************

set /p choice=Select option: 
if '%choice%'=='1' goto :opt1
if '%choice%'=='2' goto :opt2
if '%choice%'=='3' goto :opt3
if '%choice%'=='4' goto :opt4
if '%choice%'=='5' goto :EOF
goto :start

:opt1
@echo off
call :filedialog file

::DEBUG CODE
::"source\pp27\python.exe" "source\main.py" u "%file%"
source\main.exe u "%file%"

echo Ran unpack script on %file%
echo Press any key to continue...
pause >NUL
goto :start

:opt2
:: Folder select code by rojo on Stackoverflow
:: URL: https://stackoverflow.com/questions/15885132/file-folder-chooser-dialog-from-a-windows-batch-script
setlocal
set "psCommand="(new-object -COM 'Shell.Application')^
.BrowseForFolder(0,'Please choose a folder.',0,0).self.path""
for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "folder=%%I"
setlocal enabledelayedexpansion

:: DEBUG CODE
:: "source\pp27\python.exe" "source\main.py" p "%folder%"
source\main.exe p "%folder%"

endlocal
echo Ran pack script on %folder%.
echo Press any key to continue...
pause >NUL
goto :start

:opt3

:: DEBUG CODE
:: "source\pp27\python.exe" "source\main.py" u
source\main.exe u

echo Unpacked all .bin files from IN directory!
echo Press any key to continue...
pause >NUL
goto :start

:opt4
:: DEBUG CODE
:: "source\pp27\python.exe" "source\main.py" p
source\main.exe p

echo Packed all subdirectories from EDIT directory!
echo Press any key to continue...
pause >NUL
goto :start

:: Code for file dialogue shamelessly adopted from ActiveState
:: URL: https://code.activestate.com/recipes/580665-file-selector-dialog-in-batch/
:filedialog :: &file
setlocal 
set dialog="about:<input type=file id=FILE><script>FILE.click();new ActiveXObject('Scripting.FileSystemObject')
set dialog=%dialog%.GetStandardStream(1).WriteLine(FILE.value);close();resizeTo(0,0);</script>"
for /f "tokens=* delims=" %%p in ('mshta.exe %dialog%') do set "file=%%p"
endlocal  & set %1=%file%
