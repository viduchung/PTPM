-- ====================================================================
-- MICROSERVICE 3: BOOKING SERVICE (Port 8083) - DOCKER INIT SCRIPT
-- Cơ sở dữ liệu: pitchos_booking_db
-- Phụ trách: HÙNG (Database Administrator)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS pitchos_booking_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pitchos_booking_db;

DROP TABLE IF EXISTS bookings;

CREATE TABLE bookings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    
    -- ⚠️ TRIẾT LÝ DATABASE-PER-SERVICE:
    -- Chỉ lưu Logical ID dạng số nguyên (BIGINT), không tạo Foreign Key vật lý ràng buộc chéo!
    user_id BIGINT NOT NULL,        -- ID người dùng đặt sân (logic từ pitchos_user_db)
    pitch_id BIGINT NOT NULL,       -- ID sân bóng (logic từ pitchos_pitch_db)
    
    start_time DATETIME NOT NULL,   -- Thời gian bắt đầu đá
    end_time DATETIME NOT NULL,     -- Thời gian kết thúc đá
    total_price DECIMAL(12, 2) NOT NULL, -- Tổng tiền thuê = số giờ * giá sân
    
    status ENUM('cho_duyet', 'da_duyet', 'tu_choi') NOT NULL DEFAULT 'cho_duyet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Đánh index logic để tối ưu hóa truy vấn kiểm tra trùng lịch:
    INDEX idx_booking_pitch_time (pitch_id, start_time, end_time, status)
);

-- Nạp sẵn 1 đơn đặt mẫu để phục vụ kiểm thử
INSERT INTO bookings (user_id, pitch_id, start_time, end_time, total_price, status) VALUES
(3, 1, '2026-10-27 18:00:00', '2026-10-27 19:30:00', 450000.00, 'cho_duyet');
