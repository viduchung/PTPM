# BÁO CÁO PHÂN TÍCH SỰ CỐ VẬN HÀNH VÀ GIẢI PHÁP KHẮC PHỤC
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices 2026)  
**Hệ thống:** PitchOS — Hệ thống Quản lý và Đặt sân bóng mini trực tuyến  
**Người biên soạn:** HÙNG — Kỹ sư Cơ sở dữ liệu & Quản trị Vận hành  
**Trọng số đánh giá:** Mục bắt buộc có điểm riêng trong Phần 6 (1,5 Điểm Vận hành)

---

## 1. MÔ TẢ TÌNH HUỐNG SỰ CỐ THỰC TẾ

### 1.1. Bối cảnh phát sinh sự cố
Trong môi trường microservices phân tán, các dịch vụ không còn giao tiếp trong cùng một không gian bộ nhớ mà phải phụ thuộc vào hạ tầng mạng (Network-based communication). Trong quá trình vận hành thử nghiệm hệ thống PitchOS, nhóm ghi nhận sự cố sau:

* **Tình huống:** Dịch vụ Provider (`pitchos-pitch-service`) bị sự cố ngắt kết nối mạng hoặc bị quá tải dẫn đến container bị đóng băng (unresponsive / hang) trong khi dịch vụ Consumer (`pitchos-booking-service`) vẫn đang mở cổng nhận yêu cầu từ người dùng.
* **Thời điểm xảy ra:** Khách hàng thực hiện tạo đơn đặt sân bóng đá mini qua endpoint `POST /api/v1/bookings`.
* **Hiện tượng quan sát được:**
  * Request gửi từ client bị treo vô tận (thời gian xoay vòng chờ đợi vượt quá 60 giây).
  * Client sau đó nhận được mã lỗi `504 Gateway Timeout` hoặc ứng dụng ném lỗi `500 Internal Server Error` không rõ nguyên nhân.
  * Các request nghiệp vụ khác của Booking Service (như `GET /api/v1/bookings/my-bookings`) cũng bị chậm chạp và dần dần không thể phản hồi.

---

## 2. PHÂN TÍCH NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE ANALYSIS)

Sau khi kiểm tra nhật ký log và vết ngăn xếp tiến trình (Thread Dump), nhóm đã xác định được 3 nguyên nhân cốt lõi gây ra sự cố:

### 2.1. Hiện tượng Sụp đổ Dây chuyền (Cascading Failure)
Mặc định, khi một HTTP Client gửi request tới máy chủ từ xa mà không khai báo thời gian timeout, socket mạng sẽ chờ đợi phản hồi của hệ điều hành cho tới khi TCP Connection hết hạn (thường là nhiều phút). 
Do đó, khi Provider gặp sự cố:
* Luồng xử lý của Consumer (Tomcat Worker Thread) bị giữ chặt ở trạng thái `WAITING / SocketRead`.
* Các request mới tiếp tục đổ về, nhanh chóng làm cạn kiệt toàn bộ Thread Pool (mặc định 200 luồng của Spring Boot).
* Kết quả là một lỗi cục bộ tại dịch vụ Pitch đã lan rộng và làm sụp đổ hoàn toàn dịch vụ Booking — đây là hiện tượng kinh điển **Cascading Failure** trong kiến trúc microservices.

### 2.2. Nhận thức sai lệch về tính sẵn sàng (Availability Illusion)
Tại thời điểm Provider bị treo:
* Container `pitchos-pitch-service` trên Docker Desktop vẫn có Container Status là `Up` (tiến trình PID vẫn đang sống).
* Tuy nhiên, ứng dụng bên trong đã mất khả năng phản hồi (Application Health không còn đảm bảo).
* Do đó, nếu chỉ nhìn vào trạng thái `docker ps` mà không có cơ chế thăm dò sức khỏe nội tại (Actuator Healthcheck), hệ thống điều phối sẽ không nhận biết được container đã chết để khởi động lại.

### 2.3. Độ trễ cập nhật bảng định tuyến Eureka (Registry Latency)
Cơ chế tự nhiên của Netflix Eureka là đánh đổi tính nhất quán để lấy tính sẵn sàng (Mô hình AP trong Định lý CAP). Mặc định:
* Heartbeat định kỳ: 30 giây một lần.
* Thời gian chờ loại bỏ (Lease Expiration): 90 giây.
* Thời gian đồng bộ cache của Client: 30 giây.
Do đó, sau khi Provider bị sập, Consumer vẫn tiếp tục giữ địa chỉ IP cũ trong bộ nhớ đệm và liên tục gửi request vào container chết trong khoảng 30–90 giây tiếp theo nếu không có cơ chế xử lý lỗi nhanh.

---

## 3. GIẢI PHÁP ĐA TẦNG ĐÃ ĐƯỢC HIỆN THỰC HÓA

Để khắc phục hoàn toàn sự cố và đạt chuẩn vận hành TH8, nhóm đã thiết kế và triển khai giải pháp phòng thủ 4 tầng:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TẦNG 1: TIMEOUT CHỐNG PHONG TỎA LUỒNG (OPENFEIGN CONFIGURATION)             │
│ connect-timeout: 2000ms  │  read-timeout: 3000ms                            │
│ ==> Tối đa 3 giây là ngắt kết nối, giải phóng ngay Tomcat Thread            │
├─────────────────────────────────────────────────────────────────────────────┤
│ TẦNG 2: BAO BỌC NGOẠI LỆ & CHUẨN HÓA MÃ HTTP (PITCH GATEWAY)                │
│ Bắt FeignException / IllegalStateException -> Trả về HTTP 503 sạch sẽ       │
│ ==> Tuyệt đối không để lộ lỗi 500 mơ hồ hay stacktrace ra ngoài             │
├─────────────────────────────────────────────────────────────────────────────┤
│ TẦNG 3: CÂN BẰNG TẢI DƯ THỪA (REDUNDANCY & CLIENT-SIDE LOAD BALANCING)      │
│ Chạy 2 Instance Provider: pitchos-pitch-service-1 & pitch-service-2        │
│ ==> Khi Inst 1 chết, LoadBalancer tự động chuyển 100% tải sang Inst 2      │
├─────────────────────────────────────────────────────────────────────────────┤
│ TẦNG 4: ĐIỀU PHỐI DOCKER & TỰ ĐỘNG PHỤC HỒI (SELF-HEALING)                 │
│ restart: unless-stopped  │  Actuator Healthcheck wget định kỳ 10s           │
│ ==> Docker tự phát hiện container hỏng để restart tự động                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.1. Cấu hình Timeout nghiêm ngặt
Trong `pitchos-booking-service/src/main/resources/application.properties`:
```properties
# Timeout kết nối (chờ bắt tay TCP): 2 giây
spring.cloud.openfeign.client.config.pitchos-pitch-service.connect-timeout=2000

# Timeout đọc dữ liệu (chờ xử lý SQL/Logic): 3 giây
spring.cloud.openfeign.client.config.pitchos-pitch-service.read-timeout=3000
```

### 3.2. Chuẩn hóa mã lỗi HTTP 503 Service Unavailable
Trong `GlobalExceptionHandler.java` của Booking Service:
```java
@ExceptionHandler({FeignException.class, RetryableException.class})
public ResponseEntity<ErrorResponse> handleFeignFailure(FeignException ex) {
    log.warn("Không gọi được Pitch Service (status Feign = {}): {}", ex.status(), ex.getMessage());
    return build(HttpStatus.SERVICE_UNAVAILABLE, "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!");
}
```

### 3.3. Cơ chế High Availability (2 Instance Provider)
Trong `docker-compose.yml`, nhóm cấu hình 2 container độc lập cùng chia sẻ một CSDL `mysql-pitch`:
* `pitchos-pitch-service-1` (Cổng 8082, INSTANCE_ID=`pitch-instance-1`)
* `pitchos-pitch-service-2` (Cổng 8084, INSTANCE_ID=`pitch-instance-2`)

Khi một instance bị lỗi, Spring Cloud LoadBalancer lập tức phát hiện và phân phối request tiếp theo sang instance còn lại, đảm bảo nghiệp vụ không bị gián đoạn.

---

## 4. KẾT QUẢ VÀ BÀI HỌC KINH NGHIỆM

1. **Hiệu quả thực tế:** Sau khi áp dụng giải pháp trên, thời gian phản hồi tối đa khi Provider sập giảm từ >60 giây xuống còn đúng **3 giây**. Người dùng nhận được thông báo lỗi thân thiện (mã 503) thay vì màn hình đơ.
2. **Bài học vận hành:**
   * Trong hệ thống phân tán, việc "thất bại nhanh" (Fail-fast) tốt hơn rất nhiều so với việc để tiến trình chờ đợi vô tận.
   * Luôn phải có kịch bản dự phòng lỗi (Fallback / Redundancy) cho các dịch vụ Provider cốt lõi.
