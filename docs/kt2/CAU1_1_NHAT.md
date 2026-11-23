# CÂU 1.1: PHÂN BIỆT PROVIDER / CONSUMER, QUY TRÌNH GỌI API VÀ XỬ LÝ LỖI TÍCH HỢP
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)  
**Sinh viên thực hiện:** NHẬT  
**Mục tiêu điểm số:** 0,5 / 0,5 Điểm Lý thuyết (Câu 1)

---

## 1. PHÂN BIỆT DỊCH VỤ CUNG CẤP (PROVIDER) VÀ DỊCH VỤ TIÊU THỤ (CONSUMER)

Trong kiến trúc hướng dịch vụ, một dịch vụ không được định nghĩa bằng việc nó nằm ở đâu trong hệ thống, mà bằng **vai trò của nó trong một lần giao tiếp cụ thể**. Hai vai trò cơ bản là Provider và Consumer.

| Tiêu chí so sánh | Provider (Dịch vụ cung cấp) | Consumer (Dịch vụ tiêu thụ) |
|---|---|---|
| **Quyền sở hữu dữ liệu** | Sở hữu dữ liệu nghiệp vụ gốc (Data Ownership), là nguồn chân lý duy nhất về dữ liệu đó | Không sở hữu dữ liệu của Provider, chỉ xin bản sao tại thời điểm cần dùng |
| **Hợp đồng giao tiếp** | Công bố và cam kết giữ ổn định hợp đồng API (đường dẫn, tham số, cấu trúc phản hồi, mã lỗi) | Phải tuân thủ đúng hợp đồng API do Provider công bố |
| **Chiều khởi tạo kết nối** | Thụ động: chờ request đi tới rồi trả response | Chủ động: gửi request trong mã nguồn nghiệp vụ của chính nó |
| **Khả năng mở rộng** | Thường chạy nhiều instance để chia tải và chịu lỗi | Gọi tới Service ID, không cần biết có bao nhiêu instance Provider |
| **Vai trò trong PitchOS** | `pitchos-pitch-service`: quản lý thông tin sân, đơn giá `pricePerHour`, trạng thái `hoat_dong`/`bao_tri`. Chạy **2 instance** (cổng 8082 và 8084) | `pitchos-booking-service`: khi khách đặt sân, gọi sang Pitch lấy đơn giá để tính tổng tiền và kiểm tra sân có đang hoạt động |

**Ba điểm cần nhấn mạnh:**

1. **Hai vai trò là tương đối, không cố định.** Một dịch vụ có thể đồng thời là Consumer của dịch vụ này và Provider của dịch vụ khác. Trong PitchOS, `pitchos-booking-service` là Consumer của Pitch Service, nhưng lại là Provider đối với ứng dụng khách (Postman / web) khi công bố API `POST /api/v1/bookings`.
2. **Consumer phải gọi API, tuyệt đối không truy cập cơ sở dữ liệu của Provider.** Nếu Booking Service tự kết nối vào `pitchos_pitch_db` để `SELECT price_per_hour` thì hệ thống chỉ còn là một ứng dụng nguyên khối bị chia tệp, đã phá vỡ tính bao đóng của microservices.
3. **Consumer chỉ được phụ thuộc vào hợp đồng, không phụ thuộc vào địa chỉ.** Đây chính là lý do Consumer gọi Provider qua Service ID (`pitchos-pitch-service`) tra cứu trong danh bạ Eureka, thay vì gọi bằng URL cứng `http://localhost:8082`.

---

## 2. CÁC BƯỚC CƠ BẢN KHI MỘT CONSUMER GỌI API CỦA PROVIDER

Dưới đây là 7 bước của một lần Consumer gọi Provider, lấy đúng luồng `POST /api/v1/bookings` của hệ thống PitchOS làm ví dụ.

```
Client ──(1)──► Booking Service (CONSUMER)
                  │ (2) Validation dữ liệu đầu vào
                  │ (3) Tra cứu danh bạ ──────────────► Eureka Server (:8761)
                  │     Service ID: pitchos-pitch-service
                  │ ◄──── Danh sách instance: 8082, 8084
                  │ (4) LoadBalancer chọn 1 instance, gửi HTTP GET (OpenFeign)
                  ├───────────────────────────────────► Pitch Service (PROVIDER)
                  │ ◄──(5)── 200 OK + {pricePerHour, status}
                  │ (5') Kiểm tra tính hợp lệ của dữ liệu nhận về
                  │ (6) Ánh xạ DTO, kiểm tra trùng lịch, tính tổng tiền
                  │ (7) Lưu đơn vào pitchos_booking_db
                  ▼
Client ◄──── 201 Created
```

1. **Tiếp nhận và xác thực yêu cầu.** Consumer nhận request kèm JWT `Authorization: Bearer <token>`, tự giải mã và kiểm tra chữ ký HS256 bằng khóa dùng chung, lấy ra `userId` và `role` mà **không cần gọi sang Auth Service** (xác thực không trạng thái — stateless).
2. **Kiểm tra dữ liệu đầu vào (Validation).** Bean Validation kiểm tra các trường bắt buộc, sau đó tầng nghiệp vụ kiểm tra `endTime` phải sau `startTime`. Sai ở bước này thì trả `400 Bad Request` ngay, **không gọi sang Provider** để tiết kiệm một vòng gọi mạng.
3. **Định vị dịch vụ (Service Discovery).** Consumer tra cứu Service Registry (Eureka) theo Service ID `pitchos-pitch-service` để lấy danh sách địa chỉ IP/cổng của các instance đang còn sống (còn gửi heartbeat).
4. **Cân bằng tải và gửi HTTP Request.** Spring Cloud LoadBalancer chọn một instance theo thuật toán Round-Robin, OpenFeign dựng và gửi request `GET /api/v1/pitches/{id}` kèm **timeout bắt buộc** (kết nối 2s, đọc 3s).
5. **Nhận phản hồi và kiểm tra dữ liệu trả về.** Consumer đọc mã trạng thái HTTP, rồi kiểm tra chính nội dung dữ liệu: đơn giá có null hoặc `<= 0` không, trạng thái sân có phải `hoat_dong` không. Dữ liệu từ dịch vụ khác cũng là dữ liệu bên ngoài, không được tin tưởng mù quáng.
6. **Chuyển đổi DTO và thực thi nghiệp vụ.** Dữ liệu được ánh xạ sang DTO nội bộ (`PitchResponseDTO`), sau đó Consumer làm việc của riêng mình: kiểm tra trùng lịch trong CSDL của chính nó và tính `totalPrice = số giờ × pricePerHour`.
7. **Ghi nhận dữ liệu và trả lời Client.** Lưu đơn đặt sân vào `pitchos_booking_db` với trạng thái `cho_duyet` và trả về `201 Created` kèm thông tin đơn.

---

## 3. XỬ LÝ KHI PROVIDER KHÔNG PHẢN HỒI HOẶC TRẢ VỀ LỖI

### 3.1. Luôn đặt timeout — chống sụp đổ dây chuyền (Cascading Failure)

Nếu gọi Provider mà không đặt thời gian chờ, mỗi request của khách sẽ chiếm giữ một luồng (thread) của Consumer vô thời hạn. Chỉ cần Provider chậm trong vài phút, toàn bộ thread pool của Consumer bị chiếm hết (Thread Starvation) và Consumer **sập theo Provider** dù bản thân nó hoàn toàn khỏe mạnh. Đó là hiện tượng sụp đổ dây chuyền.

Vì vậy trong PitchOS, timeout được khai báo theo đúng Service ID của Provider:

```properties
spring.cloud.openfeign.client.config.pitchos-pitch-service.connect-timeout=2000
spring.cloud.openfeign.client.config.pitchos-pitch-service.read-timeout=3000
```

### 3.2. Phân loại lỗi chính xác, trả về mã HTTP đúng ngữ nghĩa

Người dùng và kỹ sư vận hành cần biết **lỗi thuộc về ai**. Trả tất cả về `500 Internal Server Error` là che mất thông tin chẩn đoán quan trọng nhất.

| Tình huống thực tế | Bản chất lỗi | Mã trả về cho Client | Cách làm trong PitchOS |
|---|---|---|---|
| Khách gửi `pitchId` không tồn tại, Provider trả `404` | Lỗi nghiệp vụ, do dữ liệu người dùng gửi | `404 Not Found` | `CustomErrorDecoder` chuyển `404` thành `ResourceNotFoundException` |
| Provider trả `200` nhưng đơn giá `null` hoặc `<= 0` | Dữ liệu của dịch vụ phía sau bị sai | `502 Bad Gateway` | `BookingService` kiểm tra và ném `BadGatewayException` |
| Sân tồn tại nhưng đang `bao_tri` | Lỗi nghiệp vụ, yêu cầu không thể thực hiện | `400 Bad Request` | `BookingService` ném `BadRequestException` |
| Provider tắt hẳn, mất kết nối, hoặc quá thời gian chờ | Lỗi hạ tầng phía Provider | `503 Service Unavailable` | Bắt `FeignException` / `RetryableException` trong `GlobalExceptionHandler` |
| Eureka không còn instance nào của Provider | Lỗi hạ tầng, không còn địa chỉ để gọi | `503 Service Unavailable` | `PitchGateway` chuyển lỗi của LoadBalancer thành `ServiceUnavailableException` |

Thông điệp trả cho người dùng luôn thân thiện và không chứa chi tiết kỹ thuật:

```json
{
  "timestamp": "2026-11-22T21:00:00",
  "status": 503,
  "error": "Service Unavailable",
  "message": "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!"
}
```

Stack trace, tên lớp ngoại lệ và câu lệnh SQL chỉ được ghi vào log của máy chủ, không bao giờ trả ra ngoài cho Client.

### 3.3. Ba nguyên tắc cốt lõi khi Provider lỗi (lưu ý trọng tâm của giảng viên)

1. **Tuyệt đối không truy cập trực tiếp cơ sở dữ liệu của Provider để lấy dữ liệu thay thế.** Khi Pitch Service sập, Booking Service **không được** mở kết nối vào `pitchos_pitch_db` đọc bảng `pitches`. Làm vậy sẽ phá vỡ tính bao đóng, Consumer bị dính chặt vào lược đồ CSDL của Provider, và Provider sẽ không bao giờ đổi được schema hay loại CSDL nữa.
2. **Ghi log đầy đủ để truy vết, nhưng không lộ dữ liệu nhạy cảm.** Log phải ghi rõ gọi Service ID nào, lỗi gì, mã trạng thái bao nhiêu, phục vụ việc đối soát log liên dịch vụ khi điều tra sự cố. Tuyệt đối không in mật khẩu hay chuỗi JWT đầy đủ ra log.
3. **Hướng phát triển: Circuit Breaker (ngắt mạch).** Khi tỉ lệ lỗi gọi Provider vượt ngưỡng, bộ ngắt mạch (ví dụ Resilience4j) sẽ "mở" và trả lỗi ngay lập tức trong một khoảng thời gian, thay vì tiếp tục gửi request vào một dịch vụ đã chết. Cách này giúp Provider có thời gian hồi phục và Consumer không phải chờ timeout cho từng request. Hệ thống PitchOS hiện dùng timeout kết hợp phân loại lỗi; Circuit Breaker được ghi nhận là bước nâng cấp tiếp theo (xem Phần 7 — Đánh giá và kết luận).

---

## 4. KẾT LUẬN

Giao tiếp Consumer → Provider trong kiến trúc hướng dịch vụ không chỉ là "gọi một API HTTP". Nó đòi hỏi ba cam kết kỹ thuật: **phụ thuộc vào hợp đồng chứ không phụ thuộc vào địa chỉ** (gọi qua Service ID), **không tin tưởng mù quáng dữ liệu nhận về** (kiểm tra trước khi dùng), và **xem lỗi của Provider là tình huống chắc chắn xảy ra** chứ không phải ngoại lệ hiếm gặp (timeout, phân loại mã lỗi, không gọi vòng sang CSDL của nhau). Hệ thống PitchOS đã áp dụng cả ba cam kết này tại `pitchos-booking-service`, được chứng minh bằng bộ kiểm thử tích hợp IT01–IT07 trong Phần 3 của báo cáo.
