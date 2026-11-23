# BẢNG HỢP ĐỒNG API (API CONTRACT) — HỆ THỐNG PITCHOS
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)  
**Người biên soạn:** NHẬT (phụ trách `pitchos-booking-service` và tích hợp liên dịch vụ)  
**Phiên bản:** Bài kiểm tra số 2 (TX2) — sau khi có Eureka và Docker

---

## 0. QUY ƯỚC CHUNG

| Hạng mục | Quy ước |
|---|---|
| Kiểu dữ liệu trao đổi | `application/json; charset=UTF-8` |
| Xác thực | `Authorization: Bearer <JWT>` ký HS256, claim gồm `sub`, `userId`, `role`, `fullName`, `iat`, `exp` |
| Vai trò (role) | `user` (khách hàng), `chusan` (chủ sân), `admin` (quản trị) |
| Định dạng thời gian | `yyyy-MM-ddTHH:mm:ss` (giờ Việt Nam, `Asia/Ho_Chi_Minh`) |
| Định dạng lỗi thống nhất | `{ "timestamp", "status", "error", "message" }` |
| Liên kết dữ liệu giữa các DB | Logical ID (`userId`, `pitchId` kiểu `BIGINT`), không có khóa ngoại vật lý xuyên CSDL |

**Cổng dịch vụ (ánh xạ ra máy chủ):** Eureka `8761` · Auth `8081` · Pitch `8082` và `8084` (2 instance) · Booking `8083`.

---

## 1. AUTH SERVICE (PROVIDER — `pitchos-auth-service`, cổng 8081)

| # | Method | Đường dẫn | Quyền | Body request | Phản hồi thành công | Mã lỗi |
|:-:|---|---|---|---|---|---|
| 1 | `POST` | `/api/v1/auth/register` | Công khai | `{username, email, password, fullName, phone}` | `201 Created` + `UserResponse` | `400` dữ liệu sai hoặc trùng tài khoản |
| 2 | `POST` | `/api/v1/auth/login` | Công khai | `{username, password}` | `200 OK` + `{accessToken, tokenType, expiresIn, userId, username, fullName, role}` | `400` thiếu trường · `401` sai tài khoản/mật khẩu |
| 3 | `GET` | `/actuator/health` | Công khai | — | `200 OK` + `{"status":"UP"}` | — |

**Tài khoản nạp sẵn phục vụ kiểm thử:** `user`, `chusan`, `admin` — mật khẩu `123456`.

---

## 2. PITCH SERVICE (PROVIDER — `pitchos-pitch-service`, cổng 8082 và 8084)

| # | Method | Đường dẫn | Quyền | Body request | Phản hồi thành công | Mã lỗi |
|:-:|---|---|---|---|---|---|
| 1 | `GET` | `/api/v1/pitches?pitchType=&status=` | Công khai | — | `200 OK` + danh sách `PitchResponse` | — |
| 2 | `GET` | `/api/v1/pitches/{id}` | Công khai | — | `200 OK` + `PitchResponse` | `404` không có sân |
| 3 | `POST` | `/api/v1/pitches` | `chusan`, `admin` | `CreatePitchRequest` | `201 Created` + `Location` | `400` · `401` · `403` |
| 4 | `PATCH` | `/api/v1/pitches/{id}/status` | `chusan`, `admin` | `{status}` | `200 OK` + `PitchResponse` | `400` · `401` · `403` · `404` |
| 5 | `GET` | `/api/v1/instance-info` | Công khai | — | `200 OK` + `{instanceId, port, host, ...}` | — |
| 6 | `GET` | `/actuator/health` | Công khai | — | `200 OK` + `{"status":"UP"}` | — |

> **Endpoint số 2 là hợp đồng quan trọng nhất đối với Booking Service.** Booking chỉ dùng 3 trường: `id`, `pricePerHour`, `status`.
>
> **Endpoint số 5 (`/api/v1/instance-info`)** do Linh triển khai trong KT2, dùng để chứng minh cân bằng tải giữa 2 instance. Booking Service gọi xuyên qua nó tại `GET /api/v1/bookings/pitch-instance`.

**Cấu trúc `PitchResponse` (phần Booking Service phụ thuộc):**

```json
{
  "id": 1,
  "name": "Sân Bóng Đại Học Thể Thao (Sân 5)",
  "pitchType": "san_5",
  "pricePerHour": 300000.00,
  "status": "hoat_dong"
}
```

**Cam kết hợp đồng từ phía Provider (Linh) với Consumer (Nhật):**

1. `pricePerHour` là số dương, đơn vị VNĐ/giờ, không bao giờ `null` với sân đang `hoat_dong`.
2. `status` chỉ nhận một trong hai giá trị: `hoat_dong` hoặc `bao_tri`.
3. Sân không tồn tại thì trả đúng `404`, không trả `200` với body rỗng.
4. Tên trường giữ nguyên `camelCase` như trên; đổi tên trường là **thay đổi phá vỡ hợp đồng** (breaking change) và phải thông báo trước cho cả nhóm.

---

## 3. BOOKING SERVICE (CONSUMER — `pitchos-booking-service`, cổng 8083)

### 3.1. Bảng tổng hợp endpoint

| # | Method | Đường dẫn | Quyền | Body request | Phản hồi thành công | Mã lỗi |
|:-:|---|---|---|---|---|---|
| 1 | `POST` | `/api/v1/bookings` | `user` | `{pitchId, startTime, endTime}` | `201 Created` + `BookingResponse` | `400` · `401` · `403` · `404` · `502` · `503` |
| 2 | `GET` | `/api/v1/bookings/my-bookings` | `user` | — | `200 OK` + danh sách `BookingResponse` | `401` |
| 3 | `PATCH` | `/api/v1/bookings/{id}/status` | `chusan`, `admin` | `{status: "da_duyet" \| "tu_choi"}` | `200 OK` + `BookingResponse` | `400` · `401` · `403` · `404` |
| 4 | `GET` | `/api/v1/bookings/pitch-instance` | Công khai | — | `200 OK` + thông tin instance Pitch đang phục vụ | `503` khi hết instance Provider |
| 5 | `GET` | `/actuator/health` | Công khai | — | `200 OK` + `{"status":"UP"}` | — |
| 6 | `GET` | `/actuator/info` | Công khai | — | `200 OK` | — |

### 3.2. Chi tiết API đặt sân — `POST /api/v1/bookings`

**Request**

```http
POST /api/v1/bookings HTTP/1.1
Host: localhost:8083
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

{
  "pitchId": 1,
  "startTime": "2027-05-01T18:00:00",
  "endTime": "2027-05-01T19:30:00"
}
```

| Trường | Kiểu | Bắt buộc | Ràng buộc |
|---|---|:-:|---|
| `pitchId` | `Long` | ✔ | Phải tồn tại trên Pitch Service |
| `startTime` | `LocalDateTime` | ✔ | — |
| `endTime` | `LocalDateTime` | ✔ | Phải **sau** `startTime` |

> `userId` **không** nằm trong body mà được lấy từ JWT, tránh việc khách hàng đặt sân thay người khác.

**Response `201 Created`**

```json
{
  "id": 12,
  "userId": 3,
  "pitchId": 1,
  "startTime": "2027-05-01T18:00:00",
  "endTime": "2027-05-01T19:30:00",
  "totalPrice": 450000.00,
  "status": "cho_duyet",
  "createdAt": "2026-11-22T21:05:33"
}
```

Công thức tính tiền: `totalPrice = (số phút đặt / 60) × pricePerHour`, làm tròn `HALF_UP` 2 chữ số thập phân. Ví dụ: 90 phút × 300.000 đ/giờ = **450.000 đ**.

### 3.3. Bảng mã lỗi đầy đủ của API đặt sân

| Mã | `error` | Nguyên nhân | Nguồn phát sinh |
|:-:|---|---|---|
| `400` | Bad Request | Thiếu trường bắt buộc; `endTime` không sau `startTime`; sân đang `bao_tri`; khung giờ đã có người đặt | Consumer (validation + nghiệp vụ) |
| `401` | Unauthorized | Không gửi token, token sai chữ ký hoặc đã hết hạn | Consumer (JWT filter) |
| `403` | Forbidden | Sai vai trò (token `chusan`/`admin` gọi API đặt sân) | Consumer (Spring Security) |
| `404` | Not Found | `pitchId` không tồn tại trên Provider | Provider trả 404 → `CustomErrorDecoder` |
| `502` | Bad Gateway | Provider trả `200` nhưng `pricePerHour` `null` hoặc `<= 0` | Consumer kiểm tra dữ liệu Provider |
| `503` | Service Unavailable | Provider tắt hẳn, quá thời gian chờ, hoặc Eureka không còn instance nào | Feign / LoadBalancer → `GlobalExceptionHandler` |

**Mẫu body lỗi (áp dụng cho mọi mã lỗi của Booking Service):**

```json
{
  "timestamp": "2026-11-22T21:00:00",
  "status": 502,
  "error": "Bad Gateway",
  "message": "Dữ liệu đơn giá từ Pitch Service không hợp lệ"
}
```

---

## 4. HỢP ĐỒNG TÍCH HỢP NỘI BỘ (CONSUMER → PROVIDER)

| Hạng mục | Giá trị |
|---|---|
| Consumer | `pitchos-booking-service` |
| Provider | `pitchos-pitch-service` (2 instance) |
| Cách định vị | Service ID trong danh bạ Eureka, **không dùng URL cứng** |
| Thư viện gọi | Spring Cloud OpenFeign + Spring Cloud LoadBalancer (Round-Robin) |
| Endpoint được gọi | `GET /api/v1/pitches/{id}` và `GET /api/v1/instance-info` |
| Timeout kết nối | `2000 ms` |
| Timeout đọc dữ liệu | `3000 ms` |
| Dữ liệu Consumer kiểm tra lại | `pricePerHour != null && pricePerHour > 0`; `status == "hoat_dong"` |
| Quy tắc tuyệt đối | Consumer **không** truy cập `pitchos_pitch_db`; mọi dữ liệu sân chỉ lấy qua API |

---

## 5. BIẾN MÔI TRƯỜNG LIÊN QUAN ĐẾN TÍCH HỢP

| Biến | Giá trị khi chạy Docker | Ý nghĩa |
|---|---|---|
| `EUREKA_URL` | `http://pitchos-service-registry:8761/eureka/` | Địa chỉ danh bạ. Trong container **không** được dùng `localhost` |
| `MYSQL_HOST` | `mysql-booking` | Tên container CSDL của Booking Service |
| `BOOKING_SERVICE_PORT` | `8083` | Cổng dịch vụ |
| `JWT_SECRET` | Khóa dùng chung toàn hệ thống | Giải mã và xác thực token do Auth Service cấp |
| `INSTANCE_ID` | Tùy chọn | Hậu tố `eureka.instance.instance-id`, phân biệt các instance |

> ⚠️ Biến `PITCH_SERVICE_URL` của KT1 **đã bị loại bỏ hoàn toàn** khỏi `pitchos-booking-service`: Consumer không còn khái niệm "địa chỉ Provider", chỉ còn Service ID.
