# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: HÙNG

> **HỌ VÀ TÊN:** HÙNG  
> **VAI TRÒ:** Phụ trách Quản trị CSDL Phân tán, Entity/Repository JPA & Script CSDL  
> **DỊCH VỤ PHỤ TRÁCH:** Quản trị toàn bộ 3 CSDL MySQL độc lập & Tầng Repository  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,25 / 10,0 Điểm** (0,75đ Lý thuyết + 1,5đ Thực nghiệm)  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 3** (Quản lý dữ liệu, lược đồ ERD từng dịch vụ, kiến trúc Entity/Repository)  
> **THỜI ĐIỂM BẮT ĐẦU:** **GIAI ĐOẠN 1 (LÀM ĐẦU TIÊN CẢ NHÓM)** — Phải hoàn thành CSDL trước thì 3 dịch vụ của Hoàng, Linh, Nhật mới có thể kết nối khi khởi động.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA HÙNG (THEO ĐÚNG ĐỀ BÀI)

### 📘 A. Phần Lý thuyết (0,75 Điểm — Câu 1 Ý 2b)
- [ ] **Giải thích nguyên tắc mỗi dịch vụ quản lý dữ liệu thuộc trách nhiệm của mình (Database-per-service):**
  - Trong kiến trúc Microservices/SOA, mỗi dịch vụ sở hữu độc quyền và chịu trách nhiệm toàn bộ về cơ sở dữ liệu riêng của nó.
  - Dữ liệu của một dịch vụ chỉ có thể được truy xuất từ bên ngoài thông qua giao diện lập trình (API công khai) của chính dịch vụ đó.
- [ ] **Vì sao một dịch vụ không nên truy cập trực tiếp cơ sở dữ liệu của dịch vụ khác?**
  - Vi phạm tính đóng gói (Encapsulation) và ranh giới nghiệp vụ (Service Boundary).
  - Làm lộ cấu trúc lưu trữ nội bộ (Internal Storage Details) ra bên ngoài, khiến việc sửa đổi schema trở nên cực kỳ nguy hiểm.
- [ ] **Phân tích các rủi ro nghiêm trọng khi vi phạm nguyên tắc này (dùng chung CSDL):**
  - **Ghép nối lược đồ dữ liệu (Schema Coupling):** Một thay đổi nhỏ ở bảng của dịch vụ này sẽ làm hỏng hoặc buộc phải refactor hàng loạt dịch vụ khác.
  - **Khóa dòng chéo / Nghẽn cổ chai (Deadlock & Contention):** Các transaction từ nhiều dịch vụ cạnh tranh tài nguyên trên cùng một bảng vật lý, dẫn đến nghẽn tắc hiệu năng và sập hệ thống.
  - **Cản trở mở rộng độc lập (Independent Scaling):** Không thể scale riêng DB chịu tải lớn hoặc áp dụng công nghệ lưu trữ linh hoạt (Polyglot Persistence - ví dụ kết hợp Redis/MongoDB khi cần).

---

### 💻 B. Phần Thực nghiệm (1,5 Điểm — Câu 2 Ý 3)
- [ ] **Khởi tạo 3 CSDL MySQL độc lập:**
  1. `pitchos_user_db` (Dành cho Hoàng - Auth Service)
  2. `pitchos_pitch_db` (Dành cho Linh - Pitch Service)
  3. `pitchos_booking_db` (Dành cho Nhật - Booking Service)
- [ ] **Soạn thảo 3 Script SQL độc lập tương ứng 3 Microservice:**
  1. `auth-user-service.sql` (Cấp cho Hoàng - `pitchos_user_db`):
     - Bảng `users`: `id`, `username`, `email` (Gmail), `password` (BCrypt), `full_name`, `phone`, `role` (`admin`, `chusan`, `user`).
     - Nạp sẵn 3 tài khoản mẫu cho 3 role với mật khẩu mặc định `123456`.
  2. `pitch-service.sql` (Cấp cho Linh - `pitchos_pitch_db`):
     - Bảng `pitches`: `id`, `name`, `pitch_type` (`san_5`, `san_7`, `san_10`), `price_per_hour`, `address`, `thumbnail_url`, `google_map_url`, `status` (`hoat_dong`, `bao_tri`).
     - Nạp sẵn 4 sân bóng mẫu đa dạng cấu hình.
  3. `booking-service.sql` (Cấp cho Nhật - `pitchos_booking_db`):
     - Bảng `bookings`: `id`, `user_id`, `pitch_id`, `start_time`, `end_time`, `total_price`, `status` (`cho_duyet`, `da_duyet`, `tu_choi`).
     - ⚠️ **QUY TẮC CỐT LÕI:** Lưu `user_id` và `pitch_id` dưới dạng số nguyên (Logical ID), **TUYỆT ĐỐI KHÔNG TẠO KHÓA NGOẠI (Foreign Key) VẬT LÝ** sang DB khác.
- [ ] **Xây dựng cấu trúc mô hình thực thể Entity & Repository JPA:**
  - Định nghĩa các Entity JPA chuẩn annotations: `@Entity`, `@Table`, `@Id`, `@GeneratedValue(strategy = GenerationType.IDENTITY)`.
  - Định nghĩa các interfaces kế thừa `JpaRepository`.
- [ ] **Viết câu truy vấn chống trùng lịch thi đấu trong `BookingRepository`:**
  - Logic toán học kiểm tra giao thoa giữa 2 khoảng thời gian và loại trừ các đơn bị từ chối:
    ```sql
    SELECT COUNT(b) FROM Booking b 
    WHERE b.pitchId = :pitchId 
      AND b.status <> 'tu_choi'
      AND b.startTime < :endTime 
      AND b.endTime > :startTime
    ```
- [ ] **Bảo đảm tính độc lập dữ liệu & Kiểm tra kết quả ghi đĩa:**
  - Đảm bảo mỗi dịch vụ chỉ cấu hình datasource trỏ vào DB của chính mình.
  - Phối hợp với Nhật: Sau khi Nhật gọi API tạo đơn thành công, thực thi câu lệnh SQL kiểm tra dữ liệu đã lưu đĩa cứng.
- [ ] **Bàn giao cấu hình cho cả nhóm:**
  - Cung cấp JDBC URL, username, password trong file master `.env` và `application.properties` cho Hoàng, Linh, Nhật.

---

### 📑 C. Phần Viết Báo cáo (Chương 3)
- [ ] **Biên soạn toàn bộ Chương 3 (Quản lý dữ liệu):**
  - Quản trị dữ liệu trong kiến trúc vi dịch vụ (Microservices Data Management).
  - Sơ đồ dữ liệu và lược đồ ERD độc lập của 3 dịch vụ.
  - Thiết kế kiến trúc Entity / Repository JPA và giải pháp toàn vẹn dữ liệu phi tập trung không dùng Foreign Key vật lý.

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Hùng trực tiếp thao tác)
- [ ] **Bước 1:** Mở phần mềm quản trị CSDL (**DBeaver / MySQL Workbench / Navicat**).
- [ ] **Bước 2:** Show 3 schema độc lập `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db` trên màn hình để chứng minh kiến trúc **Database-per-service** và tính bao đóng.
- [ ] **Bước 3:** Chứng minh rõ trong bảng `bookings` chỉ lưu ID dạng số nguyên `pitch_id`, `user_id`, không có Foreign Key vật lý ràng buộc chéo.
- [ ] **Bước 4:** Sau khi Nhật thao tác gọi API tạo đơn đặt sân ở Bước 4 kịch bản, thực thi ngay câu lệnh:
  ```sql
  SELECT * FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1;
  ```
- [ ] **Bước 5:** Phân tích cho hội đồng thấy đơn hàng đã ghi vững chắc xuống đĩa cứng với trạng thái `cho_duyet`, `total_price` được tính toán chuẩn xác từ đơn giá của Pitch Service.
