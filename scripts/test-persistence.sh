#!/bin/bash
# ========================================================
# [PITCHOS] KIỂM TRA BẢO TOÀN DỮ LIỆU QUA DOCKER VOLUME
# ========================================================

echo "========================================================"
echo "[PITCHOS] KIỂM TRA BẢO TOÀN DỮ LIỆU QUA DOCKER VOLUME"
echo "========================================================"
echo ""

echo "[BƯỚC 1] Đếm số lượng đơn đặt sân hiện có trong MySQL..."
docker exec -i mysql-booking mysql -uroot -p123456 -e "SELECT count(*) AS total_bookings FROM pitchos_booking_db.bookings;" 2>/dev/null || \
docker exec -i pitchos-mysql mysql -uroot -p123456 -e "SELECT count(*) AS total_bookings FROM pitchos_booking_db.bookings;" 2>/dev/null

echo ""
echo "[BƯỚC 2] Dừng toàn bộ hệ thống bằng Docker Compose (KHÔNG DÙNG cờ -v)..."
echo "Lệnh: docker compose down"
docker compose down

echo ""
echo "[BƯỚC 3] Khởi động lại toàn bộ hệ thống..."
echo "Lệnh: docker compose up -d"
docker compose up -d

echo ""
echo "Đang chờ MySQL khởi động lại (15 giây)..."
sleep 15

echo ""
echo "[BƯỚC 4] Kiểm tra lại dữ liệu đơn đặt sân sau khi restart..."
docker exec -i mysql-booking mysql -uroot -p123456 -e "SELECT id, user_id, pitch_id, total_price, status, created_at FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 5;" 2>/dev/null || \
docker exec -i pitchos-mysql mysql -uroot -p123456 -e "SELECT id, user_id, pitch_id, total_price, status, created_at FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 5;" 2>/dev/null

echo ""
echo "========================================================"
echo "Nếu dữ liệu các đơn cũ vẫn xuất hiện đầy đủ:"
echo "=> KẾT QUẢ: ĐẠT! Dữ liệu được bảo toàn bền vững qua Named Volume."
echo "========================================================"
