@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================================================
echo        PITCHOS - DUNG NHANH CAC DICH VU SPRING BOOT (8081, 8082, 8083)
echo ========================================================================
echo.

set "PORTS=8081 8082 8083"

for %%p in (%PORTS%) do (
    echo [DANG DUNG] Kiem tra tien trinh tren port %%p...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":%%p "') do (
        set "pid=%%a"
        if defined pid (
            if not "!pid!"=="0" (
                echo   -> Tim thay tien trinh PID !pid! tren port %%p. Dang tat...
                taskkill /F /PID !pid! >nul 2>&1
                if !ERRORLEVEL! equ 0 (
                    echo   -> Da tat thanh cong PID !pid!.
                )
            )
        )
    )
)

echo.
echo ========================================================================
echo [HOAN TAT] Da giai phong toan bo cac port 8081, 8082, 8083!
echo ========================================================================
echo.
pause
