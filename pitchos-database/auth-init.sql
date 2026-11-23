-- ====================================================================
-- MICROSERVICE 1: AUTH & USER SERVICE (Port 8081) - DOCKER INIT SCRIPT
-- Cơ sở dữ liệu: pitchos_user_db
-- Phụ trách: HÙNG (Database Administrator)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS pitchos_user_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pitchos_user_db;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role ENUM('admin', 'chusan', 'user') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nạp sẵn 3 tài khoản mẫu đại diện cho 3 Role: admin, chusan, user
-- Mật khẩu mặc định: 123456
INSERT INTO users (username, email, password, full_name, phone, role) VALUES
('admin', 'admin@gmail.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Quản Trị Viên Hệ Thống', '0901112222', 'admin'),
('chusan', 'chusan@gmail.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Trần Văn Chủ Sân', '0987654321', 'chusan'),
('user', 'user@gmail.com', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'Nguyễn Văn Khách Hàng', '0912345678', 'user');
