# PHẦN 2.1b: THIẾT KẾ DỮ LIỆU PHÂN TÁN VÀ BẢNG MÔ TẢ DỊCH VỤ PITCHOS
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)  
**Sinh viên thực hiện:** HÙNG  
**Mục tiêu điểm số:** 0,5 / 1,0 Điểm Mục 2.1 (Phân tích & thiết kế kiến trúc)

---

## 1. NGUYÊN TẮC DATABASE-PER-SERVICE VÀ QUẢN TRỊ DỮ LIỆU PHÂN TÁN

Trong kiến trúc hướng dịch vụ của hệ thống PitchOS, nhóm áp dụng triệt để mẫu thiết kế **Database-per-Service (Mỗi dịch vụ sở hữu một cơ sở dữ liệu riêng biệt)**:

```
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│  pitchos-auth-service   │   │  pitchos-pitch-service  │   │ pitchos-booking-service │
└────────────┬────────────┘   └────────────┬────────────┘   └────────────┬────────────┘
             │ độc quyền                   │ độc quyền                   │ độc quyền
             ▼                             ▼                             ▼
┌─────────────────────────┐   ┌─────────────────────────┐   ┌─────────────────────────┐
│     pitchos_user_db     │   │    pitchos_pitch_db     │   │   pitchos_booking_db    │
│  (Volume: auth_data)    │   │  (Volume: pitch_data)   │   │ (Volume: booking_data)  │
└─────────────────────────┘   └─────────────────────────┘   └─────────────────────────┘
```

### 1.1. Luận giải lý do kỹ thuật không dùng chung CSDL
Nếu dùng chung một cơ sở dữ liệu (Shared Database), hệ thống sẽ đối mặt với 4 rủi ro kỹ thuật nghiêm trọng:
1. **Ghép nối lược đồ (Schema Coupling):** Một thay đổi nhỏ ở bảng `users` hoặc `pitches` có thể làm hỏng logic của Booking Service, khiến các nhóm phát triển không thể triển khai (Deploy) độc lập.
2. **Khóa dòng chéo (Cross-Service Deadlock):** Hai transaction từ hai service khác nhau tranh chấp tài nguyên trên cùng một bảng sẽ gây nghẽn toàn bộ hệ thống.
3. **Phá vỡ tính bao đóng (Violating Encapsulation):** Service này có thể vô tình sửa đổi trực tiếp dữ liệu nghiệp vụ của service khác mà không thông qua các luật kiểm tra (Business Validation).
4. **Cản trở mở rộng đa dạng (Polyglot Persistence):** Khi cần nâng cấp Booking Service sang CSDL NoSQL (MongoDB/Redis) để xử lý lượng đơn tải cao, hệ thống không thể làm được nếu còn phụ thuộc vào CSDL chung.

### 1.2. Triết lý sử dụng Logical ID (Khóa ngoại logic) thay cho Foreign Key vật lý
* Trong bảng `bookings` thuộc cơ sở dữ liệu `pitchos_booking_db`:
  ```sql
  CREATE TABLE bookings (
      id BIGINT AUTO_INCREMENT PRIMARY KEY,
      user_id BIGINT NOT NULL,        -- Logical ID trỏ sang pitchos_user_db
      pitch_id BIGINT NOT NULL,       -- Logical ID trỏ sang pitchos_pitch_db
      start_time DATETIME NOT NULL,
      end_time DATETIME NOT NULL,
      total_price DECIMAL(12, 2) NOT NULL,
      status ENUM('cho_duyet', 'da_duyet', 'tu_choi') NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
* **Không tạo ràng buộc `FOREIGN KEY (pitch_id) REFERENCES pitches(id)`**:
  * Khi các cơ sở dữ liệu được container hóa và chạy độc lập trên các container MySQL khác nhau trong mạng Docker, việc tạo Foreign Key vật lý qua mạng là bất khả thi.
  * Tính toàn vẹn dữ liệu được đảm bảo ở **Tầng ứng dụng (Application Layer)**: Trước khi tạo đơn, Booking Service gọi OpenFeign sang Pitch Service để xác thực sự tồn tại và tính hợp lệ của `pitchId`. Nếu sân không tồn tại, trả lỗi ngay lập tức `404 Not Found` và hủy transaction.

---

## 2. BẢNG MÔ TẢ CHI TIẾT CÁC MICROSERVICES TRONG HỆ THỐNG PITCHOS

Bảng mô tả đầy đủ 4 microservices theo đúng yêu cầu đề bài KT2:

| Tên Dịch Vụ | Vai Trò Kiến Trúc | Số Instance | CSDL Sở Hữu & Volume | API Tiêu Biểu | Dịch Vụ Phụ Thuộc | Trách Nhiệm Nghiệp Vụ Cốt Lõi |
|---|:---:|:---:|---|---|---|---|
| **`pitchos-service-registry`** | Service Registry (Eureka Server) | **1** | Không sử dụng CSDL | `GET /eureka/apps`<br>`/actuator/health` | Không phụ thuộc | • Quản lý danh bạ địa chỉ mạng của tất cả các service instances.<br>• Tiếp nhận heartbeat định kỳ (30s) và hủy đăng ký tự động khi service ngừng hoạt động. |
| **`pitchos-auth-service`** | Authentication & User Provider | **1** | `pitchos_user_db`<br>*(Volume: `mysql_auth_data`)* | `POST /api/v1/auth/register`<br>`POST /api/v1/auth/login`<br>`GET /api/v1/users/{id}` | Eureka Server | • Đăng ký, đăng nhập tài khoản người dùng.<br>• Mã hóa mật khẩu BCrypt.<br>• Cấp phát và xác thực chữ ký Bearer JWT Token với 3 vai trò: `admin`, `chusan`, `user`. |
| **`pitchos-pitch-service`** | Business Service (Provider) | **2**<br>(Port 8082 & 8084) | `pitchos_pitch_db`<br>*(Volume: `mysql_pitch_data` - dùng chung cho 2 instances)* | `GET /api/v1/pitches/{id}`<br>`GET /api/v1/pitches`<br>`POST /api/v1/pitches`<br>`GET /api/v1/instance-info` | Eureka Server | • Quản lý danh mục sân bóng mini, bảng giá theo giờ và trạng thái hoạt động (`hoat_dong`, `bao_tri`).<br>• Cung cấp endpoint cho Consumer tra cứu đơn giá và kiểm tra instance phục vụ. |
| **`pitchos-booking-service`** | Business Service (Consumer) | **1** | `pitchos_booking_db`<br>*(Volume: `mysql_booking_data`)* | `POST /api/v1/bookings`<br>`GET /api/v1/bookings/my-bookings`<br>`PATCH /api/v1/bookings/{id}/status`<br>`GET /api/v1/bookings/pitch-instance` | • Eureka Server<br>• `pitchos-pitch-service` | • Tiếp nhận yêu cầu đặt sân từ khách hàng.<br>• Gọi OpenFeign sang Pitch Service theo Service ID để lấy đơn giá và kiểm tra trạng thái sân.<br>• Chạy thuật toán truy vấn chống trùng lịch thi đấu.<br>• Lưu trữ đơn đặt sân với trạng thái ban đầu `cho_duyet`. |
