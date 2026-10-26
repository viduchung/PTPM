# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: LINH

> **HỌ VÀ TÊN:** LINH  
> **VAI TRÒ:** Phụ trách Kiến trúc SOA, Chuẩn hóa RESTful API & Code Pitch Service  
> **DỊCH VỤ PHỤ TRÁCH:** `pitchos-pitch-service` (Cổng: **8082**)  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_pitch_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,5 / 10,0 Điểm** (1,5đ Lý thuyết + 1,0đ Thực nghiệm)  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 1**  
> **THỜI ĐIỂM BẮT ĐẦU:** **Giai đoạn 2 (Nhánh 2)** — Code song song với Hoàng ngay sau khi Hùng bàn giao CSDL.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA LINH (THEO ĐÚNG ĐỀ BÀI)

### 📘 A. Phần Lý thuyết (1,5 Điểm — Câu 1 Ý 1)
- [ ] **Câu 1 - Ý 1a (0,5 Điểm): Trình bày các đặc điểm chính của kiến trúc SOA & Phân biệt các khái niệm cốt lõi:**
  - *4 đặc tính cơ bản của SOA:*
    1. **Liên kết lỏng (Loose Coupling):** Các dịch vụ duy trì mức độ phụ thuộc tối thiểu vào nhau, có thể thay đổi bên trong mà không phá vỡ client.
    2. **Hợp đồng chuẩn hóa (Standardized Service Contract):** Các dịch vụ công bố giao diện rõ ràng qua HTTP/REST, chuẩn JSON và tài liệu OpenAPI.
    3. **Tính trừu tượng (Abstraction):** Che giấu toàn bộ chi tiết cài đặt nghiệp vụ và công nghệ nội bộ bên trong dịch vụ.
    4. **Khả năng tái sử dụng (Reusability):** Một dịch vụ độc lập có thể phục vụ nhiều loại ứng dụng khách hoặc dịch vụ khác nhau.
  - *Phân biệt rõ 3 khái niệm cốt lõi:*
    - **Dịch vụ (Service):** Thành phần phần mềm độc lập xử lý nghiệp vụ quản lý sân bóng mini (Pitch Service).
    - **Giao diện lập trình (API):** Cổng kết nối kỹ thuật (Endpoints, HTTP methods, Request/Response payload).
    - **Ứng dụng khách (Client):** Ứng dụng web, mobile hoặc Booking Service đóng vai trò client gọi sang Pitch Service.
- [ ] **Câu 1 - Ý 1b (1,0 Điểm): Danh mục dịch vụ PitchOS, 03 API tiêu biểu & Nguyên lý SRP:**
  - *Xác định các dịch vụ chính & trách nhiệm:*
    1. **Auth Service (Port 8081):** Quản lý tài khoản, mã hóa mật khẩu, cấp phát và giải mã JWT token.
    2. **Pitch Service (Port 8082):** Quản lý thông tin sân bóng, bảng giá theo giờ, trạng thái hoạt động/bảo trì.
    3. **Booking Service (Port 8083):** Quản lý quy trình đặt sân, kiểm tra khung giờ trống, tính tổng tiền, điều phối trạng thái đơn.
  - *03 API tiêu biểu phục vụ nghiệp vụ chính:*
    1. `POST /api/v1/auth/login`: Xác thực danh tính và cấp phát token JWT.
    2. `GET /api/v1/pitches/{id}`: Tra cứu đơn giá và kiểm tra trạng thái hoạt động của sân.
    3. `POST /api/v1/bookings`: Tạo đơn đặt sân và điều phối nghiệp vụ liên dịch vụ.
  - *Giải thích phân chia hệ thống theo nguyên lý Đơn trách nhiệm (Single Responsibility Principle - SRP):*
    - Mỗi dịch vụ chỉ chịu một trách nhiệm nghiệp vụ duy nhất. Pitch Service chỉ chuyên tâm quản lý danh mục và cấu hình sân bóng, không can thiệp vào tài khoản hay đơn đặt sân, giúp dịch vụ phát triển và kiểm thử độc lập.

---

### 💻 B. Phần Thực nghiệm (1,0 Điểm — Câu 2 Ý 1)
- [ ] **Khởi tạo và lập trình `pitchos-pitch-service` chạy trên Port 8082:**
  - Kết nối CSDL `pitchos_pitch_db` do Hùng bàn giao.
  - Tạo Entity `Pitch` và `PitchRepository` kế thừa `JpaRepository`:
    - Các trường: `id`, `name` (tên sân), `pitchType` (`san_5`, `san_7`, `san_10`), `pricePerHour` (đơn giá), `address` (địa chỉ), `thumbnailUrl` (ảnh), `googleMapUrl` (link bản đồ), `status` (`hoat_dong`, `bao_tri`).
- [ ] **Xây dựng đầy đủ 4 RESTful API có cấu trúc URL rõ ràng:**
  1. `GET /api/v1/pitches`: Lấy danh sách sân công khai (kèm lọc theo `pitchType`: `san_5`, `san_7`, `san_10`).
  2. `GET /api/v1/pitches/{id}`: Lấy chi tiết sân bóng (đơn giá, cấu hình, trạng thái `hoat_dong`) — **Bàn giao endpoint này cho Nhật gọi FeignClient**.
  3. `POST /api/v1/pitches`: Thêm sân mới (yêu cầu role `chusan` hoặc `admin`).
  4. `PATCH /api/v1/pitches/{id}/status`: Cập nhật trạng thái sân (`hoat_dong` hoặc `bao_tri`).
- [ ] **Cài đặt kiểm tra dữ liệu đầu vào (Validation) & Bắt lỗi 400 Bad Request:**
  - Áp dụng **Jakarta Validation** trên DTO:
    - `@NotBlank(message = "Tên sân bóng không được để trống")`
    - `@NotNull(message = "Loại sân không được để trống")`
    - `@Positive(message = "Đơn giá thuê mỗi giờ phải lớn hơn 0")`
    - `@NotBlank(message = "Địa chỉ sân không được để trống")`
  - Viết `GlobalExceptionHandler` bắt ngoại lệ `MethodArgumentNotValidException` và trả về chuẩn phản hồi **400 Bad Request** với chi tiết lỗi rõ ràng.
- [ ] **Tích hợp tài liệu OpenAPI / Swagger UI:**
  - Cấu hình thư viện `springdoc-openapi-starter-webmvc-ui`.
  - Kiểm tra giao diện Swagger UI trực quan tại `http://localhost:8082/swagger-ui.html`.
- [ ] **Tích hợp bảo mật (Giai đoạn 4 - Nhận cấu hình từ Hoàng):**
  - Tích hợp `JwtAuthenticationFilter` và cấu hình phân quyền: Cho phép public `GET`, chặn `POST`/`PATCH` nếu không phải role `chusan` hoặc `admin`.

---

### 📑 C. Phần Viết Báo cáo (Chương 1)
- [ ] **Biên soạn toàn bộ Chương 1 (Giới thiệu đề tài và kiến trúc dịch vụ):**
  - Mô tả bài toán nghiệp vụ đặt sân bóng mini trực tuyến.
  - Sơ đồ kiến trúc tổng thể của hệ thống PitchOS theo mô hình SOA.
  - Phân rã dịch vụ, trách nhiệm nghiệp vụ từng service và luận giải theo SRP.
  - Bảng danh mục và tài liệu đặc tả đầy đủ các RESTful API của Pitch Service.

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Linh trực tiếp thao tác)
- [ ] **Bước 1:** Mở Swagger UI tại địa chỉ `http://localhost:8082/swagger-ui.html` hoặc mở Postman.
- [ ] **Bước 2 (Thành công - 200 OK):** Gửi request `GET /api/v1/pitches` $\rightarrow$ Nhận danh sách sân với mã `200 OK`.
- [ ] **Bước 3 (Thành công - 201 Created):** Sử dụng token của `chusan` gửi request `POST /api/v1/pitches` với đầy đủ thông tin hợp lệ $\rightarrow$ Nhận mã `201 Created`.
- [ ] **Bước 4 (Validation - 400 Bad Request):** Gửi request `POST /api/v1/pitches` với tên để trống, giá âm `-500000`, địa chỉ rỗng $\rightarrow$ Chứng minh hệ thống chặn lại và trả về chuẩn mã lỗi **400 Bad Request** với thông báo lỗi chi tiết.
- [ ] **Bước 5 (Phối hợp với Hoàng):** Sử dụng token của `user` gửi request tạo sân $\rightarrow$ Chứng minh nhận mã lỗi **403 Forbidden**.
