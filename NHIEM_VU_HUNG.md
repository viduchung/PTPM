# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: HÙNG

> **HỌ VÀ TÊN:** HÙNG  
> **VAI TRÒ:** Phụ trách Quản trị CSDL Phân tán, Entity/Repository JPA & Script CSDL  
> **DỊCH VỤ PHỤ TRÁCH:** Quản trị toàn bộ 3 CSDL MySQL độc lập & Tầng Repository  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,5 / 10,0 Điểm**  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 3**  
> **THỜI ĐIỂM BẮT ĐẦU:** **GIAI ĐOẠN 1 (LÀM ĐẦU TIÊN CẢ NHÓM)** — Phải hoàn thành CSDL trước thì 3 dịch vụ của Linh, Hoàng, Nhật mới có thể khởi chạy.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA HÙNG

### 📘 A. Phần Lý thuyết (0,5 Điểm - Câu 1 Ý 2b)
- [ ] **Giải thích nguyên tắc Database-per-service:**
  - Mỗi dịch vụ chỉ sở hữu một CSDL riêng biệt, đóng gói hoàn toàn dữ liệu.
  - Tuyệt đối không dịch vụ nào được phép đọc/ghi trực tiếp vào DB của dịch vụ khác mà phải giao tiếp qua API.
- [ ] **Phân tích các rủi ro khi vi phạm Database-per-service (dùng chung database):**
  - *Ghép nối lược đồ dữ liệu (Schema Coupling):* Sửa đổi bảng của dịch vụ này sẽ gây lỗi cho các dịch vụ khác.
  - *Nghẽn bảng / Deadlock chéo:* Transaction từ nhiều ứng dụng khác nhau cạnh tranh khóa dòng dữ liệu.
  - *Phá vỡ tính bao đóng (Encapsulation):* Vi phạm ranh giới dịch vụ nghiệp vụ.
  - *Cản trở mở rộng độc lập (Scaling):* Không thể scale riêng DB chịu tải cao hoặc áp dụng đa dạng công nghệ lưu trữ (Polyglot Persistence).

---

### 💻 B. Phần Thực nghiệm (2,0 Điểm - Câu 2 Ý 3 & hỗ trợ Ý 4)
- [ ] **Khởi tạo 3 CSDL MySQL độc lập:**
  1. `pitchos_user_db` (dành cho Linh - Auth Service)
  2. `pitchos_pitch_db` (dành cho Hoàng - Pitch Service)
  3. `pitchos_booking_db` (dành cho Nhật - Booking Service)
- [ ] **Soạn thảo 3 Script SQL độc lập tương ứng với 3 Microservice:**
  1. `auth-user-service.sql` (cho Linh - `pitchos_user_db`):
     - Tạo bảng `users`: `username`, `email` (Gmail), `password` (băm BCrypt), `full_name`, `phone`, `role` (`admin`, `chusan`, `user`).
     - Nạp sẵn 3 tài khoản mẫu với mật khẩu mặc định `123456`.
  2. `pitch-service.sql` (cho Hoàng - `pitchos_pitch_db`):
     - Tạo bảng `pitches`: `name`, `pitch_type` (`san_5`, `san_7`, `san_10`), `price_per_hour`, `address`, `thumbnail_url`, `google_map_url`, `status` (`hoat_dong`, `bao_tri`).
     - Nạp sẵn 4 sân bóng mẫu.
  3. `booking-service.sql` (cho Nhật - `pitchos_booking_db`):
     - Tạo bảng `bookings`: `user_id`, `pitch_id`, `start_time`, `end_time`, `total_price`, `status` (`cho_duyet`, `da_duyet`, `tu_choi`).
     - Lưu `user_id` và `pitch_id` dưới dạng số nguyên (Logical ID).  
     - ⚠️ **QUY TẮC CỐT LÕI:** Tuyệt đối **KHÔNG TẠO FOREIGN KEY VẬT LÝ** sang `pitchos_user_db` hay `pitchos_pitch_db`.
- [ ] **Xây dựng tầng truy cập dữ liệu (Entity & Repository JPA):**
  - Xây dựng các lớp Entity chuẩn `@Entity`, `@Table`, `@Id`.
  - Xây dựng interfaces kế thừa `JpaRepository`.
- [ ] **Viết câu truy vấn chống trùng lịch thi đấu trong `BookingRepository`:**
  - Logic: Kiểm tra nếu khoảng thời gian mới giao với khoảng thời gian đã được đặt (và trạng thái khác `tu_choi`):
    `b.pitchId = :pitchId AND b.status <> 'tu_choi' AND b.startTime < :newEndTime AND b.endTime > :newStartTime`
- [ ] **Bàn giao cấu hình CSDL:**
  - Cung cấp JDBC URL, username, password cho cả nhóm trong `application.properties`.

---

### 📑 C. Phần Viết Báo cáo (Chương 3)
- [ ] **Biên soạn toàn bộ Chương 3:**
  - Quản lý dữ liệu trong kiến trúc vi dịch vụ (Microservices Data Management).
  - Lược đồ CSDL và sơ đồ ERD độc lập của 3 dịch vụ.
  - Thiết kế kiến trúc Entity / Repository JPA và giải pháp đảm bảo tính toàn vẹn dữ liệu.

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Hùng trực tiếp thao tác)
- [ ] **Bước 1:** Mở công cụ quản trị CSDL (**DBeaver / MySQL Workbench / Navicat**).
- [ ] **Bước 2:** Show 3 schema `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db` độc lập, chứng minh tính bao đóng và không có khóa ngoại vật lý chéo.
- [ ] **Bước 3:** Sau khi Nhật gọi API tạo đơn thành công, thực thi câu lệnh SQL:
  ```sql
  SELECT * FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1;
  ```
- [ ] **Bước 4:** Chứng minh bản ghi đơn đặt sân đã được lưu vững chắc xuống đĩa cứng với trạng thái `cho_duyet`, đúng `pitch_id`, `user_id` và `total_price`.
