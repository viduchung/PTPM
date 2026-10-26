# Nhiệm vụ: Hoàng — RESTful API, Validation & Pitch Service

- **Vai trò:** API Designer & Backend Pitch Engineer
- **Tổng điểm phụ trách:** **2,5 Điểm** (1,5đ Lý thuyết + 1,0đ Thực nghiệm)
- **Cổng dịch vụ (Port):** `8082`
- **Cơ sở dữ liệu:** `pitchos_pitch_db`
- **Báo cáo phụ trách:** **Chương 1** (Mô tả bài toán, sơ đồ kiến trúc hệ thống, phân rã dịch vụ, danh sách API)
- **Thứ tự thực hiện:** **GIAI ĐOẠN 2 (NHÁNH 2)** — Code song song với Linh sau khi Hùng bàn giao CSDL.

---

## 📚 1. Yêu cầu Lý thuyết (1,5 Điểm - Câu 1 Ý 1)

- [ ] **Nêu và giải thích 4 đặc tính cơ bản của SOA:**
  1. **Liên kết lỏng (Loose Coupling):** Các dịch vụ duy trì mức độ phụ thuộc tối thiểu vào nhau.
  2. **Hợp đồng chuẩn hóa (Standardized Service Contract):** Giao tiếp qua chuẩn RESTful API, JSON format.
  3. **Tính trừu tượng (Abstraction):** Che giấu toàn bộ chi tiết cài đặt nghiệp vụ bên trong.
  4. **Khả năng tái sử dụng (Reusability):** Dịch vụ độc lập phục vụ nhiều client khác nhau.
- [ ] **Phân biệt rõ ràng 3 khái niệm cốt lõi:**
  - **Dịch vụ (Service):** Thành phần xử lý nghiệp vụ sân bóng (Pitch Service).
  - **Giao diện lập trình (API):** Hợp đồng kỹ thuật (Endpoints, HTTP methods, payload).
  - **Ứng dụng khách (Client):** Ứng dụng web, mobile hoặc Booking Service.
- [ ] **Danh mục dịch vụ của PitchOS, 03 API tiêu biểu và luận giải theo nguyên lý SRP:**
  - Danh mục: Auth Service (8081), Pitch Service (8082), Booking Service (8083).
  - 03 API tiêu biểu: `POST /api/v1/auth/login`, `GET /api/v1/pitches/{id}`, `POST /api/v1/bookings`.
  - Luận giải nguyên lý Đơn trách nhiệm (SRP): Pitch Service chỉ chuyên trách quản lý thông tin, cấu hình, trạng thái sân bóng.

---

## 🛠️ 2. Yêu cầu Thực nghiệm (1,0 Điểm - Câu 2 Ý 1)

### 2.1. Xây dựng toàn bộ Pitch Service (Port 8082)
- **Thực thể `Pitch` & `PitchRepository`:** Kế thừa `JpaRepository`.
  - Cấu trúc: `name`, `pitchType` (`san_5`, `san_7`, `san_10`), `pricePerHour`, `address`, `thumbnailUrl`, `googleMapUrl`, `status` (`hoat_dong`, `bao_tri`).
- **Xây dựng các Endpoints chuẩn RESTful:**
  - `GET /api/v1/pitches`: Lấy danh sách sân công khai (kèm lọc `pitchType`: `san_5`, `san_7`, `san_10`).
  - `GET /api/v1/pitches/{id}`: Lấy chi tiết sân (đơn giá, cấu hình, trạng thái `hoat_dong`) — **Endpoint cho Booking Service gọi**.
  - `POST /api/v1/pitches`: Thêm sân mới (yêu cầu role `chusan` hoặc `admin`).
  - `PATCH /api/v1/pitches/{id}/status`: Cập nhật trạng thái sân (`hoat_dong` hoặc `bao_tri`).

### 2.2. Kiểm tra dữ liệu đầu vào (Validation) & Xử lý ngoại lệ 400
- Sử dụng **Jakarta Validation** trên DTO:
  - `@NotBlank(message = "Tên sân không được để trống")`
  - `@Positive(message = "Giá thuê sân phải lớn hơn 0")`
  - `@NotBlank(message = "Địa chỉ sân không được để trống")`
- Viết `GlobalExceptionHandler` bắt `MethodArgumentNotValidException` và trả về chuẩn **400 Bad Request**.

### 2.3. Tích hợp OpenAPI / Swagger UI
- Tích hợp dependency `springdoc-openapi-starter-webmvc-ui`.
- Truy cập Swagger UI tại `http://localhost:8082/swagger-ui.html`.

### 2.4. Tích hợp bảo mật phân quyền (Giai đoạn 4)
- Tích hợp `JwtAuthenticationFilter` (Linh chia sẻ).
- Phân quyền:
  - `GET /api/v1/pitches/**` $\rightarrow$ `permitAll()`
  - `POST /api/v1/pitches` và `PATCH /api/v1/pitches/**` $\rightarrow$ `chusan`, `admin`.
  - Trả về **401** nếu thiếu token và **403** nếu dùng token `user`.

---

## 📝 3. Viết Báo cáo: Soạn Chương 1
- Tổng quan bài toán đặt sân bóng đá mini và kiến trúc SOA.
- Sơ đồ kiến trúc tổng thể của hệ thống PitchOS.
- Nguyên tắc phân rã dịch vụ theo nghiệp vụ và SRP.
- Danh mục và tài liệu đặc tả các RESTful APIs của Pitch Service.

---

## 🎥 4. Kịch bản Demo Hội đồng (10–15 Phút)
1. Mở Swagger UI trên cổng 8082.
2. Gửi request `GET /api/v1/pitches` $\rightarrow$ nhận danh sách sân (mã `200 OK`).
3. Gửi request `POST /api/v1/pitches` với thông tin hợp lệ (token `chusan`) $\rightarrow$ nhận `201 Created`.
4. Gửi request `POST /api/v1/pitches` với tên để trống hoặc giá âm $\rightarrow$ Chứng minh bắt lỗi **400 Bad Request**.
