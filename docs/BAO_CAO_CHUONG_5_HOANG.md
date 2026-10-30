# BÁO CÁO KỸ THUẬT: CHƯƠNG 5 — KIỂM THỬ, KẾT QUẢ VÀ TỰ ĐÁNH GIÁ
**Học phần:** Kiến trúc phần mềm / Phát triển phần mềm  
**Đề tài:** PitchOS — Football Pitch Booking System (Kiến trúc SOA / Microservices)  
**Người chủ trì:** HOÀNG (Nhóm trưởng) — phối hợp cùng Linh, Hùng, Nhật  
**Phạm vi:** Tổng hợp kiểm thử toàn hệ thống, minh chứng kết quả và tự đánh giá

---

## 5.0. MÔI TRƯỜNG VÀ PHẠM VI KIỂM THỬ

### 5.0.1. Cấu hình môi trường thực nghiệm

| Thành phần | Phiên bản / Cấu hình |
| :--- | :--- |
| Java | 17 |
| Spring Boot | 3.2.5 |
| Spring Security | 6 (đi kèm Spring Boot 3.2.5) |
| Thư viện JWT | JJWT 0.11.5 |
| CSDL | MySQL 8.0 (Docker container `pitchos-mysql`) |
| Tài liệu API | SpringDoc OpenAPI 2.5.0 |
| Công cụ kiểm thử | cURL (tự động hóa bằng script Bash), Postman Collection |

> **Ghi chú về cổng dịch vụ:** cổng chuẩn của dự án là Auth 8081, Pitch 8082, Booking 8083, MySQL 3306. Tuy nhiên trên máy thực nghiệm, các cổng 8081 và 3306 đang bị những dự án khác chiếm dụng. Vì vậy đợt kiểm thử này chạy trên **cổng thay thế: Auth 18081, Pitch 18082, MySQL 3307**, thông qua biến môi trường `AUTH_SERVICE_PORT`, `PITCH_SERVICE_PORT`, `MYSQL_PORT`. Việc đổi cổng không ảnh hưởng tới logic nghiệp vụ hay kết quả bảo mật, vì toàn bộ cấu hình cổng đều được tham số hóa qua file `.env`.

### 5.0.2. Phạm vi đã kiểm chứng và chưa kiểm chứng

Để bảo đảm tính trung thực của báo cáo, phần này phân định rõ ràng:

| Nhóm ca kiểm thử | Phụ trách | Trạng thái |
| :--- | :---: | :--- |
| Xác thực, phân quyền RBAC, 401/403, quyền sở hữu | Hoàng | ✅ **Đã chạy thực tế, 36/36 đạt** |
| Token liên dịch vụ Auth → Pitch (401/403/201) | Hoàng + Linh | ✅ **Đã chạy thực tế** |
| Validation 400 trên Auth Service | Hoàng | ✅ **Đã chạy thực tế** |
| Validation 400 + Swagger UI trên Pitch Service | Linh | ⚠️ Linh tự kiểm chứng, chưa đưa vào đợt chạy này |
| Bắt lỗi 503 khi tắt Pitch Service | Nhật | ⚠️ **Chưa chạy trong đợt này** — do Nhật kiểm chứng |
| Chống trùng lịch đặt sân (409 / Conflict) | Nhật + Hùng | ⚠️ **Chưa chạy trong đợt này** — do Nhật và Hùng kiểm chứng |
| Kiểm chứng ghi dữ liệu xuống đĩa | Hùng | ⚠️ Hùng tự kiểm chứng |

---

## 5.1. MA TRẬN CA KIỂM THỬ TOÀN DIỆN

### 5.1.1. Bộ ca kiểm thử Validation dữ liệu đầu vào (400 Bad Request)

| Mã | Ca kiểm thử | Endpoint | Dữ liệu vào | Mong đợi | Kết quả |
| :---: | :--- | :--- | :--- | :---: | :---: |
| TC01 | Đăng ký hợp lệ | `POST /api/v1/auth/register` | Đầy đủ, email đúng định dạng | `201` | ✅ **Đạt** |
| TC01a | Vai trò mặc định của tài khoản mới | — | — | `role = user` | ✅ **Đạt** |
| TC01b | Phản hồi không chứa trường `password` | — | — | Không có | ✅ **Đạt** |
| TC02 | Đăng ký trùng tên đăng nhập | `POST /api/v1/auth/register` | `username = admin` | `400` | ✅ **Đạt** |
| TC03 | Đăng ký sai quy cách | `POST /api/v1/auth/register` | Email sai, mật khẩu 3 ký tự, họ tên trống | `400` + map `errors` | ✅ **Đạt** |
| TC03a | Bắt lỗi cụ thể trường `email` | — | `khong-phai-email` | Có khóa `email` | ✅ **Đạt** |
| TC03b | Bắt lỗi cụ thể trường `password` | — | `123` | Có khóa `password` | ✅ **Đạt** |
| TC03c | Đăng nhập thiếu mật khẩu | `POST /api/v1/auth/login` | Chỉ có `username` | `400` | ✅ **Đạt** |

Ví dụ phản hồi thực tế của TC03:

```json
{
  "timestamp": "2026-10-30T11:55:40.123",
  "status": 400,
  "error": "Bad Request",
  "message": "Dữ liệu đầu vào không hợp lệ. Vui lòng kiểm tra lại các trường vi phạm.",
  "path": "/api/v1/auth/register",
  "errors": {
    "email": "Email không đúng định dạng",
    "password": "Mật khẩu phải có ít nhất 6 ký tự",
    "fullName": "Họ và tên không được để trống",
    "phone": "Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0 (ví dụ 0912345678)"
  }
}
```

### 5.1.2. Bộ ca kiểm thử Xác thực và Phân quyền (401 Unauthorized, 403 Forbidden)

**Nhóm Authentication:**

| Mã | Ca kiểm thử | Mong đợi | Kết quả |
| :---: | :--- | :---: | :---: |
| TC-L1 | Đăng nhập `admin` / `123456` | `200` + token, `role = admin` | ✅ **Đạt** |
| TC-L2 | Đăng nhập `chusan` / `123456` | `200` + token, `role = chusan` | ✅ **Đạt** |
| TC-L3 | Đăng nhập `user` / `123456` | `200` + token, `role = user` | ✅ **Đạt** |
| TC04 | Đăng nhập sai mật khẩu | `401` | ✅ **Đạt** |
| TC05 | Đăng nhập tài khoản không tồn tại | `401` | ✅ **Đạt** |

**Nhóm kiểm chứng cấu trúc JWT:**

| Mã | Ca kiểm thử | Mong đợi | Kết quả |
| :---: | :--- | :---: | :---: |
| TC-J1 | Token gồm đúng 3 phần phân cách bởi dấu chấm | `3` | ✅ **Đạt** |
| TC-J2 | Header khai báo thuật toán HS256 | Có `HS256` | ✅ **Đạt** |
| TC-J3 | Payload chứa claim `userId` | Có | ✅ **Đạt** |
| TC-J4 | Claim `role` viết thường, không tiền tố `ROLE_` | `"role":"chusan"` | ✅ **Đạt** |

**Nhóm Authorization:**

| Mã | Ca kiểm thử | Token dùng | Mong đợi | Kết quả |
| :---: | :--- | :--- | :---: | :---: |
| TC06 | Gọi API bảo vệ không gửi token | — | `401` | ✅ **Đạt** |
| TC06a | Khuôn JSON lỗi 401 có `status`/`error`/`path` | — | Đầy đủ | ✅ **Đạt** |
| TC07 | Token tự bịa payload `role: admin`, sai chữ ký | Token giả mạo | `401` | ✅ **Đạt** |
| TC08 | Xem thông tin của chính mình | `user` | `200` | ✅ **Đạt** |
| TC09 | `user` gọi API danh sách người dùng | `user` | `403` | ✅ **Đạt** |
| TC09a | Khuôn JSON lỗi 403 chuẩn | — | `error = Forbidden` | ✅ **Đạt** |
| TC10 | `chusan` gọi API danh sách người dùng | `chusan` | `403` | ✅ **Đạt** |
| TC11 | `admin` gọi API danh sách người dùng | `admin` | `200` | ✅ **Đạt** |
| TC12 | `user` xem thông tin tài khoản khác (quyền sở hữu) | `user` | `403` | ✅ **Đạt** |
| TC13 | `chusan` xem thông tin tài khoản khác | `chusan` | `200` | ✅ **Đạt** |
| TC14 | Tra cứu ID người dùng không tồn tại | `admin` | `404` | ✅ **Đạt** |
| TC-N1 | Gọi đường dẫn không tồn tại (`/v3/api-docs`) | — | `404` | ✅ **Đạt** |

**Ca TC07 đáng chú ý nhất về mặt bảo mật.** Token được dùng có payload giải mã ra là `{"sub":"hacker","role":"admin"}` — tức kẻ tấn công tự khai mình là admin. Hệ thống vẫn từ chối với mã 401 vì phần chữ ký không được tạo bằng `SECRET_KEY`. Đây chính là minh chứng thực nghiệm cho giá trị của chữ ký HMAC-SHA256 đã phân tích ở mục 4.1.2.

### 5.1.3. Bộ ca kiểm thử Giao tiếp Liên dịch vụ

**Nhóm đã kiểm chứng — Token Auth Service dùng được cho Pitch Service:**

| Mã | Ca kiểm thử | Token dùng | Mong đợi | Kết quả |
| :---: | :--- | :--- | :---: | :---: |
| TC-X1 | `POST /api/v1/pitches` không gửi token | — | `401` | ✅ **Đạt** |
| TC-X2 | `POST /api/v1/pitches` với token `user` | `user` | `403` | ✅ **Đạt** |
| TC-X3 | `POST /api/v1/pitches` với token `chusan` | `chusan` | `201` | ✅ **Đạt** |
| TC-X4 | `POST /api/v1/pitches` với token `admin` | `admin` | `201` | ✅ **Đạt** |
| TC-X5 | `GET /api/v1/pitches` công khai, không cần token | — | `200` | ✅ **Đạt** |

Nhóm ca này có ý nghĩa kiến trúc quan trọng nhất trong toàn bộ đợt kiểm thử: nó chứng minh **hợp đồng token dùng chung giữa ba dịch vụ đã đồng bộ thành công**. Token do Auth Service (cổng 8081) cấp phát được Pitch Service (cổng 8082) — một tiến trình hoàn toàn độc lập, CSDL riêng, không hề gọi về Auth Service để hỏi — giải mã và phân quyền chính xác. Đây là đặc tính Stateless của JWT trong kiến trúc microservices được kiểm chứng bằng thực nghiệm.

**Nhóm chưa kiểm chứng trong đợt này** (thuộc phần của Nhật, cần chạy Booking Service):

| Mã | Ca kiểm thử | Mong đợi | Trạng thái |
| :---: | :--- | :---: | :--- |
| TC-503a | Đặt sân thành công khi Pitch Service đang bật | `201` | ⚠️ Nhật kiểm chứng |
| TC-503b | Tắt Pitch Service rồi đặt sân → bắt lỗi mạng | `503` | ⚠️ Nhật kiểm chứng |
| TC-503c | Đặt sân với `pitchId` không tồn tại | `404` | ⚠️ Nhật kiểm chứng |
| TC-X6 | Token Auth dùng được cho Booking Service | `201` | ⚠️ Chưa chạy |

> Bộ Postman Collection của Hoàng đã soạn sẵn ca **TC16** cho mục TC-X6, có thể chạy ngay khi Booking Service được khởi động.

### 5.1.4. Bộ ca kiểm thử Toàn vẹn dữ liệu và Chống trùng lịch

| Mã | Ca kiểm thử | Mong đợi | Trạng thái |
| :---: | :--- | :---: | :--- |
| TC-D1 | Đặt sân trùng khung giờ với đơn `cho_duyet` | Bị từ chối | ⚠️ Nhật + Hùng kiểm chứng |
| TC-D2 | Đặt sân trùng giờ với đơn đã `tu_choi` | Cho phép | ⚠️ Nhật + Hùng kiểm chứng |
| TC-D3 | Hai request đặt sân đồng thời cùng khung giờ | Chỉ 1 đơn thành công | ⚠️ Nhật đã xử lý ở commit `26a8de2` |
| TC-D4 | Kiểm chứng bản ghi ghi xuống đĩa với trạng thái `cho_duyet` | Có bản ghi | ⚠️ Hùng kiểm chứng |

### 5.1.5. Tổng hợp kết quả đợt kiểm thử của Hoàng

```
=============== KET QUA ===============
  PASS: 36    FAIL: 0
  => TAT CA CA KIEM THU DEU DAT
```

| Nhóm ca kiểm thử | Số ca | Đạt | Không đạt |
| :--- | :---: | :---: | :---: |
| Đăng nhập 3 vai trò | 6 | 6 | 0 |
| Cấu trúc JWT | 4 | 4 | 0 |
| Xác thực (Authentication) | 10 | 10 | 0 |
| Phân quyền RBAC (Authorization) | 11 | 11 | 0 |
| Liên dịch vụ Auth → Pitch | 5 | 5 | 0 |
| **TỔNG** | **36** | **36** | **0** |

---

## 5.2. MINH CHỨNG KẾT QUẢ THỰC NGHIỆM

### 5.2.1. Tài liệu API trên Swagger UI

Auth Service tích hợp SpringDoc OpenAPI 2.5.0, đồng bộ cấu hình đường dẫn với Pitch Service của Linh:

```properties
springdoc.api-docs.path=/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.operations-sorter=method
```

Kết quả kiểm chứng đường dẫn:

| Đường dẫn | Mã phản hồi |
| :--- | :---: |
| `/api-docs` | `200` |
| `/swagger-ui.html` | `200` |

Tài liệu OpenAPI sinh ra đầy đủ **5 endpoint**: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/users`, `/api/v1/users/{id}`, `/api/v1/users/me`.

Giao diện Swagger UI có nút **Authorize** (biểu tượng ổ khóa) cấu hình theo chuẩn `SecurityScheme` kiểu HTTP Bearer, cho phép dán token vào và kiểm thử trực quan các API được bảo vệ.

> *(Chèn ảnh chụp màn hình Swagger UI tại `http://localhost:8081/swagger-ui.html` — thể hiện danh sách endpoint và nút Authorize)*

### 5.2.2. Kết quả Postman Collection

Bộ sưu tập `pitchos-auth-service/postman/PitchOS-Auth.postman_collection.json` gồm **16 request** chia thành 5 thư mục:

| Thư mục | Nội dung | Số request |
| :--- | :--- | :---: |
| 0 | Đăng nhập 3 vai trò, tự lưu token vào biến collection | 3 |
| 1 | Demo hội đồng — 3 ca bảo mật kinh điển | 3 |
| 2 | Test cases Xác thực (đăng ký, validation, sai mật khẩu) | 5 |
| 3 | Test cases Phân quyền RBAC và quyền sở hữu | 9 |
| 4 | Bàn giao liên dịch vụ (Pitch + Booking) | 2 |

Mỗi request đều kèm **Test Script** tự động kiểm tra mã trạng thái và nội dung phản hồi, nên có thể chạy toàn bộ bằng **Collection Runner** và nhận báo cáo Pass/Fail tức thì.

> *(Chèn ảnh chụp màn hình Postman Collection Runner — thể hiện toàn bộ test case đạt trạng thái PASS)*

### 5.2.3. Minh chứng giải mã cấu trúc Token trên jwt.io

Token thật của tài khoản `chusan` thu được trong đợt kiểm thử, sau khi giải mã Base64Url:

**Header:**
```json
{ "alg": "HS256" }
```

**Payload:**
```json
{
  "sub": "chusan",
  "userId": 2,
  "role": "chusan",
  "fullName": "Trần Văn Chủ Sân",
  "iat": 1793336101,
  "exp": 1793422501
}
```

**Signature:** chuỗi băm HMAC-SHA256 của Header và Payload cùng `SECRET_KEY`. Khi dán token vào trang **jwt.io** và nhập đúng secret, trang web hiển thị dòng xác nhận **"Signature Verified"**; nếu sửa một ký tự bất kỳ trong Payload, dòng này lập tức chuyển thành **"Invalid Signature"** — minh chứng trực quan nhất cho cơ chế chống giả mạo.

> *(Chèn ảnh chụp màn hình jwt.io — thể hiện 3 phần Header / Payload / Signature và trạng thái Signature Verified)*

### 5.2.4. Minh chứng dữ liệu lưu trên MySQL

Truy vấn bảng `users` trong `pitchos_user_db` sau khi khởi động dịch vụ:

```sql
SELECT id, username, role, LEFT(password, 35) AS hash_prefix FROM pitchos_user_db.users;
```

| id | username | role | hash_prefix |
| :---: | :--- | :--- | :--- |
| 1 | admin | admin | `$2a$10$...` |
| 2 | chusan | chusan | `$2a$10$...` |
| 3 | user | user | `$2a$10$...` |

Điểm cần nhấn mạnh: cột `password` **chỉ chứa chuỗi băm BCrypt** với tiền tố `$2a$10$`, hoàn toàn không có mật khẩu dạng văn bản thuần. Mỗi tài khoản có chuỗi băm khác nhau dù cùng mật khẩu `123456`, do BCrypt tự sinh salt riêng.

> *(Chèn ảnh chụp màn hình DBeaver / MySQL Workbench — thể hiện bảng users với cột password đã băm)*

---

## 5.3. KỊCH BẢN DIỄN TẬP DEMO HỘI ĐỒNG (10–15 PHÚT)

### Bước 1 — Khởi động hệ thống *(Hùng, 2 phút)*

1. Chạy MySQL và nạp 3 script SQL trong `pitchos-database/`, hoặc dùng `docker compose up -d`.
2. Mở DBeaver hiển thị **3 schema độc lập** `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`, chỉ rõ **không có khóa ngoại vật lý** nối giữa các schema.
3. Khởi động lần lượt 3 dịch vụ trên cổng 8081, 8082, 8083.

### Bước 2 — Chuẩn hóa RESTful API và Validation *(Linh, 3 phút)*

1. Mở Swagger UI tại `http://localhost:8082/swagger-ui.html`.
2. Gọi `GET /api/v1/pitches` → nhận **200 OK** kèm danh sách sân.
3. Gọi `POST /api/v1/pitches` với dữ liệu sai (tên trống, giá âm) → nhận **400 Bad Request** kèm map `errors` chi tiết từng trường.

### Bước 3 — Xác thực và Phân quyền *(Hoàng, 5 phút)*

1. **Cấp phát token:** gọi `POST /api/v1/auth/login` với `chusan` / `123456` → nhận **200 OK** kèm `accessToken`.
2. **Soi cấu trúc token:** dán token vào **jwt.io**, chỉ cho hội đồng thấy ba phần Header (`alg: HS256`), Payload (`sub`, `userId`, `role: chusan`, `exp`) và Signature đã xác minh.
3. **Ca 1 — 401 Unauthorized:** gọi `POST /api/v1/pitches` **không gửi token** → nhận **401**.
4. **Ca 2 — 403 Forbidden:** đăng nhập bằng `user`, dùng token đó gọi `POST /api/v1/pitches` → nhận **403**.
5. **Ca 3 — 201 Created:** dùng lại token `chusan` gọi chính API đó → nhận **201**.
6. **Ca bổ sung — 403 do quyền sở hữu:** dùng token `user` gọi `GET /api/v1/users/1` (tài khoản admin) → nhận **403**, chứng minh hệ thống không tin tưởng ID client gửi lên.
7. **Ca bổ sung — chống giả mạo:** gửi token tự bịa `{"role":"admin"}` nhưng sai chữ ký → nhận **401**.

### Bước 4 — Giao tiếp liên dịch vụ và xử lý lỗi phân tán *(Nhật, 4 phút)*

1. Dùng token `user` gọi `POST /api/v1/bookings` → nhận **201 Created**; Booking Service đã gọi sang Pitch Service qua OpenFeign để lấy giá và trạng thái sân.
2. Báo Hùng chạy `SELECT` kiểm chứng đơn vừa tạo đã ghi xuống đĩa với trạng thái `cho_duyet`.
3. **Tắt Pitch Service** (Ctrl + C cửa sổ cổng 8082), gửi lại request đặt sân → nhận **503 Service Unavailable**, chứng minh Booking Service bắt lỗi an toàn thay vì sụp đổ dây chuyền.
4. Gọi lại một API khác của Booking Service để chứng minh dịch vụ này **vẫn còn sống**.

### Bước 5 — Tổng kết *(Hoàng, 1 phút)*

Chạy toàn bộ Postman Collection bằng Collection Runner, trình bày bảng kết quả Pass/Fail tổng hợp của cả bốn thành viên.

---

## 5.4. TỰ ĐÁNH GIÁ VÀ HƯỚNG PHÁT TRIỂN

### 5.4.1. Bảng tự đánh giá mức độ đáp ứng yêu cầu

| Yêu cầu theo đề | Thành viên | Mức đáp ứng | Minh chứng |
| :--- | :---: | :--- | :--- |
| Câu 1 Ý 1a — Đặc điểm SOA, phân biệt Service/API/Client | Linh | Hoàn thành | Chương 1, mục 1.2 |
| Câu 1 Ý 1b — Phân rã dịch vụ, 03 API tiêu biểu, SRP | Linh | Hoàn thành | Chương 1, mục 1.3 |
| Câu 1 Ý 2a — HTTP/REST, Request/Response, Status code | Nhật | Hoàn thành | Chương 2, mục 2.1 |
| Câu 1 Ý 2b — Database-per-service và rủi ro vi phạm | Hùng | Hoàn thành | Chương 3, mục 3.1 |
| Câu 1 Ý 3 — AuthN vs AuthZ, cấu trúc JWT, 401 vs 403 | **Hoàng** | **Hoàn thành** | **Chương 4, mục 4.1** |
| Câu 2 Ý 1 — RESTful API, Validation 400, Swagger UI | Linh | Hoàn thành | Chương 1, mục 1.4 |
| Câu 2 Ý 2 — OpenFeign, bắt lỗi 503, Sequence Diagram | Nhật | Hoàn thành | Chương 2, mục 2.2–2.3 |
| Câu 2 Ý 3 — CSDL phân tán, Entity, Repository JPA | Hùng | Hoàn thành | Chương 3, mục 3.2–3.5 |
| Câu 2 Ý 4 — Auth, JWT, RBAC, kiểm thử bảo mật | **Hoàng** | **Hoàn thành** | **Chương 4 mục 4.2–4.3; Chương 5 mục 5.1** |
| Yêu cầu II.3 — Kịch bản demo hội đồng | Cả nhóm | Hoàn thành | Chương 5, mục 5.3 |

### 5.4.2. Những vấn đề phát hiện được trong quá trình kiểm thử

Quá trình chạy thực nghiệm đã phát hiện ba vấn đề mà việc đọc code đơn thuần không thể thấy. Phần này ghi lại trung thực để nhóm xử lý.

**Vấn đề 1 — Chuỗi băm BCrypt trong script SQL không khớp mật khẩu ghi trong chú thích.**

File `pitchos-database/auth-user-service.sql` nạp sẵn ba tài khoản với chú thích *"Mật khẩu mặc định: 123456"*, nhưng chuỗi băm thực tế là `$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy` — đây là chuỗi băm mẫu lấy từ tài liệu Spring Security, **không phải** băm của `123456`. Log thực tế khi khởi động dịch vụ:

```
WARN  c.pitchos.auth.config.DataInitializer : Tài khoản 'admin' có chuỗi băm BCrypt
      không khớp mật khẩu mặc định '123456'. Đang băm lại để phục vụ kiểm thử và demo.
WARN  c.pitchos.auth.config.DataInitializer : Tài khoản 'chusan' ... (tương tự)
WARN  c.pitchos.auth.config.DataInitializer : Tài khoản 'user' ... (tương tự)
```

Nếu không phát hiện, **toàn bộ buổi demo sẽ sụp ngay bước đăng nhập đầu tiên**. Giải pháp tạm thời: lớp `DataInitializer` tự soát và băm lại ba tài khoản mẫu khi khởi động. Giải pháp triệt để: cập nhật lại chuỗi băm đúng trong file SQL.

**Vấn đề 2 — Dữ liệu tiếng Việt trong CSDL bị mã hóa hai lần (double-encoding).**

Họ tên tài khoản hiển thị sai: `Trần Văn Chủ Sân` thành `Tráº§n VÄƒn Chá»§ SÃ¢n`. Kiểm tra byte thực tế trong CSDL:

```sql
SELECT HEX(LEFT(full_name, 3)) FROM users WHERE username = 'chusan';
-- Kết quả: 5472C3A1   (đúng ra phải là 5472E1BAA7 cho chữ "Trầ")
```

Nguyên nhân: file SQL đã khai báo `CHARACTER SET utf8mb4` cho database, nhưng **thiếu câu lệnh `SET NAMES utf8mb4;`** ở đầu file. Khi MySQL client đọc file, nó mặc định dùng `latin1`, khiến các byte UTF-8 bị hiểu sai rồi mã hóa lại thành UTF-8 lần thứ hai. Đây là lỗi dữ liệu, không phải lỗi code. Giải pháp: thêm `SET NAMES utf8mb4;` vào đầu cả ba file SQL, hoặc nạp file bằng `mysql --default-character-set=utf8mb4`.

**Vấn đề 3 — Đường dẫn không tồn tại trả về 500 thay vì 404.**

Khi gọi `/v3/api-docs` (đường dẫn mặc định của SpringDoc, trong khi dự án cấu hình `/api-docs`), hệ thống trả về **500 Internal Server Error** kèm thông báo *"No static resource v3/api-docs"*. Nguyên nhân: `NoResourceFoundException` bị handler `@ExceptionHandler(Exception.class)` bắt và gói thành 500 — sai ngữ nghĩa HTTP.

Đã khắc phục bằng cách bổ sung handler tường minh cho `NoResourceFoundException` trả về **404 Not Found**. Sau khi vá, `/v3/api-docs` trả về 404 đúng chuẩn.

> **Lưu ý cho Linh và Nhật:** `GlobalExceptionHandler` của Pitch Service và Booking Service có cùng cấu trúc nên rất có thể gặp y hệt vấn đề này. Nên bổ sung handler tương tự cho đồng bộ.

### 5.4.3. Hạn chế hiện tại của hệ thống

| Hạn chế | Ảnh hưởng | Mức độ |
| :--- | :--- | :---: |
| Dùng thuật toán đối xứng HS256, mọi dịch vụ đều có khả năng tự ký token | Nếu một dịch vụ bị chiếm quyền, kẻ tấn công có thể tự phát hành token `admin` | Cao |
| Chưa có Refresh Token | Token hết hạn sau 24 giờ, người dùng phải đăng nhập lại | Trung bình |
| Chưa có cơ chế thu hồi token (Token Revocation) | Token bị lộ vẫn dùng được cho tới khi hết hạn | Trung bình |
| Chưa có API Gateway | Mỗi dịch vụ phải tự cài đặt lại logic xác thực, code bảo mật bị lặp 3 lần | Trung bình |
| Chưa giới hạn số lần đăng nhập sai (Rate Limiting) | Chưa chống được tấn công dò mật khẩu | Trung bình |
| Chưa có Circuit Breaker | Pitch Service sập chỉ được bắt bằng 503, chưa có cơ chế ngắt mạch và tự phục hồi | Thấp |
| Chưa chạy HTTPS | Token truyền dạng rõ trên đường truyền, có thể bị chặn bắt | Cao (môi trường thật) |

### 5.4.4. Hướng phát triển

1. **Chuyển sang RS256 (thuật toán bất đối xứng).** Auth Service giữ private key để ký, các dịch vụ còn lại chỉ nhận public key để xác minh. Khi đó dù Pitch hay Booking Service bị chiếm quyền, kẻ tấn công cũng **không thể tự phát hành token** — khắc phục hạn chế nghiêm trọng nhất hiện nay.
2. **Bổ sung API Gateway** (Spring Cloud Gateway) làm điểm xác thực tập trung tại biên hệ thống, loại bỏ việc lặp code bảo mật ở cả ba dịch vụ.
3. **Thêm Refresh Token** với vòng đời dài kèm cơ chế thu hồi, cải thiện trải nghiệm người dùng mà vẫn giữ Access Token thời hạn ngắn.
4. **Tích hợp Circuit Breaker** (Resilience4j) cho các lời gọi OpenFeign, bổ sung cơ chế ngắt mạch và fallback thay vì chỉ trả 503.
5. **Triển khai HTTPS/TLS** và **Rate Limiting** trên các endpoint đăng nhập.
6. **Ghi log kiểm toán bảo mật (Audit Log)** cho các sự kiện đăng nhập thất bại và truy cập bị từ chối, phục vụ truy vết sự cố.

---

## 5.5. KẾT LUẬN

Hệ thống **PitchOS** đã được xây dựng hoàn chỉnh theo kiến trúc hướng dịch vụ với ba microservice độc lập, mỗi dịch vụ sở hữu cơ sở dữ liệu riêng, giao tiếp qua HTTP/REST và được bảo vệ thống nhất bằng cơ chế JWT phi trạng thái.

Về phần bảo mật do Hoàng phụ trách, **36/36 ca kiểm thử đều đạt**, bao gồm đầy đủ các tình huống xác thực, phân quyền ba vai trò, kiểm tra quyền sở hữu tài nguyên, chống giả mạo token và phân biệt chính xác hai mã lỗi 401/403. Đặc biệt, nhóm ca kiểm thử liên dịch vụ đã chứng minh bằng thực nghiệm rằng token do Auth Service cấp phát được Pitch Service — một tiến trình độc lập hoàn toàn — xác thực và phân quyền chính xác, qua đó khẳng định tính đúng đắn của hợp đồng token dùng chung trong kiến trúc microservices.

Quá trình kiểm thử thực tế cũng phát hiện ba vấn đề tiềm ẩn mà việc đọc mã nguồn không thể thấy, trong đó có một vấn đề đủ nghiêm trọng để làm sụp toàn bộ buổi demo nếu không được xử lý kịp thời. Điều này cho thấy giá trị không thể thay thế của việc **chạy và kiểm thử thực tế** so với chỉ kiểm tra bằng mắt.
