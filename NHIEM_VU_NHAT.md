# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: NHẬT

> **HỌ VÀ TÊN:** NHẬT  
> **VAI TRÒ:** Phụ trách Giao tiếp liên dịch vụ, Sequence Diagram & Code Booking Service  
> **DỊCH VỤ PHỤ TRÁCH:** `pitchos-booking-service` (Cổng: **8083**)  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_booking_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,25 / 10,0 Điểm** (0,75đ Lý thuyết + 1,5đ Thực nghiệm)  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 2** (Thiết kế API, giao tiếp liên dịch vụ, Sequence Diagram, cơ chế chịu lỗi phân tán)  
> **THỜI ĐIỂM BẮT ĐẦU:** **GIAI ĐOẠN 3** — Bắt đầu ngay sau khi Linh hoàn thành API `GET /api/v1/pitches/{id}` trên cổng 8082.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA NHẬT (THEO ĐÚNG ĐỀ BÀI)

### 📘 A. Phần Lý thuyết (0,75 Điểm — Câu 1 Ý 2a)
- [ ] **Mô tả quy trình giao tiếp giữa hai dịch vụ trong một nghiệp vụ cụ thể:**
  - Lấy ví dụ nghiệp vụ *"Khách hàng tạo đơn đặt sân bóng"*:
    1. Booking Service tiếp nhận request đặt sân chứa `pitchId`, `startTime`, `endTime`.
    2. Booking Service đóng vai trò Client, gửi HTTP GET sang Pitch Service (`GET /api/v1/pitches/{id}`) để tra cứu đơn giá (`pricePerHour`) và kiểm tra trạng thái sân (`hoat_dong`).
    3. Pitch Service phản hồi JSON thông tin sân.
    4. Booking Service tính toán tổng tiền (`totalPrice = số giờ * pricePerHour`) và lưu đơn vào CSDL của mình.
- [ ] **Làm rõ vai trò của HTTP/REST, Request, Response và Mã trạng thái HTTP:**
  - *HTTP/REST:* Giao thức truyền thông đồng bộ phi trạng thái (Stateless), sử dụng định dạng JSON tiêu chuẩn trao đổi dữ liệu qua mạng.
  - *Cấu trúc HTTP Request:* Request Line (Method POST/GET, URI), Headers (`Authorization: Bearer <token>`, `Content-Type: application/json`), Body (JSON dữ liệu).
  - *Cấu trúc HTTP Response:* Status Line (HTTP Version, Status Code), Response Headers, Response Body.
  - *Ý nghĩa các nhóm mã trạng thái HTTP:*
    - `2xx` (Thành công): `200 OK` (Truy vấn thành công), `201 Created` (Tạo tài nguyên mới thành công).
    - `4xx` (Lỗi phía client): `400 Bad Request` (Dữ liệu sai quy chuẩn), `401 Unauthorized` (Chưa xác thực), `403 Forbidden` (Sai quyền hạn), `404 Not Found` (Không tìm thấy tài nguyên).
    - `5xx` (Lỗi phía server): `500 Internal Server Error` (Lỗi nội bộ), `503 Service Unavailable` (Dịch vụ tạm thời không khả dụng).
- [ ] **Phân tích nguy cơ sụp đổ dây chuyền (Cascading Failure) & Giải pháp:**
  - Hiện tượng: Khi dịch vụ phụ thuộc (Pitch Service) bị chậm hoặc sập, Booking Service gọi sang sẽ bị treo các luồng xử lý (thread pool starvation), dẫn đến việc Booking Service cũng bị nghẽn và sập theo.
  - Giải pháp: Cấu hình Timeout và viết bộ xử lý ngoại lệ mạng để ngắt kết nối an toàn, chuyển đổi thành mã chuẩn **503 Service Unavailable** trả về cho client mà không làm crash hệ thống.

---

### 💻 B. Phần Thực nghiệm (1,5 Điểm — Câu 2 Ý 2)
- [ ] **Khởi tạo và lập trình `pitchos-booking-service` chạy trên Port 8083:**
  - Kết nối CSDL `pitchos_booking_db` do Hùng bàn giao.
  - Tạo Entity `Booking` và `BookingRepository` (tích hợp câu truy vấn chống trùng lịch do Hùng thiết kế).
- [ ] **Xây dựng đầy đủ 3 API nghiệp vụ chính:**
  1. `POST /api/v1/bookings`: Nhận yêu cầu đặt sân, kiểm tra trùng lịch, gọi sang Pitch Service lấy giá, tính tổng tiền, tạo đơn với trạng thái `cho_duyet`.
  2. `GET /api/v1/bookings/my-bookings`: Truy vấn danh sách đơn đặt của khách hàng hiện tại trích xuất từ JWT Token (role `user`).
  3. `PATCH /api/v1/bookings/{id}/status`: Chủ sân duyệt đơn (`da_duyet`) hoặc từ chối (`tu_choi`) (yêu cầu role `chusan` hoặc `admin`).
- [ ] **Giao tiếp liên dịch vụ với Spring Cloud OpenFeign:**
  - Kích hoạt `@EnableFeignClients`.
  - Khai báo Feign Client gọi sang Pitch Service:
    ```java
    @FeignClient(name = "pitch-service", url = "${pitch.service.url:http://localhost:8082}")
    public interface PitchClient {
        @GetMapping("/api/v1/pitches/{id}")
        PitchResponseDTO getPitchById(@PathVariable("id") Long id);
    }
    ```
- [ ] **Xử lý ít nhất một tình huống lỗi giao tiếp phân tán:**
  - **Tình huống 1 (Tài nguyên không tồn tại - 404):** Cấu hình `CustomErrorDecoder` bắt mã 404 từ Pitch Service khi khách truyền `pitchId` không có thực, ném ngoại lệ rõ ràng cho client.
  - **Tình huống 2 (Dịch vụ đích không khả dụng - 503):** Viết `GlobalExceptionHandler` (`@RestControllerAdvice`) bắt các ngoại lệ mạng `FeignException`, `RetryableException` (khi Pitch Service bị tắt tiến trình), chuyển đổi an toàn thành mã chuẩn **503 Service Unavailable**:
    ```json
    {
      "timestamp": "2026-10-26T21:00:00",
      "status": 503,
      "error": "Service Unavailable",
      "message": "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!"
    }
    ```
- [ ] **Vẽ sơ đồ tuần tự (Sequence Diagram):**
  - Vẽ sơ đồ tuần tự thể hiện rõ luồng bình thường và luồng chịu lỗi khi Pitch Service offline.
- [ ] **Tích hợp bảo mật (Giai đoạn 4 - Nhận từ Hoàng):**
  - Tích hợp `JwtAuthenticationFilter` phân quyền: `POST` và `GET /my-bookings` dành cho `user`; `PATCH status` dành cho `chusan` và `admin`.

---

### 📑 C. Phần Viết Báo cáo (Chương 2)
- [ ] **Biên soạn toàn bộ Chương 2 (Thiết kế API và giao tiếp dịch vụ):**
  - Danh sách endpoints, cấu trúc Request / Response, phương thức HTTP và mã trạng thái.
  - Thiết kế giao tiếp liên dịch vụ qua OpenFeign Client.
  - Sơ đồ tuần tự (Sequence Diagram) chuẩn kỹ thuật.
  - Phân tích cơ chế xử lý lỗi phân tán và ngăn chặn Cascading Failure (503 Service Unavailable).

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Nhật trực tiếp thao tác)
- [ ] **Bước 1 (Thành công - 201 Created):**
  - Dùng token của `user` gửi request `POST /api/v1/bookings` đặt sân hợp lệ.
  - Chứng minh Booking Service tự động gọi OpenFeign sang Pitch Service (8082) lấy đơn giá 300.000đ, tính tổng tiền thành công và tạo đơn trạng thái `cho_duyet`, trả về mã **201 Created**.
- [ ] **Bước 2 (Kiểm tra CSDL):** Báo Hùng chạy lệnh `SELECT` để kiểm chứng đơn đã lưu vào `pitchos_booking_db`.
- [ ] **Bước 3 (Bắt lỗi phân tán 503 - ĐIỂM NHẤN CỦA NHẬT):**
  - **Tắt tiến trình của Pitch Service (Port 8082)** trước mặt giảng viên.
  - Gửi lại request đặt sân vào Booking Service (Port 8083).
  - **Kết quả kiểm chứng:** Booking Service không bị sập hay báo lỗi 500, mà bắt được lỗi mạng và trả về đúng chuẩn mã **503 Service Unavailable** kèm thông báo thân thiện.
