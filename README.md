# PitchOS - Football Pitch Booking System (Kiến trúc SOA / Microservices)

## 📌 1. Giới thiệu Dự án
**PitchOS** là hệ thống quản lý và đặt sân bóng đá mini trực tuyến được thiết kế và xây dựng theo mô hình **Kiến trúc hướng dịch vụ (SOA / Microservices)**. Hệ thống phân tách thành các dịch vụ nghiệp vụ độc lập giao tiếp qua giao thức HTTP/REST, áp dụng nguyên tắc quản trị dữ liệu **Database-per-Service** và cơ chế bảo mật phân quyền phi tập trung qua **JWT (JSON Web Token)** với 3 vai trò: `admin`, `chusan`, `user`.

---

## 👥 2. BẢNG PHÂN CHIA NHIỆM VỤ CHI TIẾT & BAREM ĐIỂM (TỔNG: 10,0 ĐIỂM)

> **Căn cứ theo đề thi:** Bài kiểm tra số 1 (Học phần Kiến trúc phần mềm) gồm **Câu 1: Lý thuyết (4,0 điểm)** và **Câu 2: Thực nghiệm (6,0 điểm)**.  
> Nhóm gồm 4 thành viên, phân công độc lập từng ý rõ ràng, **không ai trùng ai**, nhóm trưởng **Hoàng** phụ trách mảng bảo mật cốt lõi với điểm số nhỉnh hơn:

| STT | Thành viên | Vai trò & Dịch vụ phụ trách | Ý phụ trách theo Đề thi | Điểm chi tiết | Tổng điểm | Báo cáo |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **1** | 👑 **HOÀNG** *(Nhóm trưởng)* | **Phụ trách Cơ chế JWT, Phân quyền RBAC & Auth Service**<br>• Dịch vụ: `pitchos-auth-service` (Port 8081)<br>• CSDL: `pitchos_user_db` | • **Câu 1 - Ý 3 (Lý thuyết):** Xác thực & Phân quyền, JWT, HTTP 401 vs 403 (1,0đ)<br>• **Câu 2 - Ý 4 (Thực nghiệm):** Triển khai Auth, JWT, RBAC, kiểm thử bảo mật (2,0đ) | 1,0đ (LT)<br>+ 2,0đ (TN) | **3,0 / 10,0** | **Chương 4 & Chương 5** |
| **2** | 👤 **LINH** | **Phụ trách Kiến trúc SOA, Chuẩn hóa RESTful API & Pitch Service**<br>• Dịch vụ: `pitchos-pitch-service` (Port 8082)<br>• CSDL: `pitchos_pitch_db` | • **Câu 1 - Ý 1a (Lý thuyết):** Đặc điểm SOA, phân biệt Service - API - Client (0,5đ)<br>• **Câu 1 - Ý 1b (Lý thuyết):** Phân rã dịch vụ PitchOS, 03 API tiêu biểu, SRP (1,0đ)<br>• **Câu 2 - Ý 1 (Thực nghiệm):** Xây dựng RESTful API, Validation 400, Swagger UI (1,0đ) | 1,5đ (LT)<br>+ 1,0đ (TN) | **2,5 / 10,0** | **Chương 1** |
| **3** | 👤 **HÙNG** | **Phụ trách Quản trị CSDL Phân tán & Tầng Repository**<br>• Dịch vụ: Quản trị 3 DB MySQL độc lập<br>• CSDL: `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db` | • **Câu 1 - Ý 2b (Lý thuyết):** Nguyên tắc Database-per-service & rủi ro vi phạm (0,75đ)<br>• **Câu 2 - Ý 3 (Thực nghiệm):** CSDL phân tán, Entity, Repository JPA, kiểm chứng ghi đĩa (1,5đ) | 0,75đ (LT)<br>+ 1,5đ (TN) | **2,25 / 10,0** | **Chương 3** |
| **4** | 👤 **NHẬT** | **Phụ trách Giao tiếp Liên dịch vụ, Sequence Diagram & Booking Service**<br>• Dịch vụ: `pitchos-booking-service` (Port 8083)<br>• CSDL: `pitchos_booking_db` | • **Câu 1 - Ý 2a (Lý thuyết):** Giao tiếp HTTP/REST, Request/Response, Status code (0,75đ)<br>• **Câu 2 - Ý 2 (Thực nghiệm):** Giao tiếp liên dịch vụ qua OpenFeign, bắt lỗi 503, Sequence Diagram (1,5đ) | 0,75đ (LT)<br>+ 1,5đ (TN) | **2,25 / 10,0** | **Chương 2** |

---

## 🎯 3. CHI TIẾT NHIỆM VỤ TỪNG THÀNH VIÊN

### 👑 [1. HOÀNG (Nhóm trưởng) — Bảo mật JWT, Phân quyền RBAC & Auth Service (3,0 Điểm)](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_HOANG.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_HOANG.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_HOANG.md) | Thư mục: [`pitchos-auth-service/`](file:///c:/Users/viduc/Downloads/PTPM/pitchos-auth-service/README.md)
* **Cổng dịch vụ (Port):** `8081` | **Cơ sở dữ liệu:** `pitchos_user_db`
* **Lý thuyết (1,0đ - Câu 1 Ý 3):** Phân biệt Authentication vs Authorization; cấu trúc 3 phần của JWT (Header, Payload claims, Signature HMAC-SHA256); giải thích sự khác nhau giữa HTTP 401 Unauthorized và HTTP 403 Forbidden; liên hệ vai trò `admin`, `chusan`, `user`.
* **Thực nghiệm (2,0đ - Câu 2 Ý 4):** Xây dựng Auth & User Service; đăng ký mã hóa BCrypt; đăng nhập cấp phát Bearer JWT Token; cấu hình `JwtAuthenticationFilter`, `AuthenticationEntryPoint` (401), `AccessDeniedHandler` (403); bảo vệ các API; kiểm thử truy cập hợp lệ, không token (401), sai quyền (403); nộp bộ test cases bảo mật.
* **Báo cáo phụ trách:** **Chương 4 & Chương 5** (Chủ trì tổng hợp kiểm thử toàn hệ thống).
* **Nhiệm vụ Demo:** Đăng nhập cấp JWT, soi token trên jwt.io, test 3 ca bảo mật: 401 Unauthorized, 403 Forbidden, 200/201 Thành công.

---

### 👤 [2. LINH — Chuẩn hóa RESTful API, Validation & Pitch Service (2,5 Điểm)](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_LINH.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_LINH.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_LINH.md) | Thư mục: [`pitchos-pitch-service/`](file:///c:/Users/viduc/Downloads/PTPM/pitchos-pitch-service/README.md)
* **Cổng dịch vụ (Port):** `8082` | **Cơ sở dữ liệu:** `pitchos_pitch_db`
* **Lý thuyết (1,5đ - Câu 1 Ý 1):**
  - **Ý 1a (0,5đ):** 4 đặc điểm chính của kiến trúc SOA (Liên kết lỏng, Hợp đồng chuẩn hóa, Tính trừu tượng, Khả năng tái sử dụng); phân biệt Dịch vụ (Service), API và Ứng dụng khách (Client).
  - **Ý 1b (1,0đ):** Xác định các dịch vụ chính của PitchOS, trách nhiệm từng dịch vụ, 03 API tiêu biểu; luận giải lý do phân chia theo nguyên lý Đơn trách nhiệm (SRP).
* **Thực nghiệm (1,0đ - Câu 2 Ý 1):** Triển khai 4 API quản lý sân bóng chuẩn RESTful (URL rõ ràng, method phù hợp); cài đặt Jakarta Validation (`@Valid`, `@NotBlank`, `@Positive`); viết `GlobalExceptionHandler` trả về chuẩn mã **400 Bad Request** khi dữ liệu sai quy cách; tích hợp tài liệu OpenAPI / Swagger UI tại `/swagger-ui.html`.
* **Báo cáo phụ trách:** **Chương 1** (Mô tả bài toán, kiến trúc SOA, phân rã dịch vụ, đặc tả API).
* **Nhiệm vụ Demo:** Mở Swagger UI thao tác gọi API hợp lệ (200/201); gửi dữ liệu sai quy chuẩn (tên rỗng, giá âm) chứng minh bắt lỗi 400 Bad Request.

---

### 👤 [3. HÙNG — Quản trị CSDL Phân tán & Tầng Repository (2,25 Điểm)](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_HUNG.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_HUNG.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_HUNG.md) | Thư mục: [`pitchos-database/`](file:///c:/Users/viduc/Downloads/PTPM/pitchos-database/README.md)
* **Cơ sở dữ liệu:** 3 Schemas MySQL độc lập (`pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`)
* **Lý thuyết (0,75đ - Câu 1 Ý 2b):** Nguyên tắc mỗi dịch vụ tự quản lý dữ liệu (Database-per-service); phân tích rủi ro khi vi phạm (ghép nối lược đồ Schema Coupling, Deadlock khóa dòng chéo, phá vỡ tính bao đóng, cản trở scale).
* **Thực nghiệm (1,5đ - Câu 2 Ý 3):** Soạn thảo 3 script SQL độc lập; thiết lập cấu trúc thực thể Entity & Repository JPA; câu query chống trùng lịch thi đấu trong `BookingRepository`; kiểm soát chỉ lưu Logical ID dạng số nguyên, **tuyệt đối không tạo Foreign Key vật lý**; kiểm chứng thao tác ghi dữ liệu xuống đĩa cứng.
* **Báo cáo phụ trách:** **Chương 3** (Quản lý dữ liệu phân tán, ERD từng dịch vụ, kiến trúc Entity / Repository JPA).
* **Nhiệm vụ Demo:** Mở DBeaver/Workbench show 3 schema DB độc lập không có FK chéo; chạy `SELECT` kiểm chứng đơn lưu đĩa cứng với trạng thái `cho_duyet` sau khi đặt sân.

---

### 👤 [4. NHẬT — Giao tiếp Liên dịch vụ, Sequence Diagram & Booking Service (2,25 Điểm)](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_NHAT.md)
* **File nhiệm vụ chi tiết:** 👉 [NHIEM_VU_NHAT.md](file:///c:/Users/viduc/Downloads/PTPM/NHIEM_VU_NHAT.md) | Thư mục: [`pitchos-booking-service/`](file:///c:/Users/viduc/Downloads/PTPM/pitchos-booking-service/README.md)
* **Cổng dịch vụ (Port):** `8083` | **Cơ sở dữ liệu:** `pitchos_booking_db`
* **Lý thuyết (0,75đ - Câu 1 Ý 2a):** Mô tả quy trình giao tiếp giữa 2 dịch vụ (Booking Service $\rightarrow$ Pitch Service); làm rõ vai trò của HTTP/REST, Request (method, header, body), Response (status code, header, body); phân tích các nhóm mã trạng thái `2xx`, `4xx`, `5xx`; nguy cơ sụp đổ dây chuyền (Cascading Failure).
* **Thực nghiệm (1,5đ - Câu 2 Ý 2):** Xây dựng nghiệp vụ đặt sân có sự tham gia của từ 2 dịch vụ trở lên; tích hợp Spring Cloud OpenFeign gọi sang Pitch Service lấy thông tin giá & trạng thái; xử lý lỗi phân tán (`CustomErrorDecoder` bắt 404, `GlobalExceptionHandler` bắt lỗi mạng khi Pitch Service sập chuyển đổi thành mã chuẩn **503 Service Unavailable**); vẽ sơ đồ tuần tự Sequence Diagram.
* **Báo cáo phụ trách:** **Chương 2** (Thiết kế API Booking, giao tiếp OpenFeign, Sequence Diagram, cơ chế xử lý lỗi 503).
* **Nhiệm vụ Demo:** Đặt sân thành công nhận mã `201 Created`; sau đó **tắt Pitch Service (Port 8082)** và gửi lại request đặt sân để chứng minh Booking Service bắt lỗi an toàn và trả về mã **503 Service Unavailable**.

---

## 🗂️ 4. Cấu trúc Thư mục Dự án

```text
pitchos/
├── README.md                      # [TỔNG QUAN] Bảng điều phối toàn dự án & Barem điểm chuẩn
├── 🛠️ CONG_NGHE_SU_DUNG.md        # [TECH STACK] Toàn bộ công nghệ Backend, Frontend, CSDL
├── 🔑 .env                        # [MÔI TRƯỜNG] File cấu hình master dùng chung
├── 👤 NHIEM_VU_HOANG.md           # [HOÀNG - Nhóm trưởng] File nhiệm vụ chi tiết (3,0đ)
├── 👤 NHIEM_VU_LINH.md            # [LINH] File nhiệm vụ chi tiết (2,5đ)
├── 👤 NHIEM_VU_HUNG.md            # [HÙNG] File nhiệm vụ chi tiết (2,25đ)
├── 👤 NHIEM_VU_NHAT.md            # [NHẬT] File nhiệm vụ chi tiết (2,25đ)
│
├── pitchos-database/              # Thư mục CSDL phân tán (HÙNG phụ trách)
│   ├── auth-user-service.sql      # CSDL User & Auth (Role: admin, chusan, user)
│   ├── pitch-service.sql          # CSDL Pitch (Trạng thái: hoat_dong, bao_tri)
│   ├── booking-service.sql        # CSDL Booking (Trạng thái: cho_duyet, da_duyet, tu_choi)
│   └── README.md                  # Hướng dẫn chi tiết thiết lập CSDL (Hùng)
│
├── pitchos-auth-service/          # Thư mục Auth & User Service (HOÀNG phụ trách - Port 8081)
│   └── README.md                  # Hướng dẫn cấu hình JWT & RBAC Security (Hoàng)
│
├── pitchos-pitch-service/         # Thư mục Pitch Service (LINH phụ trách - Port 8082)
│   └── README.md                  # Hướng dẫn API Sân & Validation (Linh)
│
├── pitchos-booking-service/       # Thư mục Booking Service (NHẬT phụ trách - Port 8083)
│   └── README.md                  # Hướng dẫn OpenFeign & Xử lý lỗi 503 (Nhật)
│
└── docs/                          # Tài liệu chung & Kế hoạch diễn tập
    └── DEMO_VA_KIEM_THU.md        # Kịch bản demo 5 bước và Sequence Diagram
```

---

## 🔄 5. Quy trình Phối hợp 5 Giai đoạn

1. **Giai đoạn 1 (HÙNG khởi đầu):** Chạy 3 file SQL trong `pitchos-database/`, bàn giao chuỗi kết nối cho Hoàng, Linh và Nhật.
2. **Giai đoạn 2 (HOÀNG & LINH code song song):**
   - **Hoàng (Nhóm trưởng):** Code Auth Service (8081), tạo token JWT mẫu với các role `admin`, `chusan`, `user` và gửi Secret Key cho nhóm.
   - **Linh:** Code Pitch Service (8082), hoàn thiện endpoint `GET /api/v1/pitches/{id}`, Swagger UI và Validation 400.
3. **Giai đoạn 3 (NHẬT code Booking Service):**
   - Dùng OpenFeign gọi `GET /api/v1/pitches/{id}` của Linh.
   - Viết `CustomErrorDecoder` (404) và `GlobalExceptionHandler` (bắt tắt service ra 503).
   - Tích hợp câu query chống trùng lịch của Hùng (bỏ qua trạng thái `tu_choi`).
4. **Giai đoạn 4 (HOÀNG hỗ trợ LINH & NHẬT):**
   - Chia sẻ `JwtAuthenticationFilter` và cấu hình phân quyền vào 2 dịch vụ còn lại.
   - Thiết lập chặn mã 401 (chưa đăng nhập) và 403 (truy cập sai role).
5. **Giai đoạn 5 (TỔNG DUYỆT CẢ 4 THÀNH VIÊN):**
   - Chạy kịch bản kiểm thử 5 bước theo [DEMO_VA_KIEM_THU.md](file:///c:/Users/viduc/Downloads/PTPM/docs/DEMO_VA_KIEM_THU.md).
   - Xuất file Postman Collection dùng chung và hoàn thiện báo cáo 5 chương theo đúng phân công.
