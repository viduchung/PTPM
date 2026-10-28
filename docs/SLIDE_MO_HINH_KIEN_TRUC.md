# 📊 TÀI LIỆU & KỊCH BẢN THUYẾT TRÌNH SLIDE MÔ HÌNH KIẾN TRÚC PITCHOS

> **File trình chiếu PowerPoint:**
> - Trong thư mục dự án: [`docs/PitchOS-mo-hinh-kien-truc.pptx`](file:///c:/Users/viduc/Downloads/PTPM/docs/PitchOS-mo-hinh-kien-truc.pptx)
> - Trong thư mục Downloads cá nhân: [`PitchOS-mo-hinh-kien-truc.pptx`](file:///c:/Users/viduc/Downloads/PitchOS-mo-hinh-kien-truc.pptx)

---

## 🖼️ 1. HÌNH ẢNH MÔ HÌNH KIẾN TRÚC TỔNG THỂ (SLIDE 03 / 12)

![Kiến trúc tổng thể PitchOS](images/pitchos-kien-truc-tong-the.png)

### 📌 Phân tích 5 Tầng Kiến trúc:
1. **Tầng 1 - Người dùng (Actors):**
   - `Khách hàng (ROLE: USER)`: Tra cứu sân, xem bảng giá và đặt lịch trực tuyến.
   - `Chủ sân (ROLE: CHUSAN)`: Quản lý thông tin sân, cấu hình giá thuê, bật/tắt bảo trì và duyệt đơn.
   - `Quản trị viên (ROLE: ADMIN)`: Quản trị tài khoản, phân quyền hệ thống và giám sát vận hành.
2. **Tầng 2 - Giao diện Client (Frontend):**
   - Ứng dụng Web Single Page Application (SPA) phát triển bằng Next.js + Tailwind CSS.
   - Tự động đính kèm Token xác thực qua Header: `Authorization: Bearer <token>`.
3. **Tầng 3 - API & Bảo mật phân tán:**
   - Cơ chế bảo mật phi tập trung (Decentralized JWT Security Filter): Từng microservice tự giải mã và thẩm định token HMAC-SHA256 mà không cần gọi ngược về Auth Service.
   - Kiểm soát truy cập RBAC, chặn lỗi chuẩn `401 Unauthorized` và `403 Forbidden`.
4. **Tầng 4 - Nghiệp vụ (Microservices):**
   - `Identity & Auth Service` (Port `8081` - Hoàng phụ trách 3.0đ): Đăng ký (BCrypt), Đăng nhập (JWT), Phân quyền RBAC.
   - `Pitch Service` (Port `8082` - Linh phụ trách 2.5đ): Quản lý sân, Validation `400 Bad Request`, Swagger UI.
   - `Booking Service` (Port `8083` - Nhật phụ trách 2.25đ): Tiếp nhận đặt sân, chống trùng lịch, gọi OpenFeign sang Pitch Service, xử lý lỗi `503 Service Unavailable`.
   - `Payment Sandbox` (Port `8084` - Hướng mở rộng): Kết nối cổng thanh toán VNPAY/MoMo.
5. **Tầng 5 - Quản trị CSDL phân tán (Database-per-Service - Hùng phụ trách 2.25đ):**
   - 3 Database MySQL độc lập: `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`.
   - **Tuyệt đối không có Foreign Key vật lý:** Liên kết dữ liệu hoàn toàn thông qua Logical ID kiểu số nguyên (`pitch_id`, `user_id`).
6. **Hạ tầng Container (Infrastructure):**
   - Docker & Docker Compose (`docker-compose.yml`) đóng gói toàn bộ dịch vụ và CSDL, khởi động đồng bộ với biến môi trường `.env`.

---

## 🔄 2. SƠ ĐỒ TUẦN TỰ LUỒNG ĐẶT SÂN & GIAO TIẾP DỊCH VỤ (SLIDE 12 / 12)

![Sơ đồ tuần tự Sequence Diagram](images/pitchos-sequence-diagram.png)

### 📌 Các bước xử lý trong luồng nghiệp vụ:
1. **Đăng nhập:** Client gửi `POST /api/v1/auth/login` sang Auth Service (:8081) nhận Bearer JWT Token.
2. **Tạo yêu cầu:** Client gửi `POST /api/v1/bookings` kèm token sang Booking Service (:8083).
3. **Kiểm tra chống trùng lịch:** Booking Service truy vấn `pitchos_booking_db` xác nhận khung giờ còn trống.
4. **Giao tiếp OpenFeign:** Booking Service gọi `GET /api/v1/pitches/{id}` sang Pitch Service (:8082) để lấy giá thuê và kiểm tra trạng thái hoạt động của sân.
5. **Khối ALT phòng thủ & phản hồi:**
   - *Nếu Pitch Service sập mạng:* Booking Service bắt ngoại lệ và trả về `503 Service Unavailable`.
   - *Nếu sân đang bảo trì:* Trả về `400 Bad Request`.
   - *Nếu bị tranh chấp khung giờ:* Trả về `409 Conflict`.
   - *Nếu hợp lệ:* Ghi nhận vào CSDL với trạng thái `cho_duyet` và trả về `201 Created`.

---

## 📑 3. DANH MỤC 12 SLIDE BẢO VỆ ĐỒ ÁN TRƯỚC HỘI ĐỒNG

| Slide | Tiêu đề slide | Nội dung trọng tâm | Thành viên trình bày chính |
| :---: | :--- | :--- | :---: |
| **01** | Bìa Mô hình Kiến trúc Tổng thể | Giới thiệu đề tài PitchOS, công nghệ SOA / Microservices, thông tin nhóm. | Cả nhóm |
| **02** | Tác nhân & Phân hệ Chức năng | Phân rã 3 vai trò: Khách hàng (User), Chủ sân (Chusan), Quản trị viên (Admin). | Hoàng |
| **03** | Mô hình Kiến trúc Tổng thể (Diagram) | Sơ đồ 5 tầng: Người dùng -> Frontend -> Security -> Microservices -> Database. | Cả nhóm |
| **04** | Vì sao chia thành các Microservices? | Luận giải Single Responsibility Principle (SRP), scale độc lập giữa Read và Write. | Linh |
| **05** | Các kiểu Giao tiếp & Mô hình Bảo mật | HTTP/REST, Spring Cloud OpenFeign, Spring Data JPA, JWT Bearer RBAC. | Nhật & Hoàng |
| **06** | Luồng Nghiệp vụ Đặt Sân từ A đến Z | Quy trình 6 bước chi tiết từ lúc khách tìm sân đến khi lưu đơn xuống đĩa cứng. | Nhật |
| **07** | Vòng đời & Quản lý Trạng thái Thực thể | Máy trạng thái đơn đặt (`cho_duyet` $\rightarrow$ `da_duyet` / `tu_choi` / `da_huy`) và sân bóng. | Hùng |
| **08** | Cơ chế Chống đặt trùng Khung giờ | Ràng buộc logic, query giao thoa thời gian và giải quyết tranh chấp đồng thời (Concurrency). | Hùng |
| **09** | Xử lý Lỗi & Khả năng Chịu lỗi | Danh mục mã HTTP lỗi chuẩn: 400 Validation, 401/403 Security, 404, 503 Fault Tolerance. | Linh & Nhật |
| **10** | Ma trận Phân công & Barem Điểm | Khớp nối 10.0 điểm theo đề cương của thầy: Hoàng (3.0đ), Linh (2.5đ), Hùng (2.25đ), Nhật (2.25đ). | Hoàng (Leader) |
| **11** | Kịch bản Demo Thực nghiệm 5 Bước | Khởi chạy -> Test REST API -> Test Giao tiếp 503 -> Test Ghi đĩa DB -> Test Bảo mật JWT. | Cả nhóm |
| **12** | Phụ lục: Sơ đồ Tuần tự Chi tiết | Sequence diagram chi tiết phục vụ giảng viên hỏi sâu về luồng kỹ thuật. | Nhật |
