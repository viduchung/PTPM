# ⚡ BẢNG NHIỆM VỤ CÁ NHÂN: NHẬT — BÀI KIỂM TRA SỐ 2 (TX2)
## HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ (SOA / MICROSERVICES 2026)
### ĐỀ TÀI: HỆ THỐNG ĐẶT SÂN BÓNG TRỰC TUYẾN — PITCHOS

> **HỌ VÀ TÊN:** NHẬT  
> **VAI TRÒ:** Kỹ sư Tích hợp Dịch vụ & Consumer Booking Service  
> **VÙNG MÃ NGUỒN SỞ HỮU:** `pitchos-booking-service/`, `postman/collection.json`  
> **TRỌNG SỐ ĐÁNH GIÁ:** **10,0 / 10,0 Điểm** (60% Điểm nhóm Báo cáo + Mã nguồn, 40% Điểm cá nhân qua Video demo độc lập)  
> **THỜI HẠN THỰC HIỆN:** 01 tuần (Theo kế hoạch tại `KE_HOACH_KIEM_TRA_2.md`)

---

## 🎯 1. BAREM ĐIỂM & ĐẦU VIỆC CHI TIẾT CỦA NHẬT

### 📘 A. Phần Lý thuyết Báo cáo (0,5 Điểm — Câu 1 Ý 1.1)
*Viết vào file `docs/kt2/CAU1_1_NHAT.md` để sau này gộp vào Báo cáo chính.*
- [ ] **Phân biệt Provider Service và Consumer Service trong kiến trúc hướng dịch vụ (SOA / Microservices):**
  - *Provider Service (Dịch vụ cung cấp):* Là dịch vụ sở hữu dữ liệu nghiệp vụ gốc (Data Ownership) và công bố các giao diện API (Endpoints) công khai cùng hợp đồng giao tiếp (API Contract) cho các hệ thống khác sử dụng. Trong PitchOS: `pitchos-pitch-service` là Provider quản lý thông tin sân, bảng giá và trạng thái sân.
  - *Consumer Service (Dịch vụ tiêu thụ):* Là dịch vụ gửi yêu cầu (Request) gọi đến API của Provider trong **mã nguồn nghiệp vụ của chính nó** để lấy dữ liệu hoặc kích hoạt xử lý cần thiết nhằm hoàn thành luồng nghiệp vụ của mình. Trong PitchOS: `pitchos-booking-service` là Consumer gọi sang Pitch để lấy đơn giá và tính tiền đặt sân.
- [ ] **Trình bày các bước cơ bản khi một Consumer gọi một API của Provider:**
  1. *Tiếp nhận & Xác thực:* Consumer nhận request từ Client (kèm JWT Token), giải mã kiểm tra tính hợp lệ của người dùng.
  2. *Kiểm tra dữ liệu đầu vào (Validation):* Kiểm tra tính hợp lệ của tham số gửi lên (ví dụ: `startTime < endTime`, thời gian không trong quá khứ).
  3. *Định vị dịch vụ (Service Discovery):* Consumer tra cứu Service Registry (Eureka) thông qua Service ID (`pitchos-pitch-service`) để lấy danh sách IP/Port của các instance khả dụng.
  4. *Cân bằng tải & Gửi HTTP Request:* Bộ cân bằng tải phía client (Spring Cloud LoadBalancer) chọn một instance theo thuật toán Round-Robin và gửi request HTTP qua OpenFeign.
  5. *Nhận response & Kiểm tra dữ liệu (Data Validation):* Nhận mã trạng thái HTTP và kiểm tra tính hợp lệ của dữ liệu trả về (giá tiền, trạng thái hoạt động).
  6. *Chuyển đổi DTO & Thực thi nghiệp vụ:* Ánh xạ dữ liệu sang DTO nội bộ, kiểm tra trùng lịch trong CSDL của Consumer và tính tổng tiền.
  7. *Ghi nhận dữ liệu & Trả lời Client:* Lưu đơn đặt sân xuống DB của Consumer và trả về mã `201 Created` cho Client.
- [ ] **Cách xử lý khi Provider không phản hồi hoặc trả về lỗi:**
  - *Cấu hình Timeout:* Bắt buộc thiết lập Connect Timeout và Read Timeout (ví dụ 2–3s) để ngăn luồng xử lý của Consumer bị phong tỏa (Thread Starvation).
  - *Phân loại lỗi chính xác:*
    - Lỗi nghiệp vụ từ Provider (404 Not Found): Chuyển tiếp thông báo rõ ràng "Không tìm thấy sân".
    - Lỗi hạ tầng / Provider chết / Timeout: Trả về mã lỗi **503 Service Unavailable** hoặc **504 Gateway Timeout**, không để phát sinh lỗi 500 mơ hồ.
  - *🚨 NGUYÊN TẮC CỐT LÕI (THẦY NHẮC):* **Tuyệt đối không truy cập trực tiếp vào Cơ sở dữ liệu của Provider để lấy dữ liệu thay thế** (vi phạm tính bao đóng của Microservices). Ghi log chi tiết và áp dụng Circuit Breaker (ngắt mạch khi lỗi dồn dập).

---

### 💻 B. Phần Mã nguồn & Kỹ thuật Vận hành (Chấm 60% Nhóm)

#### 1. Nâng cấp Consumer `pitchos-booking-service` (Mục 2.2 — 2.0 Điểm):
- [ ] Cập nhật `pom.xml`: Thêm dependency `spring-cloud-starter-netflix-eureka-client` và `spring-boot-starter-actuator`.
- [ ] **Chuyển OpenFeign sang gọi theo Service ID (Bỏ hoàn toàn URL cứng):**
  - Mở file `PitchClient.java`, sửa annotation:
    ```java
    @FeignClient(name = "pitchos-pitch-service")
    public interface PitchClient { ... }
    ```
  - Xóa bỏ thuộc tính `url = "${pitch.service.url}"` và xóa key `pitch.service.url` trong `application.properties`.
  - Cấu hình Timeout cho Feign theo Service ID trong `application.properties`:
    ```properties
    spring.cloud.openfeign.client.config.pitchos-pitch-service.connect-timeout=2000
    spring.cloud.openfeign.client.config.pitchos-pitch-service.read-timeout=3000
    ```
- [ ] **Bổ sung kiểm tra tính hợp lệ dữ liệu nhận về từ Provider (Yêu cầu TH6):**
  - Trong `BookingService.java`, sau khi nhận `PitchResponseDTO` từ `PitchClient`, bổ sung logic kiểm tra:
    ```java
    if (pitch.getPricePerHour() == null || pitch.getPricePerHour().compareTo(BigDecimal.ZERO) <= 0) {
        throw new BadGatewayException("Dữ liệu đơn giá từ Pitch Service không hợp lệ");
    }
    if (!"hoat_dong".equalsIgnoreCase(pitch.getStatus())) {
        throw new BadRequestException("Sân bóng hiện không hoạt động hoặc đang bảo trì");
    }
    ```
  - Cập nhật `GlobalExceptionHandler.java`: Bắt ngoại lệ và trả về mã lỗi **`502 Bad Gateway`** rõ ràng cho Client.
- [ ] **Bổ sung endpoint kiểm tra cân bằng tải qua Consumer:**
  - Thêm phương thức trong `PitchClient`:
    ```java
    @GetMapping("/api/v1/instance-info")
    Map<String, Object> getInstanceInfo();
    ```
  - Thêm endpoint trong `BookingController`: `GET /api/v1/bookings/pitch-instance` để trả về thông tin instance Pitch do LoadBalancer phân phối.
- [ ] Cập nhật `SecurityConfig`: Mở quyền truy cập cho `/api/v1/bookings/pitch-instance`, `/actuator/health`, `/actuator/info`.
- [ ] Viết file `Dockerfile` multi-stage chuẩn không chạy quyền root.
- [ ] Xóa bỏ file `application.properties` thừa ở thư mục gốc của service.

#### 2. Chuẩn hóa Bộ Kiểm Thử Postman Collection Toàn Hệ Thống:
- [ ] Tạo file duy nhất **`postman/collection.json`** chuẩn hóa cho toàn nhóm, phân thành 3 thư mục rõ ràng:
  1. `1. Authentication & RBAC`: Đăng ký, đăng nhập 3 vai trò, sinh Bearer Token.
  2. `2. Integration & Error Handling (IT01–IT07)`: Đầy đủ các ca kiểm thử tích hợp của Consumer gọi Provider.
  3. `3. Service Discovery & Load Balancing (TC01–TC06)`: Runner gửi 20 request kiểm tra cân bằng tải.
- [ ] Cấu hình sẵn Test Script tự động lưu Token và assert Status Code, Body response.

#### 3. Chạy và Thu thập Minh chứng Bộ Kiểm Thử Tích Hợp (IT01–IT07):
- [ ] **IT01:** Đặt sân thành công (Status 201, `totalPrice` = số giờ × đơn giá Pitch).
- [ ] **IT02:** Sân không tồn tại (`pitchId = 9999`) ➔ Nhận mã 404 từ Provider.
- [ ] **IT03:** Dữ liệu Provider không hợp lệ (giá sân <= 0 hoặc sân bảo trì) ➔ Nhận mã 502 / 400.
- [ ] **IT04:** Provider sập hoàn toàn (dừng 2 instance Pitch) ➔ Nhận mã 503 sạch sẽ, không sập Booking.
- [ ] **IT05:** Timeout mạng (`docker compose pause` Pitch) ➔ Nhận 503 sau 2–3s timeout.
- [ ] **IT06:** Gửi lặp cùng yêu cầu đặt sân ➔ Lần 1 trả 201, lần 2 trả 400 ("Khung giờ này đã có người đặt").
- [ ] **IT07:** Dữ liệu đầu vào sai (`endTime < startTime`) ➔ Nhận mã 400 tại validation.

---

### 📝 C. Phần Báo cáo Chuyên đề (Phụ trách: 2,50 / 10,0 Điểm)
- [ ] **Câu 1.1 (0,5 Điểm):** Lý thuyết Provider/Consumer, các bước Consumer gọi API, kỹ thuật xử lý khi Provider lỗi (Viết vào `docs/kt2/CAU1_1_NHAT.md`).
- [ ] Viết **Phần 3: Tích hợp và Tiêu thụ dịch vụ (2,0 Điểm)** vào `docs/kt2/PHAN_3_NHAT.md`:
  - Trình bày chi tiết luồng nghiệp vụ Khách hàng đặt sân bóng.
  - Vẽ sơ đồ tuần tự (Sequence Diagram) thể hiện đầy đủ các bước: Client ➔ Booking ➔ Eureka tra cứu ➔ OpenFeign LoadBalancer ➔ Pitch Service ➔ MySQL.
  - Phân tích đoạn mã nguồn OpenFeign gọi theo Service ID và logic kiểm tra dữ liệu Provider.
  - Bảng tổng hợp API Contract (`docs/api/api-contract.md`): Đường dẫn, Method, Header, Body Request, Response thành công và các mã lỗi.
  - Chèn ảnh minh chứng kết quả kiểm thử thực tế của bộ test **IT01–IT07** kèm phân tích chi tiết.

---

### 🎬 D. Phần Quay Video Demo Cá Nhân (40% Điểm Cá Nhân Của Nhật)
*Nhật tự thực hiện trên máy tính cá nhân và quay video 10–15 phút đủ 8 bước theo checklist:*
- [ ] **Bước 1:** Mở sơ đồ kiến trúc hệ thống giới thiệu các microservices, chỉ rõ Consumer (Booking), Provider (Pitch 2 instances) và Service Registry (Eureka).
- [ ] **Bước 2:** Chạy lệnh `docker compose up -d` ➔ Chạy `docker compose ps` chứng minh toàn bộ 7 container đều `healthy`.
- [ ] **Bước 3:** Mở Eureka Dashboard `http://localhost:8761` chứng minh các dịch vụ đã đăng ký, Pitch có 2 instances (8082 và 8084).
- [ ] **Bước 4:** Dùng Postman login lấy Token ➔ Gọi `POST /api/v1/bookings` đặt sân thành công (Status 201).
- [ ] **Bước 5:** Minh họa lỗi tích hợp: Gửi sân 9999 (Status 404), dừng cả 2 Pitch gửi đặt sân (Status 503).
- [ ] **Bước 6:** Mở `/actuator/health` = `{"status":"UP"}` và mở log xem luồng trao đổi.
- [ ] **Bước 7:** Dừng Pitch instance 1 ➔ Đặt sân vẫn thành công (Status 201) nhờ instance 2.
- [ ] **Bước 8:** Chạy `docker compose down` rồi `up -d` ➔ Chứng minh dữ liệu đơn đặt sân vẫn còn nguyên vẹn qua Docker Volume.
