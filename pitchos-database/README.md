# Nhiệm vụ: Hùng — Quản trị CSDL Phân tán & Tầng Repository

- **Vai trò:** Database Administrator & Backend Data Engineer
- **Tổng điểm phụ trách:** **2,5 Điểm** (0,5đ Lý thuyết + 2,0đ Thực nghiệm)
- **Báo cáo phụ trách:** **Chương 3** (Quản lý dữ liệu, lược đồ ERD từng dịch vụ, kiến trúc Entity/Repository)
- **Thứ tự thực hiện:** **GIAI ĐOẠN 1 (LÀM ĐẦU TIÊN)** — Vì các dịch vụ Spring Boot cần CSDL hợp lệ để kết nối khi khởi động.

---

## 📚 1. Yêu cầu Lý thuyết (0,5 Điểm - Câu 1 Ý 2b)

- [ ] **Giải thích nguyên tắc Database-per-service:**
  - Mỗi microservice chỉ sở hữu và quản trị cơ sở dữ liệu riêng thuộc phạm vi của mình.
  - Tuyệt đối không dịch vụ nào được phép đọc/ghi trực tiếp vào database của dịch vụ khác. Mọi truy xuất đều phải thông qua API công khai của dịch vụ sở hữu.
- [ ] **Phân tích các rủi ro nghiêm trọng khi vi phạm Database-per-service (dùng chung CSDL):**
  - **Ghép nối lược đồ dữ liệu (Schema Coupling):** Thay đổi cấu trúc bảng của một service sẽ làm hỏng hoặc buộc phải sửa đổi các service khác.
  - **Nghẽn bảng / Khóa dòng chéo (Deadlock):** Các transaction từ nhiều dịch vụ cạnh tranh tài nguyên trên cùng bảng gây nghẽn cổ chai.
  - **Phá vỡ tính bao đóng (Encapsulation):** Logic nghiệp vụ bị phân tán và vi phạm ranh giới dịch vụ.
  - **Cản trở việc Scale độc lập:** Không thể tùy biến cơ chế lưu trữ (như cache, NoSQL) hoặc scale riêng biệt cho từng dịch vụ chịu tải cao.

---

## 🛠️ 2. Yêu cầu Thực nghiệm (2,0 Điểm - Câu 2 Ý 3 & hỗ trợ Ý 4)

### 2.1. Khởi tạo 3 CSDL MySQL độc lập
Tạo 3 schema riêng biệt trên MySQL (mặc định port 3306):
1. `pitchos_user_db` (Dành cho Auth & User Service)
2. `pitchos_pitch_db` (Dành cho Pitch Service)
3. `pitchos_booking_db` (Dành cho Booking Service)

### 2.2. Viết 3 Script Khởi tạo CSDL tương ứng 3 Microservice
Trong thư mục `pitchos-database/` có đúng 3 file SQL độc lập:
1. `auth-user-service.sql` (Cấp cho Linh - Auth Service, DB: `pitchos_user_db`)
   - Bảng `users`: `id`, `username`, `email` (Gmail), `password` (BCrypt), `full_name`, `phone`, `role` (`admin`, `chusan`, `user`).
   - Nạp sẵn 3 tài khoản mẫu cho 3 role: `admin`, `chusan`, `user` với mật khẩu mặc định là `123456`.
2. `pitch-service.sql` (Cấp cho Hoàng - Pitch Service, DB: `pitchos_pitch_db`)
   - Bảng `pitches`: `id`, `name` (tên sân), `pitch_type` (loại sân: `san_5`, `san_7`, `san_10`), `price_per_hour` (giá), `address` (địa chỉ), `thumbnail_url` (link ảnh đại diện), `google_map_url` (link Google Maps), `status` (`hoat_dong`, `bao_tri`).
   - Nạp sẵn 4 sân bóng mẫu đa dạng cấu hình.
3. `booking-service.sql` (Cấp cho Nhật - Booking Service, DB: `pitchos_booking_db`)
   - Bảng `bookings`: `user_id` và `pitch_id` chỉ lưu dưới dạng **số nguyên (Logical ID)**, **TUYỆT ĐỐI KHÔNG TẠO KHÓA NGOẠI (Foreign Key) VẬT LÝ** sang DB khác.
   - Trạng thái: `cho_duyet`, `da_duyet`, `tu_choi`.

### 2.3. Xây dựng tầng Entity & Repository JPA
- Định nghĩa các Entity JPA chuẩn annotations: `@Entity`, `@Table`, `@Id`, `@GeneratedValue(strategy = GenerationType.IDENTITY)`.
- Kế thừa `JpaRepository<Entity, Long>`.
- **Câu truy vấn chống trùng lịch thi đấu trong `BookingRepository`:**
  - Viết câu truy vấn kiểm tra giao nhau giữa khoảng thời gian đặt mới và các đơn hiện có (trạng thái khác `tu_choi`):
    ```sql
    SELECT COUNT(b) FROM Booking b 
    WHERE b.pitchId = :pitchId 
      AND b.status <> 'tu_choi'
      AND b.startTime < :endTime 
      AND b.endTime > :startTime
    ```

### 2.4. Bàn giao Cấu hình cho nhóm
- Gửi chuỗi kết nối `application.properties` (JDBC URL, username, password) cho Linh, Hoàng và Nhật.

---

## 📝 3. Viết Báo cáo: Soạn Chương 3
- Quản lý dữ liệu trong kiến trúc phân tán.
- Lược đồ CSDL & ERD của từng dịch vụ độc lập.
- Thiết kế kiến trúc Entity / Repository JPA và giải pháp toàn vẹn dữ liệu phi tập trung.

---

## 🎥 4. Kịch bản Demo Hội đồng (10–15 Phút)
1. Mở phần mềm quản trị CSDL (**DBeaver / MySQL Workbench / Navicat**).
2. Hiển thị 3 schema độc lập `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db` để chứng minh nguyên tắc **Database-per-service**.
3. Sau khi Nhật gọi API đặt sân thành công, thực thi câu lệnh:
   ```sql
   SELECT * FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1;
   ```
4. Chỉ ra bản ghi đã được ghi xuống đĩa cứng với trạng thái `cho_duyet`, đúng `pitch_id`, `user_id` và tổng tiền được tính toán.
5. Chứng minh không có Foreign Key vật lý nào được tạo giữa các database.
