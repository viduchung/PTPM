# ⚽ PitchOS — Hệ Thống Đặt Sân Bóng Trực Tuyến
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### BÀI KIỂM TRA SỐ 2 (TX2) — CHUẨN ĐẦU RA CĐR L2 (TỔNG: 10,0 ĐIỂM)

> 📌 **Định hướng đánh giá KT2:** Khác với Bài kiểm tra số 1 (tập trung vào REST API đơn lẻ và bảo mật), Bài kiểm tra số 2 đánh giá năng lực **tích hợp, container hóa và vận hành** hệ thống Microservices:
> 1. **Tích hợp & Tiêu thụ dịch vụ (TH6):** Consumer (Booking) gọi Provider (Pitch) qua OpenFeign, kiểm tra tính toàn vẹn dữ liệu và xử lý lỗi phân tán.
> 2. **Service Registry & Cân bằng tải (TH7):** Eureka Server quản lý danh bạ, gọi dịch vụ qua **Service ID** (bỏ URL cứng), chạy **2 instance Pitch Service**.
> 3. **Triển khai & Vận hành Docker (TH8):** Dockerfile multi-stage, điều phối bằng `docker-compose.yml`, Spring Boot Actuator, giám sát log, bảo toàn dữ liệu bằng Named Volume.
>
> ⚖️ **Cơ cấu chấm điểm:** **60% Điểm nhóm** (Báo cáo chuyên đề 7 phần + Mã nguồn) và **40% Điểm cá nhân** (Video demo độc lập 8 bước của từng thành viên).

---

## 🚀 1. KHỞI CHẠY TRÊN MÁY HOÀN TOÀN SẠCH

Phần này dành cho người **chưa từng mở dự án này**. Làm đúng bốn bước dưới đây là hệ thống chạy, không cần cài Java, Maven hay MySQL.

### 1.1. Yêu cầu máy tính

| Hạng mục | Yêu cầu | Cách kiểm tra |
|---|---|---|
| **Docker Desktop** | Đã cài và **đang chạy** (biểu tượng cá voi ở khay hệ thống) | `docker --version` và `docker compose version` |
| **Git** | Bất kỳ phiên bản | `git --version` |
| **RAM trống** | Tối thiểu 4 GB (6 container Java + MySQL) | — |
| **Các cổng phải còn trống** | `8761`, `8081`, `8082`, `8083`, `8084`, `3306` | `netstat -ano \| findstr ":8761 :8081 :8083"` |

> **Không cần cài** JDK 17, Maven hay MySQL. Toàn bộ quá trình biên dịch diễn ra **bên trong** Docker nhờ Dockerfile multi-stage.

### 1.2. Bốn bước khởi chạy

```powershell
git clone <DIA_CHI_REPO> PitchOS
```

```powershell
cd PitchOS
```

```powershell
Copy-Item .env.example .env
```

```powershell
docker compose up -d --build
```

Lần đầu chạy, Docker phải tải image nền và toàn bộ thư viện Maven nên mất khoảng **5–10 phút**. Các lần sau chỉ còn vài chục giây nhờ cache.

### 1.3. Kiểm tra hệ thống đã lên

```powershell
docker compose ps
```

Chờ đến khi cột `STATUS` của mọi dòng hiện `healthy` (khoảng 60–90 giây sau khi build xong). Trạng thái `Up` **chưa đủ**: `Up` chỉ nghĩa là tiến trình đang chạy, còn `healthy` mới nghĩa là ứng dụng bên trong đã sẵn sàng nhận request.

| Địa chỉ kiểm tra | Kỳ vọng |
|---|---|
| <http://localhost:8761> | Eureka Dashboard, mục *Instances currently registered* hiện đủ các Service ID, `PITCHOS-PITCH-SERVICE` hiện `UP (2)` |
| <http://localhost:8081/actuator/health> | `{"status":"UP"}` |
| <http://localhost:8081/swagger-ui.html> | Trang Swagger của Auth Service |
| <http://localhost:8083/actuator/health> | `{"status":"UP"}` |

### 1.4. Thử một lượt nghiệp vụ

```powershell
curl -X POST http://localhost:8081/api/v1/auth/login -H "Content-Type: application/json" -d "{\"username\":\"user\",\"password\":\"123456\"}"
```

Lấy giá trị `token` trong phản hồi, rồi gọi đặt sân:

```powershell
curl -X POST http://localhost:8083/api/v1/bookings -H "Authorization: Bearer <DAN_TOKEN_VAO_DAY>" -H "Content-Type: application/json" -d "{\"pitchId\":1,\"bookingDate\":\"2026-12-01\",\"startTime\":\"18:00\",\"endTime\":\"20:00\"}"
```

Kỳ vọng: `201 Created` kèm thông tin đơn đặt sân.

### 1.5. Tài khoản mẫu

Hệ thống tự tạo ba tài khoản đại diện ba vai trò khi cơ sở dữ liệu còn trống. **Mật khẩu dùng chung: `123456`**

| Tên đăng nhập | Vai trò | Quyền hạn |
|---|---|---|
| `admin` | `admin` | Xem được danh sách toàn bộ người dùng, mọi tài khoản |
| `chusan` | `chusan` | Quản lý sân bóng của mình, xem được mọi tài khoản |
| `user` | `user` | Đặt sân, chỉ xem được thông tin của chính mình |

> 🔒 Mật khẩu này **chỉ dành cho môi trường học tập**. Mã nguồn đã được sửa để **không in mật khẩu ra log** (xem `DataInitializer.java`), nên đây là nơi duy nhất ghi lại giá trị đó.

### 1.6. Dừng hệ thống

```powershell
docker compose down
```

Lệnh trên dừng và xóa container nhưng **giữ nguyên Named Volume**, nên dữ liệu đơn đặt sân vẫn còn khi bật lại.

> ⚠️ **TUYỆT ĐỐI KHÔNG** dùng `docker compose down -v`. Cờ `-v` xóa sạch volume, mất toàn bộ dữ liệu — và làm hỏng bước 8 của video demo (chứng minh dữ liệu bảo toàn qua restart).

---

## 🩺 2. XỬ LÝ SỰ CỐ THƯỜNG GẶP

| Hiện tượng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `error during connect ... dockerDesktopLinuxEngine` | Docker Desktop chưa chạy | Mở Docker Desktop, chờ biểu tượng cá voi chuyển sang trạng thái running |
| `Bind for 0.0.0.0:8081 failed: port is already allocated` | Cổng đang bị tiến trình khác chiếm | `netstat -ano \| findstr :8081` để tìm PID, rồi `taskkill /PID <pid> /F`; hoặc đổi cổng trong `.env` |
| Container Java khởi động rồi thoát ngay | Không kết nối được MySQL | `docker compose logs pitchos-auth-service`; kiểm tra `MYSQL_PASSWORD` trong `.env` không để trống |
| `Access denied for user 'root'` | Mật khẩu trong `.env` khác mật khẩu volume MySQL đã khởi tạo trước đó | Mật khẩu MySQL chỉ được đặt lần đầu tạo volume. Chạy `docker compose down -v` (chấp nhận mất dữ liệu) rồi `up -d` lại |
| Dashboard Eureka trống dù container `healthy` | Các service trỏ `EUREKA_URL` về `localhost` | Trong container, `localhost` là chính container đó. Phải dùng `http://pitchos-service-registry:8761/eureka/` |
| Pitch Service chỉ hiện 1 instance dù chạy 2 container | Hai instance trùng Instance ID nên bản ghi sau ghi đè bản trước | Đặt `eureka.instance.instance-id=${spring.application.name}:${server.port}` |
| Dashboard hiện dịch vụ nhưng gọi vào thì `Connection refused` | Đăng ký bằng hostname container (chuỗi hash) mà container khác không phân giải được | Đặt `eureka.instance.prefer-ip-address=true` |
| Dừng một instance mà Dashboard vẫn hiện `UP` rất lâu | Eureka bật chế độ Self-Preservation | Đã tắt sẵn trong `pitchos-service-registry`: `eureka.server.enable-self-preservation=false` |
| Đặt sân lỗi `503` ngay sau khi khởi động xong | Consumer chưa làm mới bản sao danh bạ (chu kỳ 30 giây) | Chờ khoảng 30–60 giây rồi gọi lại. Đây là độ trễ bình thường của Eureka, không phải lỗi |

Xem log để chẩn đoán:

```powershell
docker compose logs -f pitchos-auth-service
```

---

## 🧭 3. KIẾN TRÚC TỔNG THỂ HỆ THỐNG

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
                                         │
                        ┌────────────────▼─────────────────┐
                        │     pitchos-mysql (:3306)        │
                        │  3 schema: user / pitch / booking│
                        │  Named Volume: mysql_data        │
                        └──────────────────────────────────┘
```

**Điểm kiến trúc cần nhớ:** Eureka Server **không nằm trên đường đi của request nghiệp vụ**. Booking Service chỉ hỏi Eureka "Pitch Service đang ở đâu?", rồi gọi **trực tiếp** tới Pitch Service. Việc tiếp nhận, định tuyến và bảo vệ request từ bên ngoài là nhiệm vụ của API Gateway — một thành phần khác, chưa triển khai trong phạm vi KT2.

### Bảng cấu hình các service

| Container / Module | Eureka Service ID | Port Host | Cơ sở dữ liệu | Số Instance | Vai trò kiến trúc |
|---|---|:---:|---|:---:|---|
| **`pitchos-service-registry`** | – | `8761` | – | 1 | Service Registry (Eureka Server), khởi động đầu tiên |
| **`pitchos-auth-service`** | `pitchos-auth-service` | `8081` | `pitchos_user_db` | 1 | Xác thực, cấp phát JWT, RBAC 3 vai trò |
| **`pitchos-pitch-service-1`** | `pitchos-pitch-service` | `8082` | `pitchos_pitch_db` | **2** | **Provider** quản lý sân bóng (instance 1) |
| **`pitchos-pitch-service-2`** | `pitchos-pitch-service` | `8084` | `pitchos_pitch_db` | ^ | **Provider** quản lý sân bóng (instance 2, chung DB) |
| **`pitchos-booking-service`** | `pitchos-booking-service` | `8083` | `pitchos_booking_db` | 1 | **Consumer**, gọi Pitch qua Service ID |
| **`pitchos-mysql`** | – | `3306` | 3 schema riêng biệt | 1 | Lưu trữ bền vững qua Named Volume `mysql_data` |

---

## 📊 4. TRẠNG THÁI HOÀN THÀNH KT2

| Hạng mục | Người phụ trách | Trạng thái |
|---|---|---|
| Module `pitchos-service-registry` (Eureka Server :8761) | Hoàng | ✅ Xong, đã build và chạy được |
| Auth Service: Eureka Client + Actuator | Hoàng | ✅ Xong, build thành công |
| Auth Service: gỡ log in mật khẩu ra console | Hoàng | ✅ Xong |
| `Dockerfile` multi-stage cho Registry và Auth (`USER appuser`) | Hoàng | ✅ Xong |
| Gỡ `.env` khỏi Git, cấu hình `.gitignore` | Hoàng | ✅ Xong |
| Khai báo Registry + Auth trong `docker-compose.yml` | Hoàng | ✅ Xong |
| Pitch Service: Eureka Client, Actuator, `/api/v1/instance-info`, Dockerfile | Linh | ⏳ Đang làm |
| `docker-compose.yml` hoàn chỉnh (2 instance Pitch, Booking) | Linh | ⏳ Đang làm |
| Booking Service: **chuyển Feign sang Service ID** (bỏ `url`) | Nhật | ⏳ Đang làm |
| 3 file SQL khởi tạo + scripts kiểm thử vận hành | Hùng | ⏳ Đang làm |
| Chạy TC01–TC06 và bảng 20 request cân bằng tải | Hoàng | ⏳ Chờ đủ dịch vụ |

> Cho đến khi Linh và Nhật hoàn thành, lệnh `docker compose up -d` chỉ dựng được **MySQL + Service Registry + Auth Service**. Đó là lý do bảng ở Mục 3 mô tả kiến trúc đích, còn bảng này mô tả trạng thái thực tế.

---

## 👥 5. PHÂN CHIA NHIỆM VỤ 4 THÀNH VIÊN

> 📖 Kế hoạch tổng thể và ma trận trách nhiệm chi tiết: [KE_HOACH_KIEM_TRA_2.md](KE_HOACH_KIEM_TRA_2.md)

| Thành viên | Vùng mã nguồn sở hữu | Trách nhiệm báo cáo | Điểm | Checklist |
|---|---|---|:---:|---|
| **Hoàng** *(Nhóm trưởng)* | `pitchos-service-registry/`, `pitchos-auth-service/`, `README.md`, `.gitignore` | Câu 1.2, Phần 2.1a, Phần 4; tổng hợp `docs/report.pdf` | 2,50 | [NHIEM_VU_HOANG.md](NHIEM_VU_HOANG.md) |
| **Linh** | `pitchos-pitch-service/`, `docker-compose.yml`, `.env.example` | Câu 1.3, Phần 1, Phần 5 | 2,50 | [NHIEM_VU_LINH.md](NHIEM_VU_LINH.md) |
| **Nhật** | `pitchos-booking-service/`, `postman/` | Câu 1.1, Phần 3 | 2,50 | [NHIEM_VU_NHAT.md](NHIEM_VU_NHAT.md) |
| **Hùng** | `pitchos-database/`, `scripts/` | Câu 1.4, Phần 2.1b, Phần 6, Phần 7 | 2,50 | [NHIEM_VU_HUNG.md](NHIEM_VU_HUNG.md) |

---

## 🛠️ 6. CHẠY THỦ CÔNG KHI LẬP TRÌNH (KHÔNG DÙNG DOCKER)

Cách này dành cho lúc viết mã và gỡ lỗi, **không** dùng khi demo.

Yêu cầu: JDK 17, Maven 3.9+, MySQL 8 chạy ở `localhost:3306` với ba schema `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`.

Khởi động **theo đúng thứ tự** — Registry phải lên trước, vì các service khác cần địa chỉ này để đăng ký:

```powershell
cd pitchos-service-registry; mvn spring-boot:run
```

```powershell
cd pitchos-auth-service; mvn spring-boot:run
```

```powershell
cd pitchos-pitch-service; mvn spring-boot:run
```

```powershell
cd pitchos-booking-service; mvn spring-boot:run
```

Chạy instance thứ hai của Pitch Service trên cổng 8084:

```powershell
cd pitchos-pitch-service; mvn spring-boot:run "-Dspring-boot.run.arguments=--server.port=8084"
```

Khi chạy ngoài Docker, các service dùng giá trị mặc định `http://localhost:8761/eureka/` nên không cần khai báo thêm biến môi trường.

---

## 🧪 7. CÁC BỘ KIỂM THỬ

| Bộ | Nội dung | Người phụ trách | Biên bản |
|---|---|---|---|
| **IT01–IT07** | Tích hợp và xử lý lỗi phân tán giữa Consumer và Provider | Nhật | `docs/testing/integration-test.md` |
| **TC01–TC06** | Service Discovery và cân bằng tải | Hoàng | [docs/testing/service-discovery-test.md](docs/testing/service-discovery-test.md) |
| **DEP01–DEP08** | Vận hành, giám sát, bảo toàn dữ liệu | Hùng | `docs/testing/operation-test.md` |

Bộ kiểm thử TC01–TC06 của Hoàng:

| Mã | Tình huống | Kết quả mong đợi |
|---|---|---|
| **TC01** | Đăng ký dịch vụ | Dashboard hiện đủ Service ID, Pitch có 2 instance |
| **TC02** | Gọi qua Service ID | Đặt sân thành công mà cấu hình không chứa URL tĩnh |
| **TC03** | Cân bằng tải 20 request | Cả 2 instance đều nhận được request |
| **TC04** | Dừng 1 instance Provider | Đặt sân vẫn trả `201 Created` nhờ instance còn lại |
| **TC05** | Dừng toàn bộ Provider | Trả `503` gọn gàng, Consumer không sập |
| **TC06** | Khởi động lại Provider | Tự đăng ký lại, không cần restart Consumer |

Bộ sưu tập Postman của từng dịch vụ nằm trong `postman/` của chính dịch vụ đó, ví dụ `pitchos-auth-service/postman/`.

---

## 🎬 8. CHECKLIST VIDEO DEMO CÁ NHÂN (40% ĐIỂM)

Mỗi thành viên tự quay video màn hình 10–15 phút, đủ tám bước theo đề bài:

1. **Giới thiệu kiến trúc:** mở sơ đồ, chỉ rõ Consumer (Booking), Provider (Pitch 2 instance) và Service Registry (Eureka).
2. **Khởi động hệ thống:** `docker compose up -d` rồi `docker compose ps`, cho thấy mọi container đạt `healthy`.
3. **Kiểm tra Eureka:** mở <http://localhost:8761>, chỉ rõ `PITCHOS-PITCH-SERVICE` hiện `UP (2)` với hai Instance ID khác nhau.
4. **Gọi nghiệp vụ:** đăng nhập lấy JWT, gọi `POST /api/v1/bookings`, nhận `201 Created`.
5. **Minh họa lỗi tích hợp:** gọi sân `9999` nhận `404`; dừng cả 2 instance Pitch rồi đặt sân nhận `503`.
6. **Actuator và log:** mở `/actuator/health` thấy `{"status":"UP"}`, mở `docker compose logs` xem luồng trao đổi giữa hai dịch vụ.
7. **Khả năng chịu lỗi:** dừng Pitch instance 1, đặt sân vẫn nhận `201 Created` nhờ instance 2.
8. **Bảo toàn dữ liệu:** `docker compose down` (không có `-v`) rồi `up -d`, chứng minh đơn đặt sân vẫn còn nguyên.

---

## 🗂️ 9. CẤU TRÚC THƯ MỤC

```text
PitchOS/
├── README.md                      # File này: hướng dẫn khởi chạy và điều phối KT2
├── KE_HOACH_KIEM_TRA_2.md         # Kế hoạch nhóm, barem điểm, checklist 7 ngày
├── docker-compose.yml             # Điều phối toàn bộ container
├── .env.example                   # Mẫu biến môi trường (file DUY NHẤT được commit)
├── .env                           # Cấu hình thật, CHỨA BÍ MẬT - đã gitignore
├── .gitignore                     # Chặn .env, target/, *.log
│
├── NHIEM_VU_HOANG.md              # Checklist cá nhân từng thành viên
├── NHIEM_VU_LINH.md
├── NHIEM_VU_NHAT.md
├── NHIEM_VU_HUNG.md
│
├── pitchos-service-registry/      # Eureka Server :8761          (Hoàng)
│   ├── Dockerfile                 #   multi-stage, USER appuser
│   ├── pom.xml
│   └── src/main/
│       ├── java/com/pitchos/registry/PitchosServiceRegistryApplication.java
│       └── resources/application.properties
│
├── pitchos-auth-service/          # Auth & User :8081            (Hoàng)
│   ├── Dockerfile                 #   multi-stage, USER appuser
│   └── src/...                    #   JWT, RBAC 3 vai trò, Eureka Client, Actuator
├── pitchos-pitch-service/         # Pitch Provider :8082 & :8084 (Linh)
├── pitchos-booking-service/       # Booking Consumer :8083       (Nhật)
│
├── pitchos-database/              # Script SQL khởi tạo CSDL     (Hùng)
│   ├── auth-init.sql
│   ├── pitch-init.sql
│   └── booking-init.sql
├── scripts/                       # Kịch bản kiểm tra tự động    (Hùng)
│
└── docs/
    ├── report.pdf                 # Báo cáo 7 phần chính thức (Hoàng tổng hợp)
    ├── kt2/                       # Bài viết từng phần của 4 thành viên
    │   ├── CAU1_2_HOANG.md        #   Lý thuyết Service Registry & Discovery
    │   ├── PHAN_2_HOANG.md        #   Sơ đồ kiến trúc tích hợp và triển khai
    │   ├── PHAN_4_HOANG.md        #   Service Registry và cân bằng tải
    │   ├── CAU1_4_HUNG.md
    │   └── PHAN_2_HUNG.md
    ├── architecture/              # Ảnh sơ đồ PNG và ảnh minh chứng
    ├── testing/                   # Biên bản kiểm thử IT, TC, DEP
    ├── operation/                 # Phân tích sự cố vận hành
    └── tx1/                       # Lưu trữ tài liệu đợt kiểm tra TX1
```

---

## 🔒 10. QUY TẮC BẢO MẬT CỦA DỰ ÁN

1. **File `.env` thật không bao giờ được commit.** Nó đã được gỡ khỏi Git và thêm vào `.gitignore`. Kho lưu trữ chỉ commit `.env.example`. Khi nộp bài cũng **chỉ nộp `.env.example`**.
2. **Không in mật khẩu hay JWT ra log.** `DataInitializer.java` đã được sửa để chỉ ghi lại sự kiện, không ghi giá trị bí mật. Log container được thu thập và chia sẻ, nên mọi thông tin xác thực phải bị loại khỏi log.
3. **Không ghi bí mật vào Dockerfile.** Mật khẩu CSDL và `JWT_SECRET` được truyền vào lúc chạy bằng biến môi trường của Docker Compose.
4. **Container chạy bằng người dùng thường.** Cả hai Dockerfile đều tạo `appuser` và khai báo `USER appuser` thay vì chạy quyền `root`.
5. **Actuator chỉ mở `health` và `info`.** Không mở toàn bộ endpoint vì `/actuator/env` sẽ phơi bày chuỗi kết nối CSDL và `JWT_SECRET`.

> ⚠️ **Việc còn tồn đọng:** các file `application.properties` hiện vẫn đặt giá trị `JWT_SECRET` thật làm giá trị mặc định trong biểu thức `${JWT_SECRET:404E63...}`. Cần thay bằng `${JWT_SECRET}` không có giá trị mặc định trước khi nộp, để ứng dụng báo lỗi rõ ràng khi thiếu biến môi trường thay vì âm thầm dùng khóa đã bị lộ.

---

## ⚠️ 11. CÁC BẪY KỸ THUẬT CẦN TRÁNH

1. ❌ **Bẫy `localhost` trong container:** trong Docker, `localhost` trỏ về chính container đó. Gọi giữa các container phải dùng tên service: `EUREKA_URL=http://pitchos-service-registry:8761/eureka/`, `MYSQL_HOST=pitchos-mysql`.
2. ❌ **Bẫy `docker compose down -v`:** cờ `-v` xóa sạch volume dữ liệu. Không bao giờ dùng khi demo bảo toàn dữ liệu.
3. ❌ **Bẫy hardcode URL trong Feign:** phải là `@FeignClient(name = "pitchos-pitch-service")`, tuyệt đối không có thuộc tính `url = "..."`. Có Eureka Server mà Consumer vẫn gọi URL cố định thì **chưa đạt** yêu cầu Service Discovery.
4. ❌ **Bẫy nhầm Eureka với API Gateway:** Eureka chỉ lưu danh bạ ở tầng nội bộ, không định tuyến request nghiệp vụ. Nhầm hai khái niệm này sẽ bị trừ điểm ở câu lý thuyết 1.2.
5. ❌ **Bẫy lộ mật khẩu trong log:** không in mật khẩu hay JWT đầy đủ ra console.
6. ❌ **Bẫy trùng Instance ID:** hai instance Pitch Service trùng Instance ID sẽ bị Eureka coi là một, mất hoàn toàn khả năng cân bằng tải.
7. ❌ **Bẫy độ trễ Eureka:** danh bạ cập nhật có độ trễ tự nhiên (hàng chục giây đến vài phút tùy cấu hình). Đây là cơ chế chuẩn của mô hình AP, cần giải thích rõ trong báo cáo, không che giấu như lỗi.
8. ❌ **Bẫy ghép sai phiên bản:** Spring Boot 3.2.x chỉ tương thích Spring Cloud dòng 2023.0.x. Ghép tùy ý sẽ gây lỗi khởi động khó chẩn đoán.
