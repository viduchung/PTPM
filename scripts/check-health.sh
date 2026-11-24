#!/bin/bash
# ========================================================
# [PITCHOS] KIỂM TRA SỨC KHỎE HỆ THỐNG MICROSERVICES
# ========================================================

echo "========================================================"
echo "[PITCHOS] KIỂM TRA SỨC KHỎE HỆ THỐNG MICROSERVICES"
echo "========================================================"
echo ""

check_service() {
    local name="$1"
    local url="$2"
    local code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$code" -eq 200 ]; then
        echo "✅ $name: HTTP $code (UP)"
    else
        echo "❌ $name: HTTP $code (FAILED)"
    fi
}

check_service "1. Service Registry (:8761)" "http://localhost:8761/actuator/health"
check_service "2. Auth Service     (:8081)" "http://localhost:8081/actuator/health"
check_service "3. Pitch Instance 1 (:8082)" "http://localhost:8082/actuator/health"
check_service "4. Pitch Instance 2 (:8084)" "http://localhost:8084/actuator/health"
check_service "5. Booking Service  (:8083)" "http://localhost:8083/actuator/health"

echo ""
echo "========================================================"
echo "Kết thúc kiểm tra sức khỏe!"
echo "========================================================"
