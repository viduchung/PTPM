-- ====================================================================
-- MICROSERVICE 2: PITCH SERVICE (Port 8082) - HOÀNG PHỤ TRÁCH
-- ====================================================================

-- 1. Khởi tạo cơ sở dữ liệu riêng
CREATE DATABASE IF NOT EXISTS pitchos_pitch_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pitchos_pitch_db;

-- 2. Khởi tạo bảng pitches với loại sân và trạng thái định nghĩa bằng ENUM
DROP TABLE IF EXISTS pitches;

CREATE TABLE pitches (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,             -- Tên sân bóng
    -- Định nghĩa cứng các loại sân trong SQL:
    pitch_type ENUM('san_5', 'san_7', 'san_10') NOT NULL DEFAULT 'san_5',
    price_per_hour DECIMAL(12, 2) NOT NULL,  -- Giá thuê mỗi giờ (VND)
    address VARCHAR(255) NOT NULL,          -- Địa chỉ sân
    thumbnail_url VARCHAR(500),             -- URL hình ảnh thumbnail
    google_map_url TEXT,                    -- Link Google Map định vị sân
    -- Định nghĩa cứng trạng thái sân trong SQL:
    status ENUM('hoat_dong', 'bao_tri') NOT NULL DEFAULT 'hoat_dong',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Nạp dữ liệu sân bóng mẫu
INSERT INTO pitches (name, pitch_type, price_per_hour, address, thumbnail_url, google_map_url, status) VALUES
('Sân Bóng Đại Học Thể Thao (Sân 5)', 'san_5', 300000.00, 'Số 123 Đường Cầu Giấy, Quận Cầu Giấy, Hà Nội', 'https://images.unsplash.com/photo-1529900748604-07564a03e7a6?w=800', 'https://maps.google.com/?q=21.0333,105.7999', 'hoat_dong'),
('Sân Bóng Mỹ Đình Stadium (Sân 7)', 'san_7', 500000.00, 'Số 1 Lê Đức Thọ, Phường Mỹ Đình, Quận Nam Từ Liêm, Hà Nội', 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800', 'https://maps.google.com/?q=21.0200,105.7638', 'hoat_dong'),
('Sân Vận Động Trung Tâm (Sân 10)', 'san_10', 800000.00, 'Khu Liên Hợp Thể Thao Tây Hồ, Hà Nội', 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800', 'https://maps.google.com/?q=21.0667,105.8167', 'hoat_dong'),
('Sân Mini Phúc Diễn (Sân 5 - Đang sửa)', 'san_5', 250000.00, 'Phường Phúc Diễn, Quận Bắc Từ Liêm, Hà Nội', 'https://images.unsplash.com/photo-1529900748604-07564a03e7a6?w=800', 'https://maps.google.com/?q=21.0500,105.7500', 'bao_tri');

-- 4. Kiểm tra dữ liệu
SELECT id, name, pitch_type, price_per_hour, address, thumbnail_url, status FROM pitches;
