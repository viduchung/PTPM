# ⚽ PitchOS — Hệ Thống Đặt Sân Bóng Trực Tuyến
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### BÀI KIỂM TRA SỐ 2 (TX2) — CHUẨN ĐẦU RA CĐR L2 (TỔNG: 10,0 ĐIỂM)

> 📌 **Định hướng đánh giá KT2:** Khác với Bài kiểm tra số 1 (tập trung vào REST API đơn lẻ và bảo mật), Bài kiểm tra số 2 đánh giá năng lực **tích hợp, container hóa và vận hành** hệ thống Microservices:
> 1. **Tích hợp & Tiêu thụ dịch vụ (TH6):** Consumer (Booking) gọi Provider (Pitch) qua OpenFeign, kiểm tra tính toàn vẹn dữ liệu và xử lý lỗi phân tán (404, 502, 503).
> 2. **Service Registry & Cân bằng tải (TH7):** Eureka Server quản lý danh bạ, gọi dịch vụ qua **Service ID** (loại bỏ hoàn toàn URL cứng), chạy **2 instance Pitch Service** để cân bằng tải và chịu lỗi.
> 3. **Triển khai & Vận hành Docker (TH8):** Đóng gói Dockerfile multi-stage (chạy quyền non-root `appuser`), điều phối 8 container bằng `docker-compose.yml`, kiểm tra sức khỏe Spring Boot Actuator, giám sát log và bảo toàn dữ liệu bằng Docker Named Volumes.
>
> ⚖️ **Cơ cấu chấm điểm:** **60% Điểm nhóm** (Báo cáo chuyên đề 7 phần + Mã nguồn) và **40% Điểm cá nhân** (Video demo độc lập 8 bước của từng thành viên).

---

## 🚀 1. KHỞI CHẠY TRÊN MÁY HOÀN TOÀN SẠCH

Phần này dành cho người **chưa từng mở dự án này**. Làm đúng 4 bước dưới đây là toàn bộ hệ thống 8 container chạy mượt mà, không cần cài đặt Java, Maven hay MySQL trên máy host.

### 1.1. Yêu cầu máy tính

| Hạng mục | Yêu cầu | Cách kiểm tra |
|---|---|---|
| **Docker Desktop** | Đã cài và **đang chạy** (biểu tượng cá voi ở khay hệ thống) | `docker --version` và `docker compose version` |
| **Git** | Bất kỳ phiên bản | `git --version` |
| **RAM trống** | Tối thiểu 4–6 GB (8 container: 3 MySQL + 1 Eureka + 4 Java Services) | Task Manager |
| **Các cổng phải còn trống** | `8761`, `8081`, `8082`, `8083`, `8084`, `3307`, `3308`, `3309` | `netstat -ano \| findstr ":8761 :8081 :8083"` |

> **Không cần cài** JDK 17, Maven hay MySQL. Toàn bộ quá trình biên dịch diễn ra **bên trong** Docker nhờ Dockerfile multi-stage.

### 1.2. Bốn bước khởi chạy

```powershell
# Bước 1: Clone kho lưu trữ
git clone https://github.com/viduchung/PTPM.git PitchOS
```

```powershell
# Bước 2: Di chuyển vào thư mục dự án
cd PitchOS
```

```powershell
# Bước 3: Tạo file cấu hình môi trường từ mẫu
Copy-Item .env.example .env
```

```powershell
# Bước 4: Khởi chạy toàn bộ hệ thống
docker compose up -d --build
```

Lần đầu chạy, Docker phải tải image nền và toàn bộ thư viện Maven nên mất khoảng **5–7 phút**. Các lần sau chỉ còn vài chục giây nhờ cache layer.

### 1.3. Kiểm tra hệ thống đã lên

```powershell
docker compose ps
```

Chờ đến khi cột `STATUS` của **toàn bộ 8 container** đều hiện `healthy` (khoảng 60–90 giây sau khi build xong). Trạng thái `Up` **chưa đủ**: `Up` chỉ nghĩa là tiến trình đang chạy, còn `healthy` mới chứng minh ứng dụng bên trong đã kết nối CSDL và sẵn sàng nhận request.

| Địa chỉ kiểm tra | Kỳ vọng | Mục đích |
|---|---|---|
| <http://localhost:8761> | Eureka Dashboard hiện đủ Service ID, `PITCHOS-PITCH-SERVICE` hiện `UP (2)` | Giám sát danh bạ Service Registry |
| <http://localhost:8081/actuator/health> | `{"status":"UP"}` | Sức khỏe Auth Service |
| <http://localhost:8082/actuator/health> | `{"status":"UP"}` | Sức khỏe Pitch Service Instance 1 |
| <http://localhost:8084/actuator/health> | `{"status":"UP"}` | Sức khỏe Pitch Service Instance 2 |
| <http://localhost:8083/actuator/health> | `{"status":"UP"}` | Sức khỏe Booking Service |
| <http://localhost:8083/api/v1/bookings/pitch-instance> | JSON chứa `instanceId: pitch-instance-1` hoặc `pitch-instance-2` | Kiểm tra cân bằng tải LoadBalancer |

> 💡 **Kiểm tra tự động nhanh:** Chạy file kịch bản [scripts/check-health.bat](scripts/check-health.bat) (hoặc `bash scripts/check-health.sh`) để kiểm tra trạng thái sức khỏe của cả 5 endpoints cùng một lúc.

### 1.4. Thử một lượt nghiệp vụ

1. Đăng nhập lấy Bearer JWT Token:
```powershell
curl -X POST http://localhost:8081/api/v1/auth/login -H "Content-Type: application/json" -d "{\"username\":\"user\",\"password\":\"123456\"}"
```

2. Dán token nhận được vào lệnh đặt sân:
```powershell
curl -X POST http://localhost:8083/api/v1/bookings -H "Authorization: Bearer <DAN_TOKEN_VAO_DAY>" -H "Content-Type: application/json" -d "{\"pitchId\":1,\"startTime\":\"2026-12-01T18:00:00\",\"endTime\":\"2026-12-01T20:00:00\"}"
```

*Kỳ vọng:* Phản hồi mã HTTP `201 Created` kèm thông tin đơn đặt sân với `totalPrice = 600000.00` và `status = cho_duyet`.

### 1.5. Tài khoản mẫu có sẵn

Hệ thống tự nạp 3 tài khoản đại diện 3 vai trò qua file `auth-init.sql`. **Mật khẩu dùng chung: `123456`**

| Tên đăng nhập | Vai trò | Quyền hạn |
|---|---|---|
| `admin` | `admin` | Quản trị toàn hệ thống, xem toàn bộ người dùng, duyệt sân |
| `chusan` | `chusan` | Chủ cụm sân: thêm sân mới, cập nhật giá, bảo trì sân |
| `user` | `user` | Khách hàng: đặt sân bóng, xem danh sách đơn của chính mình |

> 🔒 Mật khẩu này **chỉ dành cho môi trường học tập**. Mã nguồn đã được sửa để **không in mật khẩu ra log** (xem `DataInitializer.java`), tuân thủ chuẩn an toàn TH8.

### 1.6. Dừng hệ thống

```powershell
docker compose down
```

Lệnh trên dừng và xóa container nhưng **giữ nguyên 3 Named Volumes**, nên toàn bộ tài khoản và đơn đặt sân vẫn còn nguyên vẹn khi bật lại.

> ⚠️ **TUYỆT ĐỐI KHÔNG** dùng cờ `-v` (`docker compose down -v`). Cờ `-v` xóa sạch volumes, mất toàn bộ dữ liệu — và làm hỏng bước 8 của video demo (chứng minh dữ liệu bảo toàn qua restart).

---

## 🧭 2. KIẾN TRÚC TỔNG THỂ HỆ THỐNG PITCHOS (KT2)

```
                                  Client / Postman
                                         │
                   ┌─────────────────────┼─────────────────────────┐
                   │                     │                         │
                   ▼                     ▼                         ▼
            ┌──────────────┐      ┌──────────────┐  OpenFeign + LB  ┌────────────────────────┐
            │ auth-service │      │booking-servic│─────────────────►│ pitch-service-1 (:8082)│
            │ Cổng: 8081   │      │ Cổng: 8083   │   Service ID:    │ pitch-service-2 (:8084)│
            │              │      │ (CONSUMER)   │  pitchos-pitch-  │ (PROVIDER - 2 INSTANCE)│
            └──────┬───────┘      └──────┬───────┘     service      └───────────┬────────────┘
                   │                     │                                      │
                   │           Heartbeat / Đăng ký danh bạ                      │
                   └─────────────────────┼──────────────────────────────────────┘
                                         ▼
                        ┌──────────────────────────────────┐
                        │     pitchos-service-registry     │
                        │       (Eureka Server :8761)      │
                        └──────────────────────────────────┘

            ───────────────── Mạng nội bộ Docker: pitchos-network ─────────────────
                   │                     │                                      │
                   ▼                     ▼                                      ▼
         ┌──────────────────┐  ┌──────────────────┐           ┌──────────────────┐
         │ mysql-auth(:3307)│  │mysql-booking:3309│           │mysql-pitch (:3308│
         │ pitchos_user_db  │  │pitchos_booking_db│           │ pitchos_pitch_db │
         │ Vol: auth_data   │  │Vol: booking_data │           │ Vol: pitch_data  │
         └──────────────────┘  └──────────────────┘           └──────────────────┘
```

### Bảng cấu hình 8 container trong Docker Compose

| Container Name | Service ID Eureka | Port Máy Chủ | CSDL Sở Hữu | Volume Bền Vững | Vai Trò Kiến Trúc |
|---|---|:---:|---|---|---|
| **`pitchos-service-registry`** | – | `8761` | – | – | Service Registry (Eureka Server), khởi động đầu tiên |
| **`pitchos-auth-service`** | `pitchos-auth-service` | `8081` | `pitchos_user_db` | `mysql_auth_data` | Xác thực, cấp phát JWT, phân quyền RBAC 3 vai trò |
| **`pitchos-pitch-service-1`** | `pitchos-pitch-service` | `8082` | `pitchos_pitch_db` | `mysql_pitch_data` | **Provider** quản lý sân bóng (Instance 1) |
| **`pitchos-pitch-service-2`** | `pitchos-pitch-service` | `8084` | `pitchos_pitch_db` | `mysql_pitch_data` | **Provider** quản lý sân bóng (Instance 2, chung CSDL) |
| **`pitchos-booking-service`** | `pitchos-booking-service` | `8083` | `pitchos_booking_db` | `mysql_booking_data` | **Consumer**, gọi Pitch qua Service ID và chống trùng lịch |
| **`mysql-auth`** | – | `3307` | `pitchos_user_db` | `mysql_auth_data` | MySQL 8.0 độc lập cho Auth Service |
| **`mysql-pitch`** | – | `3308` | `pitchos_pitch_db` | `mysql_pitch_data` | MySQL 8.0 độc lập cho 2 Instance Pitch |
| **`mysql-booking`** | – | `3309` | `pitchos_booking_db` | `mysql_booking_data` | MySQL 8.0 độc lập cho Booking Service |

---

## 📊 3. TRẠNG THÁI HOÀN THÀNH TOÀN DIỆN DỰ ÁN (100% DONE)

| Hạng Mục Triển Khai | Người Phụ Trách | Trạng Thái Kỹ Thuật | Kết Quả Kiểm Thử |
|---|:---:|:---:|---|
| Module `pitchos-service-registry` (Eureka Server :8761) | **Hoàng** | ✅ **100% Hoàn thành** | Chạy độc lập, Eureka Dashboard quản lý danh bạ chuẩn |
| Auth Service: Eureka Client + Actuator + multi-stage Dockerfile | **Hoàng** | ✅ **100% Hoàn thành** | Build thành công, xóa bỏ hoàn toàn log in mật khẩu |
| Pitch Service: Eureka Client, Actuator, `/api/v1/instance-info`, Dockerfile | **Linh** | ✅ **100% Hoàn thành** | Biên dịch thành công, hỗ trợ 2 instance 8082 & 8084 |
| Booking Service: OpenFeign gọi **Service ID**, kiểm tra dữ liệu, 502/503 | **Nhật** | ✅ **100% Hoàn thành** | **17/17 Unit & Integration tests PASS 100%** |
| Bộ sưu tập Postman chuẩn hóa 3 phân hệ (`postman/collection.json`) | **Nhật** | ✅ **100% Hoàn thành** | Tích hợp sẵn Script lưu Token và kiểm tra tự động |
| Điều phối `docker-compose.yml` 8 container chuẩn TH8 | **Hùng** | ✅ **100% Hoàn thành** | Khởi chạy 8/8 container `healthy`, cấu hình volume bền vững |
| Bộ script tự động: `check-health` và `test-persistence` | **Hùng** | ✅ **100% Hoàn thành** | Có cả bản `.bat` (Windows) và `.sh` (Linux/Mac/WSL) |
| Bộ tài liệu lý thuyết Câu 1 (4 ý: 1.1, 1.2, 1.3, 1.4) | **Cả nhóm** | ✅ **100% Hoàn thành** | Đầy đủ 4 file trong `docs/kt2/CAU1_*.md` (2,0đ) |
| Bộ báo cáo chuyên đề thực nghiệm (Phần 1 $\rightarrow$ Phần 7) | **Cả nhóm** | ✅ **100% Hoàn thành** | Đầy đủ 8 file trong `docs/kt2/PHAN_*.md` (8,0đ) |

---

## 👥 4. PHÂN CHIA NHIỆM VỤ 4 THÀNH VIÊN (ĐIỂM CHIA ĐỀU 2,50Đ)

> 📖 Kế hoạch tổng thể và ma trận trách nhiệm: [KE_HOACH_KIEM_TRA_2.md](KE_HOACH_KIEM_TRA_2.md)

| Thành viên | Vùng mã nguồn sở hữu | Trách nhiệm báo cáo | Điểm | Checklist chi tiết |
|---|---|---|:---:|---|
| **Hoàng** *(Nhóm trưởng)* | `pitchos-service-registry/`, `pitchos-auth-service/`, `.gitignore` | Câu 1.2, Phần 2.1a, Phần 4; Biên bản `service-discovery-test.md` | **2,50** | [NHIEM_VU_HOANG.md](NHIEM_VU_HOANG.md) |
| **Linh** | `pitchos-pitch-service/`, `Dockerfile`, `.env.example` | Câu 1.3, Phần 1, Phần 5 | **2,50** | [NHIEM_VU_LINH.md](NHIEM_VU_LINH.md) |
| **Nhật** | `pitchos-booking-service/`, `postman/collection.json` | Câu 1.1, Phần 3; Hợp đồng API & Biên bản `integration-test.md` | **2,50** | [NHIEM_VU_NHAT.md](NHIEM_VU_NHAT.md) |
| **Hùng** | `docker-compose.yml`, `pitchos-database/`, `scripts/` | Câu 1.4, Phần 2.1b, Phần 6, Phần 7; Biên bản `operation-test.md` & `failure-analysis.md` | **2,50** | [NHIEM_VU_HUNG.md](NHIEM_VU_HUNG.md) |

---

## 🧪 5. CÁC BỘ KIỂM THỬ CHÍNH THỨC CỦA ĐỀ TÀI

| Bộ Test | Nội dung kiểm chứng | Người phụ trách | File tài liệu chi tiết |
|---|---|:---:|---|
| **IT01–IT07** | Tích hợp và xử lý lỗi phân tán giữa Consumer và Provider (404, 502, 503, timeout) | **Nhật** | [docs/testing/integration-test.md](docs/testing/integration-test.md) |
| **TC01–TC06** | Service Discovery và Cân bằng tải Round-Robin (20 requests tới 2 instances) | **Hoàng** | [docs/testing/service-discovery-test.md](docs/testing/service-discovery-test.md) |
| **DEP01–DEP08** | Vận hành Docker, Healthcheck, Logging, Chịu lỗi và Bảo toàn dữ liệu Volume | **Hùng** | [docs/testing/operation-test.md](docs/testing/operation-test.md) |

*Bộ sưu tập Postman toàn diện:* Tất cả các kịch bản kiểm thử trên đều được đóng gói sẵn trong file duy nhất: **[postman/collection.json](postman/collection.json)**.

---

## 🎬 6. CHECKLIST QUAY VIDEO DEMO CÁ NHÂN (40% ĐIỂM CỦA TỪNG NGƯỜI)

Mỗi thành viên tự quay video màn hình 10–15 phút trên máy tính cá nhân, thực hiện đủ 8 bước theo barem:

1. **Bước 1 — Giới thiệu kiến trúc:** Mở sơ đồ hệ thống, chỉ rõ Consumer (Booking :8083), Provider (Pitch 2 instances :8082, :8084) và Service Registry (Eureka :8761).
2. **Bước 2 — Khởi động Docker:** Chạy `docker compose up -d` rồi `docker compose ps`, chứng minh toàn bộ 8 container đều đạt trạng thái `healthy`.
3. **Bước 3 — Kiểm tra Eureka Dashboard:** Mở trình duyệt <http://localhost:8761>, chứng minh các dịch vụ đã đăng ký, `PITCHOS-PITCH-SERVICE` hiển thị `UP (2)`.
4. **Bước 4 — Gọi nghiệp vụ thành công:** Đăng nhập lấy Bearer JWT Token, gọi `POST /api/v1/bookings` đặt sân thành công (Status `201 Created`).
5. **Bước 5 — Minh họa lỗi tích hợp (TH6):** Đặt sân với ID không tồn tại `9999` (nhận mã `404`); dừng cả 2 instance Pitch rồi đặt sân (nhận mã `503 Service Unavailable`).
6. **Bước 6 — Actuator Health & Log:** Gọi `http://localhost:8083/actuator/health` thấy `{"status":"UP"}`, mở `docker compose logs` xem luồng log trao đổi có tiền tố `[instanceId]`.
7. **Bước 7 — Khả năng chịu lỗi (TH7):** Dừng `pitchos-pitch-service-1` (`docker compose stop`), đặt sân vẫn thành công (`201 Created`) nhờ instance 2 gánh tải.
8. **Bước 8 — Bảo toàn dữ liệu (TH8):** Chạy `docker compose down` (không dùng cờ `-v`), bật lại bằng `docker compose up -d`, chạy script `scripts/test-persistence.bat` chứng minh đơn đặt sân vẫn còn nguyên vẹn 100%.

---

## 🗂️ 7. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
PitchOS/
├── README.md                      # Hướng dẫn khởi chạy máy sạch, sơ đồ và điều phối KT2
├── KE_HOACH_KIEM_TRA_2.md         # Kế hoạch nhóm, barem điểm, checklist 7 ngày
├── docker-compose.yml             # Điều phối 8 container hoàn chỉnh (chuẩn TH8)
├── .env.example                   # Mẫu biến môi trường (file DUY NHẤT được commit)
├── .gitignore                     # Chặn .env, target/, *.log
├── postman/
│   └── collection.json            # Bộ sưu tập Postman chuẩn hóa 3 phân hệ của cả nhóm
│
├── NHIEM_VU_HOANG.md              # Bảng phân công chi tiết 4 thành viên
├── NHIEM_VU_LINH.md
├── NHIEM_VU_NHAT.md
├── NHIEM_VU_HUNG.md
│
├── pitchos-service-registry/      # Eureka Server :8761          (Hoàng)
│   ├── Dockerfile                 #   multi-stage, USER appuser
│   └── src/...
├── pitchos-auth-service/          # Auth & User :8081            (Hoàng)
│   ├── Dockerfile                 #   multi-stage, USER appuser
│   └── src/...                    #   JWT, RBAC 3 vai trò, Eureka Client, Actuator
├── pitchos-pitch-service/         # Pitch Provider :8082 & :8084 (Linh)
│   ├── Dockerfile                 #   multi-stage, USER appuser
│   └── src/...                    #   /instance-info, log [instanceId]
├── pitchos-booking-service/       # Booking Consumer :8083       (Nhật)
│   ├── Dockerfile                 #   multi-stage, USER appuser
│   └── src/...                    #   OpenFeign Service ID, 17 automated tests
│
├── pitchos-database/              # Script SQL khởi tạo CSDL     (Hùng)
│   ├── auth-init.sql
│   ├── pitch-init.sql
│   └── booking-init.sql
├── scripts/                       # Kịch bản kiểm tra tự động    (Hùng)
│   ├── check-health.bat / .sh     #   kiểm tra actuator health 5 endpoints
│   └── test-persistence.bat / .sh #   kiểm tra bảo toàn dữ liệu qua volume
│
└── docs/
    ├── api/
    │   └── api-contract.md        # Hợp đồng API chuẩn hóa toàn hệ thống
    ├── architecture/              # Sơ đồ kiến trúc PNG và ảnh minh chứng
    ├── testing/                   # Biên bản kiểm thử IT, TC, DEP
    │   ├── integration-test.md    #   Bộ IT01–IT07 (Nhật)
    │   ├── service-discovery-test.md # Bộ TC01–TC06 (Hoàng)
    │   └── operation-test.md      #   Bộ DEP01–DEP08 (Hùng)
    ├── operation/
    │   └── failure-analysis.md    # Báo cáo phân tích chuyên sâu sự cố vận hành (Hùng)
    ├── kt2/                       # Báo cáo chuyên đề 7 phần nộp hội đồng
    │   ├── CAU1_1_NHAT.md         #   Lý thuyết Provider vs Consumer (0.5đ)
    │   ├── CAU1_2_HOANG.md        #   Lý thuyết Service Registry & Discovery (0.5đ)
    │   ├── CAU1_3_LINH.md         #   Lý thuyết Docker Image vs Container (0.5đ)
    │   ├── CAU1_4_HUNG.md         #   Lý thuyết 3 cấp độ trạng thái & Volume (0.5đ)
    │   ├── PHAN_1_LINH.md         #   Phần 1: Giới thiệu hệ thống PitchOS
    │   ├── PHAN_2_HOANG.md        #   Phần 2.1a: Sơ đồ kiến trúc tích hợp & triển khai
    │   ├── PHAN_2_HUNG.md         #   Phần 2.1b: Thiết kế CSDL phân tán & Logical ID
    │   ├── PHAN_3_NHAT.md         #   Phần 3: Tích hợp & Tiêu thụ dịch vụ OpenFeign (2.0đ)
    │   ├── PHAN_4_HOANG.md        #   Phần 4: Service Registry & Cân bằng tải (1.5đ)
    │   ├── PHAN_5_LINH.md         #   Phần 5: Container hóa & Docker Compose (2.0đ)
    │   ├── PHAN_6_HUNG.md         #   Phần 6: Vận hành, Giám sát & Phân tích sự cố (1.5đ)
    │   └── PHAN_7_HUNG.md         #   Phần 7: Tự chấm điểm 10/10 & Hướng mở rộng
    └── tx1/                       # Lưu trữ tài liệu Bài kiểm tra số 1
```

---

## 🔒 8. NGUYÊN TẮC BẢO MẬT & BẪY KỸ THUẬT (CHUẨN TH8)

1. **Tuyệt đối không commit file `.env` thật:** File `.env` chứa mật khẩu CSDL đã được đưa vào `.gitignore`. Khi nộp bài hoặc chia sẻ mã nguồn chỉ nộp file `.env.example`.
2. **Không in mật khẩu hoặc JWT ra log:** `DataInitializer.java` đã được sửa đổi triệt để để không bao giờ ghi mật khẩu người dùng ra log console.
3. **Container chạy bằng Non-root User:** Toàn bộ các file Dockerfile đều tạo nhóm `appgroup`, người dùng `appuser` và chuyển ngữ cảnh bằng chỉ thị `USER appuser` theo nguyên tắc đặc quyền tối thiểu (Least Privilege).
4. **Bẫy `localhost` trong container:** Trong Docker, `localhost` trỏ về chính container đó. Gọi giữa các container bắt buộc phải dùng Service Name: `EUREKA_URL=http://pitchos-service-registry:8761/eureka/`, `MYSQL_HOST=mysql-pitch`.
5. **Bẫy hardcode URL trong Feign:** Phải dùng `@FeignClient(name = "pitchos-pitch-service")`, tuyệt đối không có thuộc tính `url = "..."`.
6. **Bẫy Race Condition nạp dữ liệu:** `pitchos-pitch-service-2` phải có `depends_on: pitchos-pitch-service-1: condition: service_healthy` để tránh 2 instance cùng chạy `DataInitializer` chèn trùng dữ liệu vào CSDL.
7. **Bẫy cờ `docker compose down -v`:** Cờ `-v` sẽ xóa sạch các Docker Named Volumes. Tuyệt đối không dùng cờ `-v` khi demo bảo toàn dữ liệu.
