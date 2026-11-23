@echo off
chcp 65001 >nul
echo ========================================================
echo [PITCHOS] KIỂM TRA SỨC KHỎE HỆ THỐNG MICROSERVICES
echo ========================================================
echo.

echo 1. Kiểm tra Service Registry (Eureka Server :8761)...
curl -s -o nul -w "%%{http_code}" http://localhost:8761/actuator/health > temp_status.txt
set /p status_reg=<temp_status.txt
echo    HTTP Status: %status_reg% (Expected: 200)

echo.
echo 2. Kiểm tra Auth & User Service (:8081)...
curl -s -o nul -w "%%{http_code}" http://localhost:8081/actuator/health > temp_status.txt
set /p status_auth=<temp_status.txt
echo    HTTP Status: %status_auth% (Expected: 200)

echo.
echo 3. Kiểm tra Pitch Service Instance 1 (:8082)...
curl -s -o nul -w "%%{http_code}" http://localhost:8082/actuator/health > temp_status.txt
set /p status_pitch1=<temp_status.txt
echo    HTTP Status: %status_pitch1% (Expected: 200)

echo.
echo 4. Kiểm tra Pitch Service Instance 2 (:8084)...
curl -s -o nul -w "%%{http_code}" http://localhost:8084/actuator/health > temp_status.txt
set /p status_pitch2=<temp_status.txt
echo    HTTP Status: %status_pitch2% (Expected: 200)

echo.
echo 5. Kiểm tra Booking Service (:8083)...
curl -s -o nul -w "%%{http_code}" http://localhost:8083/actuator/health > temp_status.txt
set /p status_book=<temp_status.txt
echo    HTTP Status: %status_book% (Expected: 200)

if exist temp_status.txt del temp_status.txt

echo.
echo ========================================================
echo Kết thúc kiểm tra sức khỏe!
echo ========================================================
pause
