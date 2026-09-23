@echo off
title Stark Expo Server Controller
color 0A

:menu
cls
echo ============================================================
echo          STARK EXPO TECH EXCHANGE - SERVER CONTROLLER
echo ============================================================
echo.
echo  Current IP: %ip%
echo  Server Port: 8000
echo.
echo  [1] Start Server
echo  [2] Stop Server
echo  [3] Restart Server
echo  [4] Show Server Info
echo  [5] Open in Browser
echo  [6] Exit
echo.
echo ============================================================
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto restart
if "%choice%"=="4" goto info
if "%choice%"=="5" goto open
if "%choice%"=="6" goto exit

:start
echo.
echo 🚀 Starting server...
cd /d "C:\Users\User\Desktop\stark"
start /min python server.py
echo ✅ Server started in background
echo.
echo 🌐 Access from other devices: http://%ip%:8000
echo.
pause
goto menu

:stop
echo.
echo 🛑 Stopping server...
cd /d "C:\Users\User\Desktop\stark"
python server.py stop
echo.
pause
goto menu

:restart
echo.
echo 🔄 Restarting server...
cd /d "C:\Users\User\Desktop\stark"
python server.py stop
timeout /t 2 /nobreak >nul
start /min python server.py
echo ✅ Server restarted
echo.
pause
goto menu

:info
echo.
echo 📋 Server Information
echo ========================================
if exist "C:\Users\User\Desktop\stark\server_info.txt" (
    type "C:\Users\User\Desktop\stark\server_info.txt"
) else (
    echo Server not running or no info file found.
)
echo.
echo To access from other devices, use:
echo - http://%ip%:8000
echo.
pause
goto menu

:open
echo.
echo 🌐 Opening browser...
cd /d "C:\Users\User\Desktop\stark"
if exist "server_info.txt" (
    for /f "tokens=3" %%i in ('findstr "Local IP" server_info.txt') do (
        start http://%%i:8000
        goto menu
    )
) else (
    echo Unable to get IP. Please start the server first.
    pause
    goto menu
)
goto menu

:exit
echo.
echo 👋 Goodbye!
exit