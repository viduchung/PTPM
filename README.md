# PitchOS - Football Pitch Booking System (Kiến trúc SOA / Microservices)

## 📌 1. Giới thiệu Dự án
**PitchOS** là hệ thống quản lý và đặt sân bóng đá mini trực tuyến được thiết kế và xây dựng theo mô hình **Kiến trúc hướng dịch vụ (SOA / Microservices)**. Hệ thống phân tách thành 3 dịch vụ nghiệp vụ độc lập giao tiếp qua giao thức HTTP/REST, áp dụng nguyên tắc quản trị dữ liệu **Database-per-Service** và cơ chế bảo mật phân quyền phi tập trung qua **JWT (JSON Web Token)** với 3 vai trò: `admin`, `chusan`, `user`.

---

## 👥 2. DANH SÁCH THÀNH VIÊN & NHIỆM VỤ CÁ NHÂN (Tổng: 10.0 Điểm)

Dự án gồm 4 thành viên với vai trò và file nhiệm vụ chi tiết riêng biệt:

### 👤 [1. HÙNG — Phụ trách CSDL Phân tán & Tầng Repository](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_HUNG.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_HUNG.md](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_HUNG.md) | Thư mục: [`pitchos-database/`](file:///c:/Users/viduc/Downloads/loll/pitchos-database/README.md)
* **Cơ sở dữ liệu:** 3 Schemas MySQL độc lập (`pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`)
* **Lý thuyết (0,5đ):** Nguyên tắc Database-per-service & rủi ro vi phạm (Schema coupling, Deadlock chéo).
* **Thực nghiệm (2,0đ):** Viết 3 script SQL độc lập, Entity & Repository JPA, câu query chống trùng lịch trong `BookingRepository`, kiểm soát chỉ dùng logical ID không tạo FK vật lý.
* **Báo cáo phụ trách:** **Chương 3**
* **Nhiệm vụ Demo:** Mở DBeaver/Workbench chạy `SELECT` kiểm chứng đơn lưu đĩa cứng với trạng thái `cho_duyet`, chứng minh 3 DB độc lập.

---

### 👤 [2. LINH — Phụ trách Cơ chế JWT, Phân quyền RBAC & Auth Service](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_LINH.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_LINH.md](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_LINH.md) | Thư mục: [`pitchos-auth-service/`](file:///c:/Users/viduc/Downloads/loll/pitchos-auth-service/README.md)
* **Cổng dịch vụ (Port):** `8081` | **Cơ sở dữ liệu:** `pitchos_user_db`
* **Lý thuyết (1,0đ):** Phân biệt Authentication vs Authorization, cấu trúc 3 phần của JWT, phân biệt mã 401 vs 403.
* **Thực nghiệm (1,5đ):** Đăng ký (mã hóa mật khẩu BCrypt), Đăng nhập cấp phát JWT Bearer, nạp quyền `admin` / `chusan` / `user`, cấu hình `JwtAuthenticationFilter`, `AuthenticationEntryPoint` (401), `AccessDeniedHandler` (403). Bàn giao token mẫu & secret key cho nhóm.
* **Báo cáo phụ trách:** **Chương 4 & Chương 5**
* **Nhiệm vụ Demo:** Demo đăng nhập cấp JWT, test 3 ca bảo mật: không token (401), sai quyền (403), đúng quyền (200/201).

---

### 👤 [3. HOÀNG — Phụ trách Chuẩn hóa RESTful API & Pitch Service](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_HOANG.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_HOANG.md](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_HOANG.md) | Thư mục: [`pitchos-pitch-service/`](file:///c:/Users/viduc/Downloads/loll/pitchos-pitch-service/README.md)
* **Cổng dịch vụ (Port):** `8082` | **Cơ sở dữ liệu:** `pitchos_pitch_db`
* **Lý thuyết (1,5đ):** 4 đặc tính cơ bản của SOA, phân biệt Service - API - Client, danh mục dịch vụ PitchOS & SRP.
* **Thực nghiệm (1,0đ):** Xây dựng 4 API quản lý sân bóng (tên sân, giá, loại sân 5/7/10, địa chỉ, ảnh thumbnail, link map, trạng thái `hoat_dong` / `bao_tri`), cài đặt Jakarta Validation (`@Valid`, `@NotBlank`, `@Positive`), viết `GlobalExceptionHandler` trả về mã **400 Bad Request**, tích hợp OpenAPI / Swagger UI.
* **Báo cáo phụ trách:** **Chương 1**
* **Nhiệm vụ Demo:** Trực tiếp thao tác Swagger UI/Postman gọi API dữ liệu chuẩn (200/201), sau đó gửi dữ liệu sai quy cách để chứng minh mã lỗi 400 Bad Request.

---

### 👤 [4. NHẬT — Phụ trách Giao tiếp Liên dịch vụ, Sequence Diagram & Booking Service](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_NHAT.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_NHAT.md](file:///c:/Users/viduc/Downloads/loll/NHIEM_VU_NHAT.md) | Thư mục: [`pitchos-booking-service/`](file:///c:/Users/viduc/Downloads/loll/pitchos-booking-service/README.md)
* **Cổng dịch vụ (Port):** `8083` | **Cơ sở dữ liệu:** `pitchos_booking_db`
* **Lý thuyết (1,0đ):** Quy trình giao tiếp HTTP/REST, cấu trúc Request/Response, ý nghĩa các Status Code (2xx, 4xx, 5xx), nguy cơ sụp đổ dây chuyền (Cascading Failure).
* **Thực nghiệm (1,5đ):** Xây dựng nghiệp vụ đặt sân (kiểm tra khung giờ trống, tính tổng tiền, trạng thái `cho_duyet`, `da_duyet`, `tu_choi`), tích hợp Spring Cloud OpenFeign gọi Pitch Service (8082), xử lý lỗi phân tán (`ErrorDecoder` 404, ControllerAdvice bắt lỗi tắt Pitch Service trả về **503 Service Unavailable**), vẽ sơ đồ Sequence Diagram.
* **Báo cáo phụ trách:** **Chương 2**
* **Nhiệm vụ Demo:** Đặt sân thành công (201 Created); sau đó tắt Pitch Service (8082) và gọi lại để chứng minh bắt lỗi 503 Service Unavailable an toàn, không bị crash.

---

## 🗂️ 3. Cấu trúc Thư mục Dự án

```text
pitchos/
├── README.md                      # [TỔNG QUAN] Bảng điều phối toàn dự án
├── 🛠️ CONG_NGHE_SU_DUNG.md        # [TECH STACK] Toàn bộ công nghệ Backend, Frontend, CSDL
├── 🔑 .env                        # [MÔI TRƯỜNG] File cấu hình master dùng chung
├── 👤 NHIEM_VU_HUNG.md            # [HÙNG] File nhiệm vụ cá nhân chi tiết
├── 👤 NHIEM_VU_LINH.md            # [LINH] File nhiệm vụ cá nhân chi tiết
├── 👤 NHIEM_VU_HOANG.md           # [HOÀNG] File nhiệm vụ cá nhân chi tiết
├── 👤 NHIEM_VU_NHAT.md            # [NHẬT] File nhiệm vụ cá nhân chi tiết
│
├── pitchos-database/              # Thư mục CSDL phân tán (HÙNG)
│   ├── auth-user-service.sql      # CSDL User & Auth (Role: admin, chusan, user)
│   ├── pitch-service.sql          # CSDL Pitch (Trạng thái: hoat_dong, bao_tri)
│   ├── booking-service.sql        # CSDL Booking (Trạng thái: cho_duyet, da_duyet, tu_choi)
│   └── README.md                  # Hướng dẫn chi tiết thiết lập CSDL
│
├── pitchos-auth-service/          # Thư mục Auth & User Service (LINH - Port 8081)
│   └── README.md                  # Hướng dẫn cấu hình JWT & Security
│
├── pitchos-pitch-service/         # Thư mục Pitch Service (HOÀNG - Port 8082)
│   └── README.md                  # Hướng dẫn API Sân & Validation
│
├── pitchos-booking-service/       # Thư mục Booking Service (NHẬT - Port 8083)
│   └── README.md                  # Hướng dẫn OpenFeign & Xử lý lỗi 503
│
└── docs/                          # Tài liệu chung & Kế hoạch diễn tập
    └── DEMO_VA_KIEM_THU.md        # Kịch bản demo 5 bước và Sequence Diagram
```

---

## 🔄 4. Quy trình Phối hợp 5 Giai đoạn

1. **Giai đoạn 1 (HÙNG khởi đầu):** Chạy 3 file SQL trong `pitchos-database/`, bàn giao chuỗi kết nối cho Linh, Hoàng và Nhật.
2. **Giai đoạn 2 (LINH & HOÀNG code song song):**
   - **Linh:** Code Auth Service (8081), tạo token JWT mẫu với các role `admin`, `chusan`, `user` và gửi Secret Key cho nhóm.
   - **Hoàng:** Code Pitch Service (8082), hoàn thiện endpoint `GET /api/v1/pitches/{id}`, Swagger UI và Validation 400.
3. **Giai đoạn 3 (NHẬT code Booking Service):**
   - Dùng OpenFeign gọi `GET /api/v1/pitches/{id}` của Hoàng.
   - Viết `CustomErrorDecoder` (404) và `GlobalExceptionHandler` (bắt tắt service ra 503).
   - Tích hợp câu query chống trùng lịch của Hùng (bỏ qua trạng thái `tu_choi`).
4. **Giai đoạn 4 (LINH hỗ trợ HOÀNG & NHẬT):**
   - Chia sẻ `JwtAuthenticationFilter` và cấu hình phân quyền vào 2 dịch vụ còn lại.
   - Thiết lập chặn mã 401 (chưa đăng nhập) và 403 (truy cập sai role).
5. **Giai đoạn 5 (TỔNG DUYỆT CẢ 4 THÀNH VIÊN):**
   - Chạy kịch bản kiểm thử 5 bước theo [DEMO_VA_KIEM_THU.md](file:///c:/Users/viduc/Downloads/loll/docs/DEMO_VA_KIEM_THU.md).
   - Xuất file Postman Collection dùng chung và hoàn thiện báo cáo 5 chương.
