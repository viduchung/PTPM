# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: NHẬT

> **HỌ VÀ TÊN:** NHẬT  
> **VAI TRÒ:** Phụ trách Giao tiếp liên dịch vụ, Sequence Diagram & Code Booking Service  
> **DỊCH VỤ PHỤ TRÁCH:** `pitchos-booking-service` (Cổng: **8083**)  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_booking_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,5 / 10,0 Điểm**  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 2**  
> **THỜI ĐIỂM BẮT ĐẦU:** **Giai đoạn 3** — Bắt đầu ngay sau khi Hoàng hoàn thành API `GET /api/v1/pitches/{id}` trên cổng 8082.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA NHẬT

### 📘 A. Phần Lý thuyết (1,0 Điểm - Câu 1 Ý 2a + phối hợp Ý 2b)
- [ ] **Trình bày quy trình giao tiếp HTTP/REST giữa các dịch vụ:**
  - Mô tả cách thức Booking Service gửi HTTP GET sang Pitch Service để lấy giá và trạng thái sân (`hoat_dong`).
  - Nhận và phân tích JSON response để hoàn tất nghiệp vụ tạo đơn.
- [ ] **Phân tích cấu trúc HTTP Request / Response & ý nghĩa các nhóm Status Code:**
  - Cấu trúc Request: Request Line, Headers (Authorization Bearer, Content-Type), Body (JSON).
  - Cấu trúc Response: Status Line, Response Headers, Response Body.
  - Các nhóm mã trạng thái:
    - `2xx`: Thành công (`200 OK`, `201 Created`).
    - `4xx`: Lỗi phía client (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).
    - `5xx`: Lỗi phía máy chủ (`500 Internal Server Error`, `503 Service Unavailable`).
- [ ] **Trình bày nguy cơ sụp đổ dây chuyền (Cascading Failure):**
  - Hiện tượng: Khi dịch vụ phụ thuộc (Pitch Service) bị chậm hoặc sập, dịch vụ gọi (Booking Service) bị nghẽn thread pool do chờ phản hồi, dẫn tới quá tải và sập toàn bộ hệ thống.
  - Biện pháp khắc phục: Cấu hình Timeout hợp lý, cơ chế Circuit Breaker, và bắt ngoại lệ mạng trả về ngay mã **503 Service Unavailable** để ngắt kết nối an toàn.

---

### 💻 B. Phần Thực nghiệm (1,5 Điểm - Câu 2 Ý 2)
- [ ] **Khởi tạo và lập trình `pitchos-booking-service` chạy trên Port 8083:**
  - Kết nối CSDL `pitchos_booking_db` do Hùng bàn giao.
  - Tạo Entity `Booking` và interface `BookingRepository` (sử dụng query chống trùng lịch của Hùng, loại trừ các đơn có trạng thái `tu_choi`).
- [ ] **Xây dựng đầy đủ 3 API nghiệp vụ chính:**
  1. `POST /api/v1/bookings`: Nhận yêu cầu đặt sân, kiểm tra khung giờ trống, gọi Feign sang Pitch Service lấy giá, tính tổng tiền, tạo đơn trạng thái `cho_duyet`.
  2. `GET /api/v1/bookings/my-bookings`: Truy vấn lịch sử đặt sân của người dùng thông qua Token JWT (role `user`).
  3. `PATCH /api/v1/bookings/{id}/status`: Chủ sân duyệt đơn (`da_duyet`) hoặc từ chối (`tu_choi`) (yêu cầu role `chusan` hoặc `admin`).
- [ ] **Tích hợp Spring Cloud OpenFeign gọi sang Pitch Service:**
  - Tạo `PitchClient` interface hướng đến `http://localhost:8082/api/v1/pitches/{id}`.
- [ ] **Lập trình tầng xử lý lỗi liên dịch vụ phân tán:**
  - **`CustomErrorDecoder`:** Bắt mã 404 từ Pitch Service khi khách truyền sai `pitchId`, ném lỗi rõ ràng.
  - **`GlobalExceptionHandler`:** Bắt `FeignException`, `RetryableException`, lỗi mất kết nối khi Pitch Service bị tắt, chuyển đổi mượt mà thành phản hồi **503 Service Unavailable** (hệ thống không bị văng 500 hay crash).
- [ ] **Vẽ sơ đồ tuần tự (Sequence Diagram):**
  - Mô tả đầy đủ luồng nghiệp vụ tạo đơn đặt sân (bao gồm nhánh thành công và nhánh Pitch Service offline).

---

### 📑 C. Phần Viết Báo cáo (Chương 2)
- [ ] **Biên soạn toàn bộ Chương 2:**
  - Thiết kế các API của Booking Service.
  - Giao tiếp liên dịch vụ qua giao thức HTTP/REST và Spring Cloud OpenFeign.
  - Sơ đồ tuần tự (Sequence Diagram) chuẩn kỹ thuật.
  - Cơ chế xử lý lỗi phân tán, ngăn chặn Cascading Failure (HTTP 503).

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Nhật trực tiếp thao tác)
- [ ] **Bước 1 (Thành công):** Gửi `POST /api/v1/bookings` đặt sân bằng Token của `user` $\rightarrow$ Chứng minh Booking Service tự động gọi sang Pitch Service (8082) lấy giá và tạo đơn với trạng thái `cho_duyet`, trả về **201 Created**.
- [ ] **Bước 2 (Kiểm tra CSDL):** Báo Hùng chạy SELECT để đối chiếu dữ liệu vừa tạo.
- [ ] **Bước 3 (Bắt lỗi phân tán 503 - ĐIỂM NHẤN CỦA NHẬT):**
  - **Tắt tiến trình của Pitch Service (Port 8082)**.
  - Gửi lại request đặt sân vào Booking Service (Port 8083).
  - Chứng minh Booking Service vẫn đứng vững, bắt được lỗi ngắt kết nối và trả về chuẩn xác mã **503 Service Unavailable**.
