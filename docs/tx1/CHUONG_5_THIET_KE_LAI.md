# CHƯƠNG 5. KIỂM THỬ, KẾT QUẢ VÀ TỰ ĐÁNH GIÁ

*(Hoàng chủ trì, cả nhóm phối hợp)*

## 5.1. Kế hoạch, môi trường và phạm vi kiểm thử

Hệ thống được kiểm thử theo hướng **hộp đen ở mức API**: gửi request HTTP thật tới dịch vụ đang chạy, đối chiếu mã trạng thái và nội dung phản hồi với kỳ vọng, rồi truy vấn cơ sở dữ liệu để xác nhận dữ liệu đã ghi đĩa. Môi trường thực nghiệm: Java 17, Spring Boot 3.2.5, Spring Security 6, JJWT 0.11.5, MySQL 8.0 (Docker container `pitchos-mysql`), SpringDoc OpenAPI 2.5.0. Công cụ: cURL tự động hóa bằng script Bash và hai bộ Postman Collection kèm Test Script.

> **Ghi chú về cổng dịch vụ:** cổng chuẩn của dự án là Auth 8081, Pitch 8082, Booking 8083, MySQL 3306; nhưng trên máy thực nghiệm cổng 8081 và 3306 đang bị dự án khác chiếm dụng, nên đợt kiểm thử này chạy trên **cổng thay thế Auth 18081, Pitch 18082, MySQL 3307** qua biến môi trường `AUTH_SERVICE_PORT`, `PITCH_SERVICE_PORT`, `MYSQL_PORT`. Việc đổi cổng không ảnh hưởng logic nghiệp vụ hay kết quả bảo mật vì toàn bộ cấu hình cổng đều tham số hóa qua `.env`.

[TABLE] Bảng 5.1. Phạm vi kiểm thử và kết quả theo nhóm ca

| Nhóm ca kiểm thử | Phụ trách | Số ca | Đạt | Trạng thái |
| :--- | :---: | :---: | :---: | :--- |
| Đăng nhập 3 vai trò và kiểm chứng cấu trúc JWT | Hoàng | 10 | 10 | Đã chạy thực tế |
| Xác thực 401 và kiểm tra dữ liệu đầu vào 400 | Hoàng | 10 | 10 | Đã chạy thực tế |
| Phân quyền RBAC và quyền sở hữu 403 | Hoàng | 11 | 11 | Đã chạy thực tế |
| Liên dịch vụ Auth → Pitch (401 / 403 / 201) | Hoàng + Linh | 5 | 5 | Đã chạy thực tế |
| **Cộng — đợt kiểm thử bảo mật** | | **36** | **36** | **Đạt 36/36, không có ca lỗi** |
| Booking Service: 503, trùng lịch, đặt đồng thời | Nhật | 20 | 20 | Chạy với Pitch Service giả lập; cần chạy lại với dịch vụ thật |
| Validation 400 và Swagger UI trên Pitch Service | Linh | — | — | Linh tự kiểm chứng (mục 1.4) |
| Kiểm chứng dữ liệu ghi xuống đĩa | Hùng | — | — | Hùng tự kiểm chứng (mục 3.5) |

Cột trạng thái ghi đúng thực tế phần nào đã chạy, phần nào do thành viên khác tự kiểm chứng. Ma trận chi tiết từng ca đặt tại Phụ lục B cùng hai bộ Postman Collection.

## 5.2. Kết quả kiểm thử theo mã trạng thái HTTP

Bộ ca kiểm thử được tổ chức theo **mã trạng thái HTTP** thay vì theo thứ tự chức năng: mỗi mã ứng với một yêu cầu trong đề bài và do một cơ chế riêng sinh ra, nên bảng dưới cho thấy ngay mỗi tầng phòng thủ được kiểm chứng bằng ca nào.

[TABLE] Bảng 5.2. Ca kiểm thử tiêu biểu theo từng mã trạng thái

| Mã | Ý nghĩa — cơ chế sinh mã | Ca kiểm thử tiêu biểu | Kết quả |
| :---: | :--- | :--- | :---: |
| `400` | Dữ liệu đầu vào sai — Jakarta Validation + `GlobalExceptionHandler` | TC03 — đăng ký email sai, mật khẩu 3 ký tự, họ tên trống → map `errors` đúng từng trường | Đạt |
| `401` | Không biết người gọi là ai — `AuthenticationEntryPoint` | TC06 không gửi token; **TC07 token tự bịa `role: admin`, sai chữ ký**; TC04 sai mật khẩu | Đạt |
| `403` | Biết là ai nhưng không đủ quyền — `AccessDeniedHandler`, kiểm tra quyền sở hữu | TC09 `user` gọi danh sách người dùng; TC12 `user` xem tài khoản khác; TC-X2 `user` tạo sân | Đạt |
| `404` | Tài nguyên không tồn tại — `ResourceNotFoundException`, `CustomErrorDecoder` | TC14 ID người dùng không có; TC-503c đặt sân `pitchId = 99` | Đạt |
| `201` | Tạo mới thành công đúng quyền — `SecurityConfig` cho qua, nghiệp vụ ghi đĩa | **TC-X3 `chusan` tạo sân bằng token Auth Service cấp**; TC-D1 `user` đặt sân, đơn `cho_duyet` | Đạt |
| `503` | Dịch vụ phụ thuộc chết — `GlobalExceptionHandler` bắt `RetryableException` | TC-503b tắt Pitch Service rồi gửi lại request đặt sân | Nhật kiểm chứng |

**TC07 — chống giả mạo token.** Payload của token trong ca này giải mã ra `{"sub":"hacker","role":"admin"}`, tức kẻ tấn công tự khai là quản trị viên, nhưng hệ thống vẫn trả 401 vì chữ ký không được tạo bằng `SECRET_KEY`. Đây là minh chứng thực nghiệm cho chữ ký HMAC-SHA256 ở mục 4.1.2: Payload đọc được nhưng không sửa được.

**Nhóm TC-X — hợp đồng token dùng chung.** Token do Auth Service (8081) cấp được Pitch Service (8082) — tiến trình độc lập, CSDL riêng, không gọi về Auth Service để hỏi — giải mã và phân quyền chính xác: không token trả 401, token `user` trả 403, token `chusan` trả 201. Đặc tính phi trạng thái của JWT vì vậy được kiểm chứng bằng thực nghiệm chứ không chỉ bằng lập luận.

## 5.3. Minh chứng kết quả thực nghiệm

- **Swagger UI** — `/swagger-ui.html` và `/api-docs` đều trả `200`; sinh đủ 5 endpoint, có nút **Authorize** chuẩn Bearer để thử API được bảo vệ ngay trên web.
- **Postman Collection** — 16 request chia 5 thư mục (đăng nhập 3 vai trò tự lưu token, 3 ca demo, 5 ca xác thực, 9 ca phân quyền, 2 ca bàn giao); mỗi request kèm Test Script nên chạy cả bộ bằng Collection Runner cho báo cáo Pass/Fail tức thì.
- **jwt.io** — token thật kèm đúng secret hiện **"Signature Verified"**; sửa một ký tự trong Payload là thành **"Invalid Signature"**.
- **MySQL** — cột `password` chỉ chứa chuỗi băm tiền tố `$2a$10$`; ba tài khoản có ba chuỗi băm khác nhau dù cùng mật khẩu `123456`, do BCrypt tự sinh salt riêng.

*(Ảnh chụp màn hình bốn minh chứng trên: xem Phụ lục B.)*

## 5.4. Kịch bản diễn tập demo hội đồng (10–15 phút)

*(Yêu cầu II.3)*

[TABLE] Bảng 5.3. Kịch bản demo 5 bước, phân vai theo phần phụ trách

| Bước | Người | Phút | Thao tác | Mã mong đợi |
| :---: | :---: | :---: | :--- | :--- |
| 1 | Hùng | 2 | Nạp 3 script SQL (hoặc `docker compose up -d`), mở DBeaver cho thấy **3 schema độc lập, không có khóa ngoại vật lý**; khởi động 3 dịch vụ | — |
| 2 | Linh | 3 | Swagger UI cổng 8082: gọi `GET /pitches`; rồi `POST /pitches` với tên trống và đơn giá âm | `200`, rồi `400` kèm `errors` |
| 3 | Hoàng | 5 | Đăng nhập `chusan` lấy token, soi ba phần trên **jwt.io**; `POST /pitches` không token; bằng token `user`; bằng token `chusan`; token `user` gọi `GET /users/1`; gửi token tự bịa `role: admin` | `200` → `401` → `403` → `201` → `403` → `401` |
| 4 | Nhật | 4 | Token `user` gọi `POST /bookings`; Hùng chạy `SELECT` xác nhận đơn `cho_duyet` vừa ghi đĩa; **tắt Pitch Service** rồi gửi lại request; gọi API khác để chứng minh Booking Service vẫn sống | `201` → `503` → `200` |
| 5 | Hoàng | 1 | Chạy cả bộ Postman bằng Collection Runner, trình bày bảng Pass/Fail tổng hợp của bốn thành viên | — |


## 5.5. Tự đánh giá mức độ đáp ứng yêu cầu

[TABLE] Bảng 5.4. Ánh xạ từng ý của đề bài sang vị trí trong báo cáo

| Yêu cầu theo đề | Thành viên | Mức đáp ứng | Minh chứng |
| :--- | :---: | :--- | :--- |
| Câu 1 Ý 1a — Đặc điểm SOA, phân biệt Service / API / Client | Linh | Hoàn thành | Mục 1.2 |
| Câu 1 Ý 1b — Phân rã dịch vụ, 03 API tiêu biểu, nguyên lý SRP | Linh | Hoàn thành | Mục 1.3 |
| Câu 1 Ý 2a — HTTP/REST, Request/Response, nhóm mã trạng thái | Nhật | Hoàn thành | Mục 2.1 |
| Câu 1 Ý 2b — Database-per-service và rủi ro khi vi phạm | Hùng | Hoàn thành | Mục 3.1 |
| Câu 1 Ý 3 — AuthN vs AuthZ, cấu trúc JWT, 401 vs 403 | **Hoàng** | **Hoàn thành** | **Mục 4.1** |
| Câu 2 Ý 1 — RESTful API, validation 400, Swagger UI | Linh | Hoàn thành | Mục 1.4 |
| Câu 2 Ý 2 — OpenFeign, bắt lỗi 503, sơ đồ tuần tự | Nhật | Hoàn thành | Mục 2.2 – 2.3 |
| Câu 2 Ý 3 — CSDL phân tán, Entity, Repository JPA | Hùng | Hoàn thành | Mục 3.2 – 3.5 |
| Câu 2 Ý 4 — Đăng nhập JWT, RBAC, bộ kiểm thử bảo mật | **Hoàng** | **Hoàn thành** | **Mục 4.2 – 4.3 và 5.1 – 5.3** |
| Yêu cầu II.3 — Kịch bản demo hội đồng | Cả nhóm | Hoàn thành | Mục 5.4 |

## 5.6. Vấn đề phát hiện, hạn chế và hướng phát triển

Ba vấn đề sau chỉ lộ ra khi chạy hệ thống thật, đọc mã nguồn không thể thấy.

**Vấn đề 1 — chuỗi băm BCrypt trong script SQL không khớp mật khẩu ghi trong chú thích.** File `auth-user-service.sql` nạp ba tài khoản kèm chú thích *"Mật khẩu mặc định: 123456"*, nhưng chuỗi băm thực tế là chuỗi mẫu trong tài liệu Spring Security, **không phải** băm của `123456`; nếu không phát hiện thì buổi demo sụp ngay bước đăng nhập đầu tiên. Giải pháp tạm: `DataInitializer` tự soát và băm lại ba tài khoản mẫu khi khởi động. Giải pháp triệt để: sửa chuỗi băm trong file SQL.

**Vấn đề 2 — dữ liệu tiếng Việt bị mã hóa hai lần.** Họ tên `Trần Văn Chủ Sân` hiển thị thành `Tráº§n VÄƒn Chá»§ SÃ¢n`, byte thực tế là `5472C3A1` thay vì `5472E1BAA7`. Nguyên nhân: file SQL khai báo `CHARACTER SET utf8mb4` nhưng **thiếu `SET NAMES utf8mb4;`** ở đầu file nên MySQL client đọc theo `latin1` rồi mã hóa lại lần hai. Đây là lỗi dữ liệu, không phải lỗi code.

**Vấn đề 3 — đường dẫn không tồn tại trả 500 thay vì 404.** Gọi `/v3/api-docs` trả **500** kèm *"No static resource"* vì `NoResourceFoundException` bị handler `Exception.class` bắt và gói thành 500 — sai ngữ nghĩa HTTP. Đã khắc phục bằng handler tường minh trả **404**; Pitch và Booking Service dùng cùng cấu trúc nên cần bổ sung tương tự.

[TABLE] Bảng 5.5. Hạn chế của hệ thống, ảnh hưởng và hướng khắc phục

| Hạn chế | Ảnh hưởng | Mức độ | Hướng khắc phục |
| :--- | :--- | :---: | :--- |
| HS256 đối xứng — mọi dịch vụ đều tự ký được token | Một dịch vụ bị chiếm quyền là kẻ tấn công phát hành được token `admin` | Cao | **RS256**: Auth giữ private key để ký, hai dịch vụ còn lại chỉ có public key để xác minh |
| Chưa chạy HTTPS | Token truyền dạng rõ, có thể bị chặn bắt | Cao | HTTPS/TLS ở tầng cổng vào |
| Chưa có Refresh Token và thu hồi token | Hết 24 giờ phải đăng nhập lại; token bị lộ dùng được tới khi hết hạn | TB | Refresh Token vòng đời dài kèm danh sách thu hồi |
| Chưa có API Gateway | Mã xác thực lặp ở cả 3 dịch vụ | TB | Spring Cloud Gateway xác thực tập trung ở biên |
| Chưa chặn đăng nhập sai nhiều lần, chưa có Circuit Breaker | Chưa chống dò mật khẩu; Pitch Service sập chỉ bắt bằng 503 | TB | Rate Limiting cho endpoint đăng nhập; Resilience4j cho OpenFeign |

**RS256 là ưu tiên số một** vì khắc phục đúng hạn chế nghiêm trọng nhất của mô hình secret dùng chung. Nhóm cũng dự kiến thêm **Audit Log** cho sự kiện đăng nhập thất bại và truy cập bị từ chối.

## 5.7. Kết luận

Hệ thống **PitchOS** được xây dựng theo kiến trúc hướng dịch vụ với ba microservice độc lập, mỗi dịch vụ sở hữu CSDL riêng, giao tiếp qua HTTP/REST và bảo vệ thống nhất bằng JWT phi trạng thái. Đợt kiểm thử bảo mật đạt **36/36 ca**, phủ đủ sáu mã trạng thái đề bài yêu cầu phân biệt, trong đó hai ca then chốt chứng minh hệ thống chống được token giả mạo và chia sẻ được hợp đồng token giữa các tiến trình độc lập. Quá trình chạy thực tế còn phát hiện ba vấn đề mà đọc mã nguồn không thể thấy, một trong số đó đủ nghiêm trọng để làm sụp buổi demo — cho thấy giá trị không thể thay thế của việc kiểm thử trên hệ thống đang chạy.
