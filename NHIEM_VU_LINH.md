# 🌸 BẢNG NHIỆM VỤ CÁ NHÂN: LINH — BÀI KIỂM TRA SỐ 2 (TX2)
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### ĐỀ TÀI: HỆ THỐNG ĐẶT SÂN BÓNG TRỰC TUYẾN — PITCHOS

> **HỌ VÀ TÊN:** LINH  
> **VAI TRÒ:** Kỹ sư Triển khai Container & Provider Pitch Service  
> **VÙNG MÃ NGUỒN SỞ HỮU:** `pitchos-pitch-service/`, `docker-compose.yml`, `.env.example`  
> **TRỌNG SỐ ĐÁNH GIÁ:** **10,0 / 10,0 Điểm** (60% Điểm nhóm Báo cáo + Mã nguồn, 40% Điểm cá nhân qua Video demo độc lập)  
> **THỜI HẠN THỰC HIỆN:** 01 tuần (Theo kế hoạch tại `KE_HOACH_KIEM_TRA_2.md`)

---

## 🎯 1. BAREM ĐIỂM & ĐẦU VIỆC CHI TIẾT CỦA LINH

### 📘 A. Phần Lý thuyết Báo cáo (0,5 Điểm — Câu 1 Ý 1.3)
*Viết vào file `docs/kt2/CAU1_3_LINH.md` để sau này gộp vào Báo cáo chính.*
- [ ] **Phân biệt Docker Image và Docker Container:**
  - *Docker Image:* Là bản thiết kế khuôn mẫu bất biến (Read-only Blueprint / Template) được đóng gói bao gồm mã nguồn ứng dụng, môi trường thực thi (JRE 17), các thư viện phụ thuộc và cấu hình hệ thống. Image được tổ chức theo cấu trúc phân lớp (Layers).
  - *Docker Container:* Là một thể hiện đang chạy (Running Instance) được khởi tạo từ Docker Image, có trạng thái động (Stateful), có một lớp ghi tạm thời (Writable Container Layer) trên cùng và chạy hoàn toàn cô lập (Isolated Process) với các container khác trên cùng một hệ điều hành máy chủ.
  - *Nhấn mạnh mối quan hệ:* Một Image duy nhất có thể được sử dụng để khởi chạy nhiều Container đồng thời (ví dụ: cùng 1 image `pitchos-pitch-service` khởi chạy 2 container `pitchos-pitch-service-1` và `pitchos-pitch-service-2`).
- [ ] **Trình bày vai trò của Dockerfile và Docker Compose trong triển khai Microservices:**
  - *Dockerfile:* Là file văn bản chứa kịch bản các câu lệnh chỉ dẫn để tự động hóa việc đóng gói và xây dựng (Build) một Docker Image cho **từng microservice đơn lẻ**. Kỹ thuật Multi-stage build giúp tối ưu dung lượng image (tách phase build Maven cồng kềnh khỏi phase runtime JRE nhẹ nhàng) và tăng tính bảo mật (chạy bằng non-root user).
  - *Docker Compose:* Là công cụ điều phối (Orchestration) cấp độ phát triển để khai báo, liên kết và quản lý vòng đời của **nhiều microservices đồng thời** qua một file cấu hình duy nhất (`docker-compose.yml`). Định nghĩa mạng nội bộ (Docker Network), thứ tự khởi động (Dependencies & Healthchecks), các biến môi trường (Environment Variables) và cơ chế lưu trữ bền vững (Named Volumes).

---

### 💻 B. Phần Mã nguồn & Kỹ thuật Vận hành (Chấm 60% Nhóm)

#### 1. Nâng cấp Provider `pitchos-pitch-service` (Mục 2.2 & 2.3):
- [ ] Cập nhật `pom.xml`: Bổ sung khối Spring Cloud Dependency Management `2023.0.1`, thêm dependency `spring-cloud-starter-netflix-eureka-client` và `spring-boot-starter-actuator`.
- [ ] Cập nhật `src/main/resources/application.properties`:
  ```properties
  eureka.client.service-url.defaultZone=${EUREKA_URL:http://localhost:8761/eureka/}
  eureka.instance.prefer-ip-address=true
  eureka.instance.instance-id=${spring.application.name}:${INSTANCE_ID:${server.port}}
  management.endpoints.web.exposure.include=health,info
  management.endpoint.health.show-details=never
  ```
- [ ] **Xây dựng endpoint kiểm tra instance:** Tạo API `GET /api/v1/instance-info` trả về thông tin JSON:
  ```json
  {
    "serviceName": "pitchos-pitch-service",
    "instanceId": "${INSTANCE_ID:pitch-default}",
    "port": 8082
  }
  ```
- [ ] Thêm thông tin `instanceId` vào log trong các hàm xử lý API của Controller/Service để khi đọc log (`docker compose logs`) thấy rõ instance nào đang phục vụ request.
- [ ] Cập nhật `SecurityConfig`: Mở quyền truy cập tự do cho `/api/v1/instance-info`, `/actuator/health`, `/actuator/info`.
- [ ] Viết file `Dockerfile` multi-stage chuẩn không chạy quyền root (tạo `USER appuser`).
- [ ] Xóa bỏ file `application.properties` thừa ở thư mục gốc của service.

#### 2. Xây dựng File Điều Phối Toàn Hệ Thống `docker-compose.yml` (Mục 2.4 — 2.0 Điểm):
- [ ] Thiết lập file `docker-compose.yml` khởi chạy toàn bộ 7 container trong mạng nội bộ `pitchos-network`:
  1. `pitchos-service-registry` (Cổng 8761).
  2. `pitchos-auth-service` (Cổng 8081).
  3. `pitchos-pitch-service-1` (Cổng 8082, `INSTANCE_ID=pitch-instance-1`).
  4. `pitchos-pitch-service-2` (Cổng 8084, `INSTANCE_ID=pitch-instance-2`, chung DB với instance 1).
  5. `pitchos-booking-service` (Cổng 8083).
  6. 3 Container MySQL riêng biệt (hoặc 1 MySQL chứa 3 schemas phân lập).
- [ ] Cấu hình **Healthcheck** cho toàn bộ các dịch vụ:
  - MySQL: kiểm tra bằng `mysqladmin ping -h localhost`.
  - Java Services: kiểm tra bằng `curl` hoặc `wget` đến `/actuator/health`.
- [ ] Cấu hình **`depends_on` với điều kiện `condition: service_healthy`**:
  - Các service Java chỉ khởi động sau khi MySQL và Eureka Server đã đạt trạng thái `healthy`.
  - 🚨 **TRÁNH XUNG ĐỘT KHỞI TẠO DB:** Cấu hình `pitchos-pitch-service-2` chờ `pitchos-pitch-service-1` `service_healthy` để tránh 2 instance cùng chạy `DataInitializer` chèn trùng dữ liệu mẫu vào DB.
- [ ] Cấu hình chính sách tự khởi động lại: `restart: unless-stopped`.
- [ ] Gắn Named Volume cho các cơ sở dữ liệu (`mysql_auth_data`, `mysql_pitch_data`, `mysql_booking_data`).

#### 3. Xây dựng file mẫu biến môi trường `.env.example`:
- [ ] Tạo file `.env.example` chứa toàn bộ các biến môi trường mẫu chuẩn xác:
  ```env
  MYSQL_HOST=mysql-pitch
  MYSQL_PORT=3306
  MYSQL_USERNAME=root
  MYSQL_PASSWORD=
  EUREKA_URL=http://pitchos-service-registry:8761/eureka/
  JWT_SECRET=404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970
  ```

---

### 📝 C. Phần Báo cáo Chuyên đề (Phụ trách: 2,50 / 10,0 Điểm)
- [ ] **Câu 1.3 (0,5 Điểm):** Lý thuyết Docker Image vs Container, vai trò Dockerfile và Docker Compose (Viết vào `docs/kt2/CAU1_3_LINH.md`).
- [ ] Viết **Phần 1: Giới thiệu hệ thống PitchOS** vào `docs/kt2/PHAN_1_LINH.md`:
  - Trình bày bài toán đặt sân bóng, mục tiêu hệ thống, các phân hệ chức năng.
  - Lập bảng tổng hợp công nghệ sử dụng trong đề tài (bổ sung: Eureka Server, Spring Cloud LoadBalancer, Spring Boot Actuator, Docker, Docker Compose).
  - Phân tích rõ ràng: Phần nào đã hoàn thành từ KT1, phần nào được bổ sung nâng cấp cho bài kiểm tra số 2 (KT2).
- [ ] Viết **Phần 5: Container hóa và Triển khai toàn hệ thống (2,0 Điểm)** vào `docs/kt2/PHAN_5_LINH.md`:
  - Phân tích kiến trúc Dockerfile multi-stage, giải thích cơ chế non-root user và cách tối ưu image layer.
  - Phân tích cấu trúc file `docker-compose.yml`, cấu hình mạng Docker Network nội bộ và cơ chế phân giải DNS theo tên container.
  - Trình bày cơ chế Healthcheck và thứ tự khởi động các dịch vụ.
  - Giải thích cách thức quản lý biến môi trường qua file `.env.example`.
  - Chèn ảnh minh chứng kết quả lệnh `docker compose ps` cho thấy toàn bộ các container đều đạt trạng thái `healthy`.

---

### 🎬 D. Phần Quay Video Demo Cá Nhân (40% Điểm Cá Nhân Của Linh)
*Linh tự thực hiện trên máy tính cá nhân và quay video 10–15 phút đủ 8 bước theo checklist:*
- [ ] **Bước 1:** Mở sơ đồ kiến trúc hệ thống giới thiệu các microservices, chỉ rõ Consumer (Booking), Provider (Pitch 2 instances) và Service Registry (Eureka).
- [ ] **Bước 2:** Chạy lệnh `docker compose up -d` ➔ Chạy `docker compose ps` chứng minh toàn bộ 7 container đều `healthy`.
- [ ] **Bước 3:** Mở Eureka Dashboard `http://localhost:8761` chứng minh các dịch vụ đã đăng ký, Pitch có 2 instances (8082 và 8084).
- [ ] **Bước 4:** Dùng Postman login lấy Token ➔ Gọi `POST /api/v1/bookings` đặt sân thành công (Status 201).
- [ ] **Bước 5:** Minh họa lỗi tích hợp: Gửi sân 9999 (Status 404), dừng cả 2 Pitch gửi đặt sân (Status 503).
- [ ] **Bước 6:** Mở `/actuator/health` = `{"status":"UP"}` và mở log xem luồng trao đổi.
- [ ] **Bước 7:** Dừng Pitch instance 1 ➔ Đặt sân vẫn thành công (Status 201) nhờ instance 2.
- [ ] **Bước 8:** Chạy `docker compose down` rồi `up -d` ➔ Chứng minh dữ liệu đơn đặt sân vẫn còn nguyên vẹn qua Docker Volume.
