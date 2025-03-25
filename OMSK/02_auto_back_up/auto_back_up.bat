@echo off
setlocal

if not "%minimized%"=="" goto :minimized
set minimized=true
start /min cmd /c "%~f0"
goto :eof
:minimized

:: Settings
set FTP_SERVER1=192.168.3.93
set FTP_SERVER2=192.168.3.92
set FTP_USER=rs_pdu
set FTP_PASS=rs_pdu
set REMOTE_PATH=/home/rs_pdu/mpux/data
set LOCAL_BASE_PATH=C:\back_up
set INTERVAL=8h
set INITIAL_DELAY=0s :: Delay before the first download (e.g., 1h for 1 hour)

:: Convert INITIAL_DELAY to seconds
for /f "tokens=1,2 delims=hmds" %%a in ("%INITIAL_DELAY%") do (
    set /a delay_seconds=%%a*3600 + %%b*60
)

:: Delay before the first download
if %delay_seconds% GTR 0 (
    echo Waiting before the first download: %INITIAL_DELAY%
    call :wait %delay_seconds%
)

:: Main loop
:download_ftp
:: Create a folder with a timestamp
for /f "tokens=1-4 delims=:., " %%a in ("%time%") do (
    set timestamp=%date:~6,4%-%date:~3,2%-%date:~0,2%_%%a-%%b-%%c
)
set DOWNLOAD_FOLDER=%LOCAL_BASE_PATH%\%timestamp%
mkdir "%DOWNLOAD_FOLDER%"
mkdir "%DOWNLOAD_FOLDER%\us_1(93)"
mkdir "%DOWNLOAD_FOLDER%\us_2(92)"

:: Download from FTP_SERVER1
echo Connecting to %FTP_SERVER1%...
echo user %FTP_USER% %FTP_PASS%> ftpcmd.dat
echo cd %REMOTE_PATH%>> ftpcmd.dat
echo lcd "%DOWNLOAD_FOLDER%\us_1(93)">> ftpcmd.dat
echo binary>> ftpcmd.dat
echo prompt>> ftpcmd.dat :: Добавлено: Отключение запросов подтверждения
echo mget *>> ftpcmd.dat
echo quit>> ftpcmd.dat
ftp -n -s:ftpcmd.dat %FTP_SERVER1%
del ftpcmd.dat

:: Download from FTP_SERVER2
echo Connecting to %FTP_SERVER2%...
echo user %FTP_USER% %FTP_PASS%> ftpcmd.dat
echo cd %REMOTE_PATH%>> ftpcmd.dat
echo lcd "%DOWNLOAD_FOLDER%\server2">> ftpcmd.dat
echo binary>> ftpcmd.dat
echo prompt>> ftpcmd.dat :: Добавлено: Отключение запросов подтверждения
echo mget *>> ftpcmd.dat
echo quit>> ftpcmd.dat
ftp -n -s:ftpcmd.dat %FTP_SERVER2%
del ftpcmd.dat

:: Timer until the next download
:wait_interval
for /l %%i in (28800,-1,1) do (
    cls
    echo Waiting for the next download...
    set /a hours=%%i/3600
    set /a minutes=(%%i%%3600)/60
    set /a seconds=%%i%%60
    echo Time left: %hours% hours %minutes% minutes %seconds% seconds
    timeout /t 1 >nul
)

:: Repeat the process
goto download_ftp

:: Wait function
:wait
set /a wait_seconds=%1
for /l %%i in (%wait_seconds%,-1,1) do (
    cls
    echo Waiting: %%i seconds...
    timeout /t 1 >nul
)
goto :eof

endlocal