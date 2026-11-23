# 👑 BẢNG NHIỆM VỤ CÁ NHÂN: HOÀNG (NHÓM TRƯỞNG) — BÀI KIỂM TRA SỐ 2 (TX2)
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### ĐỀ TÀI: HỆ THỐNG ĐẶT SÂN BÓNG TRỰC TUYẾN — PITCHOS

> **HỌ VÀ TÊN:** HOÀNG  
> **VAI TRÒ:** Nhóm trưởng, Phụ trách Service Registry (Eureka Server), Auth Service & Tổng hợp Báo cáo  
> **VÙNG MÃ NGUỒN SỞ HỮU:** `pitchos-service-registry/`, `pitchos-auth-service/`, `README.md`, `.gitignore`  
> **TRỌNG SỐ ĐÁNH GIÁ:** **10,0 / 10,0 Điểm** (60% Điểm nhóm Báo cáo + Mã nguồn, 40% Điểm cá nhân qua Video demo độc lập)  
> **THỜI HẠN THỰC HIỆN:** 01 tuần (Theo kế hoạch tại `KE_HOACH_KIEM_TRA_2.md`)

---

## 🎯 1. BAREM ĐIỂM & ĐẦU VIỆC CHI TIẾT CỦA HOÀNG

### 📘 A. Phần Lý thuyết Báo cáo (0,5 Điểm — Câu 1 Ý 1.2)
*Viết vào file `docs/kt2/CAU1_2_HOANG.md` để sau này gộp vào Báo cáo chính.*
- [ ] **Trình bày vai trò của Service Registry và Service Discovery trong kiến trúc Microservices:**
  - *Service Registry:* Đóng vai trò là "cuốn danh bạ điện thoại" trung tâm lưu trữ thông tin mạng (IP, Port, trạng thái sức khỏe) của toàn bộ các service instances trong hệ thống.
  - *Service Discovery:* Cơ chế tự động giúp các service (Consumer) tra cứu và định vị địa chỉ mạng của service khác (Provider) thông qua tên định danh (Service ID) thay vì phải cấu hình cứng.
  - Phân tích cơ chế Heartbeat và độ trễ cập nhật (khoảng 30 giây).
- [ ] **Phân biệt chức năng của Eureka Server với API Gateway (Tránh bẫy nhầm lẫn của thầy):**
  - *Eureka Server (Service Registry):* Hoạt động ở tầng nội bộ (Internal Discovery), chỉ có nhiệm vụ lưu trữ và cung cấp danh bạ địa chỉ dịch vụ cho các service nội bộ tìm thấy nhau. Eureka **không tiếp nhận hay định tuyến request từ bên ngoài vào**.
  - *API Gateway (Cổng giao tiếp):* Hoạt động ở tầng biên (Edge/Perimeter), là điểm tiếp nhận duy nhất toàn bộ request từ Client/Frontend, thực hiện định tuyến (Routing), kiểm tra bảo mật (Authentication/Rate Limiting), cân bằng tải và tổng hợp dữ liệu.
- [ ] **Giải thích vì sao Consumer nên gọi Provider thông qua Service ID thay vì địa chỉ IP hoặc URL cố định:**
  - Trong môi trường Docker/Cloud, địa chỉ IP và Port của container mang tính động (ephemeral), tự động thay đổi sau mỗi lần restart hoặc mở rộng (Scale).
  - Một Service có thể có nhiều instance (ví dụ Pitch Service có 2 instance chạy song song), nếu dùng URL cứng sẽ không thể thực hiện cân bằng tải (Client-side Load Balancing).
  - Gọi qua Service ID giúp lỏng liên kết (Loose Coupling) và tăng tính sẵn sàng của hệ thống.

---

### 💻 B. Phần Mã nguồn & Kỹ thuật Vận hành (Chấm 60% Nhóm)

#### 1. Khởi tạo module `pitchos-service-registry` (Mục 2.3 — 1.5 Điểm):
- [ ] Tạo module Spring Boot mới `pitchos-service-registry` độc lập.
- [ ] Cấu hình `pom.xml`: Thêm `spring-cloud-starter-netflix-eureka-server` và `spring-boot-starter-actuator`.
- [ ] Gắn annotation `@EnableEurekaServer` vào class khởi chạy chính `PitchosServiceRegistryApplication.java`.
- [ ] Cấu hình file `src/main/resources/application.properties`:
  ```properties
  server.port=8761
  spring.application.name=pitchos-service-registry
  eureka.client.register-with-eureka=false
  eureka.client.fetch-registry=false
  management.endpoints.web.exposure.include=health,info
  ```
- [ ] Viết `Dockerfile` multi-stage cho Service Registry.
- [ ] Kiểm tra Eureka Dashboard khởi chạy thành công tại `http://localhost:8761`.

#### 2. Cập nhật `pitchos-auth-service`:
- [ ] Cập nhật `pom.xml`: Bổ sung Spring Cloud Dependency Management `2023.0.1`, thêm dependency `spring-cloud-starter-netflix-eureka-client` và `spring-boot-starter-actuator`.
- [ ] Cập nhật `src/main/resources/application.properties`: Cấu hình kết nối Eureka Server, Actuator `health,info`, `show-details=never`.
- [ ] Cập nhật `SecurityConfig`: Mở quyền permitAll cho các endpoint `/actuator/health` và `/actuator/info`.
- [ ] 🚨 **BẮT BUỘC (SỬA LỖI BẢO MẬT THEO TH8):** Mở file `DataInitializer.java`, **xóa bỏ hoàn toàn dòng log in mật khẩu mặc định ra console**.
- [ ] Viết `Dockerfile` multi-stage chuẩn không chạy quyền root (`USER appuser`).
- [ ] Xóa bỏ file `application.properties` thừa ở thư mục gốc của service.

#### 3. Quản trị Kho lưu trữ & Cấu hình Chung:
- [ ] Gỡ theo dõi file `.env` thật khỏi Git bằng lệnh: `git rm --cached .env`.
- [ ] Cập nhật `.gitignore` để chắc chắn không bao giờ commit file `.env`, file `.log`, thư mục `target/`.
- [ ] Viết hoàn chỉnh file **`README.md`** hướng dẫn chi tiết cách clone repo về và khởi chạy 1 lệnh duy nhất bằng Docker Compose trên máy tính hoàn toàn sạch.
- [ ] Thiết lập branch rule bảo vệ nhánh `main`, thực hiện review và merge Pull Request cho Linh, Nhật, Hùng.

#### 4. Thực hiện Kiểm thử Service Registry & Cân bằng tải:
- [ ] Chạy bộ kiểm thử **TC01–TC06** (Kiểm tra đăng ký, gọi Service ID, cân bằng tải 2 instance, dừng 1 instance, dừng toàn bộ, phục hồi).
- [ ] Gửi tối thiểu **20 request** liên tiếp qua Consumer (`GET /api/v1/bookings/pitch-instance`) bằng Postman Runner.
- [ ] Lập bảng phân phối request chứng minh Spring Cloud LoadBalancer phân bổ luồng tải cho cả 2 instance Pitch-1 và Pitch-2.

---

### 📝 C. Phần Báo cáo Chuyên đề (Phụ trách: 2,50 / 10,0 Điểm)
- [ ] **Câu 1.2 (0,5 Điểm):** Lý thuyết Service Registry, Discovery, Eureka vs API Gateway, Service ID (Viết vào `docs/kt2/CAU1_2_HOANG.md`).
- [ ] **Phần 2.1a: Sơ đồ kiến trúc tích hợp và triển khai (0,5 Điểm)** vào `docs/kt2/PHAN_2_HOANG.md`:
  - Vẽ sơ đồ kiến trúc TRƯỚC (KT1 - gọi URL cứng) và SAU (KT2 - có Eureka, Docker Compose, 2 instance Pitch).
  - Phân tích luồng tương tác và phân định ranh giới giữa các dịch vụ.
- [ ] **Phần 4: Service Registry và Cân bằng tải (1,5 Điểm)** vào `docs/kt2/PHAN_4_HOANG.md`:
  - Giải thích cấu hình Eureka Server và cơ chế đăng ký của các Eureka Client.
  - Phân tích cơ chế Spring Cloud LoadBalancer.
  - Đưa ảnh chụp Eureka Dashboard hiển thị đầy đủ dịch vụ (Pitch có 2 instances).
  - Đưa bảng số liệu 20 request và nhận xét về độ trễ cập nhật bảng định tuyến khi một instance dừng.
- [ ] Xuất tài liệu `docs/testing/service-discovery-test.md` (Ghi lại kết quả chi tiết của TC01–TC06).
- [ ] **Chủ trì tổng hợp toàn bộ bài viết từ 4 thành viên thành bản Báo cáo hoàn chỉnh (`docs/report.docx` ➔ `docs/report.pdf`)**.

---

### 🎬 D. Phần Quay Video Demo Cá Nhân (40% Điểm Cá Nhân Của Hoàng)
*Hoàng tự thực hiện trên máy tính cá nhân và quay video 10–15 phút đủ 8 bước theo checklist:*
- [ ] **Bước 1:** Mở sơ đồ kiến trúc hệ thống giới thiệu các microservices, chỉ rõ Consumer (Booking), Provider (Pitch 2 instances) và Service Registry (Eureka).
- [ ] **Bước 2:** Chạy lệnh `docker compose up -d` ➔ Chạy `docker compose ps` chứng minh toàn bộ 7 container đều `healthy`.
- [ ] **Bước 3:** Mở Eureka Dashboard `http://localhost:8761` chứng minh các dịch vụ đã đăng ký, Pitch có 2 instances (8082 và 8084).
- [ ] **Bước 4:** Dùng Postman login lấy Token ➔ Gọi `POST /api/v1/bookings` đặt sân thành công (Status 201).
- [ ] **Bước 5:** Minh họa lỗi tích hợp: Gửi sân 9999 (Status 404), dừng cả 2 Pitch gửi đặt sân (Status 503).
- [ ] **Bước 6:** Mở `/actuator/health` = `{"status":"UP"}` và mở log xem luồng trao đổi.
- [ ] **Bước 7:** Dừng Pitch instance 1 ➔ Đặt sân vẫn thành công (Status 201) nhờ instance 2.
- [ ] **Bước 8:** Chạy `docker compose down` rồi `up -d` ➔ Chứng minh dữ liệu đơn đặt sân vẫn còn nguyên vẹn qua Docker Volume.
