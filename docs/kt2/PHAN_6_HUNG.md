# PHẦN 6: VẬN HÀNH, GIÁM SÁT VÀ KIỂM THỬ SỰ CỐ HỆ THỐNG PITCHOS
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices 2026)  
**Sinh viên thực hiện:** HÙNG  
**Vai trò đề tài:** Kỹ sư Cơ sở Dữ liệu & Quản trị Vận hành Hệ thống  
**Trọng số điểm báo cáo:** 1,5 / 10,0 Điểm (Mục 2.4 - Vận hành, Giám sát & Xử lý sự cố)  
**Tập tin sở hữu & minh chứng:** `docker-compose.yml`, `scripts/`, `docs/testing/operation-test.md`, `docs/operation/failure-analysis.md`

---

## 6.1. GIÁM SÁT SỨC KHỎE ỨNG DỤNG BẰNG SPRING BOOT ACTUATOR

Trong kiến trúc phân tán gồm nhiều microservices độc lập, việc nắm bắt trạng thái sức khỏe nội tại của từng tiến trình là yêu cầu tiên quyết để duy trì tính liên tục của hệ thống. Nhóm triển khai thư viện **Spring Boot Actuator** trên toàn bộ 4 dịch vụ (`pitchos-service-registry`, `pitchos-auth-service`, `pitchos-pitch-service`, `pitchos-booking-service`).

### 6.1.1. Cấu hình kiểm soát an toàn (Security Hardening for Actuator)
Để vừa phục vụ giám sát vận hành vừa tuân thủ nghiêm ngặt nguyên tắc bảo mật thông tin (chuẩn TH8 - tránh phơi bày thông tin cấu hình nhạy cảm như kết nối CSDL, chuỗi bí mật JWT), nhóm thiết lập cấu hình thống nhất trong `application.properties`:

```properties
# Chỉ công bố endpoint health và info ra giao diện web
management.endpoints.web.exposure.include=health,info

# Không hiển thị chi tiết nội bộ cho người dùng nặc danh (tránh lộ thông tin đĩa, host DB)
management.endpoint.health.show-details=never
```

Đồng thời, trong `SecurityConfig.java` của từng dịch vụ, nhóm mở quyền truy cập tự do (`permitAll`) cho các đường dẫn này để Docker Healthcheck và các công cụ giám sát hạ tầng có thể thăm dò định kỳ mà không cần đính kèm JWT Bearer Token:

```java
.requestMatchers("/actuator/health", "/actuator/health/**", "/actuator/info").permitAll()
```

### 6.1.2. Kết quả thăm dò sức khỏe 5 endpoints thực tế
Khi toàn bộ 8 container trong file `docker-compose.yml` khởi chạy thành công, kết quả kiểm tra sức khỏe của từng thành phần thông qua kịch bản tự động `scripts/check-health.bat` như sau:

| Dịch Vụ | Cổng Mạng | Endpoint Giám Sát | Mã HTTP | Kết Quả JSON | Thành Phần Quyết Định Trạng Thái |
|---|:---:|---|:---:|:---:|---|
| **Service Registry** | `8761` | `http://localhost:8761/actuator/health` | `200 OK` | `{"status":"UP"}` | Eureka Server Engine sẵn sàng nhận đăng ký |
| **Auth & User Service** | `8081` | `http://localhost:8081/actuator/health` | `200 OK` | `{"status":"UP"}` | Kết nối HikariCP tới `mysql-auth:3306` (`pitchos_user_db`) thành công |
| **Pitch Service (Inst 1)** | `8082` | `http://localhost:8082/actuator/health` | `200 OK` | `{"status":"UP"}` | Kết nối HikariCP tới `mysql-pitch:3306` (`pitchos_pitch_db`) thành công |
| **Pitch Service (Inst 2)** | `8084` | `http://localhost:8084/actuator/health` | `200 OK` | `{"status":"UP"}` | Kết nối HikariCP tới `mysql-pitch:3306` (`pitchos_pitch_db`) thành công |
| **Booking Service** | `8083` | `http://localhost:8083/actuator/health` | `200 OK` | `{"status":"UP"}` | Kết nối HikariCP tới `mysql-booking:3306` (`pitchos_booking_db`) thành công |

```json
// Phản hồi tiêu chuẩn khi dịch vụ khỏe mạnh (HTTP Status 200 OK):
{
  "status": "UP"
}
```

---

## 6.2. TRUY VẾT VÀ PHÂN TÍCH NHẬT KÝ HOẠT ĐỘNG (DISTRIBUTED LOGGING)

Nhật ký hoạt động (Log) là công cụ quan trọng nhất để kỹ sư vận hành theo dõi luồng trao đổi dữ liệu liên dịch vụ và xác định nguyên nhân gốc rễ (Root Cause Analysis) khi có lỗi phát sinh.

### 6.2.1. Phân tích Log luồng Đặt sân thành công (201 Created)
Khi khách hàng gửi yêu cầu đặt sân: `POST http://localhost:8083/api/v1/bookings` (Sân 1, thời gian 18:00 – 19:30), công cụ theo dõi log thời gian thực ghi nhận chuỗi sự kiện phối hợp giữa Booking Service và Pitch Service:

```text
==> LOG TẠI PITCHOS-BOOKING-SERVICE (Consumer):
2026-11-24 15:30:10.125 [http-nio-8083-exec-2] INFO  c.p.booking.service.BookingService - [TẠO ĐƠN] Nhận yêu cầu đặt sân từ userId=3, pitchId=1, thời gian 18:00 -> 19:30
2026-11-24 15:30:10.130 [http-nio-8083-exec-2] INFO  c.p.b.client.PitchGateway - Gửi HTTP GET sang Provider qua OpenFeign: pitchos-pitch-service/api/v1/pitches/1
2026-11-24 15:30:10.155 [http-nio-8083-exec-2] INFO  c.p.booking.service.BookingService - Pitch Service trả về sân 1: giá 300000.00 /giờ, trạng thái hoat_dong
2026-11-24 15:30:10.158 [http-nio-8083-exec-2] INFO  c.p.booking.service.BookingService - Dữ liệu hợp lệ. Tính tổng tiền: 1.5 giờ * 300000.00 = 450000.00 VNĐ
2026-11-24 15:30:10.165 [http-nio-8083-exec-2] INFO  c.p.booking.service.BookingService - Kiểm tra trùng lịch: Khung giờ trống. Lưu đơn đặt sân id=12 (status: cho_duyet)

==> LOG TẠI PITCHOS-PITCH-SERVICE-1 (Provider - Instance 1):
2026-11-24 15:30:10.140 [http-nio-8082-exec-1] INFO  c.p.pitch.controller.PitchController - [pitch-instance-1] GET /api/v1/pitches/1 - Tra cứu chi tiết sân bóng
2026-11-24 15:30:10.145 [http-nio-8082-exec-1] INFO  c.p.pitch.service.PitchService - [pitch-instance-1] Tìm thấy sân bóng id=1 (Sân 5 số 1), giá: 300000.00, trạng thái: hoat_dong
```

*Nhận xét:*
* Log thể hiện rõ ràng luồng tương tác logic: Consumer (Booking) nhận request $\rightarrow$ tra cứu Eureka $\rightarrow$ LoadBalancer chọn `pitch-instance-1` $\rightarrow$ Pitch Controller ghi nhận và trả kết quả $\rightarrow$ Booking kiểm tra dữ liệu và lưu đơn vào CSDL riêng.
* Tiền tố `[pitch-instance-1]` giúp người vận hành biết chính xác container nào đã xử lý request mà không cần tra cứu địa chỉ IP.

### 6.2.2. Phân tích Log khi Provider gặp sự cố (Chống Cascading Failure)
Khi cả 2 instance của Pitch Service bị dừng (`docker compose stop pitchos-pitch-service-1 pitchos-pitch-service-2`), khách hàng gửi request đặt sân:

```text
==> LOG TẠI PITCHOS-BOOKING-SERVICE (Consumer):
2026-11-24 15:35:45.210 [http-nio-8083-exec-5] INFO  c.p.booking.service.BookingService - [TẠO ĐƠN] Nhận yêu cầu đặt sân từ userId=3, pitchId=1
2026-11-24 15:35:45.215 [http-nio-8083-exec-5] WARN  c.p.b.client.PitchGateway - Eureka không còn instance nào của pitchos-pitch-service: No instances available for pitchos-pitch-service
2026-11-24 15:35:45.218 [http-nio-8083-exec-5] WARN  c.p.b.exception.GlobalExceptionHandler - Không còn instance Provider khả dụng: Không còn instance nào của pitchos-pitch-service trong danh bạ Eureka
2026-11-24 15:35:45.220 [http-nio-8083-exec-5] INFO  c.p.b.exception.GlobalExceptionHandler - Trả về mã HTTP 503 SERVICE_UNAVAILABLE cho client
```

*Nhận xét bảo mật & ổn định:*
* Tiến trình Booking Service **không bị sập, không bị đơ luồng (No Thread Starvation)**.
* Ngoại lệ được bao bọc an toàn, trả về mã HTTP `503 Service Unavailable` có cấu trúc JSON rõ ràng cho người dùng thay vì mã lỗi `500 Internal Server Error` kèm vết ngăn xếp (Stacktrace) dài dòng.
* Không in bất kỳ thông tin nhạy cảm hay mật khẩu ra log theo đúng tiêu chuẩn TH8.

---

## 6.3. BẢNG TỔNG HỢP KIỂM THỬ VẬN HÀNH VÀ SỰ CỐ (DEP01 – DEP08)

Bộ kiểm thử triển khai và vận hành hệ thống được thực hiện trên môi trường Docker Compose hoàn chỉnh:

| Mã Ca | Tên Kịch Bản Kiểm Thử | Thao Tác Thực Hiện | Kết Quả Kỳ Vọng | Trạng Thái Thực Tế |
|:---:|---|---|---|:---:|
| **DEP01** | Khởi tạo toàn bộ hệ thống | `docker compose up -d --build` | 8 container khởi chạy, `docker compose ps` báo toàn bộ đều `healthy` | ✅ **ĐẠT** |
| **DEP02** | Giám sát Actuator Health | Chạy `scripts/check-health.bat` | Toàn bộ 5 endpoints trả về HTTP `200` kèm `{"status":"UP"}` | ✅ **ĐẠT** |
| **DEP03** | Giám sát Log phân tán | `docker compose logs -f` | Đọc được thông điệp giao tiếp liên dịch vụ có tiền tố `[instanceId]` | ✅ **ĐẠT** |
| **DEP04** | Dừng Consumer quan sát Registry | `docker compose stop pitchos-booking-service` | Eureka Dashboard gỡ bỏ Booking Service sau thời gian heartbeat | ✅ **ĐẠT** |
| **DEP05** | Tự phục hồi Consumer | `docker compose start pitchos-booking-service` | Container tự healthy trở lại, tự đăng ký vào Eureka, đặt sân bình thường | ✅ **ĐẠT** |
| **DEP06** | **Bảo toàn dữ liệu qua Volume** | Đặt sân $\rightarrow$ `docker compose down` $\rightarrow$ `docker compose up -d` $\rightarrow$ chạy `scripts/test-persistence.bat` | Dữ liệu bảng `bookings` trong MySQL **còn nguyên vẹn 100%**, không mất bản ghi | ✅ **ĐẠT** |
| **DEP07** | **Sự cố mất kết nối CSDL** | `docker compose stop mysql-pitch` | Actuator của 2 Pitch Service lập tức chuyển `DOWN`, log báo lỗi ngắt HikariCP | ✅ **ĐẠT** |
| **DEP08** | **Chịu lỗi Provider (Fault Tolerance)** | Dừng `pitchos-pitch-service-1` $\rightarrow$ gửi request đặt sân qua Booking | Booking tự chuyển sang gọi `pitchos-pitch-service-2`, **đặt sân thành công 201 Created** | ✅ **ĐẠT** |

---

## 6.4. PHÂN TÍCH CHUYÊN SÂU MỘT TÌNH HUỐNG SỰ CỐ VẬN HÀNH THỰC TẾ

> 📌 **Yêu cầu barem điểm:** Trình bày chi tiết một tình huống sự cố thực tế xảy ra trong quá trình tích hợp/vận hành, phân tích nguyên nhân gốc rễ và giải pháp khắc phục triệt để.

### 6.4.1. Bối cảnh và Mô tả Hiện tượng Sự cố
* **Tình huống xảy ra:** Trong quá trình vận hành cao điểm, một hoặc cả hai container của dịch vụ Provider (`pitchos-pitch-service`) bị treo do quá tải CPU/RAM hoặc bị tiến trình bên ngoài vô tình dừng lại (`container terminated / crash`).
* **Hiện tượng quan sát được:**
  * Khách hàng sử dụng ứng dụng web / Postman gọi API đặt sân: `POST /api/v1/bookings`.
  * Trước khi có cơ chế phòng vệ: Request của khách hàng bị quay vòng chờ đợi vô tận (thời gian phản hồi kéo dài hơn 60 giây), sau đó trình duyệt báo lỗi `504 Gateway Timeout` hoặc máy chủ báo lỗi `500 Internal Server Error`.
  * Các request đặt sân đến sau của những người dùng khác tiếp tục dồn ứ, chiếm hết toàn bộ luồng xử lý (Tomcat worker threads) của `pitchos-booking-service`, dẫn đến việc chức năng xem lịch sử đặt sân (`GET /api/v1/bookings/my-bookings`) cũng bị tê liệt theo.

### 6.4.2. Phân tích Nguyên nhân Gốc rễ (Root Cause Analysis - RCA)
1. **Hiện tượng Sụp đổ dây chuyền (Cascading Failure):** Khi gọi qua giao thức mạng HTTP REST, nếu dịch vụ nhận cuộc gọi (Provider) không phản hồi và dịch vụ gọi (Consumer) không thiết lập thời gian chờ (Timeout), tiến trình gọi sẽ bị phong tỏa vĩnh viễn ở trạng thái chờ I/O (`SocketRead0`).
2. **Cạn kiệt luồng kết nối (Thread Exhaustion):** Mỗi container Spring Boot có kích thước Thread Pool mặc định là 200 luồng. Khi 200 người dùng gửi request cùng lúc và bị treo, toàn bộ pool cạn kiệt, dịch vụ Consumer hoàn toàn mất khả năng phục vụ ngay cả với các nghiệp vụ nội bộ không liên quan tới Provider.
3. **Độ trễ nhận diện của Service Registry (Registry Latency):** Theo cơ chế mặc định của Netflix Eureka, khoảng thời gian gửi heartbeat là 30 giây và thời gian chờ hết hạn bản ghi (Lease Expiration) là 90 giây. Khi Provider chết đột ngột, Consumer vẫn tiếp tục lấy địa chỉ cũ từ bộ nhớ đệm (Local Cache) và cố gắng gửi request tới địa chỉ chết trong suốt 30–90 giây tiếp theo.

### 6.4.3. Giải pháp Kiến trúc và Khắc phục Kỹ thuật Đã Triển Khai
Để xử lý triệt để bài toán này, nhóm đã phối hợp áp dụng bộ giải pháp đa tầng (Defense-in-depth):

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. TẦNG CONTAINER: Triển khai 2 Instance Provider song song (8082 & 8084)   │
│    └─ Khi Instance 1 chết, LoadBalancer tự động chuyển 100% tải sang Inst 2 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. TẦNG TIMEOUT: Thiết lập OpenFeign Connect=2000ms & Read=3000ms           │
│    └─ Cắt đứt kết nối sau tối đa 3 giây, giải phóng ngay Tomcat Thread       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. TẦNG XỬ LÝ LỖI: Lớp chắn PitchGateway + GlobalExceptionHandler           │
│    └─ Bắt FeignException / IllegalStateException -> Trả HTTP 503 sạch sẽ    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. TẦNG ĐIỀU PHỐI DOCKER: restart: unless-stopped                           │
│    └─ Docker Engine tự động khởi động lại container bị crash                │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Thiết lập Timeout chặt chẽ cho OpenFeign:**
   Trong `pitchos-booking-service/src/main/resources/application.properties`, nhóm cấu hình thời gian ngắt kết nối dứt khoát:
   ```properties
   spring.cloud.openfeign.client.config.pitchos-pitch-service.connect-timeout=2000
   spring.cloud.openfeign.client.config.pitchos-pitch-service.read-timeout=3000
   ```
2. **Chuyển đổi mã lỗi hạ tầng sang mã lỗi nghiệp vụ chuẩn (HTTP 503):**
   Trong `GlobalExceptionHandler.java`, toàn bộ các lỗi liên quan đến việc Provider không khả dụng hoặc timeout đều được bắt và chuyển hóa thành mã phản hồi `503 Service Unavailable`:
   ```java
   @ExceptionHandler({FeignException.class, RetryableException.class})
   public ResponseEntity<ErrorResponse> handleFeignFailure(FeignException ex) {
       log.warn("Không gọi được Pitch Service (status Feign = {}): {}", ex.status(), ex.getMessage());
       return build(HttpStatus.SERVICE_UNAVAILABLE, "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!");
   }
   ```
3. **Cấu hình 2 Instance Provider cân bằng tải:**
   Trong `docker-compose.yml`, nhóm duy trì đồng thời `pitchos-pitch-service-1` (port 8082) và `pitchos-pitch-service-2` (port 8084). Khi một instance bị dừng trong ca kiểm thử DEP08, Spring Cloud LoadBalancer phát hiện lỗi kết nối và tự động chuyển tiếp request sang instance còn lại, đảm bảo nghiệp vụ đặt sân của khách hàng không bị gián đoạn dù chỉ một giây.

---

## 6.5. BẢO TOÀN DỮ LIỆU BẰNG DOCKER NAMED VOLUME

Một trong những tiêu chí chấm điểm quan trọng nhất của phần vận hành (TH8) là chứng minh dữ liệu cơ sở dữ liệu không bị mất khi container bị xóa bỏ.

### 6.5.1. Cơ chế Named Volume trong hệ thống PitchOS
Hệ thống PitchOS cấu hình 3 Named Volumes tương ứng với 3 cơ sở dữ liệu độc lập:
* `mysql_auth_data` $\rightarrow$ Ánh xạ tới `/var/lib/mysql` của container `mysql-auth`.
* `mysql_pitch_data` $\rightarrow$ Ánh xạ tới `/var/lib/mysql` của container `mysql-pitch`.
* `mysql_booking_data` $\rightarrow$ Ánh xạ tới `/var/lib/mysql` của container `mysql-booking`.

Toàn bộ dữ liệu bảng, chỉ mục và transaction log của MySQL được lưu trực tiếp tại thư mục do Docker Engine quản lý trên ổ đĩa vật lý của máy chủ (`C:\ProgramData\Docker\volumes\...` trên Windows).

### 6.5.2. Kịch bản kiểm thử bảo toàn dữ liệu (`scripts/test-persistence.bat`)
Quy trình thực nghiệm chứng minh:
1. **Bước 1 (Ghi dữ liệu):** Sử dụng Postman đặt thành công một đơn sân mới (ví dụ đơn số `15`). Câu lệnh truy vấn trực tiếp container kiểm tra thấy có 15 bản ghi:
   ```sql
   SELECT count(*) FROM pitchos_booking_db.bookings; -- Kết quả: 15
   ```
2. **Bước 2 (Xóa container):** Thực thi lệnh hủy toàn bộ hệ thống container:
   ```bash
   docker compose down
   ```
   > ⚠️ **Quy tắc an toàn:** Tuyệt đối không thêm cờ `-v` (flag `-v` / `--volumes` sẽ ra lệnh cho Docker xóa sạch volume).
3. **Bước 3 (Khởi dựng lại):** Khởi động lại toàn bộ hệ thống:
   ```bash
   docker compose up -d
   ```
4. **Bước 4 (Đối soát):** Truy vấn lại dữ liệu ngay khi MySQL khởi động xong:
   ```sql
   SELECT id, user_id, pitch_id, total_price, status, created_at 
   FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1;
   ```
   *Kết quả thu được:* Đơn đặt sân số `15` với đầy đủ thông tin `user_id`, `pitch_id`, `total_price` và mốc thời gian `created_at` vẫn còn nguyên vẹn 100%. Không có bất kỳ hiện tượng mất mát dữ liệu nào xảy ra.
