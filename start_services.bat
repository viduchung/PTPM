@echo off
setlocal
chcp 65001 >nul

echo ========================================================================
echo        PITCHOS - HE THONG DAT SAN BONG DA MINI (SOA / MICROSERVICES)
echo                  KHOI DONG DONG THOI 3 DICH VU SPRING BOOT
echo ========================================================================
echo.

:: 1. Thiet lap thu muc goc
set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

:: 2. Kiem tra Java JDK
where java >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LOI] Khong tim thay Java! Vui long cai dat JDK 17+ va them vao PATH.
    pause
    exit /b 1
)

:: 3. Kiem tra Apache Maven
where mvn >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [LOI] Khong tim thay Maven (mvn)! Vui long them Maven vao PATH.
    pause
    exit /b 1
)

:: 4. Doc file cau hinh .env neu ton tai
if exist "%ROOT_DIR%.env" (
    echo [INFO] Dang nap bien moi truong tu file .env...
    for /f "usebackq eol=# tokens=1* delims==" %%a in ("%ROOT_DIR%.env") do (
        set "%%a=%%b"
    )
    echo [OK] Da nap xong cau hinh tu file .env!
) else (
    echo [CANH BAO] Khong tim thay file .env, su dung cau hinh mac dinh.
)
echo.

:: 5. Kiem tra cong 3306 (MySQL Server)
echo [KIEM TRA] Kiem tra ket noi MySQL tren cong 3306...
netstat -ano | findstr /R /C:":3306 " >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo **********************************************************************
    echo [CANH BAO] Cong 3306 chua mo! MySQL Server co the chua duoc khoi dong.
    echo Vui long mo Laragon / XAMPP / MySQL Service va dam bao port 3306 hoat dong.
    echo **********************************************************************
    echo.
) else (
    echo [OK] MySQL Server dang chay tren cong 3306!
)
echo.

:: 6. Thiet lap gia tri mac dinh neu chua co
if not defined AUTH_SERVICE_PORT set AUTH_SERVICE_PORT=8081
if not defined PITCH_SERVICE_PORT set PITCH_SERVICE_PORT=8082
if not defined BOOKING_SERVICE_PORT set BOOKING_SERVICE_PORT=8083

echo ========================================================================
echo DANG KHOI CHAY 3 DICH VU TRONG 3 CUA SO CMD RIENG BIET:
echo   1. Auth Service    : http://localhost:%AUTH_SERVICE_PORT%/swagger-ui.html
echo   2. Pitch Service   : http://localhost:%PITCH_SERVICE_PORT%/swagger-ui.html
echo   3. Booking Service : http://localhost:%BOOKING_SERVICE_PORT%/swagger-ui.html
echo ========================================================================
echo.

:: 7. Khoi dong Microservice 1: Auth Service (Port 8081)
echo [1/3] Dang khoi dong PitchOS Auth Service (Port %AUTH_SERVICE_PORT%)...
start "PitchOS - Auth & User Service [Port %AUTH_SERVICE_PORT%]" cmd /k "chcp 65001 >nul && title PitchOS - Auth Service [Port %AUTH_SERVICE_PORT%] && cd /d "%ROOT_DIR%pitchos-auth-service" && echo ==================================================== && echo   DANG CHAY AUTH SERVICE TREN PORT %AUTH_SERVICE_PORT%... && echo ==================================================== && mvn spring-boot:run"

:: 8. Khoi dong Microservice 2: Pitch Service (Port 8082)
echo [2/3] Dang khoi dong PitchOS Pitch Service (Port %PITCH_SERVICE_PORT%)...
start "PitchOS - Pitch Service [Port %PITCH_SERVICE_PORT%]" cmd /k "chcp 65001 >nul && title PitchOS - Pitch Service [Port %PITCH_SERVICE_PORT%] && cd /d "%ROOT_DIR%pitchos-pitch-service" && echo ==================================================== && echo   DANG CHAY PITCH SERVICE TREN PORT %PITCH_SERVICE_PORT%... && echo ==================================================== && mvn spring-boot:run"

:: 9. Khoi dong Microservice 3: Booking Service (Port 8083)
echo [3/3] Dang khoi dong PitchOS Booking Service (Port %BOOKING_SERVICE_PORT%)...
start "PitchOS - Booking Service [Port %BOOKING_SERVICE_PORT%]" cmd /k "chcp 65001 >nul && title PitchOS - Booking Service [Port %BOOKING_SERVICE_PORT%] && cd /d "%ROOT_DIR%pitchos-booking-service" && echo ==================================================== && echo   DANG CHAY BOOKING SERVICE TREN PORT %BOOKING_SERVICE_PORT%... && echo ==================================================== && mvn spring-boot:run"

echo.
echo ========================================================================
echo [HOAN TAT] Ca 3 microservice da duoc lenh khoi dong thanh cong!
echo.
echo Cac duong link kiem thu Swagger UI:
echo   - Auth API    : http://localhost:%AUTH_SERVICE_PORT%/swagger-ui.html
echo   - Pitch API   : http://localhost:%PITCH_SERVICE_PORT%/swagger-ui.html
echo   - Booking API : http://localhost:%BOOKING_SERVICE_PORT%/swagger-ui.html
echo.
echo Luu y:
echo   - Giu nguyen 3 cua so CMD dang chay de quan sat nhat ky (logs).
echo   - Muon dung rieng dich vu nao (vi du test loi 503), chi can dong cua so do.
echo   - Hoac chay file stop_services.bat de dung nhanh tat ca dich vu.
echo ========================================================================
echo.
pause
