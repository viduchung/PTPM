-- ====================================================================
-- MICROSERVICE 1: AUTH & USER SERVICE (Port 8081) - LINH PHỤ TRÁCH
-- ====================================================================

-- 1. Khởi tạo cơ sở dữ liệu riêng
CREATE DATABASE IF NOT EXISTS pitchos_user_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pitchos_user_db;

-- 2. Khởi tạo bảng users với Role định nghĩa trực tiếp bằng ENUM
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,     -- Gmail người dùng
    password VARCHAR(255) NOT NULL,         -- Mật khẩu băm BCrypt
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    -- Định nghĩa cứng 3 role trực tiếp trong SQL bằng ENUM:
    role ENUM('admin', 'chusan', 'user') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Nạp sẵn 3 tài khoản mẫu đại diện cho 3 Role: admin, chusan, user
-- Mật khẩu mặc định: 123456
-- Chuỗi mã hóa BCrypt của '123456': $2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
INSERT INTO users (username, email, password, full_name, phone, role) VALUES
('admin', 'admin@gmail.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Quản Trị Viên Hệ Thống', '0901112222', 'admin'),
('chusan', 'chusan@gmail.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Trần Văn Chủ Sân', '0987654321', 'chusan'),
('user', 'user@gmail.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Nguyễn Văn Khách Hàng', '0912345678', 'user');

-- 4. Kiểm tra dữ liệu
SELECT id, username, email, full_name, role, created_at FROM users;
