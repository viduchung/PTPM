# 🛡️ BẢNG NHIỆM VỤ CÁ NHÂN: HÙNG — BÀI KIỂM TRA SỐ 2 (TX2)
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### ĐỀ TÀI: HỆ THỐNG ĐẶT SÂN BÓNG TRỰC TUYẾN — PITCHOS

> **HỌ VÀ TÊN:** HÙNG  
> **VAI TRÒ:** Kỹ sư Cơ sở Dữ liệu & Quản trị Vận hành Hệ thống  
> **VÙNG MÃ NGUỒN SỞ HỮU:** `pitchos-database/`, `scripts/`, Khối cấu hình MySQL & Volume trong Docker Compose  
> **TRỌNG SỐ ĐÁNH GIÁ:** **10,0 / 10,0 Điểm** (60% Điểm nhóm Báo cáo + Mã nguồn, 40% Điểm cá nhân qua Video demo độc lập)  
> **THỜI HẠN THỰC HIỆN:** 01 tuần (Theo kế hoạch tại `KE_HOACH_KIEM_TRA_2.md`)

---

## 🎯 1. BAREM ĐIỂM & ĐẦU VIỆC CHI TIẾT CỦA HÙNG

### 📘 A. Phần Lý thuyết Báo cáo (0,5 Điểm — Câu 1 Ý 1.4)
*Viết vào file `docs/kt2/CAU1_4_HUNG.md` để sau này gộp vào Báo cáo chính.*
- [ ] **Phân biệt 3 cấp độ trạng thái theo đúng tiêu chuẩn TH8 của giảng viên:**
  - *1. Trạng thái hoạt động của Container (Container Status):* Thể hiện tiến trình trong container có đang chạy hay không (`Up` / `Running` / `Exited`). Đây chỉ là trạng thái mức hệ điều hành máy chủ (OS-level process). **Container đang running KHÔNG ĐỒNG NGHĨA với việc ứng dụng hoạt động bình thường** (ví dụ: JVM đang bị crash lặp, đang treo Deadlock hoặc lỗi kết nối DB nhưng tiến trình PID vẫn tồn tại).
  - *2. Trạng thái sức khỏe của ứng dụng (Application Health):* Thể hiện mức độ sẵn sàng nội tại của ứng dụng Spring Boot thông qua Actuator (`/actuator/health`). Ứng dụng chỉ đạt `UP` khi toàn bộ các thành phần phụ thuộc thiết yếu (kết nối Datasource HikariCP tới MySQL, dung lượng ổ đĩa, kết nối Eureka) đều sẵn sàng phục vụ request.
  - *3. Khả năng thực hiện nghiệp vụ của hệ thống (Business Availability):* Thể hiện việc luồng nghiệp vụ end-to-end có thực hiện thành công hay không. Đây là mức cao nhất, phụ thuộc vào sự phối hợp của nhiều dịch vụ đồng thời.
  - *Ví dụ thực tế trong PitchOS:* Container Booking Service đang `Running` và `/actuator/health` báo `UP`, nhưng nếu cả 2 instance của Pitch Service đều bị dừng thì người dùng **hoàn toàn không thể đặt được sân bóng**. Do đó: Container Status ➔ Application Health ➔ Business Availability là 3 cấp độ hoàn toàn khác nhau.
- [ ] **Trình bày vai trò của Health Check, Log và Docker Volume trong vận hành Microservices:**
  - *Health Check:* Giúp Docker Engine và bộ điều phối (Orchestrator) tự động phát hiện container bị lỗi nội bộ để khởi động lại (Self-healing), đồng thời giúp Docker Compose (`depends_on: condition: service_healthy`) kiểm soát chính xác thứ tự khởi động (chỉ cho phép service Java bật sau khi MySQL đã thực sự sẵn sàng nhận kết nối).
  - *Log (Giám sát & Khắc phục sự cố):* Là nhật ký hoạt động của ứng dụng, giúp kỹ sư vận hành truy vết lỗi liên dịch vụ (Distributed Tracing), xác định nguyên nhân gốc rễ (Root Cause Analysis). *🚨 Lưu ý bảo mật bắt buộc của thầy:* Log tuyệt đối không được in dữ liệu nhạy cảm (mật khẩu người dùng, token bí mật).
  - *Docker Volume (Bảo toàn dữ liệu):* Vùng lưu trữ được Docker quản lý độc lập ngoài vòng đời của container (Lifecycle Independence). Dữ liệu CSDL MySQL được ghi xuống Named Volume sẽ không bị mất khi container bị dừng (`stop`), khởi động lại (`restart`) hoặc thậm chí bị xóa bỏ (`down`). Dữ liệu chỉ bị xóa khi cố tình dùng cờ `-v` (`down -v`).

---

### 💻 B. Phần Mã nguồn & Kỹ thuật Vận hành (Chấm 60% Nhóm)

#### 1. Quản trị Cơ sở Dữ liệu & Script Tự Động Hóa (Mục 2.4 & 2.5):
- [ ] **Tách và chuẩn bị 3 file SQL nạp dữ liệu sạch** trong thư mục `pitchos-database/`:
  1. `auth-init.sql`: Khởi tạo bảng `users`, nạp 3 tài khoản mẫu với mật khẩu băm BCrypt (`admin`, `chusan`, `user`).
  2. `pitch-init.sql`: Khởi tạo bảng `pitches`, nạp sẵn danh sách sân bóng mẫu và bảng giá theo giờ.
  3. `booking-init.sql`: Khởi tạo bảng `bookings`, cấu hình các chỉ mục logic (`pitch_id`, `user_id`, thời gian bắt đầu, kết thúc).
- [ ] Phối hợp với Linh đưa các file SQL này vào thư mục `/docker-entrypoint-initdb.d/` của từng container MySQL tương ứng trong file `docker-compose.yml` để tự động khởi tạo khi container dựng lên lần đầu.
- [ ] Kiểm tra và đảm bảo các CSDL được gắn vào **Named Volume** bền vững:
  - `mysql_auth_data` gắn vào `/var/lib/mysql` của `mysql-auth`.
  - `mysql_pitch_data` gắn vào `/var/lib/mysql` của `mysql-pitch`.
  - `mysql_booking_data` gắn vào `/var/lib/mysql` của `mysql-booking`.

#### 2. Viết Kịch Bản Script Kiểm Tra Tự Động (Thư mục `scripts/`):
- [ ] Tạo file script `scripts/check-health.bat` (và `scripts/check-health.sh`): Tự động gửi request kiểm tra endpoint `/actuator/health` của 4 dịch vụ (Registry :8761, Auth :8081, Pitch :8082, Booking :8083) và in ra trạng thái màn hình.
- [ ] Tạo file script `scripts/test-persistence.bat`: Tự động truy vấn số lượng bản ghi trong bảng `bookings` trước và sau khi thực hiện chuỗi lệnh `docker compose down` rồi `docker compose up -d` để chứng minh dữ liệu còn nguyên vẹn.

#### 3. Thực hiện Bộ Kiểm Thử Vận Hành, Giám Sát & Sự Cố (DEP01–DEP08):
- [ ] **DEP01:** Chạy `docker compose up -d --build` ➔ Kiểm tra `docker compose ps` (7 container đều `healthy`).
- [ ] **DEP02:** Kiểm tra sức khỏe `/actuator/health` của từng service ➔ Chụp ảnh minh chứng `{"status":"UP"}`.
- [ ] **DEP03:** Đọc log liên dịch vụ (`docker compose logs`) của Booking và Pitch ➔ Chỉ rõ dòng log giao tiếp giữa 2 service.
- [ ] **DEP04:** Dừng container Booking Service ➔ Quan sát Eureka Dashboard loại bỏ Booking sau khoảng thời gian trễ.
- [ ] **DEP05:** Khởi động lại container Booking ➔ Đăng ký lại thành công vào Eureka và đặt sân bình thường.
- [ ] **DEP06:** Kiểm tra bảo toàn dữ liệu: Chạy `docker compose down` (không dùng cờ `-v`), sau đó chạy lại `docker compose up -d` ➔ Thực thi câu lệnh SQL chứng minh toàn bộ đơn đặt sân đã tạo trước đó **vẫn còn nguyên vẹn**.
- [ ] **DEP07 (Sự cố đặc thù 1):** Dừng container `mysql-pitch` ➔ Actuator của Pitch Service lập tức chuyển sang trạng thái `DOWN`, đọc log thấy lỗi ngắt kết nối HikariCP pool.
- [ ] **DEP08 (Sự cố đặc thù 2 - Chịu lỗi):** Dừng container `pitchos-pitch-service-1` ➔ Gửi request đặt sân qua Booking Service, chứng minh hệ thống vẫn xử lý thành công 100% nhờ có `pitchos-pitch-service-2`.

---

### 📝 C. Phần Báo cáo Chuyên đề (Phụ trách: 2,50 / 10,0 Điểm)
- [ ] **Câu 1.4 (0,5 Điểm):** Lý thuyết 3 mức (Container Status, App Health, Business Availability); vai trò Health Check, Log, Volume (Viết vào `docs/kt2/CAU1_4_HUNG.md`).
- [ ] **Phần 2.1b: Bảng mô tả dịch vụ và Thiết kế CSDL phân tán (0,5 Điểm)** vào `docs/kt2/PHAN_2_HUNG.md`:
  - Lập bảng mô tả chi tiết 4 dịch vụ: Tên dịch vụ, chức năng nghiệp vụ, API chính, DB sở hữu, Consumer/Provider, số instance.
  - Luận giải nguyên tắc Database-per-service và triết lý sử dụng Logical ID (không dùng Foreign Key vật lý ràng buộc chéo giữa các container MySQL).
- [ ] **Phần 6: Vận hành, Giám sát và Kiểm thử sự cố (1,5 Điểm)** vào `docs/kt2/PHAN_6_HUNG.md`:
  - Trình bày kết quả gọi endpoint `/actuator/health` của các dịch vụ.
  - Phân tích log hoạt động của ít nhất 2 dịch vụ (Booking và Pitch) khi có request đặt sân và khi xảy ra lỗi.
  - Bảng tổng hợp kết quả bộ kiểm thử vận hành **DEP01–DEP08** kèm ảnh chụp minh chứng.
  - **Phân tích chuyên sâu 1 tình huống sự cố thực tế (Mục bắt buộc có điểm riêng):**
    - *Tình huống:* Dịch vụ Provider (Pitch Service) bị quá tải hoặc sập tiến trình.
    - *Nguyên nhân:* Mạng đứt kết nối hoặc container bị kill.
    - *Ảnh hưởng:* Booking Service không thể lấy được giá sân; nếu không có xử lý lỗi thì Booking sẽ bị treo luồng (Cascading Failure).
    - *Phương án xử lý:* Cấu hình OpenFeign Timeout (2s/3s), GlobalExceptionHandler bắt FeignException chuyển thành mã **503 Service Unavailable**, thiết lập 2 instance Pitch để cân bằng tải và cấu hình chính sách `restart: unless-stopped` trong Docker Compose.
- [ ] Viết **Phần 7: Đánh giá và Kết luận** vào `docs/kt2/PHAN_7_HUNG.md`:
  - Lập bảng tự chấm điểm theo đúng barem 10 điểm của giảng viên.
  - Nêu rõ các vấn đề kỹ thuật phát sinh trong quá trình triển khai và cách cả nhóm khắc phục.
  - Đề xuất hướng phát triển mở rộng: Bổ sung API Gateway (Spring Cloud Gateway), áp dụng Circuit Breaker (Resilience4j) và giải pháp khóa phân tán (Distributed Lock với Redis) nếu scale Booking Service.
- [ ] Xuất tài liệu kiểm thử vận hành `docs/testing/operation-test.md` và phân tích sự cố `docs/operation/failure-analysis.md`.

---

### 🎬 D. Phần Quay Video Demo Cá Nhân (40% Điểm Cá Nhân Của Hùng)
*Hùng tự thực hiện trên máy tính cá nhân và quay video 10–15 phút đủ 8 bước theo checklist:*
- [ ] **Bước 1:** Mở sơ đồ kiến trúc hệ thống giới thiệu các microservices, chỉ rõ Consumer (Booking), Provider (Pitch 2 instances) và Service Registry (Eureka).
- [ ] **Bước 2:** Chạy lệnh `docker compose up -d` ➔ Chạy `docker compose ps` chứng minh toàn bộ 7 container đều `healthy`.
- [ ] **Bước 3:** Mở Eureka Dashboard `http://localhost:8761` chứng minh các dịch vụ đã đăng ký, Pitch có 2 instances (8082 và 8084).
- [ ] **Bước 4:** Dùng Postman login lấy Token ➔ Gọi `POST /api/v1/bookings` đặt sân thành công (Status 201).
- [ ] **Bước 5:** Minh họa lỗi tích hợp: Gửi sân 9999 (Status 404), dừng cả 2 Pitch gửi đặt sân (Status 503).
- [ ] **Bước 6:** Mở `/actuator/health` = `{"status":"UP"}` và mở log xem luồng trao đổi.
- [ ] **Bước 7:** Dừng Pitch instance 1 ➔ Đặt sân vẫn thành công (Status 201) nhờ instance 2.
- [ ] **Bước 8:** Chạy `docker compose down` rồi `up -d` ➔ Mở công cụ quản trị CSDL hoặc thực thi câu lệnh SQL chứng minh dữ liệu đơn đặt sân vẫn còn nguyên vẹn qua Docker Volume.
