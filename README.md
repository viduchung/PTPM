# ⚽ PitchOS — Hệ Thống Đặt Sân Bóng Trực Tuyến
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### BÀI KIỂM TRA SỐ 2 (TX2) — CHUẨN ĐẦU RA CĐR L2 (TỔNG: 10,0 ĐIỂM)

> 📌 **Định hướng đánh giá KT2:** Khác với Bài kiểm tra số 1 (tập trung vào REST API đơn lẻ và bảo mật), Bài kiểm tra số 2 đánh giá năng lực **tích hợp, container hóa và vận hành** hệ thống Microservices trong thực tế:
> 1. **Tích hợp & Tiêu thụ dịch vụ (TH6):** Consumer (Booking) gọi Provider (Pitch) qua OpenFeign, kiểm tra tính toàn vẹn dữ liệu và xử lý lỗi phân tán.
> 2. **Service Registry & Cân bằng tải (TH7):** Eureka Server quản lý danh bạ, gọi dịch vụ qua **Service ID** (bỏ URL cứng), chạy **2 instance Pitch Service** để cân bằng tải và chịu lỗi.
> 3. **Triển khai & Vận hành Docker (TH8):** Đóng gói Dockerfile multi-stage, điều phối toàn bộ hệ thống bằng `docker-compose.yml`, kiểm tra sức khỏe Spring Boot Actuator, giám sát log và bảo toàn dữ liệu bằng Docker Named Volume.
> 
> ⚖️ **Cơ cấu chấm điểm:** **60% Điểm nhóm** (Báo cáo chuyên đề 7 phần + Mã nguồn) và **40% Điểm cá nhân** (Video demo độc lập 8 bước của từng thành viên).

---

## 🧭 1. KIẾN TRÚC TỔNG THỂ HỆ THỐNG PITCHOS (KT2)

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

### Bảng cấu hình các Service trong hệ thống:
| Tên Container / Module | Eureka Service ID | Port Host | Cơ sở dữ liệu | Số Instance | Vai trò kiến trúc |
|---|---|:---:|---|:---:|---|
| **`pitchos-service-registry`** | – | `8761` | – | 1 | Quản lý danh bạ dịch vụ trung tâm (Eureka Server) |
| **`pitchos-auth-service`** | `pitchos-auth-service` | `8081` | `pitchos_user_db` | 1 | Xác thực & Cấp phát JWT Token, RBAC 3 role |
| **`pitchos-pitch-service-1`** | `pitchos-pitch-service` | `8082` | `pitchos_pitch_db` | **2** | **Provider** quản lý sân bóng (Instance 1) |
| **`pitchos-pitch-service-2`** | `pitchos-pitch-service` | `8084` | `pitchos_pitch_db` | ^ | **Provider** quản lý sân bóng (Instance 2, chung DB) |
| **`pitchos-booking-service`** | `pitchos-booking-service` | `8083` | `pitchos_booking_db` | 1 | **Consumer** gọi Pitch qua Service ID & đặt sân |
| **`mysql-auth / pitch / booking`**| – | `3306` nội bộ | 3 DB riêng biệt | 3 | Lưu trữ dữ liệu bền vững qua Named Volume |

---

## 👥 2. BẢNG PHÂN CHIA NHIỆM VỤ 4 THÀNH VIÊN (KT2)

> 📖 *Kế hoạch tổng thể và ma trận trách nhiệm chi tiết xem tại file:* 👉 [KE_HOACH_KIEM_TRA_2.md](file:///c:/Users/viduc/Downloads/PTPM/KE_HOACH_KIEM_TRA_2.md)

| STT | Thành viên | Vùng mã nguồn sở hữu | Trách nhiệm Code & Vận hành | Trách nhiệm viết Báo cáo & Điểm chi tiết | File checklist cá nhân |
|:---:|:---|:---|:---|:---|:---:|
| **1** | 👑 **HOÀNG**<br>*(Nhóm trưởng)* | `pitchos-service-registry/`<br>`pitchos-auth-service/`<br>`README.md`, `.gitignore` | • Dựng Eureka Server (:8761).<br>• Auth: Actuator, Eureka client, **xóa in mật khẩu ra log**.<br>• Gỡ `.env` khỏi Git; viết `README.md`.<br>• Chạy bộ test **TC01–TC06** & 20 request cân bằng tải.<br>• Review & merge toàn bộ PR. | • **Câu 1.2 (0.5đ):** Service Registry & Discovery, Eureka vs Gateway, Service ID.<br>• **Phần 2.1a (0.5đ):** Sơ đồ kiến trúc tích hợp và triển khai (trước & sau).<br>• **Phần 4 (1.5đ):** Service Registry, Eureka & LoadBalancer.<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM**<br>• Tổng hợp và xuất file `docs/report.pdf`. | 👉 [NHIEM_VU_HOANG.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_HOANG.md) |
| **2** | 🌸 **LINH** | `pitchos-pitch-service/`<br>`docker-compose.yml`<br>`.env.example` | • Pitch: Actuator, Eureka client, endpoint `/api/v1/instance-info`.<br>• Viết `Dockerfile` multi-stage cho Pitch.<br>• Viết file **`docker-compose.yml`** chạy 7 container (2 instance Pitch, network, healthcheck, volume).<br>• Tạo `.env.example`. | • **Câu 1.3 (0.5đ):** Docker Image vs Container, Dockerfile & Compose.<br>• **Phần 1:** Giới thiệu hệ thống PitchOS, công nghệ mới.<br>• **Phần 5 (2.0đ):** Container hóa và Triển khai toàn hệ thống (Compose, Network, Volume).<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM** | 👉 [NHIEM_VU_LINH.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_LINH.md) |
| **3** | ⚡ **NHẬT** | `pitchos-booking-service/`<br>`postman/collection.json` | • Booking: Đổi Feign sang **Service ID** (bỏ URL cứng).<br>• **Kiểm tra dữ liệu Provider** (giá <= 0 / sân bảo trì trả lỗi **502**).<br>• Thêm endpoint `pitch-instance` test LoadBalancer.<br>• Gộp `postman/collection.json`; chạy test **IT01–IT07**. | • **Câu 1.1 (0.5đ):** Consumer/Provider, quy trình gọi API, xử lý lỗi khi Provider chết/timeout.<br>• **Phần 3 (2.0đ):** Tích hợp và Tiêu thụ dịch vụ (OpenFeign, API contract, xử lý lỗi 404/502/503/timeout).<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM** | 👉 [NHIEM_VU_NHAT.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_NHAT.md) |
| **4** | 🛡️ **HÙNG** | `pitchos-database/`<br>`scripts/`<br>Khối MySQL Compose | • Tách 3 file SQL init sạch (`pitchos-database/*.sql`).<br>• Cấu hình Named Volume MySQL bền vững.<br>• Viết script `check-health` & `test-persistence`.<br>• Chạy toàn bộ bộ test vận hành **DEP01–DEP08**.<br>• Thu thập và phân tích log 2 service. | • **Câu 1.4 (0.5đ):** 3 mức trạng thái (Container Status, App Health, Business Availability); vai trò Healthcheck, Log, Volume.<br>• **Phần 2.1b (0.5đ):** Bảng mô tả dịch vụ, phân định trách nhiệm CSDL phân tán & Logical ID.<br>• **Phần 6 (1.5đ):** Vận hành hệ thống (Actuator, log, restart service, **phân tích sự cố**).<br>• **Phần 7:** Đánh giá & Kết luận.<br>➔ **TỔNG: 2,50 / 10,0 ĐIỂM** | 👉 [NHIEM_VU_HUNG.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_HUNG.md) |

---

## 🚀 3. HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG

### 🔹 Cách 1: Khởi chạy toàn bộ bằng Docker Compose (Khuyên dùng — 1 lệnh duy nhất)

> **Yêu cầu trước khi chạy:**
> - Đã cài đặt và khởi động **Docker Desktop** trên máy tính.
> - Đảm bảo cổng `8761`, `8081`, `8082`, `8083`, `8084` không bị chiếm dụng bởi tiến trình khác.

Mở Terminal (PowerShell hoặc CMD) tại thư mục gốc dự án và thực hiện:

```bash
# 1. Tạo file cấu hình môi trường từ mẫu (nếu chưa có)
copy .env.example .env

# 2. Xây dựng image và khởi động toàn bộ 7 container chạy ngầm
docker compose up -d --build

# 3. Kiểm tra trạng thái toàn bộ các container (đợi ~30-45s để đạt healthy)
docker compose ps
```

#### 🌐 Các địa chỉ truy cập kiểm tra:
* **Eureka Dashboard:** [http://localhost:8761](http://localhost:8761) *(Thấy 4 Service IDs, riêng Pitch có 2 instances)*
* **Auth Service Swagger:** [http://localhost:8081/swagger-ui.html](http://localhost:8081/swagger-ui.html)
* **Pitch Service 1 Swagger:** [http://localhost:8082/swagger-ui.html](http://localhost:8082/swagger-ui.html)
* **Pitch Service 2 Swagger:** [http://localhost:8084/swagger-ui.html](http://localhost:8084/swagger-ui.html)
* **Booking Actuator Health:** [http://localhost:8083/actuator/health](http://localhost:8083/actuator/health) *(Kết quả: `{"status":"UP"}`)*

#### 🛑 Dừng hệ thống:
```bash
# Dừng container nhưng BẢO TOÀN DỮ LIỆU CSDL (Named Volume được giữ nguyên)
docker compose down

# ⚠️ LƯU Ý SỐNG CÒN: Tuyệt đối KHÔNG dùng cờ -v nếu không muốn bị xóa sạch dữ liệu CSDL!
```

---

### 🔹 Cách 2: Khởi chạy thủ công từng Service (Local Development khi Code/Debug)

Nếu bạn muốn chạy từng service riêng biệt bằng Maven trong quá trình lập trình:
1. Đảm bảo MySQL cục bộ (cổng 3306) đang bật và đã nạp 3 CSDL (`pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`).
2. Mở 4 cửa sổ Terminal riêng biệt chạy theo thứ tự:
   ```bash
   # Terminal 1: Eureka Server
   cd pitchos-service-registry && mvn spring-boot:run

   # Terminal 2: Auth Service
   cd pitchos-auth-service && mvn spring-boot:run

   # Terminal 3: Pitch Service (Instance 1)
   cd pitchos-pitch-service && mvn spring-boot:run

   # Terminal 4: Booking Service
   cd pitchos-booking-service && mvn spring-boot:run
   ```

---

## 🧪 4. DANH MỤC CÁC BỘ KIỂM THỬ (POSTMAN COLLECTION)

Toàn bộ kịch bản kiểm thử được tổ chức tập trung tại file: 👉 **[`postman/collection.json`](file:///c:/Users/viduc/Downloads/PTPM/postman/collection.json)**

### 1. Bộ kiểm thử Tích hợp & Xử lý lỗi (IT01–IT07 — Nhật phụ trách):
* **IT01:** Khách đặt sân hợp lệ ➔ Trả mã **`201 Created`**, giá tính tự động từ đơn giá Pitch Service.
* **IT02:** Đặt sân không tồn tại (`pitchId = 9999`) ➔ Nhận mã **`404 Not Found`** từ Provider.
* **IT03:** Dữ liệu đơn giá Provider không hợp lệ (giá <= 0 / sân bảo trì) ➔ Nhận mã lỗi **`502 Bad Gateway`** / 400.
* **IT04:** Provider sập hoàn toàn (dừng 2 Pitch) ➔ Nhận mã **`503 Service Unavailable`** sạch sẽ, Booking không sập.
* **IT05:** Timeout mạng (`docker compose pause` Pitch) ➔ Nhận **`503`** sau 2–3s timeout.
* **IT06:** Gửi lặp yêu cầu đặt sân cùng khung giờ ➔ Lần 1 `201 Created`, lần 2 `400 Bad Request` ("Trùng giờ").
* **IT07:** Dữ liệu đầu vào sai (`endTime < startTime`) ➔ Bắt lỗi `400 Bad Request` tại validation.

### 2. Bộ kiểm thử Service Discovery & Cân bằng tải (TC01–TC06 — Hoàng phụ trách):
* **TC01:** Các service tự động đăng ký vào Eureka sau khi khởi động.
* **TC02:** Booking gọi Pitch theo Service ID `pitchos-pitch-service` (không dùng URL cứng).
* **TC03:** Gửi 20 request liên tiếp qua Consumer ➔ LoadBalancer phân phối đều cho cả 2 instance Pitch-1 và Pitch-2.
* **TC04:** Dừng instance Pitch-1 ➔ Hệ thống tự động chuyển sang Pitch-2, đặt sân vẫn thành công.
* **TC05:** Dừng cả 2 instance ➔ Consumer trả lỗi 503 sạch sẽ.
* **TC06:** Khởi động lại ➔ Tự động đăng ký lại vào Eureka và phục hồi sau ~30 giây.

### 3. Bộ kiểm thử Vận hành, Giám sát & Sự cố (DEP01–DEP08 — Hùng phụ trách):
* **DEP01–DEP02:** Khởi chạy `docker compose up -d` và kiểm tra `/actuator/health` = `UP`.
* **DEP03:** Đọc log đồng thời 2 service (`docker compose logs`) chứng minh luồng liên kết.
* **DEP04–DEP05:** Dừng và bật lại Booking Service, quan sát nhịp Heartbeat trên Eureka.
* **DEP06:** Tắt hệ thống bằng `docker compose down` rồi `up -d` ➔ Dữ liệu đơn đặt sân **vẫn còn nguyên vẹn**.
* **DEP07–DEP08:** Dừng container `mysql-pitch` ➔ Actuator Pitch chuyển `DOWN`, log ghi rõ ngắt kết nối; bật lại MySQL ➔ tự động phục hồi.

---

## 🎬 5. CHECKLIST VIDEO DEMO CÁ NHÂN (40% ĐIỂM BẮT BUỘC)

*Mỗi thành viên tự quay video màn hình từ 10–15 phút đủ 8 bước theo chuẩn đề bài:*
1. **Giới thiệu kiến trúc:** Mở sơ đồ kiến trúc, chỉ rõ Consumer (Booking), Provider (Pitch chạy 2 instance).
2. **Khởi động hệ thống:** Chạy `docker compose up -d` ➔ Chạy `docker compose ps` (cho thấy 7 container đều `healthy`).
3. **Kiểm tra Eureka:** Mở `http://localhost:8761` ➔ Thấy đủ các service, Pitch Service hiển thị **2 instances** (:8082 và :8084).
4. **Gọi nghiệp vụ:** Đăng nhập lấy JWT ➔ Gọi `POST /api/v1/bookings` ➔ Nhận mã **`201 Created`**.
5. **Minh họa lỗi tích hợp:** Gọi sân `9999` (404); dừng cả 2 instance Pitch rồi đặt sân (503).
6. **Actuator & Log:** Mở `/actuator/health` = `{"status":"UP"}` ➔ Xem `docker compose logs`.
7. **Khả năng chịu lỗi:** Tắt Pitch instance 1 ➔ Đặt sân vẫn nhận mã **`201 Created`** (nhờ instance 2 phục vụ).
8. **Bảo toàn dữ liệu:** Chạy `docker compose down` (không dùng `-v`) ➔ `docker compose up -d` ➔ Kiểm tra đơn đặt sân vẫn còn nguyên vẹn trong CSDL.

---

## 🗂️ 6. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
PTPM-PitchOS/
├── README.md                      # [TỔNG QUAN] Bảng điều phối KT2 & Hướng dẫn khởi chạy Docker
├── KE_HOACH_KIEM_TRA_2.md         # [KẾ HOẠCH] Kế hoạch nhóm, barem điểm & checklist 7 ngày
├── docker-compose.yml             # [DOCKER] File điều phối khởi chạy toàn bộ 7 container
├── .env.example                   # [ENV] File mẫu các biến môi trường
├── .gitignore                     # [GIT] Chặn commit .env và thư mục target
│
├── NHIEM_VU_HOANG.md              # [HOÀNG] Nhiệm vụ Eureka Server, Auth Service & Báo cáo
├── NHIEM_VU_LINH.md               # [LINH] Nhiệm vụ Pitch 2 instances, Compose & Dockerfile
├── NHIEM_VU_NHAT.md               # [NHẬT] Nhiệm vụ Booking Consumer, Feign Service ID & Postman
├── NHIEM_VU_HUNG.md               # [HÙNG] Nhiệm vụ CSDL MySQL, Scripts, Volume & Vận hành
│
├── pitchos-service-registry/      # Module Eureka Server (Cổng 8761 - Hoàng)
├── pitchos-auth-service/          # Module Auth & User (Cổng 8081 - Hoàng)
├── pitchos-pitch-service/         # Module Pitch - 2 instances (Cổng 8082 & 8084 - Linh)
├── pitchos-booking-service/       # Module Booking - Consumer (Cổng 8083 - Nhật)
│
├── pitchos-database/              # 3 file SQL nạp dữ liệu sạch cho Docker (Hùng)
│   ├── auth-init.sql
│   ├── pitch-init.sql
│   └── booking-init.sql
├── scripts/                       # Kịch bản kiểm tra tự động (Hùng)
│   ├── check-health.bat
│   └── test-persistence.bat
├── postman/                       # Bộ kiểm thử chuẩn nộp bài (Nhật)
│   └── collection.json
│
└── docs/                          # Thư mục Báo cáo & Minh chứng
    ├── report.pdf                 # Bản báo cáo 7 phần chính thức nộp Thầy (Hoàng tổng hợp)
    ├── tx1/                       # Lưu trữ toàn bộ tài liệu & slide đợt kiểm tra TX1 cũ
    ├── kt2/                       # Các file báo cáo từng phần do 4 thành viên soạn thảo
    ├── architecture/              # Sơ đồ kiến trúc trước/sau & bảng mô tả dịch vụ
    ├── api/                       # API Contract chi tiết
    ├── testing/                   # Báo cáo kết quả kiểm thử (IT, TC, DEP)
    └── operation/                 # Phân tích sự cố và hướng dẫn vận hành
```

---

## ⚠️ 7. CÁC BẪY KỸ THUẬT CẦN TUYỆT ĐỐI TRÁNH (LỜI THẦY DẶN)

1. ❌ **Bẫy `localhost` trong container:** Trong môi trường Docker, `localhost` trỏ về chính container đó. Gọi giữa các container bắt buộc phải dùng tên container (ví dụ `EUREKA_URL=http://pitchos-service-registry:8761/eureka/`, `MYSQL_HOST=mysql-pitch`).
2. ❌ **Bẫy cờ `docker compose down -v`:** Cờ `-v` sẽ xóa sạch các volume dữ liệu. Tuyệt đối không dùng `-v` khi demo bảo toàn dữ liệu.
3. ❌ **Bẫy hardcode URL trong Feign:** Trong `@FeignClient` phải dùng `name = "pitchos-pitch-service"`, tuyệt đối không để thuộc tính `url = "..."`.
4. ❌ **Bẫy lộ mật khẩu trong Log:** Không in mật khẩu hoặc JWT đầy đủ ra console/log (đặc biệt trong `DataInitializer`).
5. ❌ **Bẫy độ trễ của Eureka (30s latency):** Eureka cập nhật danh bạ có độ trễ tự nhiên (15–30s). Đây là cơ chế chuẩn của Eureka, cần giải thích rõ trong báo cáo, không giấu lỗi.
