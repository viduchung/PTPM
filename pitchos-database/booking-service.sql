-- ====================================================================
-- MICROSERVICE 3: BOOKING SERVICE (Port 8083) - NHẬT PHỤ TRÁCH
-- ====================================================================

-- 1. Khởi tạo cơ sở dữ liệu riêng
CREATE DATABASE IF NOT EXISTS pitchos_booking_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pitchos_booking_db;

-- 2. Khởi tạo bảng bookings với Trạng thái định nghĩa trực tiếp bằng ENUM
DROP TABLE IF EXISTS bookings;

CREATE TABLE bookings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- ⚠️ QUY TẮC DATABASE-PER-SERVICE:
    -- Chỉ lưu logical ID dạng số nguyên (BIGINT).
    -- TUYỆT ĐỐI KHÔNG TẠO FOREIGN KEY SANG DATABASE KHÁC!
    user_id BIGINT NOT NULL,        -- ID người dùng đặt sân (logic từ pitchos_user_db)
    pitch_id BIGINT NOT NULL,       -- ID sân bóng (logic từ pitchos_pitch_db)
    
    start_time DATETIME NOT NULL,   -- Thời gian bắt đầu đá
    end_time DATETIME NOT NULL,     -- Thời gian kết thúc đá
    total_price DECIMAL(12, 2) NOT NULL, -- Tổng tiền thuê = số giờ * giá sân
    
    -- Định nghĩa cứng trạng thái trực tiếp trong SQL bằng ENUM:
    status ENUM('cho_duyet', 'da_duyet', 'tu_choi') NOT NULL DEFAULT 'cho_duyet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Nạp 1 đơn đặt mẫu để kiểm thử:
-- user_id = 3 (khách hàng 'user' trong pitchos_user_db) đặt pitch_id = 1 (Sân 5)
INSERT INTO bookings (user_id, pitch_id, start_time, end_time, total_price, status) VALUES
(3, 1, '2026-10-27 18:00:00', '2026-10-27 19:30:00', 450000.00, 'cho_duyet');

-- 4. Kiểm tra dữ liệu
SELECT id, user_id, pitch_id, start_time, end_time, total_price, status, created_at FROM bookings;
