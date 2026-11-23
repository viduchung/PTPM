# 🧭 KẾ HOẠCH NHÓM & PHÂN CÔNG NHIỆM VỤ BÀI KIỂM TRA SỐ 2 (TX2)
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### ĐỀ TÀI: HỆ THỐNG ĐẶT SÂN BÓNG TRỰC TUYẾN — PITCHOS

> 📌 **Căn cứ thực hiện:**
> 1. Đề thi chính thức: **Bài kiểm tra số 2 – PTPM Hướng dịch vụ (Chuẩn đầu ra CĐR L2)**.
> 2. Các bài thực hành nền tảng của giảng viên: **TH6** (Tích hợp dịch vụ & Consumer/Provider), **TH7** (Microservices & Service Registry Eureka), **TH8** (Container hóa Docker, Compose & Vận hành).
> 3. Cơ cấu điểm số: **Tổng 10 điểm** (60% Điểm nhóm Báo cáo + Mã nguồn, **40% Điểm cá nhân qua Video demo độc lập**).
> 4. Thời gian thực hiện: **01 tuần (7 ngày)**.

---

## MỤC LỤC
1. [I. Barem Chấm Điểm & Yêu Cầu Cốt Lõi Của Đề Bài](#i-barem-chấm-điểm--yêu-cầu-cốt-lõi-của-đề-bài)
2. [II. Hiện Trạng Hệ Thống & Những Việc Cần Làm](#ii-hiện-trạng-hệ-thống--những-việc-cần-làm)
3. [III. Kiến Trúc Đích Hệ Thống PitchOS Sau KT2](#iii-kiến-trúc-đích-hệ-thống-pitchos-sau-kt2)
4. [IV. Bảng Phân Công Nhiệm Vụ 4 Thành Viên (Hoàng, Linh, Nhật, Hùng)](#iv-bảng-phân-công-nhiệm-vụ-4-thành-viên)
5. [V. Danh Mục Việc Cần Làm Chi Tiết Theo Kỹ Thuật](#v-danh-mục-việc-cần-làm-chi-tiết-theo-kỹ-thuật)
6. [VI. Khung Báo Cáo 7 Phần & Cấu Trúc Thư Mục Nộp Bài](#vi-khung-báo-cáo-7-phần--cấu-trúc-thư-mục-nộp-bài)
7. [VII. Kịch Bản Quay Video Demo Cá Nhân 8 Bước (40% Điểm Cá Nhân)](#vii-kịch-bản-quay-video-demo-cá-nhân-8-bước)
8. [VIII. Quy Trình Phối Hợp Git & Lịch Trình 7 Ngày](#viii-quy-trình-phối-hợp-git--lịch-trình-7-ngày)
9. [IX. Các Bẫy Kỹ Thuật Cần Tuyệt Đối Tránh (Lời Thầy Dặn)](#ix-các-bẫy-kỹ-thuật-cần-tuyệt-đối-tránh)

---

## I. BAREM CHẤM ĐIỂM & YÊU CẦU CỐT LÕI CỦA ĐỀ BÀI

### 1. Bảng tổng hợp barem điểm (10,0 Điểm)
| Phần | Nội dung đánh giá | Điểm | Phân công đảm nhiệm | Điểm cá nhân |
|---|---|:---:|---|:---:|
| **Câu 1** | **Lý thuyết nền tảng (1.1 → 1.4)** | **2,0** | **Chia đều 4 người (mỗi người 0,5đ)** | |
| • 1.1 | Phân biệt Consumer/Provider, quy trình gọi API, cách xử lý lỗi | 0,5 | **Nhật** viết | 0,5đ |
| • 1.2 | Vai trò Service Registry & Discovery, phân biệt Eureka vs API Gateway, Service ID | 0,5 | **Hoàng** viết | 0,5đ |
| • 1.3 | Phân biệt Image/Container, vai trò Dockerfile và Docker Compose | 0,5 | **Linh** viết | 0,5đ |
| • 1.4 | Phân biệt Container Status, App Health, Business Availability; vai trò Healthcheck, Log, Volume | 0,5 | **Hùng** viết | 0,5đ |
| **Câu 2** | **Thực nghiệm trên đề tài PitchOS (Dùng để quay video cá nhân)** | **8,0** | **Chia đều 4 người (mỗi người 2,0đ)** | |
| • 2.1a | Sơ đồ kiến trúc tích hợp và triển khai (trước & sau khi có Eureka/Docker) | 0,5 | **Hoàng** phụ trách | 0,5đ |
| • 2.1b | Bảng mô tả dịch vụ, phân định trách nhiệm CSDL phân tán & Logical ID | 0,5 | **Hùng** phụ trách | 0,5đ |
| • 2.2 | Tích hợp dịch vụ: Booking gọi Pitch qua Feign, kiểm tra dữ liệu Provider, xử lý ≥ 2 lỗi | 2,0 | **Nhật** phụ trách | 2,0đ |
| • 2.3 | Service Registry: Eureka Server, đăng ký bằng Service ID, chạy **2 instance Pitch**, test dừng/bật | 1,5 | **Hoàng** phụ trách | 1,5đ |
| • 2.4 | Container hóa: Dockerfile multi-stage, `docker-compose.yml`, network, env, named volume | 2,0 | **Linh** phụ trách | 2,0đ |
| • 2.5 | Vận hành, giám sát: Actuator `/actuator/health`, đọc log ≥ 2 service, test restart, phân tích sự cố | 1,5 | **Hùng** phụ trách | 1,5đ |
| **Tổng** | **Toàn bộ bài kiểm tra số 2** | **10,0** | **Mỗi người đúng 2,50 / 10,0 điểm (Chia đều 100%)** | **2,5đ / người** |

---

## II. HIỆN TRẠNG HỆ THỐNG & NHỮNG VIỆC CẦN LÀM

### 1. So sánh hiện trạng và yêu cầu KT2
| Thành phần | Hiện trạng sau KT1 | Yêu cầu bắt buộc của KT2 (TH6–TH8) | Đánh giá & Việc cần làm |
|---|---|---|---|
| **Auth Service (:8081)** | JWT, RBAC 3 role, đăng nhập/đăng ký | Thêm Actuator, Eureka Client, container hóa | ⚠️ Đang in mật khẩu mặc định ra log ➔ **Phải gỡ bỏ log nhạy cảm** |
| **Pitch Service (:8082)** | Provider quản lý sân, CRUD, Swagger | Chạy **2 instance** (:8082 & :8084), endpoint `/api/v1/instance-info` | ❌ Thiếu endpoint kiểm tra instance, chưa chạy 2 instance |
| **Booking Service (:8083)** | Consumer gọi Pitch tính tiền & đặt sân | Gọi Pitch qua **Service ID** (bỏ URL cứng), kiểm tra dữ liệu Provider | ⚠️ Feign đang hardcode `localhost:8082`, chưa kiểm tra giá âm/null |
| **Service Registry** | Chưa có | Module **Eureka Server** (`pitchos-service-registry` :8761) | ❌ Chưa có ➔ **Phải tạo mới** |
| **Xử lý lỗi tích hợp** | 404 (sân không tồn tại), 503 (mất kết nối) | Bổ sung kiểm tra dữ liệu không hợp lệ (502), timeout, gửi lặp (400) | ⚠️ Bổ sung thêm minh chứng timeout và kiểm tra giá trả về |
| **Triển khai Docker** | Chỉ có compose chạy 1 MySQL cục bộ | Dockerfile multi-stage cho 4 service, compose toàn bộ hệ thống | ❌ Thiếu toàn bộ Dockerfile của các Java service |
| **Cơ sở dữ liệu** | 3 schema trong 1 MySQL cục bộ | Tách thành 3 named volume bảo toàn dữ liệu | ⚠️ Cần chuẩn bị script SQL init tự động nạp khi dựng container |
| **Giám sát Actuator** | Chưa có | `/actuator/health` (show-details: never) | ❌ Cần thêm dependency & cấu hình |

> ⚠️ **ĐÁNH GIÁ NGUY CƠ:** Nếu nộp nguyên trạng mã nguồn KT1 hiện tại, bài chỉ đạt **1.5 – 2.0 / 10 điểm** vì hoàn toàn thiếu Eureka, Docker toàn hệ thống, 2 instance Provider và Actuator.

---

## III. KIẾN TRÚC ĐÍCH HỆ THỐNG PITCHOS SAU KT2

```
                                  Client / Postman
                                         │
                   ┌─────────────────────┼─────────────────────────┐
                   │                     │                         │
                   ▼                     ▼                         ▼
            ┌──────────────┐      ┌──────────────┐   OpenFeign+LB   ┌────────────────────────┐
            │ auth-service │      │booking-servic│─────────────────►│ pitch-service-1 (:8082)│
            │ Cổng: 8081   │      │ Cổng: 8083   │    Service ID:   │ pitch-service-2 (:8084)│
            │              │      │ (CONSUMER)   │   pitchos-pitch- │ (PROVIDER - 2 INSTANCE)│
            └──────┬───────┘      └──────┬───────┘      service     └───────────┬────────────┘
                   │                     │                                      │
                   │           Heartbeat / Đăng ký danh bạ                      │
                   └─────────────────────┼──────────────────────────────────────┘
                                         ▼
                        ┌──────────────────────────────────┐
                        │     pitchos-service-registry     │
                        │        (Eureka Server :8761)     │
                        └──────────────────────────────────┘
                   │                     │                                      │
                   ▼                     ▼                                      ▼
            ┌──────────────┐      ┌──────────────┐                  ┌────────────────────────┐
            │  mysql-auth  │      │mysql-booking │                  │      mysql-pitch       │
            │ volume: auth │      │ vol: booking │                  │ (Dùng chung cho 2 inst)│
            └──────────────┘      └──────────────┘                  └────────────────────────┘
            ─────────────────── Mạng nội bộ Docker: pitchos-network ──────────────────────────
```

### Bảng cấu hình các Service trong Docker Compose:
| Tên Container | Eureka Service ID | Port Host | Cơ sở dữ liệu | Số Instance | Ghi chú vận hành |
|---|---|:---:|---|:---:|---|
| `pitchos-service-registry` | – | `8761` | – | 1 | Khởi động đầu tiên, quản lý danh bạ |
| `pitchos-auth-service` | `pitchos-auth-service` | `8081` | `pitchos_user_db` | 1 | Xác thực JWT, nạp sẵn 3 tài khoản |
| `pitchos-pitch-service-1` | `pitchos-pitch-service` | `8082` | `pitchos_pitch_db` | **2** | Instance Provider 1 |
| `pitchos-pitch-service-2` | `pitchos-pitch-service` | `8084` | `pitchos_pitch_db` | ^ | Instance Provider 2 (cùng Service ID, chung DB) |
| `pitchos-booking-service` | `pitchos-booking-service` | `8083` | `pitchos_booking_db` | 1 | Consumer gọi Pitch, giữ 1 instance để chống đặt trùng |
| `mysql-auth`, `mysql-pitch`, `mysql-booking` | – | `3306` nội bộ | 3 DB riêng biệt | 3 | Gắn Named Volume, nạp tự động qua file SQL init |

---

## IV. BẢNG PHÂN CÔNG NHIỆM VỤ 4 THÀNH VIÊN

### 1. Phân định vùng sở hữu mã nguồn (Code Ownership)
*Nguyên tắc: Mỗi người sở hữu tuyệt đối một vùng thư mục để tránh xung đột trên Git.*

```
c:\Users\viduc\Downloads\PTPM\
├── pitchos-service-registry/    ──► SỞ HỮU BỞI: HOÀNG
├── pitchos-auth-service/        ──► SỞ HỮU BỞI: HOÀNG
├── pitchos-pitch-service/       ──► SỞ HỮU BỞI: LINH
├── pitchos-booking-service/     ──► SỞ HỮU BỞI: NHẬT
├── pitchos-database/           ──► SỞ HỮU BỞI: HÙNG
├── scripts/                    ──► SỞ HỮU BỞI: HÙNG
├── docker-compose.yml          ──► SỞ HỮU BỞI: LINH
├── postman/collection.json     ──► SỞ HỮU BỞI: NHẬT
├── README.md & .gitignore      ──► SỞ HỮU BỞI: HOÀNG
└── docs/kt2/                   ──► CẢ 4 THÀNH VIÊN (viết file riêng)
```

### 2. Bảng phân công chi tiết công việc

| Thành viên | Trách nhiệm Code & Vận hành | Trách nhiệm Báo cáo & Điểm chi tiết | File giao nộp cụ thể |
|---|---|---|---|
| **HOÀNG** *(Nhóm trưởng)* | 1. Xây dựng module **`pitchos-service-registry`** (Eureka Server port 8761).<br>2. Cập nhật `pitchos-auth-service`: thêm Eureka Client, Actuator, **xóa bỏ in mật khẩu mặc định ra log**.<br>3. Gỡ theo dõi file `.env` thật trên Git, cấu hình `.gitignore`.<br>4. Viết `README.md` chuẩn giúp người lạ clone về chạy 1 lệnh là lên toàn bộ.<br>5. Thực hiện test bộ **TC01–TC06** (Service Registry) & bảng 20 request cân bằng tải.<br>6. Review & merge toàn bộ Pull Request của các thành viên. | • **Câu 1.2 (0.5đ):** Lý thuyết Service Registry, Discovery, Eureka vs API Gateway, Service ID.<br>• **Phần 2.1a (0.5đ):** Sơ đồ kiến trúc tích hợp và triển khai (trước & sau khi có Eureka/Docker).<br>• **Phần 4 (1.5đ):** Service Registry (Eureka, cơ chế đăng ký, cân bằng tải LoadBalancer, bảng 20 request).<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM**<br>• Tổng hợp và xuất file `docs/report.pdf`. | • `pitchos-service-registry/*`<br>• `docs/kt2/CAU1_2_HOANG.md`<br>• `docs/kt2/PHAN_2_HOANG.md`<br>• `docs/kt2/PHAN_4_HOANG.md`<br>• `docs/testing/service-discovery-test.md`<br>• `README.md` |
| **LINH** | 1. Cập nhật `pitchos-pitch-service`: thêm Eureka Client, Actuator, bổ sung endpoint **`/api/v1/instance-info`** và cấu hình ghi rõ instance trong log.<br>2. Viết `Dockerfile` multi-stage chuẩn không chạy quyền root cho Pitch Service.<br>3. Xây dựng file **`docker-compose.yml`** hoàn chỉnh toàn hệ thống: 4 Java services, 3 MySQL container, cấu hình network `pitchos-network`, healthcheck (`service_healthy`), restart policy.<br>4. Tạo file **`.env.example`** chuẩn và đầy đủ biến môi trường. | • **Câu 1.3 (0.5đ):** Lý thuyết Docker Image, Container, vai trò Dockerfile và Docker Compose.<br>• **Phần 1:** Giới thiệu hệ thống PitchOS, phạm vi đề tài, bảng tổng hợp công nghệ mới.<br>• **Phần 5 (2.0đ):** Triển khai hệ thống (Chi tiết Dockerfile, Compose, Network nội bộ, Volume, Biến môi trường).<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM** | • `pitchos-pitch-service/*`<br>• `docker-compose.yml`<br>• `.env.example`<br>• `docs/kt2/CAU1_3_LINH.md`<br>• `docs/kt2/PHAN_1_LINH.md`<br>• `docs/kt2/PHAN_5_LINH.md` |
| **NHẬT** | 1. Cập nhật `pitchos-booking-service`: chuyển FeignClient sang gọi bằng **Service ID** (`name = "pitchos-pitch-service"`), xóa URL hardcode.<br>2. Bổ sung **kiểm tra tính hợp lệ dữ liệu từ Provider**: giá <= 0 hoặc null, sân đang bảo trì ➔ Trả mã lỗi rõ ràng (**502 Bad Gateway** hoặc 400).<br>3. Thêm endpoint Consumer gọi instance info (ví dụ `GET /api/v1/bookings/pitch-instance`) để gửi 20 request kiểm thử cân bằng tải.<br>4. Chuẩn hóa và gộp toàn bộ test case vào file duy nhất: **`postman/collection.json`**.<br>5. Chạy và chụp minh chứng bộ test tích hợp **IT01–IT07**. | • **Câu 1.1 (0.5đ):** Lý thuyết Provider/Consumer, các bước Consumer gọi API, kỹ thuật xử lý khi Provider lỗi (timeout, fallback, không gọi trực tiếp DB).<br>• **Phần 3 (2.0đ):** Tích hợp dịch vụ (Quy trình nghiệp vụ đặt sân, API Contract, cơ chế Feign + LoadBalancer, xử lý lỗi 404/502/503/timeout).<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM** | • `pitchos-booking-service/*`<br>• `postman/collection.json`<br>• `docs/kt2/CAU1_1_NHAT.md`<br>• `docs/kt2/PHAN_3_NHAT.md`<br>• `docs/api/api-contract.md`<br>• `docs/testing/integration-test.md` |
| **HÙNG** *(Bạn)* | 1. Quản trị Cơ sở dữ liệu: Tách và chuẩn bị 3 file SQL nạp dữ liệu sạch cho 3 DB trong thư mục `pitchos-database/` (`auth-init.sql`, `pitch-init.sql`, `booking-init.sql`).<br>2. Cấu hình Docker Named Volume đảm bảo dữ liệu ghi bền vững xuống ổ cứng container.<br>3. Viết các kịch bản kiểm thử: `scripts/check-health.bat` (hoặc `.sh`), `scripts/test-persistence.bat`.<br>4. Thực hiện toàn bộ kịch bản kiểm thử vận hành, giám sát và sự cố **DEP01–DEP08**.<br>5. Thu thập và đối soát log của ít nhất 2 dịch vụ (Booking và Pitch) khi phát sinh lỗi kết nối. | • **Câu 1.4 (0.5đ):** Lý thuyết 3 mức (Container Status, App Health, Business Availability); vai trò Health Check, Log, Volume.<br>• **Phần 2.1b (0.5đ):** Bảng mô tả dịch vụ, phân định trách nhiệm CSDL phân tán & Logical ID.<br>• **Phần 6 (1.5đ):** Vận hành hệ thống (Kiểm tra Actuator `/actuator/health`, phân tích log 2 dịch vụ, kiểm thử dừng/bật container, bảo toàn dữ liệu sau restart, **phân tích tình huống sự cố cụ thể**).<br>• **Phần 7:** Đánh giá & Kết luận.<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM** | • `pitchos-database/*.sql`<br>• `scripts/*`<br>• `docs/kt2/CAU1_4_HUNG.md`<br>• `docs/kt2/PHAN_2_HUNG.md`<br>• `docs/kt2/PHAN_6_HUNG.md`<br>• `docs/kt2/PHAN_7_HUNG.md`<br>• `docs/testing/operation-test.md`<br>• `docs/operation/failure-analysis.md` |

---

## V. DANH MỤC VIỆC CẦN LÀM CHI TIẾT THEO KỸ THUẬT

### 1. Chuẩn hóa chung cho tất cả các Service Java (Hoàng, Linh, Nhật đều phải làm)
1. **Thêm dependency vào `pom.xml`**:
   ```xml
   <dependency>
       <groupId>org.springframework.cloud</groupId>
       <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
   </dependency>
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-actuator</artifactId>
   </dependency>
   ```
2. **Cấu hình `application.properties` (chỉ đặt trong `src/main/resources/`)**:
   ```properties
   eureka.client.service-url.defaultZone=${EUREKA_URL:http://localhost:8761/eureka/}
   eureka.instance.prefer-ip-address=true
   eureka.instance.instance-id=${spring.application.name}:${INSTANCE_ID:${server.port}}
   management.endpoints.web.exposure.include=health,info
   management.endpoint.health.show-details=never
   ```
3. **Mở quyền trong `SecurityConfig`**:
   Cho phép truy cập không cần token: `.requestMatchers("/actuator/health", "/actuator/info").permitAll()`.
4. **Viết `Dockerfile` Multi-stage**:
   Sử dụng Maven build phase và Eclipse Temurin JRE 17 runtime, tạo `appuser` (không chạy quyền root).
5. **Dọn dẹp**: Xóa bỏ các file `application.properties` trùng lặp ở thư mục gốc của từng service.

---

### 2. Danh mục các bộ kiểm thử bắt buộc (Phục vụ lấy điểm Báo cáo & Video)

#### 🔹 Bộ 1: Kiểm thử Tích hợp & Xử lý lỗi Consumer → Provider (Nhật phụ trách)
| Mã Test | Tình huống kiểm thử | Hành động & Dữ liệu | Kết quả mong đợi |
|---|---|---|---|
| **IT01** | Đặt sân hợp lệ | Gửi giờ hợp lệ, sân tồn tại và đang hoạt động | `201 Created`, `totalPrice` = số giờ × giá sân |
| **IT02** | Sân không tồn tại | Gửi `pitchId = 9999` | `404 Not Found`, thông báo lỗi rõ ràng từ Provider |
| **IT03** | Dữ liệu Provider không hợp lệ | Giá sân <= 0 hoặc null, trạng thái bảo trì | Trả về lỗi kiểm tra dữ liệu (**502 Bad Gateway** hoặc 400) |
| **IT04** | Provider sập hoàn toàn | Dừng cả 2 container Pitch (`docker compose stop ...`) | `503 Service Unavailable`, không bị treo hay sập Booking |
| **IT05** | Timeout mạng | Pause container Pitch (`docker compose pause ...`) | Sau 2-3s trả về `503 Gateway Timeout`, sau đó unpause |
| **IT06** | Gửi lặp yêu cầu đặt sân | Gửi 2 lần cùng một khung giờ cho 1 sân | Lần 1 `201 Created`, lần 2 `400 Bad Request` ("Trùng giờ") |
| **IT07** | Dữ liệu đầu vào sai | `endTime` trước `startTime` | `400 Bad Request` ngay tại tầng validation |

#### 🔹 Bộ 2: Kiểm thử Service Discovery & Cân bằng tải (Hoàng phụ trách)
| Mã Test | Tình huống kiểm thử | Hành động & Dữ liệu | Kết quả mong đợi |
|---|---|---|---|
| **TC01** | Đăng ký dịch vụ | Khởi động Registry + các service | Eureka Dashboard hiện đủ các Service ID, Pitch có 2 instance |
| **TC02** | Gọi qua Service ID | Booking gọi Pitch qua Service ID | Đặt sân thành công mà không cần URL tĩnh |
| **TC03** | Cân bằng tải 2 instance | Gửi 20 request liên tiếp qua Consumer | Cả 2 instance Pitch-1 và Pitch-2 đều nhận request (lập bảng phân phối) |
| **TC04** | Dừng 1 instance Provider | Dừng Pitch-1 (`docker compose stop pitchos-pitch-service-1`) | Pitch-2 vẫn xử lý 100% request đặt sân bình thường |
| **TC05** | Dừng toàn bộ Provider | Dừng cả Pitch-1 và Pitch-2 | Consumer trả lỗi 503 sạch sẽ, không sập dây chuyền |
| **TC06** | Khởi động lại Provider | Khởi động lại Pitch-1 và Pitch-2 | Đăng ký lại vào Eureka sau khoảng 30s và hoạt động bình thường |

#### 🔹 Bộ 3: Kiểm thử Vận hành, Giám sát & Bảo toàn dữ liệu (Hùng phụ trách)
| Mã Test | Tình huống kiểm thử | Hành động & Dữ liệu | Kết quả mong đợi |
|---|---|---|---|
| **DEP01** | Khởi động toàn hệ thống | Chạy lệnh `docker compose up -d` | Tất cả 7 container chạy và đạt trạng thái `healthy` |
| **DEP02** | Kiểm tra sức khỏe | Truy vấn `GET /actuator/health` của cả 4 service | Trả về `{"status":"UP"}` |
| **DEP03** | Đọc log liên dịch vụ | Đọc log đồng thời của Booking và Pitch | Thấy dòng log nhận request và xử lý logic giữa 2 service |
| **DEP04** | Dừng Booking Service | Dừng container Booking | Các service khác vẫn sống; Eureka loại bỏ Booking sau độ trễ |
| **DEP05** | Khởi động lại Booking | Bật lại container Booking | Đăng ký lại vào Eureka, đặt sân lại bình thường |
| **DEP06** | Kiểm tra Volume MySQL | `docker compose down` rồi `docker compose up -d` (không có cờ `-v`) | Toàn bộ dữ liệu đặt sân đã tạo trước đó **vẫn còn nguyên vẹn** |
| **DEP07** | Phân tích sự cố đặc thù | Dừng container `mysql-pitch` | Actuator của Pitch chuyển `DOWN`, log ghi rõ mất kết nối DB |
| **DEP08** | Phục hồi sau sự cố | Khởi động lại container MySQL | Service tự kết nối lại thành công mà không cần restart lại mã nguồn |

---

## VI. KHUNG BÁO CÁO 7 PHẦN & CẤU TRÚC THƯ MỤC NỘP BÀI

### 1. Khung báo cáo thống nhất (Theo đúng Mục III.1 của đề thi)
*Báo cáo bắt đầu bằng 4 câu trả lời Lý thuyết Câu 1 (2.0đ), sau đó đi vào 7 phần chính thức:*

* **CÂU 1. LÝ THUYẾT NỀN TẢNG (2,0 ĐIỂM)**
  * 1.1: Provider/Consumer & Xử lý lỗi (Nhật)
  * 1.2: Service Registry, Service Discovery & Eureka vs API Gateway (Hoàng)
  * 1.3: Docker Image vs Container, Dockerfile & Compose (Linh)
  * 1.4: 3 Mức trạng thái & Vai trò Healthcheck, Log, Volume (Hùng)
* **PHẦN 1: GIỚI THIỆU HỆ THỐNG PITCHOS** *(Linh viết)*
  * Tên đề tài, bài toán đặt sân bóng, công nghệ sử dụng (bổ sung Eureka, Feign, LoadBalancer, Actuator, Docker).
  * Làm rõ: phần nào kế thừa từ KT1, phần nào mới phát triển cho KT2.
* **PHẦN 2: PHÂN TÍCH VÀ THIẾT KẾ KIẾN TRÚC** *(Hoàng viết)*
  * Sơ đồ kiến trúc trước KT2 (URL cứng) và sau KT2 (Eureka, Docker, 2 instance Pitch).
  * Bảng mô tả chi tiết từng dịch vụ: Tên, chức năng, API chính, DB, Consumer/Provider, số instance.
* **PHẦN 3: TÍCH HỢP VÀ TIÊU THỤ DỊCH VỤ** *(Nhật viết)*
  * Quy trình nghiệp vụ Khách đặt sân.
  * API Contract chi tiết (`docs/api/api-contract.md`).
  * Đoạn mã OpenFeign gọi theo Service ID và kiểm tra dữ liệu Provider.
  * Bảng minh chứng kiểm thử tích hợp (IT01–IT07) kèm ảnh Postman và phân tích.
* **PHẦN 4: SERVICE REGISTRY VÀ CÂN BẰNG TẢI** *(Hoàng viết)*
  * Cấu hình Eureka Server và Eureka Client.
  * Cơ chế cân bằng tải Spring Cloud LoadBalancer.
  * Minh chứng Dashboard Eureka, Bảng kết quả 20 request và bộ test TC01–TC06.
* **PHẦN 5: CONTAINER HÓA VÀ TRIỂN KHAI TOÀN HỆ THỐNG** *(Linh viết)*
  * Chi tiết cấu trúc Dockerfile multi-stage.
  * File `docker-compose.yml`, cấu hình mạng Docker network, biến môi trường `.env.example`.
  * Cơ chế Named Volume bảo toàn dữ liệu cho 3 CSDL.
* **PHẦN 6: VẬN HÀNH, GIÁM SÁT VÀ KIỂM THỬ SỰ CỐ** *(Hùng viết)*
  * Kết quả giám sát trạng thái qua Spring Boot Actuator (`/actuator/health`).
  * Trích xuất và phân tích log hoạt động của Booking và Pitch.
  * Bảng kết quả kiểm thử vận hành DEP01–DEP08.
  * **Phân tích chuyên sâu 1 tình huống sự cố thực tế**: Nguyên nhân ➔ Ảnh hưởng ➔ Phương án xử lý.
* **PHẦN 7: ĐÁNH GIÁ VÀ KẾT LUẬN** *(Hùng viết)*
  * Bảng tự đánh giá điểm số theo barem của giảng viên.
  * Các vấn đề kỹ thuật phát sinh và bài học kinh nghiệm.
  * Hướng phát triển nâng cấp hệ thống (API Gateway, Circuit Breaker Resilience4j).

---

### 2. Cấu trúc thư mục nộp bài chuẩn (Theo Mục III.2 của đề thi)
```
PTPM-NhomXX-PitchOS/
├── pitchos-service-registry/       # Module Eureka Server (Hoàng)
├── pitchos-auth-service/           # Module Auth & User (Hoàng)
├── pitchos-pitch-service/          # Module Pitch - 2 instance (Linh)
├── pitchos-booking-service/        # Module Booking - Consumer (Nhật)
├── pitchos-database/               # 3 file SQL init sạch (Hùng)
│   ├── auth-init.sql
│   ├── pitch-init.sql
│   └── booking-init.sql
├── scripts/                        # Script kiểm tra sức khỏe và dữ liệu (Hùng)
│   ├── check-health.bat
│   └── test-persistence.bat
├── postman/                        # File Postman collection chuẩn nộp bài (Nhật)
│   └── collection.json
├── docker-compose.yml              # File chạy toàn hệ thống (Linh)
├── .env.example                    # File mẫu biến môi trường (Linh)
├── .gitignore                      # Chặn commit .env và target (Hoàng)
├── README.md                       # Hướng dẫn chạy 1 lệnh từ đầu trên máy sạch (Hoàng)
└── docs/                           # Thư mục báo cáo & tài liệu minh chứng
    ├── report.pdf                  # Báo cáo tổng hợp chính thức (Hoàng xuất)
    ├── architecture/
    │   ├── integration-architecture.png
    │   └── deployment-architecture.png
    ├── api/
    │   └── api-contract.md
    ├── testing/
    │   ├── integration-test.md
    │   ├── service-discovery-test.md
    │   └── operation-test.md
    └── operation/
        └── failure-analysis.md
```

---

## VII. KỊCH BẢN QUAY VIDEO DEMO CÁ NHÂN 8 BƯỚC
*(Bắt buộc: 40% Điểm cá nhân — Mỗi thành viên tự chạy trên máy mình và quay video màn hình từ 10 đến 15 phút theo đúng 8 bước)*

* **Bước 1: Giới thiệu kiến trúc tổng thể (1 phút)**
  * Mở sơ đồ kiến trúc: Trình bày các microservices, chỉ rõ Booking Service là Consumer, Pitch Service là Provider chạy 2 instance để cân bằng tải và chịu lỗi.
* **Bước 2: Khởi động hệ thống bằng Docker Compose (1.5 phút)**
  * Chạy lệnh: `docker compose up -d`
  * Chạy lệnh: `docker compose ps` ➔ Chỉ cho thầy thấy toàn bộ 7 container đều đang ở trạng thái `healthy` hoặc `Up`.
* **Bước 3: Kiểm tra Service Registry Eureka (1.5 phút)**
  * Mở trình duyệt truy cập `http://localhost:8761`.
  * Chỉ rõ trên Dashboard: Các dịch vụ đã đăng ký thành công, trong đó `PITCHOS-PITCH-SERVICE` hiển thị rõ **2 instances** (cổng 8082 và 8084).
* **Bước 4: Thực hiện quy trình nghiệp vụ Consumer gọi Provider (2 phút)**
  * Mở Postman: Gửi request đăng nhập `POST /api/v1/auth/login` lấy Bearer Token của tài khoản khách hàng.
  * Gửi request đặt sân `POST /api/v1/bookings` kèm Token ➔ Nhận mã **`201 Created`**, chỉ ra giá tiền `totalPrice` được tự động tính toán dựa trên đơn giá từ Pitch Service.
* **Bước 5: Minh họa tối thiểu 2 tình huống lỗi tích hợp (2 phút)**
  * Gửi `pitchId = 9999` (sân không tồn tại) ➔ Nhận lỗi **`404 Not Found`**.
  * Dừng cả 2 instance Pitch (`docker compose stop pitchos-pitch-service-1 pitchos-pitch-service-2`) rồi bấm đặt sân ➔ Nhận lỗi **`503 Service Unavailable`** (chứng minh hệ thống có xử lý lỗi, không bị treo). Bật lại Pitch Service.
* **Bước 6: Kiểm tra Actuator Health & Xem Log liên dịch vụ (2 phút)**
  * Trên trình duyệt: Truy cập `http://localhost:8083/actuator/health` ➔ Thấy `{"status":"UP"}`.
  * Mở terminal chạy `docker compose logs --tail=50 pitchos-booking-service pitchos-pitch-service-1` ➔ Chỉ cho thấy dòng log Consumer gửi request và Provider nhận xử lý.
* **Bước 7: Kiểm thử dừng 1 instance Provider & Khả năng chịu lỗi (2 phút)**
  * Dừng instance 1: `docker compose stop pitchos-pitch-service-1`.
  * Trên Postman gửi request đặt sân ➔ Vẫn nhận mã **`201 Created`** thành công.
  * Giải thích: *Nhờ có Eureka và Spring Cloud LoadBalancer, hệ thống tự động định tuyến sang Pitch instance 2 đang chạy ở cổng 8084.*
* **Bước 8: Kiểm tra bảo toàn dữ liệu bằng Docker Volume (2 phút)**
  * Chạy lệnh tắt toàn bộ: `docker compose down` (nhấn mạnh: **không dùng cờ -v**).
  * Chạy lại hệ thống: `docker compose up -d`.
  * Vào kiểm tra lại đơn đặt sân vừa tạo ở Bước 4 vẫn còn nguyên vẹn trong CSDL ➔ Khẳng định Named Volume hoạt động bền vững.

---

## VIII. QUY TRÌNH PHỐI HỢP GIT & LỊCH TRÌNH 7 NGÀY

### 1. Quy tắc Git Flow không xung đột
1. Nhánh `main` được bảo vệ: Tuyệt đối không commit trực tiếp lên `main`.
2. Mỗi người làm việc trên 1 nhánh riêng: `hoang`, `linh`, `nhat`, `hung`.
3. Khi hoàn thành một tính năng:
   ```bash
   git checkout <nhanh-cua-ban>
   git pull origin main --rebase
   git add <cac-file-trong-vung-so-huu>
   git commit -m "[KT2][vung-so-huu] Noi dung cong viec"
   git push origin <nhanh-cua-ban>
   ```
4. Tạo Pull Request trên GitHub hướng về `main` để Hoàng duyệt và merge.

### 2. Lịch trình hành động 7 ngày
* **Ngày 1:** Hoàng dựng `pitchos-service-registry`; thống nhất hợp đồng API `/instance-info`. Cả nhóm pull code mẫu về.
* **Ngày 2:** Linh hoàn thiện `pitchos-pitch-service` (thêm `/instance-info`); Nhật sửa Feign sang Service ID; Hùng tách 3 file SQL init; mỗi người viết nháp câu hỏi lý thuyết của mình.
* **Ngày 3:** Linh viết `docker-compose.yml`; Hùng cấu hình volume và script test; Nhật chạy thử bộ test tích hợp IT01–IT07 cục bộ.
* **Ngày 4:** Khởi chạy toàn bộ hệ thống trên Docker Compose; sửa các lỗi kết nối môi trường đến khi toàn bộ container đều `healthy`.
* **Ngày 5:** Hoàng chạy TC01–TC06 và bảng 20 request; Hùng chạy DEP01–DEP08 và thu thập log; Nhật hoàn thiện file `postman/collection.json`.
* **Ngày 6:** Viết hoàn chỉnh 7 phần báo cáo vào thư mục `docs/kt2/`; Hoàng tổng hợp thành file `docs/report.pdf`.
* **Ngày 7:** **Từng thành viên tự quay video demo cá nhân 8 bước trên máy tính của mình**; kiểm tra lại toàn bộ file nộp bài trước khi nộp cho giảng viên.

---

## IX. CÁC BẪY KỸ THUẬT CẦN TUYỆT ĐỐI TRÁNH
*(Rút ra trực tiếp từ lưu ý của giảng viên trong TH6, TH7, TH8)*

1. ❌ **Bẫy `localhost` trong container:** Khi đóng gói vào Docker, `localhost` trỏ về chính container đó. Gọi dịch vụ khác hoặc MySQL bắt buộc phải dùng tên container (ví dụ `EUREKA_URL=http://pitchos-service-registry:8761/eureka/`, `MYSQL_HOST=mysql-pitch`).
2. ❌ **Bẫy cờ `docker compose down -v`:** Lệnh `down` có cờ `-v` sẽ **xóa sạch volume dữ liệu**. Tuyệt đối không dùng cờ `-v` khi quay video minh họa bảo toàn dữ liệu.
3. ❌ **Bẫy hardcode URL trong Feign:** Nếu trong `@FeignClient` vẫn còn thuộc tính `url = "..."` thì dù Eureka có chạy, Consumer vẫn gọi qua URL tĩnh ➔ Giảng viên trừ điểm nặng mục Service Discovery. Bắt buộc chỉ dùng `name = "pitchos-pitch-service"`.
4. ❌ **Bẫy lộ mật khẩu trong Log:** Tuyệt đối không in mật khẩu hoặc chuỗi JWT đầy đủ ra màn hình console / log.
5. ❌ **Bẫy tranh chấp khởi tạo DB (Race Condition):** Khi chạy 2 instance Pitch Service cùng kết nối vào 1 DB rỗng, cả 2 có thể cùng chạy `DataInitializer` chèn trùng dữ liệu ➔ Cấu hình `depends_on: pitchos-pitch-service-1: condition: service_healthy` cho instance 2.
6. ❌ **Bẫy độ trễ của Eureka (30s latency):** Khi tắt 1 instance, Eureka và LoadBalancer mất từ 15–30s mới cập nhật bảng định tuyến. Trong khoảng thời gian này request có thể gặp lỗi tạm thời. Đây là cơ chế tự nhiên của Eureka, cần giải thích rõ trong báo cáo, không giấu lỗi.
