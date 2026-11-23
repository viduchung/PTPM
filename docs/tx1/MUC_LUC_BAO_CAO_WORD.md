# 📑 MỤC LỤC CHI TIẾT BÁO CÁO KỸ THUẬT WORD (10 – 15 TRANG)
**Học phần:** Kiến trúc phần mềm (BÀI KIỂM TRA SỐ 1 - CĐR L1)  
**Đề tài:** Hệ thống quản lý và đặt sân bóng đá mini PitchOS (Kiến trúc SOA / Microservices)  
**Nhóm sinh viên thực hiện:**
1. **Hoàng (Nhóm trưởng):** Phụ trách Xác thực JWT, RBAC & Auth Service (3,0 Điểm)
2. **Linh:** Phụ trách Kiến trúc SOA, Chuẩn hóa RESTful API & Pitch Service (2,5 Điểm)
3. **Hùng:** Phụ trách Quản trị CSDL Phân tán & Tầng Repository (2,25 Điểm)
4. **Nhật:** Phụ trách Giao tiếp Liên dịch vụ, Sequence Diagram & Booking Service (2,25 Điểm)

---

## 📌 BẢNG MA TRẬN ÁNH XẠ: CÂU HỎI ĐỀ THI $\rightarrow$ CHƯƠNG BÁO CÁO & THÀNH VIÊN

| Phần trong Đề thi | Nội dung & Mức điểm | Thành viên phụ trách | Vị trí trong Báo cáo Word |
| :--- | :--- | :---: | :--- |
| **Câu 1 - Ý 1a** *(0,5đ)* | Đặc điểm kiến trúc SOA, phân biệt Service - API - Client | **Linh** | Mục 1.2 (Chương 1) |
| **Câu 1 - Ý 1b** *(1,0đ)* | Phân rã dịch vụ PitchOS, trách nhiệm, 03 API tiêu biểu, nguyên lý SRP | **Linh** | Mục 1.3 (Chương 1) |
| **Câu 2 - Ý 1** *(1,0đ)* | Triển khai RESTful API Pitch Service, Validation 400, Swagger UI | **Linh** | Mục 1.4 (Chương 1) |
| **Câu 1 - Ý 2a** *(0,75đ)* | Giao tiếp HTTP/REST, Request/Response, Status Code, Cascading Failure | **Nhật** | Mục 2.1 (Chương 2) |
| **Câu 2 - Ý 2** *(1,5đ)* | Giao tiếp liên dịch vụ qua OpenFeign, xử lý lỗi 503, Sequence Diagram | **Nhật** | Mục 2.2 & 2.3 (Chương 2) |
| **Câu 1 - Ý 2b** *(0,75đ)* | Nguyên tắc Database-per-service & 4 rủi ro kỹ thuật khi vi phạm | **Hùng** | Mục 3.1 (Chương 3) |
| **Câu 2 - Ý 3** *(1,5đ)* | 3 CSDL phân tán, Entity, Repository JPA, query chống trùng lịch, kiểm chứng ghi đĩa | **Hùng** | Mục 3.2, 3.3, 3.4, 3.5 (Chương 3) |
| **Câu 1 - Ý 3** *(1,0đ)* | Phân biệt AuthN vs AuthZ, cấu trúc JWT, HTTP 401 vs 403, liên hệ vai trò | **Hoàng** | Mục 4.1 (Chương 4) |
| **Câu 2 - Ý 4** *(2,0đ)* | Triển khai đăng nhập JWT, phân quyền RBAC 401/403, bộ kiểm thử bảo mật | **Hoàng** | Mục 4.2, 4.3 (Chương 4) & Toàn bộ Chương 5 |
| **Yêu cầu II.3** | Kịch bản Demo Hội đồng 5 bước (10–15 phút) | **Cả nhóm** | Mục 5.3 & Phụ lục Demo |

---

# 📖 MỤC LỤC CHI TIẾT TỪNG CHƯƠNG CHO FILE WORD

```text
MỤC LỤC
DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT
DANH MỤC BẢNG BIỂU
DANH MỤC HÌNH VẼ VÀ SƠ ĐỒ

CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI VÀ KIẾN TRÚC DỊCH VỤ (LINH PHỤ TRÁCH - 2,5 ĐIỂM)
  1.1. Mô tả bài toán nghiệp vụ đặt sân bóng đá mini trực tuyến
  1.2. Tổng quan kiến trúc hướng dịch vụ (SOA) [Câu 1 - Ý 1a: 0,5đ]
       1.2.1. 4 đặc tính cơ bản của SOA (Loose Coupling, Contract, Abstraction, Reusability)
       1.2.2. Phân biệt Dịch vụ (Service), Giao diện lập trình (API) và Ứng dụng khách (Client)
  1.3. Phân rã dịch vụ hệ thống PitchOS và Nguyên lý SRP [Câu 1 - Ý 1b: 1,0đ]
       1.3.1. Danh mục các dịch vụ chính và trách nhiệm nghiệp vụ
       1.3.2. Đặc tả 03 API tiêu biểu phục vụ nghiệp vụ cốt lõi
       1.3.3. Luận giải phân chia hệ thống theo nguyên lý Đơn trách nhiệm (SRP)
       1.3.4. Sơ đồ kiến trúc tổng thể hệ thống PitchOS
  1.4. Thiết kế và Triển khai RESTful API (Pitch Service) [Câu 2 - Ý 1: 1,0đ]
       1.4.1. Danh mục endpoints quản lý sân bóng và phương thức HTTP
       1.4.2. Kiểm tra dữ liệu đầu vào (Jakarta Validation) và chuẩn phản hồi 400 Bad Request
       1.4.3. Tài liệu hóa API trực quan với OpenAPI 3.0 / Swagger UI

CHƯƠNG 2. THIẾT KẾ API VÀ GIAO TIẾP DỊCH VỤ (NHẬT PHỤ TRÁCH - 2,25 ĐIỂM)
  2.1. Cơ chế giao tiếp giữa các dịch vụ qua giao thức HTTP/REST [Câu 1 - Ý 2a: 0,75đ]
       2.1.1. Quy trình trao đổi thông tin giữa Booking Service và Pitch Service
       2.1.2. Cấu trúc HTTP Request và HTTP Response chuẩn trao đổi JSON
       2.1.3. Ý nghĩa các nhóm mã trạng thái HTTP (2xx, 4xx, 5xx)
       2.1.4. Phân tích nguy cơ sụp đổ dây chuyền (Cascading Failure) và giải pháp
  2.2. Triển khai Giao tiếp Liên dịch vụ với Spring Cloud OpenFeign [Câu 2 - Ý 2: 1,5đ]
       2.2.1. Khởi tạo Feign Client gọi tra cứu thông tin sân
       2.2.2. Xây dựng các nghiệp vụ điều phối đặt sân (Tạo đơn, Lịch sử, Duyệt đơn)
  2.3. Sơ đồ Tuần tự (Sequence Diagram) và Cơ chế Xử lý Lỗi Phân tán [Câu 2 - Ý 2: 1,5đ]
       2.3.1. Sơ đồ tuần tự nghiệp vụ đặt sân thành công (Luồng bình thường - 201 Created)
       2.3.2. Sơ đồ tuần tự và cơ chế bắt lỗi khi dịch vụ đích không khả dụng (HTTP 503)
       2.3.3. Cài đặt CustomErrorDecoder (404) và GlobalExceptionHandler bắt sập mạng

CHƯƠNG 3. QUẢN LÝ DỮ LIỆU PHÂN TÁN (HÙNG PHỤ TRÁCH - 2,25 ĐIỂM)
  3.1. Nguyên tắc Quản lý Dữ liệu Độc lập (Database-per-Service) [Câu 1 - Ý 2b: 0,75đ]
       3.1.1. Bản chất nguyên tắc Database-per-service trong kiến trúc SOA
       3.1.2. Phân tích 4 rủi ro kỹ thuật khi vi phạm (Schema Coupling, Deadlock chéo, v.v.)
  3.2. Thiết kế Cơ sở dữ liệu phân tán hệ thống PitchOS [Câu 2 - Ý 3: 1,5đ]
       3.2.1. Cấu trúc 3 Database MySQL độc lập (pitchos_user_db, pitchos_pitch_db, pitchos_booking_db)
       3.2.2. Sơ đồ quan hệ thực thể phân tán (Distributed ERD)
       3.2.3. Cơ chế toàn vẹn dữ liệu bằng Logical ID, không dùng Foreign Key vật lý
  3.3. Kiến trúc Tầng dữ liệu ORM (Spring Data JPA & Hibernate) [Câu 2 - Ý 3: 1,5đ]
       3.3.1. Thiết kế các lớp Entity JPA (User, Pitch, Booking)
       3.3.2. Thiết kế các interface JpaRepository
  3.4. Giải thuật và Câu truy vấn Chống trùng lịch thi đấu [Câu 2 - Ý 3: 1,5đ]
       3.4.1. Điều kiện toán học kiểm tra giao thoa thời gian đặt sân
       3.4.2. Cài đặt câu truy vấn JPQL tối ưu trong BookingRepository
  3.5. Kiểm chứng Dữ liệu Lưu đĩa cứng (Data Verification phục vụ Demo) [Câu 2 - Ý 3: 1,5đ]
       3.5.1. Dữ liệu nạp ban đầu (Seed Data qua script SQL)
       3.5.2. Thao tác nghiệp vụ và câu lệnh SQL kiểm tra ghi đĩa trạng thái cho_duyet

CHƯƠNG 4. XÁC THỰC VÀ BẢO MẬT HỆ THỐNG (HOÀNG PHỤ TRÁCH - 3,0 ĐIỂM)
  4.1. Cơ chế Xác thực và Phân quyền dịch vụ [Câu 1 - Ý 3: 1,0đ]
       4.1.1. Phân biệt bản chất Authentication và Authorization
       4.1.2. Cấu trúc 3 phần của JSON Web Token (Header, Payload Claims, Signature HMAC-SHA256)
       4.1.3. Phân biệt chính xác giữa HTTP 401 Unauthorized và HTTP 403 Forbidden
       4.1.4. Ma trận phân quyền Role-Based Access Control (RBAC) cho 3 vai trò: admin, chusan, user
  4.2. Triển khai Auth & User Service (Port 8081) [Câu 2 - Ý 4: 2,0đ]
       4.2.1. Đăng ký tài khoản và mã hóa mật khẩu an toàn với BCryptPasswordEncoder
       4.2.2. Đăng nhập và cơ chế sinh Bearer JWT Token (JwtTokenProvider)
  4.3. Cấu hình Bảo vệ API với Spring Security 6 [Câu 2 - Ý 4: 2,0đ]
       4.3.1. Xây dựng JwtAuthenticationFilter giải mã token trong SecurityContextHolder
       4.3.2. Cấu hình AuthenticationEntryPoint (xử lý 401) và AccessDeniedHandler (xử lý 403)
       4.3.3. Cơ chế đồng bộ Secret Key bảo vệ liên dịch vụ (Giai đoạn 4)

CHƯƠNG 5. KIỂM THỬ, KẾT QUẢ VÀ TỰ ĐÁNH GIÁ (HOÀNG CHỦ TRÌ & CẢ NHÓM PHỐI HỢP)
  5.1. Kế hoạch và Ma trận Ca kiểm thử toàn diện (Test Cases Matrix) [Câu 2 - Ý 4: 2,0đ]
       5.1.1. Bộ Test Cases cho RESTful API và Validation dữ liệu đầu vào (400 Bad Request)
       5.1.2. Bộ Test Cases cho Xác thực và Phân quyền bảo mật (401 Unauthorized, 403 Forbidden)
       5.1.3. Bộ Test Cases cho Giao tiếp Liên dịch vụ và Bắt lỗi phân tán (503 Service Unavailable)
       5.1.4. Bộ Test Cases cho Toàn vẹn dữ liệu và Chống trùng lịch (201 Created & Conflict)
  5.2. Hình ảnh Minh chứng Kết quả Thực nghiệm Thực tế
       5.2.1. Kết quả kiểm thử trên giao diện Swagger UI (Port 8082)
       5.2.2. Kết quả kiểm thử bộ sưu tập Postman Collection
       5.2.3. Minh chứng giải mã cấu trúc Token trên jwt.io
       5.2.4. Minh chứng bản ghi đơn lưu đĩa cứng trên DBeaver / MySQL Workbench
  5.3. Kịch bản Diễn tập Demo 5 Bước Hội đồng (10–15 Phút) [Yêu cầu II.3]
  5.4. Tự đánh giá Mức độ Hoàn thành và Hướng phát triển
       5.4.1. Bảng tự đánh giá mức độ đáp ứng Chuẩn đầu ra CĐR L1
       5.4.2. Những điểm hạn chế hiện tại và giải pháp mở rộng (Circuit Breaker, API Gateway)

PHỤ LỤC & TÀI LIỆU KÈM THEO
  Phụ lục A. Hướng dẫn Khởi chạy Hệ thống (README, .env, Docker Compose, Laragon)
  Phụ lục B. Đường dẫn Tài liệu OpenAPI Swagger và Tệp Postman Collection
  Phụ lục C. Toàn văn Script SQL khởi tạo 3 cơ sở dữ liệu
```

---

## 📄 HƯỚNG DẪN ĐỊNH DẠNG TRANG WORD CHUẨN KỸ THUẬT:
* **Khổ giấy:** A4, Căn lề: Trái 3cm, Phải 2cm, Trên 2cm, Dưới 2cm.
* **Font chữ:** Times New Roman, Cỡ chữ: 13pt (Nội dung), Giãn dòng: 1.3 – 1.5 lines.
* **Heading 1:** In hoa, đậm, cỡ 14–16pt (Ví dụ: **CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI...**).
* **Heading 2:** Đậm, cỡ 13–14pt (Ví dụ: **1.1. Mô tả bài toán nghiệp vụ...**).
* **Heading 3:** Đậm nghiêng, cỡ 13pt (Ví dụ: *1.2.1. 4 đặc tính cơ bản của SOA*).
* **Bảng biểu & Hình vẽ:** Đánh số theo chương (Ví dụ: *Bảng 3.1, Hình 1.2, Sơ đồ 2.1*), có chú thích rõ ràng bên dưới.
* **Dung lượng:** 10 – 15 trang nội dung chính (mỗi chương khoảng 2,5 – 3,5 trang).
