# CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI VÀ KIẾN TRÚC DỊCH VỤ

*(Linh phụ trách — 2,5 điểm)*

## 1.1. Mô tả bài toán nghiệp vụ

Quy trình quản lý tại đa số cụm sân bóng đá mini hiện nay vẫn thủ công. Khách hàng phải gọi điện hoặc nhắn tin từng cụm sân để hỏi giờ trống, không nắm được đơn giá và chất lượng mặt sân. Chủ sân ghi lịch bằng sổ tay hoặc Excel rời rạc, nên trong khung giờ cao điểm (17h30 – 20h30) rất dễ ghi trùng lịch (*double booking*) dẫn tới tranh chấp sân.

Từ thực trạng đó, nhóm thực hiện đề tài **"Xây dựng hệ thống quản lý đặt lịch sân bóng đá"**, đặt tên **PitchOS** (*Pitch Operating System*), gồm ba nhóm chức năng: khách hàng tra cứu danh mục sân theo quy mô (sân 5, 7, 10) kèm đơn giá và địa chỉ; khách hàng đặt sân trực tuyến theo khung giờ với hệ thống tự kiểm tra trùng lịch và tính tổng tiền; chủ sân đăng sân mới, đổi trạng thái sân giữa `hoat_dong` và `bao_tri`, duyệt hoặc từ chối đơn.

## 1.2. Tổng quan kiến trúc hướng dịch vụ (SOA)

*(Câu 1 – Ý 1a: 0,5đ)*

### 1.2.1. Bốn đặc tính cơ bản của SOA

Kiến trúc hướng dịch vụ (SOA) chia chức năng nghiệp vụ thành các đơn vị phần mềm độc lập gọi là **Dịch vụ (Service)**, giao tiếp qua mạng bằng giao thức chuẩn hóa, không phụ thuộc nền tảng hay ngôn ngữ bên dưới.

[TABLE] Bảng 1.1. Bốn đặc tính cốt lõi của SOA và ứng dụng trong PitchOS

| Đặc tính | Bản chất | Ứng dụng trong PitchOS |
| :--- | :--- | :--- |
| **Liên kết lỏng** | Giảm phụ thuộc trực tiếp; dịch vụ đổi bên trong không phá vỡ dịch vụ khác | Booking Service lấy đơn giá sân bằng request HTTP tới API Pitch Service, **không** nối trực tiếp vào `pitchos_pitch_db` |
| **Hợp đồng chuẩn hóa** | Mỗi dịch vụ công bố bản mô tả giao tiếp chính thức: giao thức, định dạng, tham số, kết quả | HTTP/REST + JSON, đặc tả tự động theo chuẩn OpenAPI v3 tại `/swagger-ui.html` |
| **Tính trừu tượng** | Che giấu chi tiết cài đặt, chỉ để lộ phần công bố trong hợp đồng | Phía gọi chỉ cần `GET /api/v1/pitches/1`, không cần biết dịch vụ viết bằng gì hay lưu ở đâu |
| **Khả năng tái sử dụng** | Logic đóng gói đủ tổng quát để dùng lại trong nhiều ngữ cảnh | `GET /api/v1/pitches/{id}` dùng cho cả Web khách hàng, trang quản trị chủ sân và Booking Service |

### 1.2.2. Phân biệt Dịch vụ, API và Ứng dụng khách

[TABLE] Bảng 1.2. Phân biệt Dịch vụ (Service), API và Ứng dụng khách (Client)

| Tiêu chí | Dịch vụ (Service) | API | Ứng dụng khách (Client) |
| :--- | :--- | :--- | :--- |
| **Bản chất** | Thành phần độc lập, có logic nghiệp vụ và dữ liệu riêng | Cổng giao tiếp kỹ thuật, là hợp đồng giữa các thành phần | Bên chủ động gửi request để dùng tài nguyên của dịch vụ |
| **Trách nhiệm** | Xử lý trọn nghiệp vụ: CRUD, kiểm tra dữ liệu, lưu đĩa | Định nghĩa URI, HTTP Method, Header, Request/Response JSON | Nhận tương tác người dùng, gửi request, hiển thị kết quả |
| **Ví dụ trong PitchOS** | Tiến trình `pitchos-pitch-service` cổng 8082 | `GET /api/v1/pitches`, `POST /api/v1/pitches` | Web React/Next.js, Postman, hoặc Booking Service (8083) |

## 1.3. Phân rã dịch vụ và nguyên lý SRP

*(Câu 1 – Ý 1b: 1,0đ)*

### 1.3.1. Danh mục dịch vụ và trách nhiệm nghiệp vụ

[TABLE] Bảng 1.3. Ba microservice của hệ thống PitchOS

| Microservice | Cổng | CSDL sở hữu | Trách nhiệm nghiệp vụ |
| :--- | :---: | :--- | :--- |
| **Auth & User Service** | 8081 | `pitchos_user_db` | Quản lý tài khoản, băm mật khẩu BCrypt, cấp và xác thực JWT cho 3 vai trò `admin`, `chusan`, `user` |
| **Pitch Service** *(Linh)* | 8082 | `pitchos_pitch_db` | Quản lý danh mục sân (quy mô, đơn giá, địa chỉ) và trạng thái `hoat_dong` / `bao_tri` |
| **Booking Service** | 8083 | `pitchos_booking_db` | Điều phối đặt sân, chống trùng lịch, gọi Pitch Service lấy giá, quản lý vòng đời đơn `cho_duyet` / `da_duyet` / `tu_choi` |

### 1.3.2. Đặc tả 03 API tiêu biểu

[TABLE] Bảng 1.4. Ba API tiêu biểu phục vụ luồng nghiệp vụ cốt lõi

| API | Phương thức & URI | Dịch vụ | Dữ liệu trao đổi |
| :--- | :--- | :---: | :--- |
| Xác thực đăng nhập | `POST /api/v1/auth/login` | Auth (8081) | Gửi `username` + `password`; trả `200` kèm `Bearer <JWT>` chứa `role` |
| Tra cứu thông tin sân | `GET /api/v1/pitches/{id}` | Pitch (8082) | Gửi `id`; trả `200` kèm `pricePerHour`, `status`; không có sân trả `404` |
| Tạo đơn đặt sân | `POST /api/v1/bookings` | Booking (8083) | Gửi JWT + `pitchId`, `startTime`, `endTime`; kiểm tra trùng lịch, gọi API (2) lấy giá, trả `201` |

### 1.3.3. Luận giải theo nguyên lý Đơn trách nhiệm (SRP)

SRP quy định *"mỗi dịch vụ chỉ nên có một và chỉ một lý do để thay đổi"*. Ba dịch vụ của PitchOS có ba lý do thay đổi tách biệt: Auth Service chỉ đổi khi chính sách bảo mật đổi (thuật toán băm, thời hạn token, thêm OAuth2); Pitch Service chỉ đổi khi nghiệp vụ cơ sở vật chất đổi (thêm loại sân, thêm tiện ích); Booking Service chỉ đổi khi quy trình điều phối đơn đổi (khuyến mãi, cổng thanh toán). Nhờ đó hệ thống đạt ba lợi ích: **triển khai độc lập** (build lại Pitch Service không cần restart hai dịch vụ còn lại), **cô lập lỗi** (Auth Service nghẽn thì vẫn xem được danh sách sân) và **mở rộng chọn lọc** (chỉ nhân bản dịch vụ chịu tải đọc cao).

### 1.3.4. Sơ đồ kiến trúc tổng thể

![Hình 1.1. Kiến trúc tổng thể PitchOS: tầng ứng dụng khách, tầng microservice và tầng dữ liệu độc lập](IMG:image2.png)

## 1.4. Thiết kế và triển khai RESTful API (Pitch Service)

*(Câu 2 – Ý 1: 1,0đ)*

### 1.4.1. Danh mục endpoint và phương thức HTTP

Pitch Service xây dựng 4 endpoint chuẩn RESTful, dùng danh từ số nhiều `/api/v1/pitches` và phương thức HTTP đúng ngữ nghĩa:

[TABLE] Bảng 1.5. Danh mục endpoint RESTful của Pitch Service

| Method & URI | Quyền | Mã trả về | Chức năng |
| :--- | :---: | :---: | :--- |
| `GET /api/v1/pitches` | Công khai | `200` | Danh sách sân; hỗ trợ `?pitchType=`, `?status=` |
| `GET /api/v1/pitches/{id}` | Công khai | `200`, `404` | Chi tiết một sân — endpoint cho Booking Service gọi sang |
| `POST /api/v1/pitches` | `chusan`, `admin` | `201`, `400`, `401`, `403` | Thêm sân mới, trả header `Location` |
| `PATCH /api/v1/pitches/{id}/status` | `chusan`, `admin` | `200`, `400`, `401`, `403`, `404` | Cập nhật từng phần trạng thái sân |

### 1.4.2. Kiểm tra dữ liệu đầu vào và chuẩn phản hồi 400 Bad Request

Để ngăn dữ liệu phi lý, lớp `CreatePitchRequest` khai báo ràng buộc theo chuẩn **Jakarta Bean Validation 3.0**: `@NotBlank` cho `name` và `address`, `@NotNull` cho `pitchType`, `@NotNull @Positive` cho `pricePerHour`, `@Size` giới hạn độ dài; controller đánh dấu tham số bằng `@Valid` nên Spring MVC tự kiểm tra trước khi vào tầng nghiệp vụ. Khi có vi phạm, Spring ném `MethodArgumentNotValidException`; lớp `GlobalExceptionHandler` (`@RestControllerAdvice`) bắt ngoại lệ, gom lỗi từng trường thành map `errors` trong khuôn `ErrorResponse` dùng chung cho cả ba dịch vụ. Phản hồi thực tế khi gửi `name` rỗng và `pricePerHour` âm:

```json
{ "status": 400, "error": "Bad Request", "path": "/api/v1/pitches",
  "message": "Dữ liệu đầu vào không hợp lệ. Vui lòng kiểm tra lại các trường vi phạm.",
  "errors": {
    "name": "Tên sân bóng không được để trống",
    "pricePerHour": "Đơn giá thuê mỗi giờ phải lớn hơn 0",
    "address": "Địa chỉ sân không được để trống" } }
```

### 1.4.3. Tài liệu hóa API với OpenAPI 3.0 / Swagger UI

Pitch Service tích hợp `springdoc-openapi-starter-webmvc-ui`, tự sinh tài liệu OpenAPI v3 tại `http://localhost:8082/swagger-ui.html` (bản JSON tại `/api-docs`), hiển thị đủ endpoint kèm tham số và response mẫu. Lớp `OpenApiConfig` khai báo `SecurityScheme` kiểu Bearer nên người kiểm thử chỉ cần bấm **Authorize**, dán JWT là thử được cả các API được bảo vệ ngay trên web.

# CHƯƠNG 2. THIẾT KẾ API VÀ GIAO TIẾP DỊCH VỤ

*(Nhật phụ trách — 2,25 điểm)*

## 2.1. Cơ chế giao tiếp giữa các dịch vụ qua HTTP/REST

*(Câu 1 – Ý 2a: 0,75đ)*

### 2.1.1. Quy trình trao đổi thông tin giữa Booking Service và Pitch Service

Nghiệp vụ minh họa: **khách hàng tạo đơn đặt sân**. Booking Service không sở hữu dữ liệu giá và trạng thái sân (nằm trong `pitchos_pitch_db`) nên phải hỏi Pitch Service qua API:

1. Booking Service nhận request đặt sân chứa `pitchId`, `startTime`, `endTime` kèm JWT để biết người đặt.
2. Booking Service đóng vai **Client**, gửi `GET /api/v1/pitches/{id}` sang Pitch Service lấy `pricePerHour` và `status`.
3. Pitch Service trả JSON thông tin sân, hoặc `404` nếu sân không tồn tại.
4. Booking Service kiểm tra trùng lịch trong CSDL của mình, tính `totalPrice = số giờ × pricePerHour`, lưu đơn `cho_duyet` và trả `201 Created`.

### 2.1.2. Cấu trúc HTTP Request và HTTP Response

HTTP/REST là giao thức **đồng bộ, phi trạng thái**: mỗi request tự mang đủ thông tin (kể cả danh tính qua token), server không lưu phiên; dữ liệu trao đổi bằng JSON.

[TABLE] Bảng 2.1. Cấu trúc HTTP Request / Response trong nghiệp vụ đặt sân

| Thành phần | HTTP Request | HTTP Response |
| :--- | :--- | :--- |
| Dòng đầu | `POST /api/v1/bookings HTTP/1.1` | `HTTP/1.1 201 Created` |
| Headers | `Authorization: Bearer <token>`, `Content-Type: application/json` | `Content-Type: application/json` |
| Body | `{"pitchId":1,"startTime":"2026-10-30T18:00:00","endTime":"2026-10-30T19:30:00"}` | `{"id":2,"pitchId":1,"totalPrice":450000.00,"status":"cho_duyet"}` |

### 2.1.3. Ý nghĩa các nhóm mã trạng thái HTTP

[TABLE] Bảng 2.2. Các nhóm mã trạng thái HTTP dùng trong hệ thống

| Nhóm | Ý nghĩa | Mã dùng trong Booking Service |
| :---: | :--- | :--- |
| **2xx** | Thành công | `200` (xem lịch sử, duyệt đơn), `201` (tạo đơn) |
| **4xx** | Lỗi phía client | `400` (dữ liệu sai, trùng lịch, sân bảo trì), `401` (chưa đăng nhập, token sai/hết hạn), `403` (sai vai trò), `404` (sân hoặc đơn không tồn tại) |
| **5xx** | Lỗi phía server | `500` (lỗi nội bộ), `503` (dịch vụ phụ thuộc tạm thời không khả dụng) |

Client nhìn nhóm mã để biết **phải sửa request (4xx)** hay **thử lại sau (5xx)**. Vì vậy khi Pitch Service sập, Booking Service phải trả `503` chứ không trả `500`.

### 2.1.4. Nguy cơ sụp đổ dây chuyền (Cascading Failure) và giải pháp

Booking Service gọi Pitch Service theo cơ chế đồng bộ. Nếu Pitch Service treo, mỗi request đặt sân giữ một luồng của Booking Service để chờ; khi request dồn lại, thread pool cạn kiệt (*thread pool starvation*) khiến Booking Service không phục vụ được cả những API không liên quan và sập theo — lỗi lan dây chuyền. Ba biện pháp đã áp dụng:

1. **Timeout:** kết nối tối đa 2 giây, đọc tối đa 3 giây (`spring.cloud.openfeign.client.config.pitch-service.*`), luồng không bị treo vô hạn.
2. **Chuyển lỗi mạng thành 503:** Feign ném `RetryableException` → `GlobalExceptionHandler` trả `503` kèm thông báo thân thiện, không để thành `500`.
3. **Cô lập ảnh hưởng:** khi Pitch Service tắt, API không cần tới nó (`GET /my-bookings`) vẫn trả `200` — đã kiểm chứng thực tế.

Hướng mở rộng: Circuit Breaker (Resilience4j), retry có giới hạn, cache giá sân làm fallback.

## 2.2. Triển khai giao tiếp liên dịch vụ với Spring Cloud OpenFeign

*(Câu 2 – Ý 2: 1,5đ)*

### 2.2.1. Khởi tạo Feign Client

```java
@FeignClient(name = "pitch-service", url = "${pitch.service.url:http://localhost:8082}")
public interface PitchClient {
    @GetMapping("/api/v1/pitches/{id}")
    PitchResponseDTO getPitchById(@PathVariable("id") Long id);
}
```

Lớp khởi động khai báo `@EnableFeignClients`; OpenFeign tự sinh phần cài đặt gửi HTTP request và chuyển JSON trả về thành `PitchResponseDTO` (`id`, `name`, `pricePerHour`, `status`). URL Pitch Service đọc từ cấu hình `pitch.service.url`, không viết cứng trong mã nguồn.

### 2.2.2. Các nghiệp vụ điều phối đặt sân

[TABLE] Bảng 2.3. API của Booking Service (cổng 8083)

| Method & Endpoint | Vai trò | Mô tả | Thành công |
| :--- | :---: | :--- | :---: |
| `POST /api/v1/bookings` | `user` | Tạo đơn đặt sân, gọi Pitch Service lấy giá | `201` |
| `GET /api/v1/bookings/my-bookings` | `user` | Danh sách đơn của người dùng trong token | `200` |
| `PATCH /api/v1/bookings/{id}/status` | `chusan`, `admin` | Duyệt (`da_duyet`) hoặc từ chối (`tu_choi`) | `200` |

Sáu bước trong `BookingService.createBooking`: (1) `endTime` phải sau `startTime`, sai → `400`; (2) gọi `pitchClient.getPitchById(pitchId)`, sân không tồn tại → `404`, Pitch Service tắt → `503`; (3) sân không ở trạng thái `hoat_dong` → `400`; (4) tính `totalPrice = pricePerHour × số phút / 60`; (5) khóa theo sân rồi gọi `countOverlappingBookings` (truy vấn của Hùng, bỏ qua đơn `tu_choi`), kết quả > 0 → `400`; (6) lưu đơn `cho_duyet`, nhả khóa, trả `201`. Lời gọi Pitch Service đặt **trước** bước kiểm tra trùng lịch để kịch bản demo "tắt Pitch Service rồi gửi lại request vừa đặt" luôn đi tới lời gọi liên dịch vụ và trả `503`.

**Chống đặt trùng khi nhiều khách gửi cùng lúc.** Nếu hai request cùng kiểm tra trùng lịch (đều thấy trống) rồi mới lưu thì cả hai đều được lưu, tức một khung giờ bị đặt hai lần — kiểm thử phiên bản chưa khóa với 5 request đồng thời cho đúng hiện tượng này. Vì vậy bước 5–6 được đặt trong khối `synchronized` theo `pitchId`: các request **cùng sân** phải lần lượt "kiểm tra → lưu", các sân khác vẫn chạy song song; lời gọi Pitch Service nằm ngoài khóa nên không chặn request khác. Hạn chế: khóa nằm trong bộ nhớ tiến trình, chỉ đúng khi chạy một instance; khi mở rộng nhiều instance cần khóa ở tầng CSDL (`SELECT … FOR UPDATE`) hoặc khóa phân tán.

## 2.3. Sơ đồ tuần tự và cơ chế xử lý lỗi phân tán

*(Câu 2 – Ý 2: 1,5đ)*

![Hình 2.1. Sơ đồ tuần tự nghiệp vụ đặt sân thành công — 201 Created](IMG:image3.jpeg)

![Hình 2.2. Sơ đồ tuần tự khi dịch vụ đích lỗi — 404 Not Found và 503 Service Unavailable](IMG:image4.jpeg)

Hai nhánh lỗi được xử lý ở hai chỗ khác nhau: **Pitch Service có phản hồi 404** → `CustomErrorDecoder` chuyển thành `ResourceNotFoundException` → client nhận `404`; **Pitch Service không phản hồi** (tắt tiến trình, mất mạng, quá thời gian chờ) → không có response để decode, Feign ném `RetryableException` → `GlobalExceptionHandler` trả `503`:

```java
@ExceptionHandler({FeignException.class, RetryableException.class})
public ResponseEntity<ErrorResponse> handlePitchServiceUnavailable(FeignException ex) {
    log.warn("Không gọi được Pitch Service: {}", ex.getMessage());
    return build(HttpStatus.SERVICE_UNAVAILABLE,
                 "Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!");
}
```

Khi đó Booking Service không bị dừng, không trả `500` và không ghi đơn xuống CSDL. Toàn bộ 20 ca kiểm thử Booking Service (gồm ca 503, ca trùng lịch, ca 10 request đồng thời) đặt tại Phụ lục B; kết quả tổng hợp ở mục 5.1.

# CHƯƠNG 3. QUẢN LÝ DỮ LIỆU PHÂN TÁN

*(Hùng phụ trách — 2,25 điểm)*

## 3.1. Nguyên tắc quản lý dữ liệu độc lập

*(Câu 1 – Ý 2b: 0,75đ)*

### 3.1.1. Bản chất nguyên tắc Database-per-Service

Trong hệ thống nguyên khối (Monolithic), mọi mô-đun dùng chung một CSDL nên dễ tạo khóa ngoại và câu JOIN, nhưng đổi lại là phụ thuộc chặt chẽ và triệt tiêu tính độc lập của dịch vụ. PitchOS áp dụng nghiêm ngặt **Database-per-Service** với ba quy tắc: (1) **quyền sở hữu độc quyền** — mỗi microservice sở hữu toàn bộ CSDL thuộc miền nghiệp vụ của mình; (2) **tính đóng gói** — tuyệt đối không dịch vụ nào đọc hoặc ghi trực tiếp vào CSDL của dịch vụ khác; (3) **truy xuất qua API** — mọi nhu cầu đọc/ghi từ bên ngoài đều đi qua RESTful API do chính dịch vụ sở hữu dữ liệu cung cấp.

### 3.1.2. Bốn rủi ro kỹ thuật khi vi phạm

1. **Ghép nối lược đồ (Schema Coupling):** dịch vụ A đổi tên hoặc xóa cột thì dịch vụ B, C đang đọc bảng đó lỗi ngay thời gian chạy, buộc phải kiểm thử và triển khai đồng thời cả hệ thống — mất khả năng phát hành độc lập.
2. **Deadlock chéo giữa các dịch vụ:** transaction từ nhiều dịch vụ tranh chấp khóa dòng và khóa bảng; Service 1 giữ khóa bảng A chờ bảng B trong khi Service 2 giữ bảng B chờ bảng A sẽ treo toàn bộ thread pool.
3. **Phá vỡ bao đóng nghiệp vụ:** nếu Booking Service tự cập nhật bảng `pitches` thay vì gọi API Pitch Service thì mọi quy tắc nghiệp vụ và kiểm tra hợp lệ của Pitch Service bị bỏ qua.
4. **Cản trở mở rộng độc lập:** không scale riêng được CSDL của dịch vụ chịu tải cao, cũng không áp dụng được lưu trữ đa dạng (Polyglot Persistence) như cache Redis cho tra cứu sân, RDBMS cho ghi đơn.

## 3.2. Thiết kế cơ sở dữ liệu phân tán

*(Câu 2 – Ý 3: 1,5đ)*

[TABLE] Bảng 3.1. Ba cơ sở dữ liệu MySQL 8.0 độc lập của PitchOS

| CSDL (bảng) | Dịch vụ sở hữu | Các trường chính |
| :--- | :--- | :--- |
| `pitchos_user_db` (`users`) | Auth (8081) | `id` PK; `username`, `email` UNIQUE; `password` (băm BCrypt); `full_name`; `phone`; `role` `ENUM('admin','chusan','user')` mặc định `user`; `created_at` |
| `pitchos_pitch_db` (`pitches`) | Pitch (8082) | `id` PK; `name`; `pitch_type` `ENUM('san_5','san_7','san_10')`; `price_per_hour` `DECIMAL(12,2)`; `address`; `status` `ENUM('hoat_dong','bao_tri')`; `created_at` |
| `pitchos_booking_db` (`bookings`) | Booking (8083) | `id` PK; `user_id`, `pitch_id` *(Logical ID)*; `start_time`; `end_time`; `total_price` `DECIMAL(12,2)`; `status` `ENUM('cho_duyet','da_duyet','tu_choi')`; `created_at` |

**Khẳng định kỹ thuật then chốt:** trong bảng `bookings`, `user_id` và `pitch_id` chỉ là `BIGINT NOT NULL` thông thường — **không tồn tại** mệnh đề `FOREIGN KEY … REFERENCES pitches(id)`. Toàn vẹn dữ liệu được bảo đảm bằng **Logical ID** cộng lời gọi `GET /api/v1/pitches/{id}` để xác minh sân trước khi ghi đơn. Đây là bằng chứng tuân thủ nguyên tắc cách ly dữ liệu. Script SQL đầy đủ: xem Phụ lục C.

![Hình 3.1. Sơ đồ quan hệ thực thể phân tán (Distributed ERD) — ba schema độc lập, liên kết bằng Logical ID](IMG:image6.png)

## 3.3. Tầng dữ liệu JPA Entity và Repository

Tầng truy cập dữ liệu dùng **Spring Data JPA** kết hợp **Hibernate ORM**. Ba lớp thực thể `User`, `Pitch`, `Booking` khai báo `@Entity` và `@Table` trỏ tới ba bảng nêu trên; trường kiểu liệt kê ánh xạ bằng `@Enumerated(EnumType.STRING)` để giá trị trong Java trùng khớp `ENUM` của MySQL; `createdAt` dùng `@CreationTimestamp`; `pricePerHour` và `totalPrice` dùng `BigDecimal` với `@Column(precision = 12, scale = 2)` nhằm triệt tiêu sai số làm tròn khi tính tiền. Riêng `Booking` ánh xạ `user_id` và `pitch_id` thành hai thuộc tính `Long` độc lập, **không** dùng `@ManyToOne`, đúng tinh thần Logical ID.

Các interface Repository kế thừa `JpaRepository<T, ID>` nên có sẵn `save`, `findById`, `findAll`, `deleteById`, cùng truy vấn dẫn xuất theo tên phương thức: `UserRepository` có `findByUsername`, `existsByUsername`, `existsByEmail`; `PitchRepository` có `findByPitchType`, `findByStatus`, `findByPitchTypeAndStatus` phục vụ lọc danh sách sân công khai.

## 3.4. Giải thuật chống trùng lịch thi đấu

Một sân tại một thời điểm chỉ cho một đội thuê, nên trùng lịch (*double booking*) là rủi ro nghiệp vụ lớn nhất. Gọi đơn đã có là `[start_old, end_old]`, đơn mới là `[start_new, end_new]`; hai khoảng **giao nhau** khi và chỉ khi đồng thời `start_old < end_new` **và** `end_old > start_new`. Điều kiện kép duy nhất này phủ hết bốn tình huống trùng: đơn mới bắt đầu trước và kết thúc giữa; bắt đầu giữa và kết thúc sau; nằm hoàn toàn bên trong; bao trùm toàn bộ. Đơn đã bị chủ sân từ chối (`status = 'tu_choi'`) được coi là khung giờ trống. Truy vấn JPQL trong `BookingRepository`:

```java
@Query("SELECT COUNT(b) FROM Booking b " +
       "WHERE b.pitchId = :pitchId " +
       "  AND b.status <> com.pitchos.booking.entity.BookingStatus.tu_choi " +
       "  AND b.startTime < :endTime AND b.endTime > :startTime")
Long countOverlappingBookings(@Param("pitchId") Long pitchId,
                              @Param("startTime") LocalDateTime startTime,
                              @Param("endTime") LocalDateTime endTime);
```

Dùng `COUNT(b)` để MySQL chỉ trả về một con số, không tải tập thực thể vào RAM. Kết quả `> 0` → ném ngoại lệ *"Khung giờ này sân đã có người đặt"* (`400`); bằng `0` → tiếp tục tính tiền và lưu đơn.

## 3.5. Kiểm chứng dữ liệu lưu đĩa cứng

Ba script SQL nạp sẵn dữ liệu ban đầu: 3 tài khoản (`admin`, `chusan`, `user`); 4 sân (Cầu Giấy 300.000đ/h, Mỹ Đình 500.000đ/h, Tây Hồ 800.000đ/h, Phúc Diễn đang bảo trì); 1 đơn mẫu. Thao tác kiểm chứng: khách `user` (ID 3) đặt sân ID 1 từ 18:00 đến 19:30 — hệ thống chạy truy vấn chống trùng lịch (trả `0`), gọi OpenFeign lấy đơn giá 300.000đ/h, tính `1,5 × 300.000 = 450.000đ`, rồi `bookingRepository.save()` ghi đĩa trạng thái `cho_duyet`. Sau khi nhận `201 Created`, truy vấn trực tiếp trên DBeaver:

```sql
SELECT id, user_id, pitch_id, start_time, end_time, total_price, status
FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1;
```

Kết quả: bản ghi mới xuất hiện ngay, `status = 'cho_duyet'`, `total_price = 450000.00`, `pitch_id = 1` và `user_id = 3` lưu đúng dạng Logical ID — xác nhận dữ liệu đã ghi đĩa và toàn vẹn.

# CHƯƠNG 4. XÁC THỰC VÀ BẢO MẬT HỆ THỐNG

*(Hoàng phụ trách — 3,0 điểm)*

## 4.1. Cơ chế xác thực và phân quyền dịch vụ

*(Câu 1 – Ý 3: 1,0đ)*

### 4.1.1. Phân biệt Authentication và Authorization

[TABLE] Bảng 4.1. Phân biệt xác thực và phân quyền

| Tiêu chí | Authentication (Xác thực) | Authorization (Phân quyền) |
| :--- | :--- | :--- |
| **Câu hỏi trả lời** | *"Bạn là ai?"* — đối chiếu `username` + `password` | *"Bạn được phép làm gì?"* — đối chiếu vai trò và quyền sở hữu |
| **Thời điểm & kết quả** | Một lần khi đăng nhập, cấp phát JWT Access Token | Mọi lần gọi API về sau, cho phép hoặc từ chối thao tác |
| **Vị trí trong PitchOS** | `AuthService.login()` + `JwtTokenProvider` | `SecurityConfig` + kiểm tra quyền sở hữu tại `AuthService` |
| **Mã lỗi khi thất bại** | **401 Unauthorized** | **403 Forbidden** |

Cốt lõi về trình tự: **xác thực luôn đi trước phân quyền** — không thể quyết định một người được làm gì nếu chưa biết người đó là ai. Ngược lại, xác thực thành công không đồng nghĩa được phép truy cập: tài khoản `user` đăng nhập hoàn toàn hợp lệ vẫn bị từ chối khi gọi API thêm sân của `chusan`.

### 4.1.2. Cấu trúc ba phần của JSON Web Token

JWT gồm ba phần phân cách bởi dấu chấm, mỗi phần mã hóa Base64Url: `Header.Payload.Signature`. **Header** khai báo thuật toán ký — token của PitchOS giải mã ra `{ "alg": "HS256" }`. **Payload (Claims)** chứa ngữ cảnh người dùng; đây là payload thật của tài khoản `chusan` thu được khi kiểm thử:

```json
{ "sub": "chusan", "userId": 2, "role": "chusan",
  "fullName": "Trần Văn Chủ Sân", "iat": 1793336101, "exp": 1793422501 }
```

Trong đó `sub` là định danh chính để tra cứu người dùng; `userId` được Booking Service dùng làm principal để gán đơn cho đúng chủ; `role` là căn cứ duy nhất để phân quyền RBAC; `iat` và `exp` giới hạn vòng đời token (24 giờ). Cần nhấn mạnh: **Payload chỉ được mã hóa Base64Url, không phải mã hóa bảo mật** — ai cũng giải mã đọc được, nên tuyệt đối không đặt mật khẩu hay dữ liệu nhạy cảm vào đây.

**Signature** là phần bảo đảm toàn vẹn: `Signature = HMAC-SHA256(Base64Url(Header) + "." + Base64Url(Payload), SECRET_KEY)`. Nếu kẻ tấn công sửa Payload (đổi `"role":"user"` thành `"role":"admin"`) thì chữ ký không còn khớp và server từ chối ngay; kẻ tấn công không tự tạo được chữ ký hợp lệ vì không có `SECRET_KEY`.

**Cơ chế Stateless:** server không lưu session; mỗi request tự gửi kèm token qua header `Authorization: Bearer <token>`, server chỉ cần xác minh chữ ký. Nhờ đó ba dịch vụ của PitchOS tự xác thực độc lập, không cần hỏi lẫn nhau và không cần kho session dùng chung.

### 4.1.3. Phân biệt HTTP 401 Unauthorized và HTTP 403 Forbidden

> **401** = hệ thống **không biết bạn là ai** → thất bại ở tầng Authentication. **403** = hệ thống **biết rõ bạn là ai, nhưng bạn không được phép** → thất bại ở tầng Authorization.

[TABLE] Bảng 4.2. Tình huống sinh mã 401 và 403 trong PitchOS

| Tình huống | Mã | Lớp xử lý |
| :--- | :---: | :--- |
| Không gửi header `Authorization`; token sai chữ ký hoặc đã hết hạn | **401** | `AuthenticationEntryPoint` |
| Sai tên đăng nhập hoặc mật khẩu | **401** | `GlobalExceptionHandler` bắt `UnauthorizedException` |
| `user` gọi API thêm sân; `chusan` gọi API danh sách người dùng của `admin` | **403** | `AccessDeniedHandler` |
| `user` xem thông tin tài khoản người khác | **403** | `AuthService` ném `AccessDeniedException` |

Trả đúng mã không chỉ là hình thức: client gặp **401** thì điều hướng về trang đăng nhập, còn gặp **403** thì hiển thị "bạn không có quyền" và **không** bắt đăng nhập lại, vì đăng nhập lại cũng không giải quyết được gì.

### 4.1.4. Ma trận phân quyền RBAC

Ba vai trò lưu dưới dạng `ENUM('admin','chusan','user')`: `user` là khách thuê sân (xem sân, tạo đơn, xem đơn của mình); `chusan` là chủ sân (quản lý sân, duyệt hoặc từ chối đơn); `admin` là quản trị viên (toàn quyền, gồm quản trị tài khoản).

[TABLE] Bảng 4.3. Ma trận phân quyền RBAC toàn hệ thống

| Endpoint | Method | Công khai | `user` | `chusan` | `admin` | Khi bị từ chối |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `/api/v1/auth/register`, `/login` | POST | ✔ | ✔ | ✔ | ✔ | — |
| `/api/v1/users/me` | GET | ✘ | ✔ | ✔ | ✔ | 401 |
| `/api/v1/users/{id}` | GET | ✘ | Chỉ mình | ✔ | ✔ | 401 / 403 |
| `/api/v1/users` | GET | ✘ | ✘ | ✘ | ✔ | 401 / 403 |
| `/api/v1/pitches` | GET | ✔ | ✔ | ✔ | ✔ | — |
| `/api/v1/pitches` (POST), `/pitches/{id}/status` (PATCH) | POST, PATCH | ✘ | ✘ | ✔ | ✔ | 401 / 403 |
| `/api/v1/bookings` (POST), `/bookings/my-bookings` (GET) | POST, GET | ✘ | ✔ | ✘ | ✘ | 401 / 403 |
| `/api/v1/bookings/{id}/status` | PATCH | ✘ | ✘ | ✔ | ✔ | 401 / 403 |

Ma trận thể hiện nguyên lý **đặc quyền tối thiểu**: `chusan` **không** được tạo đơn đặt sân và `user` **không** được duyệt đơn — quyền hạn không bao hàm theo thứ bậc mà thiết kế theo đúng chức năng nghiệp vụ.

## 4.2. Triển khai Auth & User Service (cổng 8081)

*(Câu 2 – Ý 4: 2,0đ)*

### 4.2.1. Đăng ký tài khoản và băm mật khẩu bằng BCrypt

Cấu trúc bảng `users` đã trình bày ở Bảng 3.1. **Nguyên tắc tối quan trọng: CSDL không bao giờ lưu mật khẩu dạng văn bản thuần** — mật khẩu được băm một chiều bằng `BCryptPasswordEncoder` trước khi lưu. BCrypt được chọn thay cho MD5 hay SHA-1 vì ba đặc tính: **tự sinh salt riêng cho từng mật khẩu** (hai người cùng đặt `123456` vẫn cho hai chuỗi băm khác hẳn nhau, vô hiệu hóa Rainbow Table); **cố tình chạy chậm** (cost factor mặc định 10, tức 2¹⁰ vòng lặp, khiến Brute Force bất khả thi về thời gian); **một chiều, không giải mã ngược** (CSDL bị rò rỉ cũng không lấy lại được mật khẩu gốc).

Luồng `POST /api/v1/auth/register`: `@Valid` kiểm tra dữ liệu (sai → `400` kèm map `errors`) → kiểm tra trùng `username` / `email` (trùng → `400`) → băm mật khẩu → lưu bản ghi → trả `201 Created` kèm header `Location`. Hai quyết định thiết kế đáng lưu ý: **vai trò luôn bị ép thành `user`** bất kể client gửi gì (nếu để client tự khai `role` thì ai cũng tự đăng ký được tài khoản `admin` — lỗ hổng leo thang đặc quyền kinh điển); và **DTO `UserResponse` không có trường `password`** nên chuỗi băm không bao giờ lọt ra ngoài qua API.

### 4.2.2. Đăng nhập và cơ chế sinh Bearer JWT Token

Luồng `POST /api/v1/auth/login`: tra `findByUsername` (không có → `401`) → `passwordEncoder.matches(mậtKhẩuThô, chuỗiBămTrongDB)` (không khớp → `401`) → `JwtTokenProvider.generateToken(user)` → trả `200 OK` kèm `accessToken`, `expiresIn`, `userId`, `username`, `role`. Hàm `matches` trích salt từ chuỗi băm đã lưu, băm lại mật khẩu thô bằng chính salt đó rồi so sánh — **không** giải mã ngược chuỗi băm (điều không thể làm được).

```java
Map<String, Object> claims = new LinkedHashMap<>();
claims.put("userId", user.getId());
claims.put("role", user.getRole().name().toLowerCase());
claims.put("fullName", user.getFullName());
return Jwts.builder().setSubject(user.getUsername()).addClaims(claims)
        .setIssuedAt(now).setExpiration(expiryDate)
        .signWith(key, SignatureAlgorithm.HS256).compact();
```

Một chi tiết nhỏ nhưng sống còn cho tính đồng bộ toàn hệ thống: claim `role` được ghi **viết thường, không tiền tố** (`"chusan"` chứ không phải `"ROLE_CHUSAN"`) — lý do ở mục 4.3.1. **Chống dò quét tài khoản:** sai tên đăng nhập và sai mật khẩu đều trả **cùng một thông báo** *"Tên đăng nhập hoặc mật khẩu không đúng"*; nếu phân biệt hai thông báo, kẻ tấn công có thể dùng API đăng nhập để dò xem tài khoản nào tồn tại (User Enumeration).

## 4.3. Cấu hình bảo vệ API với Spring Security 6

*(Câu 2 – Ý 4: 2,0đ)*

### 4.3.1. JwtAuthenticationFilter

![Hình 4.1. Chuỗi lọc bảo mật: đường đi của một request tới mã 401, 403 hoặc 200/201](IMG:image9.png)

```java
if (authHeader != null && authHeader.startsWith("Bearer ")) {
    try {
        Claims claims = jwtTokenProvider.parseToken(authHeader.substring(7).trim());
        String role = jwtTokenProvider.getRole(claims);
        var authorities = List.of(new SimpleGrantedAuthority("ROLE_" + role.toLowerCase()),
                                  new SimpleGrantedAuthority(role.toLowerCase()));
        SecurityContextHolder.getContext().setAuthentication(
                new UsernamePasswordAuthenticationToken(username, null, authorities));
    } catch (JwtException | IllegalArgumentException ex) {
        SecurityContextHolder.clearContext();   // để EntryPoint sinh 401
    }
}
```

**Vì sao claim `role` phải viết thường và không tiền tố?** Spring Security quy ước `hasRole("chusan")` **tự ghép thêm** tiền tố `ROLE_` rồi mới so sánh, tức nó tìm authority `ROLE_chusan`; bộ lọc của cả ba dịch vụ đều ghép `"ROLE_" + role` từ claim. Do đó nếu Auth Service cấp token với `role = "ROLE_CHUSAN"` thì authority thành `ROLE_ROLE_CHUSAN`, không khớp cấu hình nào, và **toàn bộ API của Pitch lẫn Booking Service sẽ trả 403**. Đây là hợp đồng ngầm giữa ba dịch vụ, bắt buộc giữ nguyên. Bộ lọc nạp đồng thời hai dạng authority (`ROLE_chusan` và `chusan`) để cấu hình viết bằng `hasRole()` hay `hasAuthority()` đều chạy.

### 4.3.2. AuthenticationEntryPoint (401) và AccessDeniedHandler (403)

```java
.authorizeHttpRequests(auth -> auth
        .requestMatchers(HttpMethod.POST, "/api/v1/auth/register", "/api/v1/auth/login").permitAll()
        .requestMatchers("/swagger-ui/**", "/api-docs/**", "/error").permitAll()
        .requestMatchers(HttpMethod.GET, "/api/v1/users").hasRole("admin")
        .anyRequest().authenticated())
.exceptionHandling(ex -> ex.authenticationEntryPoint(authenticationEntryPoint())  // 401
                           .accessDeniedHandler(accessDeniedHandler()))           // 403
.sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
```

Cấu hình `STATELESS` là bắt buộc với JWT: Spring Security không tạo `HttpSession`, mỗi request được xác thực độc lập dựa trên token. Hai bộ xử lý lỗi trả JSON đúng khuôn `ErrorResponse` mà Pitch và Booking Service dùng (`timestamp`, `status`, `error`, `message`, `path`), nên client chỉ xử lý một định dạng lỗi duy nhất cho cả hệ thống.

**Kiểm tra quyền sở hữu tài nguyên.** Phân quyền theo vai trò là chưa đủ: tài khoản `user` ID 3 gọi `GET /api/v1/users/1` để xem thông tin `admin` — token hợp lệ, vai trò `user` cũng được phép gọi endpoint này, nên nếu chỉ dựa vào vai trò thì dữ liệu người khác bị lộ. Nguyên tắc là **không tin tưởng ID do client gửi lên**: tầng nghiệp vụ `AuthService` so `current.getId()` với `target.getId()`, nếu vai trò là `user` mà hai ID khác nhau thì ném `AccessDeniedException`. Lưu ý kỹ thuật: ngoại lệ này **phải có handler tường minh** trong `GlobalExceptionHandler`, vì `@RestControllerAdvice` chạy bên trong `DispatcherServlet`, tức ở *phía trong* `ExceptionTranslationFilter` của Spring Security; không khai báo riêng thì nó bị handler `Exception.class` bắt trước và bị gói thành **500** thay vì 403.

### 4.3.3. Đồng bộ Secret Key bảo vệ liên dịch vụ

Mỗi dịch vụ phải tự xác minh được token mà không cần gọi về Auth Service. Điều này đạt được bằng cách **ba dịch vụ dùng chung một `SECRET_KEY`**, khai báo tập trung ở file `.env` và nạp qua `application.properties` (`jwt.secret=${JWT_SECRET:…}`, `JWT_EXPIRATION_MS=86400000`). Ba điều kiện bắt buộc để token dùng chung được cả hệ thống: (1) **cùng `SECRET_KEY`** — khác key thì chữ ký không khớp; (2) **cùng cách nạp key** — cả ba dùng `Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret))`, nếu một dịch vụ nạp kiểu khác (`secret.getBytes()`) thì dù chuỗi secret giống nhau, mảng byte khóa vẫn khác và chữ ký lệch; (3) **cùng hợp đồng claim** — `role` viết thường không tiền tố, và `userId` **bắt buộc phải có** vì Booking Service dùng nó làm principal để gán đơn.

# CHƯƠNG 5. KIỂM THỬ, KẾT QUẢ VÀ TỰ ĐÁNH GIÁ

*(Hoàng chủ trì, cả nhóm phối hợp)*

## 5.1. Môi trường, phạm vi và kết quả kiểm thử

### 5.1.1. Môi trường thực nghiệm

Java 17, Spring Boot 3.2.5, Spring Security 6, JJWT 0.11.5, MySQL 8.0 (Docker container `pitchos-mysql`), SpringDoc OpenAPI 2.5.0; công cụ kiểm thử gồm cURL tự động hóa bằng script Bash và Postman Collection.

> **Ghi chú về cổng dịch vụ:** cổng chuẩn của dự án là Auth 8081, Pitch 8082, Booking 8083, MySQL 3306; nhưng trên máy thực nghiệm cổng 8081 và 3306 đang bị dự án khác chiếm dụng nên đợt kiểm thử này chạy trên **cổng thay thế Auth 18081, Pitch 18082, MySQL 3307** qua biến môi trường `AUTH_SERVICE_PORT`, `PITCH_SERVICE_PORT`, `MYSQL_PORT`. Việc đổi cổng không ảnh hưởng logic nghiệp vụ hay kết quả bảo mật vì toàn bộ cấu hình cổng đều tham số hóa qua `.env`.

### 5.1.2. Phạm vi đã kiểm chứng và kết quả

[TABLE] Bảng 5.1. Tổng hợp kết quả kiểm thử theo nhóm ca

| Nhóm ca kiểm thử | Phụ trách | Số ca | Đạt | Trạng thái |
| :--- | :---: | :---: | :---: | :--- |
| Đăng nhập 3 vai trò và kiểm chứng cấu trúc JWT | Hoàng | 10 | 10 | Đã chạy thực tế |
| Xác thực 401 và validation 400 | Hoàng | 10 | 10 | Đã chạy thực tế |
| Phân quyền RBAC và quyền sở hữu 403 | Hoàng | 11 | 11 | Đã chạy thực tế |
| Liên dịch vụ Auth → Pitch (401/403/201) | Hoàng + Linh | 5 | 5 | Đã chạy thực tế |
| **Tổng đợt kiểm thử bảo mật** | | **36** | **36** | **Đạt 36/36, không có ca lỗi** |
| Booking Service: 503, trùng lịch, đặt đồng thời | Nhật | 20 | 20 | Chạy với Pitch Service giả lập; cần chạy lại với dịch vụ thật |
| Validation 400 + Swagger (Pitch), ghi dữ liệu xuống đĩa | Linh, Hùng | — | — | Hai bạn tự kiểm chứng (mục 1.4, 3.5) |

Ma trận chi tiết từng ca (mã ca, endpoint, dữ liệu vào, mã mong đợi, kết quả) đặt tại Phụ lục B cùng bộ Postman Collection.

[TABLE] Bảng 5.2. Các ca kiểm thử tiêu biểu về bảo mật

| Mã | Ca kiểm thử | Mong đợi | Kết quả |
| :---: | :--- | :---: | :---: |
| TC03 | Đăng ký sai quy cách (email sai, mật khẩu 3 ký tự, họ tên trống) | `400` + map `errors` | Đạt |
| TC06 | Gọi API được bảo vệ, không gửi token | `401` | Đạt |
| TC07 | Token tự bịa payload `role: admin`, sai chữ ký | `401` | Đạt |
| TC09 / TC11 | `user` / `admin` gọi API danh sách người dùng | `403` / `200` | Đạt |
| TC12 | `user` xem thông tin tài khoản khác (quyền sở hữu) | `403` | Đạt |
| TC-X2 / TC-X3 | `POST /api/v1/pitches` bằng token `user` / token `chusan` | `403` / `201` | Đạt |

**TC07 đáng chú ý nhất về mặt bảo mật:** token trong ca này có payload giải mã ra `{"sub":"hacker","role":"admin"}` — kẻ tấn công tự khai là admin — nhưng hệ thống vẫn từ chối với mã 401 vì chữ ký không được tạo bằng `SECRET_KEY`; đây là minh chứng thực nghiệm cho giá trị của chữ ký HMAC-SHA256 ở mục 4.1.2. **Nhóm TC-X có ý nghĩa kiến trúc quan trọng nhất:** token do Auth Service cấp được Pitch Service — một tiến trình độc lập, CSDL riêng, không hề gọi về Auth Service để hỏi — giải mã và phân quyền chính xác, tức đặc tính Stateless của JWT và hợp đồng token dùng chung giữa ba dịch vụ đã được kiểm chứng bằng thực nghiệm.

### 5.1.3. Minh chứng kết quả thực nghiệm

- **Swagger UI:** `/swagger-ui.html` và `/api-docs` đều trả `200`; Auth Service sinh đủ 5 endpoint, có nút **Authorize** theo chuẩn `SecurityScheme` Bearer.
- **Postman Collection:** 16 request chia 5 thư mục (đăng nhập 3 vai trò tự lưu token, 3 ca demo hội đồng, 5 ca xác thực, 9 ca phân quyền, 2 ca bàn giao liên dịch vụ); mỗi request kèm Test Script nên chạy được bằng Collection Runner và nhận báo cáo Pass/Fail tức thì.
- **jwt.io:** dán token thật kèm đúng secret thì hiện **"Signature Verified"**; sửa một ký tự trong Payload là chuyển ngay thành **"Invalid Signature"**.
- **MySQL:** `SELECT id, username, role, LEFT(password,35) FROM users;` cho thấy cột `password` chỉ chứa chuỗi băm tiền tố `$2a$10$`, ba tài khoản có ba chuỗi băm khác nhau dù cùng mật khẩu `123456`.

*(Ảnh chụp màn hình bốn minh chứng trên: xem Phụ lục B.)*

## 5.2. Kịch bản diễn tập demo hội đồng (10–15 phút)

*(Yêu cầu II.3)*

[TABLE] Bảng 5.3. Kịch bản demo 5 bước

| Bước | Người | Phút | Thao tác | Mã mong đợi |
| :---: | :---: | :---: | :--- | :--- |
| 1 | Hùng | 2 | Nạp 3 script SQL (hoặc `docker compose up -d`), mở DBeaver cho thấy **3 schema độc lập, không khóa ngoại vật lý**; khởi động 3 dịch vụ | — |
| 2 | Linh | 3 | Swagger UI 8082: `GET /pitches`; rồi `POST /pitches` với tên trống và giá âm | `200`, rồi `400` + `errors` |
| 3 | Hoàng | 5 | Login `chusan` lấy token → soi 3 phần trên **jwt.io**; `POST /pitches` không token; token `user`; token `chusan`; token `user` gọi `GET /users/1`; token tự bịa `role: admin` | `200` → `401` → `403` → `201` → `403` → `401` |
| 4 | Nhật | 4 | Token `user` gọi `POST /bookings`; Hùng `SELECT` kiểm chứng đơn `cho_duyet` vừa ghi đĩa; **tắt Pitch Service** rồi gửi lại; gọi API khác để chứng minh Booking vẫn sống | `201` → `503` → `200` |
| 5 | Hoàng | 1 | Chạy toàn bộ Postman Collection bằng Collection Runner, trình bày bảng Pass/Fail của cả nhóm | — |

## 5.3. Tự đánh giá và hướng phát triển

### 5.3.1. Mức độ đáp ứng yêu cầu đề bài

[TABLE] Bảng 5.4. Tự đánh giá mức độ đáp ứng từng ý của đề bài

| Yêu cầu theo đề | Thành viên | Mức đáp ứng | Minh chứng |
| :--- | :---: | :--- | :--- |
| Câu 1 Ý 1a — Đặc điểm SOA, phân biệt Service/API/Client | Linh | Hoàn thành | Mục 1.2 |
| Câu 1 Ý 1b — Phân rã dịch vụ, 03 API tiêu biểu, SRP | Linh | Hoàn thành | Mục 1.3 |
| Câu 1 Ý 2a — HTTP/REST, Request/Response, status code | Nhật | Hoàn thành | Mục 2.1 |
| Câu 1 Ý 2b — Database-per-service và rủi ro vi phạm | Hùng | Hoàn thành | Mục 3.1 |
| Câu 1 Ý 3 — AuthN vs AuthZ, cấu trúc JWT, 401 vs 403 | **Hoàng** | **Hoàn thành** | **Mục 4.1** |
| Câu 2 Ý 1 — RESTful API, validation 400, Swagger UI | Linh | Hoàn thành | Mục 1.4 |
| Câu 2 Ý 2 — OpenFeign, bắt lỗi 503, sequence diagram | Nhật | Hoàn thành | Mục 2.2 – 2.3 |
| Câu 2 Ý 3 — CSDL phân tán, Entity, Repository JPA | Hùng | Hoàn thành | Mục 3.2 – 3.5 |
| Câu 2 Ý 4 — Đăng nhập JWT, RBAC, bộ kiểm thử bảo mật | **Hoàng** | **Hoàn thành** | **Mục 4.2 – 4.3, 5.1** |
| Yêu cầu II.3 — Kịch bản demo hội đồng | Cả nhóm | Hoàn thành | Mục 5.2 |

### 5.3.2. Ba vấn đề phát hiện được khi chạy thực tế

**Vấn đề 1 — chuỗi băm BCrypt trong script SQL không khớp mật khẩu ghi trong chú thích.** File `auth-user-service.sql` nạp ba tài khoản với chú thích *"Mật khẩu mặc định: 123456"*, nhưng chuỗi băm thực tế là chuỗi mẫu lấy từ tài liệu Spring Security, **không phải** băm của `123456`; nếu không phát hiện thì **buổi demo sẽ sụp ngay bước đăng nhập đầu tiên**. Giải pháp tạm: lớp `DataInitializer` tự soát và băm lại ba tài khoản mẫu khi khởi động (ghi log WARN). Giải pháp triệt để: sửa lại chuỗi băm trong file SQL.

**Vấn đề 2 — dữ liệu tiếng Việt bị mã hóa hai lần.** Họ tên `Trần Văn Chủ Sân` hiển thị thành `Tráº§n VÄƒn Chá»§ SÃ¢n`; kiểm tra byte thực tế cho `5472C3A1` thay vì `5472E1BAA7`. Nguyên nhân: file SQL khai báo `CHARACTER SET utf8mb4` cho database nhưng **thiếu `SET NAMES utf8mb4;`** ở đầu file, nên MySQL client đọc theo `latin1` rồi mã hóa lại thành UTF-8 lần thứ hai. Đây là lỗi dữ liệu, không phải lỗi code; chỉ cần thêm `SET NAMES utf8mb4;` vào đầu cả ba file SQL.

**Vấn đề 3 — đường dẫn không tồn tại trả 500 thay vì 404.** Gọi `/v3/api-docs` (đường dẫn mặc định của SpringDoc, trong khi dự án cấu hình `/api-docs`) trả **500** kèm *"No static resource v3/api-docs"*, vì `NoResourceFoundException` bị handler `Exception.class` bắt và gói thành 500 — sai ngữ nghĩa HTTP. Đã khắc phục bằng handler tường minh trả **404**; `GlobalExceptionHandler` của Pitch và Booking Service có cùng cấu trúc nên cần bổ sung tương tự.

### 5.3.3. Hạn chế hiện tại

[TABLE] Bảng 5.5. Hạn chế của hệ thống và mức độ ảnh hưởng

| Hạn chế | Ảnh hưởng | Mức độ |
| :--- | :--- | :---: |
| Dùng thuật toán đối xứng HS256, mọi dịch vụ đều có khả năng tự ký token | Một dịch vụ bị chiếm quyền là kẻ tấn công tự phát hành được token `admin` | Cao |
| Chưa chạy HTTPS | Token truyền dạng rõ, có thể bị chặn bắt | Cao (môi trường thật) |
| Chưa có Refresh Token và cơ chế thu hồi token | Hết 24 giờ phải đăng nhập lại; token bị lộ vẫn dùng được tới khi hết hạn | Trung bình |
| Chưa có API Gateway | Mỗi dịch vụ tự cài lại logic xác thực, mã bảo mật lặp 3 lần | Trung bình |
| Chưa giới hạn số lần đăng nhập sai và chưa có Circuit Breaker | Chưa chống dò mật khẩu; Pitch Service sập chỉ bắt được bằng 503 | Trung bình |

### 5.3.4. Hướng phát triển

1. **Chuyển sang RS256** (bất đối xứng): Auth Service giữ private key để ký, hai dịch vụ còn lại chỉ nhận public key để xác minh — dù Pitch hay Booking Service bị chiếm quyền, kẻ tấn công cũng không tự phát hành được token. Đây là cách khắc phục hạn chế nghiêm trọng nhất hiện nay.
2. **Bổ sung API Gateway** (Spring Cloud Gateway) làm điểm xác thực tập trung ở biên hệ thống, loại bỏ việc lặp mã bảo mật ở cả ba dịch vụ; **thêm Refresh Token** vòng đời dài kèm cơ chế thu hồi.
3. **Tích hợp Circuit Breaker** (Resilience4j) cho lời gọi OpenFeign, triển khai **HTTPS/TLS**, **Rate Limiting** trên endpoint đăng nhập và **Audit Log** cho sự kiện đăng nhập thất bại.

## 5.4. Kết luận

Hệ thống **PitchOS** đã được xây dựng theo kiến trúc hướng dịch vụ với ba microservice độc lập, mỗi dịch vụ sở hữu CSDL riêng, giao tiếp qua HTTP/REST và được bảo vệ thống nhất bằng JWT phi trạng thái. Phần bảo mật đạt **36/36 ca kiểm thử**, phủ đủ các tình huống xác thực, phân quyền ba vai trò, kiểm tra quyền sở hữu tài nguyên, chống giả mạo token và phân biệt chính xác 401 với 403; nhóm ca liên dịch vụ chứng minh bằng thực nghiệm rằng token do Auth Service cấp được một tiến trình hoàn toàn độc lập xác thực và phân quyền chính xác. Quá trình kiểm thử thực tế cũng phát hiện ba vấn đề tiềm ẩn mà đọc mã nguồn không thể thấy, trong đó một vấn đề đủ nghiêm trọng để làm sụp buổi demo nếu không xử lý kịp — cho thấy giá trị không thể thay thế của việc chạy và kiểm thử thực tế.

# PHỤ LỤC

**Phụ lục A. Hướng dẫn khởi chạy hệ thống.** `README.md` (hướng dẫn chạy từng dịch vụ), `.env` / `.env.example` (cấu hình cổng, `JWT_SECRET`, thông tin MySQL), `docker-compose.yml` (MySQL 8.0 container `pitchos-mysql`).

**Phụ lục B. Bộ kiểm thử, mã nguồn trích dẫn và ảnh minh chứng.** Postman Collection: `pitchos-auth-service/postman/PitchOS-Auth.postman_collection.json` (16 request) và `pitchos-booking-service/postman/PitchOS-Booking.postman_collection.json` (20 ca); ma trận chi tiết 36 ca bảo mật và 20 ca Booking Service; mã nguồn đầy đủ `CreatePitchRequest`, `GlobalExceptionHandler`, `JwtTokenProvider`, `JwtAuthenticationFilter`, `SecurityConfig`, `CustomErrorDecoder`; ảnh chụp Swagger UI, Postman Collection Runner, jwt.io và DBeaver.

**Phụ lục C. Script SQL khởi tạo ba cơ sở dữ liệu.** `pitchos-database/auth-user-service.sql`, `pitch-service.sql`, `booking-service.sql`.
