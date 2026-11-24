# BIÊN BẢN KIỂM THỬ TRIỂN KHAI VÀ VẬN HÀNH HỆ THỐNG (DEP01 – DEP08)
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices 2026)  
**Hệ thống:** PitchOS — Hệ thống Quản lý và Đặt sân bóng mini trực tuyến  
**Kỹ sư thực hiện:** HÙNG — Phụ trách Cơ sở dữ liệu & Quản trị Vận hành  
**Mục tiêu:** Kiểm chứng toàn bộ yêu cầu về Container hóa, Healthcheck, Service Discovery, Chịu lỗi và Bảo toàn dữ liệu theo chuẩn TH8.

---

## 1. MÔI TRƯỜNG THỰC HIỆN KIỂM THỬ

* **Máy chủ kiểm thử:** Windows 11 Pro 64-bit / WSL2
* **Nền tảng ảo hóa:** Docker Desktop (Engine Version 26.x, Compose v2.x)
* **Mạng nội bộ:** `pitchos-network` (bridge driver)
* **Bộ nhớ RAM cấp phát:** Tối thiểu 6 GB
* **Số lượng container:** 8 container (3 MySQL 8.0, 1 Eureka Server, 4 Spring Boot Microservices)

---

## 2. KẾT QUẢ CHI TIẾT BỘ KIỂM THỬ VẬN HÀNH (DEP01 – DEP08)

### DEP01: Khởi tạo toàn bộ hệ thống bằng Docker Compose
* **Mục tiêu:** Kiểm tra khả năng đóng gói image multi-stage và điều phối 8 container khởi chạy thành công từ một lệnh duy nhất.
* **Lệnh thực hiện:**
  ```bash
  docker compose up -d --build
  docker compose ps
  ```
* **Kết quả kỳ vọng:** Cột `STATUS` của toàn bộ 8 container đều hiển thị `Up ... (healthy)`.
* **Kết quả thực tế:**
  ```text
  NAME                       IMAGE                             COMMAND                  SERVICE                    STATUS
  mysql-auth                 mysql:8.0                         "docker-entrypoint.s…"   mysql-auth                 Up (healthy)
  mysql-pitch                mysql:8.0                         "docker-entrypoint.s…"   mysql-pitch                Up (healthy)
  mysql-booking              mysql:8.0                         "docker-entrypoint.s…"   mysql-booking              Up (healthy)
  pitchos-service-registry   pitchos-service-registry:latest   "java -jar /app/app.…"   pitchos-service-registry   Up (healthy)
  pitchos-auth-service       pitchos-auth-service:latest       "java -jar /app/app.…"   pitchos-auth-service       Up (healthy)
  pitchos-pitch-service-1    pitchos-pitch-service:latest      "sh -c 'java $JAVA_O…"   pitchos-pitch-service-1    Up (healthy)
  pitchos-pitch-service-2    pitchos-pitch-service:latest      "sh -c 'java $JAVA_O…"   pitchos-pitch-service-2    Up (healthy)
  pitchos-booking-service    pitchos-booking-service:latest    "java -jar /app/app.…"   pitchos-booking-service    Up (healthy)
  ```
* **Đánh giá:** ✅ **ĐẠT (PASS)**. Toàn bộ 8 container đều đạt trạng thái `healthy`.

---

### DEP02: Giám sát Trạng thái Sức khỏe nội tại (Application Healthcheck)
* **Mục tiêu:** Xác minh các endpoint Spring Boot Actuator `/actuator/health` hoạt động chính xác và phản hồi HTTP `200 OK`.
* **Lệnh thực hiện:** Chạy file kịch bản `scripts/check-health.bat` hoặc dùng `curl`:
  ```bash
  curl http://localhost:8761/actuator/health
  curl http://localhost:8081/actuator/health
  curl http://localhost:8082/actuator/health
  curl http://localhost:8084/actuator/health
  curl http://localhost:8083/actuator/health
  ```
* **Kết quả kỳ vọng:** Toàn bộ 5 endpoints đều trả về JSON: `{"status":"UP"}`.
* **Kết quả thực tế:** Cả 5 dịch vụ đều trả về HTTP `200` với body `{"status":"UP"}`.
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

### DEP03: Giám sát Nhật ký hoạt động liên dịch vụ (Distributed Logging)
* **Mục tiêu:** Đọc log đồng thời từ 2 container Booking và Pitch-1 để quan sát luồng trao đổi dữ liệu khi có request đặt sân.
* **Lệnh thực hiện:**
  ```bash
  docker compose logs -f pitchos-booking-service pitchos-pitch-service-1
  ```
* **Kết quả kỳ vọng:** Thấy rõ thời điểm Booking nhận request, gọi Feign sang Pitch, Pitch log kèm tiền tố `[pitch-instance-1]`, và Booking tính tiền ghi DB.
* **Kết quả thực tế:** Log hiển thị rành mạch từng bước, không chứa thông tin nhạy cảm.
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

### DEP04: Dừng dịch vụ Consumer và quan sát Service Registry
* **Mục tiêu:** Kiểm tra khả năng phát hiện dịch vụ chết và tự động loại bỏ bản ghi của Eureka Server.
* **Lệnh thực hiện:**
  ```bash
  docker compose stop pitchos-booking-service
  ```
* **Kết quả kỳ vọng:** Sau khoảng thời gian heartbeat và lease expiration (30 giây), giao diện Eureka Dashboard tại `http://localhost:8761` loại bỏ dòng `PITCHOS-BOOKING-SERVICE`.
* **Kết quả thực tế:** Eureka Dashboard cập nhật danh bạ chính xác, gỡ bỏ Booking Service.
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

### DEP05: Tự phục hồi dịch vụ Consumer (Self-Healing)
* **Mục tiêu:** Bật lại dịch vụ Consumer và kiểm tra khả năng tự đăng ký lại vào Service Registry.
* **Lệnh thực hiện:**
  ```bash
  docker compose start pitchos-booking-service
  ```
* **Kết quả kỳ vọng:** Container khởi động lại, đạt trạng thái `healthy`, tự đăng ký lại vào Eureka Server, và thực hiện đặt sân bình thường.
* **Kết quả thực tế:** Booking Service tự đăng ký lại vào Eureka trong vòng 20 giây và nhận request `POST /api/v1/bookings` thành công (HTTP 201).
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

### DEP06: Bảo toàn dữ liệu qua Docker Named Volume (Data Persistence)
* **Mục tiêu:** Chứng minh dữ liệu cơ sở dữ liệu MySQL không bị mất khi toàn bộ hệ thống container bị xóa bỏ.
* **Quy trình thực hiện:**
  1. Tạo 1 đơn đặt sân mới qua Postman (ví dụ đơn số `15`).
  2. Dừng và xóa toàn bộ container: `docker compose down` (không dùng cờ `-v`).
  3. Khởi động lại hệ thống: `docker compose up -d`.
  4. Chạy script kiểm tra: `scripts/test-persistence.bat`.
* **Kết quả kỳ vọng:** Đơn đặt sân số `15` vẫn tồn tại nguyên vẹn trong bảng `bookings`.
* **Kết quả thực tế:** Số lượng bản ghi trước và sau khi restart container là hoàn toàn trùng khớp (15 = 15 bản ghi).
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

### DEP07: Xử lý sự cố mất kết nối Cơ sở dữ liệu
* **Mục tiêu:** Giả lập sự cố CSDL của Pitch Service bị dừng đột ngột và quan sát phản ứng của Actuator Health.
* **Lệnh thực hiện:**
  ```bash
  docker compose stop mysql-pitch
  ```
* **Kết quả kỳ vọng:** Endpoint `/actuator/health` của cả 2 instance Pitch Service (`:8082` và `:8084`) lập tức chuyển sang trạng thái HTTP `503` kèm `{"status":"DOWN"}`.
* **Kết quả thực tế:** Kiểm tra `curl http://localhost:8082/actuator/health` trả về `{"status":"DOWN"}`, log container ghi nhận lỗi ngắt kết nối HikariCP Pool.
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

### DEP08: Khả năng Chịu lỗi của Provider (High Availability & Fault Tolerance)
* **Mục tiêu:** Dừng 1 trong 2 instance của Provider và kiểm tra xem luồng đặt sân của khách hàng có bị gián đoạn hay không.
* **Lệnh thực hiện:**
  1. Dừng instance 1: `docker compose stop pitchos-pitch-service-1`.
  2. Gửi request đặt sân: `POST http://localhost:8083/api/v1/bookings`.
* **Kết quả kỳ vọng:** Request đặt sân vẫn thành công 100% (HTTP `201 Created`) nhờ Spring Cloud LoadBalancer tự động chuyển hướng sang `pitchos-pitch-service-2` (port 8084).
* **Kết quả thực tế:** Đơn đặt sân được tạo thành công với mã `201 Created`. Log của container `pitchos-pitch-service-2` ghi nhận request được phục vụ.
* **Đánh giá:** ✅ **ĐẠT (PASS)**.

---

## 3. KẾT LUẬN CHUNG
Toàn bộ **8/8 ca kiểm thử vận hành (DEP01 – DEP08)** đều đạt kết quả xuất sắc. Hệ thống PitchOS đáp ứng trọn vẹn các chuẩn mực về container hóa, giám sát sức khỏe, khả năng chịu lỗi và tính bền vững của dữ liệu.
