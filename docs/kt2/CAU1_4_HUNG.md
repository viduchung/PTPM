# CÂU 1.4: VẬN HÀNH DỊCH VỤ, CÁC MỨC TRẠNG THÁI VÀ CÔNG CỤ GIÁM SÁT
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)  
**Sinh viên thực hiện:** HÙNG  
**Mục tiêu điểm số:** 0,5 / 0,5 Điểm Lý thuyết (Câu 1)

---

## 1. PHÂN BIỆT 3 CẤP ĐỘ TRẠNG THÁI CỦA HỆ THỐNG MICROSERVICES

Trong quá trình vận hành hệ thống hướng dịch vụ, việc đánh giá tính sẵn sàng của hệ thống không thể chỉ nhìn vào một chỉ số đơn lẻ. Theo chuẩn kỹ thuật TH8, trạng thái hệ thống được phân cấp thành 3 mức độ độc lập:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Trạng thái hoạt động của Container (Container Status)    │
│    └─ Mức OS: Tiến trình PID đang chạy (Up/Running)         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Trạng thái sức khỏe ứng dụng (Application Health)        │
│    └─ Mức App: Spring Boot + DB + Disk sẵn sàng (UP)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Khả năng thực hiện nghiệp vụ (Business Availability)     │
│    └─ Mức Hệ thống: Luồng đặt sân end-to-end thành công     │
└─────────────────────────────────────────────────────────────┘
```

### 1.1. Trạng thái hoạt động của Container (Container Status)
* **Bản chất kỹ thuật:** Là trạng thái tiến trình (Process Level) do Docker Engine / Daemon quản lý ở tầng hệ điều hành máy chủ (`docker ps` hiển thị `Up` hoặc `Exited`).
* **Ý nghĩa:** Chỉ chứng minh tiến trình bên trong container (ví dụ `java -jar app.jar`) chưa bị tắt, chưa bị kill hoặc crash thoát mã lỗi.
* **Hạn chế cốt lõi:** **Container đang ở trạng thái `Running` KHÔNG ĐỒNG NGHĨA với việc ứng dụng hoạt động tốt.** Một container Java có thể đang `Running` nhưng bên trong JVM đang bị rò rỉ bộ nhớ (OutOfMemoryError), bị treo luồng (Thread Deadlock) hoặc đang khởi động dở chưa sẵn sàng mở cổng mạng.

### 1.2. Trạng thái sức khỏe của Ứng dụng (Application Health)
* **Bản chất kỹ thuật:** Là trạng thái sẵn sàng nội tại của ứng dụng (Internal Component Readiness) được đánh giá qua endpoint giám sát Spring Boot Actuator (`GET /actuator/health`).
* **Ý nghĩa:** Cho biết ứng dụng đã khởi động hoàn tất và toàn bộ các thành phần phụ thuộc cốt lõi của dịch vụ đều hoạt động bình thường:
  * Pool kết nối cơ sở dữ liệu (HikariCP) kết nối thành công tới MySQL Server.
  * Dung lượng đĩa cứng còn đủ chỗ trống (DiskSpaceHealthIndicator).
  * Đã đăng ký thành công vào Service Registry (Eureka Client).
* **Kết quả:** Trả về `{"status": "UP"}` (khỏe mạnh) hoặc `{"status": "DOWN"}` (nếu mất kết nối MySQL).

### 1.3. Khả năng thực hiện nghiệp vụ của Hệ thống (Business Availability)
* **Bản chất kỹ thuật:** Là khả năng hoàn thành một quy trình nghiệp vụ xuyên suốt có sự tham gia của nhiều dịch vụ phân tán (End-to-End Business Flow).
* **Ý nghĩa:** Đây là cấp độ cao nhất và là mục tiêu cuối cùng của người dùng. Khả năng thực hiện nghiệp vụ phụ thuộc vào sự sẵn sàng đồng thời của toàn bộ chuỗi dịch vụ: Client ➔ Consumer ➔ Service Discovery ➔ LoadBalancer ➔ Provider ➔ CSDL.

### 1.4. Ví dụ minh họa thực tế từ hệ thống PitchOS
> Trong hệ thống PitchOS, xét quy trình **Khách hàng đặt sân bóng**:
> * Giả sử container `pitchos-booking-service` đang có Container Status là **`Running`**.
> * Endpoint `/actuator/health` của Booking Service báo **`UP`** (vì kết nối tốt tới DB `pitchos_booking_db`).
> * **Tuy nhiên:** Nếu cả 2 instance của `pitchos-pitch-service` (Provider) đều bị sập mạng hoặc tạm dừng, thì khi khách hàng gửi request đặt sân, Booking Service không thể lấy được giá sân và trả về lỗi `503 Service Unavailable`.
> * 👉 **Kết luận:** Tại thời điểm này, Container Status = `Running`, Application Health = `UP`, nhưng Business Availability = **`FAILED`** (không thực hiện được nghiệp vụ đặt sân). Do đó, người kỹ sư vận hành bắt buộc phải phân biệt rạch ròi 3 mức độ này.

---

## 2. VAI TRÒ CỦA HEALTH CHECK, LOG VÀ DOCKER VOLUME TRONG VẬN HÀNH

| Thành phần | Vai trò kỹ thuật trong vận hành Microservices | Áp dụng cụ thể trong hệ thống PitchOS |
|---|---|---|
| **Health Check** | • Giúp Docker Engine tự động theo dõi tiến trình nội bộ, hỗ trợ cơ chế tự phục hồi (Self-healing: tự khởi động lại khi ứng dụng bị treo).<br>• Phối hợp với Docker Compose điều phối thứ tự khởi động chính xác: `depends_on: condition: service_healthy` (ngăn chặn tình trạng Service Java khởi động khi MySQL chưa mở cổng). | Cấu hình healthcheck cho MySQL (`mysqladmin ping`) và các service Java (`/actuator/health`). Nhờ đó, Booking Service chỉ bật sau khi MySQL Booking và Eureka Server đã đạt trạng thái `healthy`. |
| **Log (Nhật ký)** | • Công cụ hàng đầu để chẩn đoán nguyên nhân sự cố (Root Cause Analysis) và truy vết luồng xử lý phân tán.<br>• Giúp phát hiện kịp thời các bất thường (lỗi timeout mạng, mất kết nối CSDL, lỗi xác thực JWT).<br>• ⚠️ **Lưu ý bảo mật (TH8):** Log vận hành tuyệt đối **không được in dữ liệu nhạy cảm** (mật khẩu người dùng, token bí mật, số thẻ). | Đọc log đồng thời (`docker compose logs pitchos-booking-service pitchos-pitch-service-1`) để thấy rõ thời điểm Booking gửi request và Pitch nhận tính toán; sửa bỏ dòng in mật khẩu mặc định trong `DataInitializer`. |
| **Docker Volume** | • Tách biệt hoàn toàn vòng đời của dữ liệu (Data Persistence) khỏi vòng đời ngắn hạn của container (Lifecycle Independence).<br>• Đảm bảo dữ liệu CSDL ghi xuống đĩa cứng máy chủ vật lý, không bị mất mát khi container bị dừng (`stop`), xóa bỏ (`down`) hoặc nâng cấp phiên bản image mới. | Thiết lập Named Volumes (`mysql_auth_data`, `mysql_pitch_data`, `mysql_booking_data`). Khi chạy `docker compose down` rồi bật lại bằng `docker compose up -d`, các đơn đặt sân đã tạo vẫn được bảo toàn nguyên vẹn 100%. |
