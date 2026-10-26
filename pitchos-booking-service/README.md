# Nhiệm vụ: Nhật — Giao tiếp Liên dịch vụ, Sequence Diagram & Booking Service

- **Vai trò:** Integration Specialist & Backend Booking Engineer
- **Tổng điểm phụ trách:** **2,25 / 10,0 Điểm** (0,75đ Lý thuyết + 1,5đ Thực nghiệm)
- **Cổng dịch vụ (Port):** `8083`
- **Cơ sở dữ liệu:** `pitchos_booking_db`
- **Báo cáo phụ trách:** **Chương 2** (Thiết kế API, giao tiếp liên dịch vụ, Sequence Diagram, cơ chế xử lý lỗi phân tán)
- **Thứ tự thực hiện:** **GIAI ĐOẠN 3** — Code sau khi Linh hoàn thiện `GET /api/v1/pitches/{id}` trên cổng 8082.

---

## 📚 1. Yêu cầu Lý thuyết (0,75 Điểm — Câu 1 Ý 2a)

- [ ] **Quy trình giao tiếp HTTP/REST giữa Booking Service và Pitch Service:**
  - Booking Service đóng vai trò Client sử dụng OpenFeign gửi HTTP GET tra cứu thông tin sân sang Pitch Service (`GET /api/v1/pitches/{id}`).
  - Kiểm tra trạng thái sân (`hoat_dong`) và đơn giá thuê (`pricePerHour`) để tính tổng tiền.
- [ ] **Phân tích cấu trúc HTTP Request / Response và ý nghĩa các nhóm HTTP Status Code:**
  - HTTP Request (Method, URI, Headers, Body), HTTP Response (Status Line, Headers, Body).
  - Các nhóm mã trạng thái:
    - `2xx` (Thành công: `200 OK`, `201 Created`).
    - `4xx` (Lỗi client: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).
    - `5xx` (Lỗi server: `500 Internal Server Error`, `503 Service Unavailable`).
- [ ] **Nguy cơ sụp đổ dây chuyền (Cascading Failure):**
  - Hiện tượng thread pool bị nghẽn khi Pitch Service chậm hoặc sập.
  - Giải pháp timeout và chuyển đổi ngoại lệ mạng sang mã **503 Service Unavailable**.

---

## 🛠️ 2. Yêu cầu Thực nghiệm (1,5 Điểm — Câu 2 Ý 2)

### 2.1. Xây dựng nghiệp vụ chính tại Booking Service (Port 8083)
- **Thực thể `Booking` & `BookingRepository`:**
  - Lưu `userId`, `pitchId` (dạng `Long`, không tạo khóa ngoại Foreign Key vật lý).
  - Áp dụng truy vấn chống trùng lịch thi đấu từ Hùng (`startTime < :endTime AND endTime > :startTime`, loại trừ đơn có trạng thái `tu_choi`).
- **Các Endpoints chính:**
  - `POST /api/v1/bookings`: Tiếp nhận yêu cầu đặt sân, kiểm tra khung giờ trống, gọi sang Pitch Service lấy giá, tính tổng tiền, tạo đơn với trạng thái `cho_duyet`.
  - `GET /api/v1/bookings/my-bookings`: Truy vấn lịch sử đặt chỗ của khách hàng trích xuất từ Token JWT (role `user`).
  - `PATCH /api/v1/bookings/{id}/status`: Chủ sân duyệt đơn (`da_duyet`) hoặc từ chối (`tu_choi`) (role `chusan` hoặc `admin`).

### 2.2. Giao tiếp liên dịch vụ với Spring Cloud OpenFeign
- Kích hoạt `@EnableFeignClients`.
- Định nghĩa Client interface gọi sang Pitch Service:
  ```java
  @FeignClient(name = "pitch-service", url = "${pitch.service.url:http://localhost:8082}")
  public interface PitchClient {
      @GetMapping("/api/v1/pitches/{id}")
      PitchResponseDTO getPitchById(@PathVariable("id") Long id);
  }
  ```

### 2.3. Lập trình tầng xử lý lỗi liên dịch vụ phân tán
- **Cấu hình `CustomErrorDecoder`:** Bắt mã `404 Not Found` từ Pitch Service khi khách truyền `pitchId` không tồn tại.
- **Cấu hình `GlobalExceptionHandler` (`@RestControllerAdvice`):**
  - Bắt lỗi mất kết nối, timeout mạng khi Pitch Service bị ngắt (`FeignException`, `RetryableException`).
  - Chuyển đổi an toàn thành mã phản hồi **503 Service Unavailable**:
    ```json
    {
      "timestamp": "2026-10-26T21:00:00",
      "status": 503,
      "error": "Service Unavailable",
      "message": "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!"
    }
    ```

### 2.4. Vẽ sơ đồ tuần tự (Sequence Diagram)
- Mô tả chi tiết luồng nghiệp vụ tạo đơn đặt chỗ và kịch bản bắt lỗi 503 khi Pitch Service bị tắt.

---

## 📝 3. Viết Báo cáo: Soạn Chương 2
- Thiết kế các API đặt sân và điều phối nghiệp vụ.
- Giao tiếp liên dịch vụ qua OpenFeign và Sequence Diagram.
- Cơ chế xử lý lỗi phân tán, phòng chống Cascading Failure (503 Service Unavailable).

---

## 🎥 4. Kịch bản Demo Hội đồng (10–15 Phút)
1. **Ca 1 (Thành công - 201 Created):**
   - Đặt sân thành công với token `user`, tạo đơn với trạng thái `cho_duyet`.
2. **Ca 2 (Sập dịch vụ phân tán - 503 Service Unavailable):**
   - **Tắt tiến trình Pitch Service (Port 8082)**.
   - Gửi lại request đặt sân vào Booking Service (Port 8083).
   - Chứng minh Booking Service bắt lỗi an toàn và trả về mã chuẩn **503 Service Unavailable**.
