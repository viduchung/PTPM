# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: HOÀNG

> **HỌ VÀ TÊN:** HOÀNG  
> **VAI TRÒ:** Phụ trách Kiến trúc SOA, Chuẩn hóa RESTful API & Code Pitch Service  
> **DỊCH VỤ PHỤ TRÁCH:** `pitchos-pitch-service` (Cổng: **8082**)  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_pitch_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,5 / 10,0 Điểm**  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 1**  
> **THỜI ĐIỂM BẮT ĐẦU:** **Giai đoạn 2 (Nhánh 2)** — Code song song với Linh ngay sau khi Hùng bàn giao CSDL.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA HOÀNG

### 📘 A. Phần Lý thuyết (1,5 Điểm - Câu 1 Ý 1)
- [ ] **Nêu 4 đặc tính cơ bản của kiến trúc hướng dịch vụ (SOA):**
  1. *Liên kết lỏng (Loose Coupling):* Các dịch vụ giảm thiểu tối đa sự phụ thuộc trực tiếp vào nhau.
  2. *Hợp đồng chuẩn hóa (Standardized Contract):* Giao tiếp qua chuẩn RESTful, JSON, OpenAPI spec.
  3. *Tính trừu tượng (Abstraction):* Giấu kín logic xử lý và công nghệ cài đặt bên trong dịch vụ.
  4. *Khả năng tái sử dụng (Reusability):* Dịch vụ có thể phục vụ nhiều ứng dụng khách hoặc dịch vụ khác.
- [ ] **Phân biệt rõ ràng 3 khái niệm:**
  - *Dịch vụ (Service):* Thành phần phần mềm độc lập xử lý nghiệp vụ sân bóng (Pitch Service).
  - *Giao diện lập trình (API):* Cổng kết nối kỹ thuật (Endpoints, HTTP methods, Request/Response format).
  - *Ứng dụng khách (Client):* Web app, mobile app hoặc dịch vụ Booking Service gọi sang.
- [ ] **Trình bày danh mục dịch vụ PitchOS & 03 API tiêu biểu:**
  - Danh mục: Auth Service (8081), Pitch Service (8082), Booking Service (8083).
  - 03 API tiêu biểu: `POST /api/v1/auth/login`, `GET /api/v1/pitches/{id}`, `POST /api/v1/bookings`.
  - Luận giải nguyên lý Đơn trách nhiệm (Single Responsibility Principle - SRP): Pitch Service chỉ chịu trách nhiệm duy nhất về thông số, trạng thái và giá cả sân bóng.

---

### 💻 B. Phần Thực nghiệm (1,0 Điểm - Câu 2 Ý 1)
- [ ] **Khởi tạo và lập trình `pitchos-pitch-service` chạy trên Port 8082:**
  - Kết nối CSDL `pitchos_pitch_db` do Hùng bàn giao.
  - Tạo Entity `Pitch` đầy đủ các trường:
    - `name` (tên sân)
    - `pitchType` (loại sân: `san_5`, `san_7`, `san_10`)
    - `pricePerHour` (giá thuê)
    - `address` (địa chỉ)
    - `thumbnailUrl` (link ảnh thumbnail)
    - `googleMapUrl` (link Google Map)
    - `status` (`hoat_dong`, `bao_tri`)
  - Tạo interface `PitchRepository` kế thừa `JpaRepository`.
- [ ] **Xây dựng đầy đủ 4 RESTful API:**
  1. `GET /api/v1/pitches`: Lấy danh sách sân công khai (kèm lọc theo `pitchType` như `san_5`, `san_7`, `san_10`).
  2. `GET /api/v1/pitches/{id}`: Lấy chi tiết sân (đơn giá, cấu hình, trạng thái `hoat_dong`) — **Bàn giao endpoint này cho Nhật gọi FeignClient**.
  3. `POST /api/v1/pitches`: Thêm sân mới (yêu cầu role `chusan` hoặc `admin`).
  4. `PATCH /api/v1/pitches/{id}/status`: Cập nhật trạng thái sân (`hoat_dong` hoặc `bao_tri`).
- [ ] **Cài đặt kiểm tra dữ liệu đầu vào (Validation) & Bắt lỗi 400 Bad Request:**
  - Áp dụng Jakarta Validation trên DTO: `@NotBlank`, `@Positive`, `@NotNull`.
  - Viết `GlobalExceptionHandler` bắt `MethodArgumentNotValidException` trả về chuẩn mã **400 Bad Request**.
- [ ] **Tích hợp tài liệu OpenAPI / Swagger UI:**
  - Truy cập được Swagger UI tại `http://localhost:8082/swagger-ui.html`.
- [ ] **Tích hợp bảo mật (Giai đoạn 4 - Nhận từ Linh):**
  - Cấu hình `SecurityFilterChain`: Cho phép public `GET /api/v1/pitches/**`, chặn `POST`/`PATCH` nếu không phải role `chusan` hoặc `admin`.

---

### 📑 C. Phần Viết Báo cáo (Chương 1)
- [ ] **Biên soạn toàn bộ Chương 1:**
  - Mô tả bài toán nghiệp vụ quản lý sân bóng mini.
  - Sơ đồ kiến trúc tổng quan hệ thống SOA PitchOS.
  - Phân rã dịch vụ và luận giải tính độc lập theo SRP.
  - Bảng danh sách và tài liệu đặc tả RESTful API của Pitch Service.

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Hoàng trực tiếp thao tác)
- [ ] **Bước 1:** Mở Swagger UI (`http://localhost:8082/swagger-ui.html`) hoặc Postman.
- [ ] **Bước 2 (Thành công):** Gửi `GET /api/v1/pitches` $\rightarrow$ Nhận danh sách sân với trạng thái `hoat_dong` (mã `200 OK`).
- [ ] **Bước 3 (Thành công):** Dùng token của `chusan` gửi `POST /api/v1/pitches` dữ liệu hợp lệ $\rightarrow$ Nhận mã `201 Created`.
- [ ] **Bước 4 (Validation 400):** Gửi `POST /api/v1/pitches` với tên sân để trống hoặc giá âm $\rightarrow$ Chứng minh hệ thống chặn lại và trả về mã lỗi **400 Bad Request** với thông báo rõ ràng.
- [ ] **Bước 5 (Phối hợp với Linh):** Dùng token của `user` thêm sân $\rightarrow$ Chứng minh nhận mã lỗi **403 Forbidden**.
