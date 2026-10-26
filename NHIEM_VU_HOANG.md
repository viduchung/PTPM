# 👑 BẢNG NHIỆM VỤ CÁ NHÂN: HOÀNG (NHÓM TRƯỞNG)

> **HỌ VÀ TÊN:** HOÀNG  
> **VAI TRÒ:** Nhóm trưởng, Phụ trách Cơ chế JWT, Phân quyền RBAC & Code Auth Service  
> **DỊCH VỤ PHỤ TRÁCH:** `pitchos-auth-service` (Cổng: **8081**)  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_user_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **3,0 / 10,0 Điểm** (Nhóm trưởng phụ trách bảo mật cốt lõi, điểm số nhỉnh hơn)  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 4 & Chương 5** (Chủ trì tổng hợp kiểm thử cùng nhóm)  
> **THỜI ĐIỂM BẮT ĐẦU:** **Giai đoạn 2 (Nhánh 1)** — Code song song với Linh ngay sau khi Hùng bàn giao CSDL.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA HOÀNG (THEO ĐÚNG ĐỀ BÀI)

### 📘 A. Phần Lý thuyết (1,0 Điểm — Câu 1 Ý 3)
- [ ] **Phân biệt bản chất Xác thực (Authentication) và Phân quyền (Authorization):**
  - *Authentication (Xác thực):* Trả lời câu hỏi *"Bạn là ai?"* — Xác minh danh tính người dùng thông qua thông tin đăng nhập (`username`/`password`).
  - *Authorization (Phân quyền):* Trả lời câu hỏi *"Bạn được phép làm gì?"* — Kiểm tra quyền hạn và vai trò của danh tính đối với tài nguyên hệ thống (Role: `admin`, `chusan`, `user`).
- [ ] **Trình bày cách sử dụng JSON Web Token (JWT) để bảo vệ API:**
  - Giải thích cấu trúc 3 phần của JWT:
    1. *Header:* Định nghĩa loại token (`typ: "JWT"`) và thuật toán ký băm (`alg: "HS256"`), mã hóa Base64Url.
    2. *Payload (Claims):* Chứa thông tin ngữ cảnh người dùng: Subject `sub` (userId/username), claim vai trò `role` (`admin`, `chusan`, `user`), ngày phát hành `iat`, hạn dùng `exp`, mã hóa Base64Url.
    3. *Signature (Chữ ký số):* Băm Header + Payload cùng với `Secret Key` qua HMAC-SHA256 để đảm bảo tính toàn vẹn và chống giả mạo token.
  - Cơ chế Stateless: Server không cần lưu Session trong RAM/DB, chỉ cần giải mã token kèm chữ ký bí mật để xác thực request gửi lên ở Header `Authorization: Bearer <token>`.
- [ ] **Giải thích sự khác nhau giữa HTTP 401 Unauthorized và HTTP 403 Forbidden:**
  - *401 Unauthorized:* Khi request không gửi kèm token hoặc token không hợp lệ / hết hạn (người dùng chưa xác thực danh tính).
  - *403 Forbidden:* Khi token hợp lệ nhưng vai trò của người dùng không đủ quyền truy cập tài nguyên (ví dụ: tài khoản role `user` cố tình gọi API tạo sân mới của `chusan`).
- [ ] **Liên hệ với các vai trò người dùng trong đề tài PitchOS:**
  - Phân tích rõ 3 vai trò: `admin` (toàn quyền hệ thống), `chusan` (quản lý sân, duyệt/từ chối đơn), `user` (khách hàng xem sân, tạo đơn đặt).

---

### 💻 B. Phần Thực nghiệm (2,0 Điểm — Câu 2 Ý 4)
- [ ] **Khởi tạo và lập trình `pitchos-auth-service` chạy trên Port 8081:**
  - Kết nối CSDL `pitchos_user_db` do Hùng bàn giao.
  - Xây dựng Entity `User` (`username`, `email` Gmail, `password`, `full_name`, `phone`, `role`: `admin`, `chusan`, `user`) và `UserRepository` kế thừa `JpaRepository`.
  - Cấu hình mã hóa mật khẩu an toàn bằng `BCryptPasswordEncoder`.
- [ ] **Xây dựng `JwtTokenProvider`:**
  - Tạo hàm sinh token chứa `sub` (userId/username) và claim `role` (`admin`, `chusan`, `user`).
  - Tạo hàm trích xuất claims và kiểm tra tính hợp lệ của token.
- [ ] **Xây dựng đầy đủ các API xác thực:**
  1. `POST /api/v1/auth/register`: Đăng ký tài khoản mới (mặc định role `user`), mã hóa mật khẩu bằng BCrypt trước khi lưu.
  2. `POST /api/v1/auth/login`: Xác thực thông tin đăng nhập, sinh và trả về `Bearer <token>`.
  3. `GET /api/v1/users/{id}`: Truy vấn thông tin người dùng theo ID.
- [ ] **Cấu hình Spring Security & JwtAuthenticationFilter:**
  - `JwtAuthenticationFilter`: Trích xuất token từ header `Authorization: Bearer <token>`, giải mã và nạp quyền vào `SecurityContextHolder`.
  - Cấu hình `AuthenticationEntryPoint`: Trả về chuẩn mã **401 Unauthorized** khi chưa đăng nhập / thiếu token.
  - Cấu hình `AccessDeniedHandler`: Trả về chuẩn mã **403 Forbidden** khi truy cập sai quyền.
- [ ] **Bảo vệ các API cần đăng nhập & Phân quyền ít nhất 2 vai trò:**
  - Thiết lập ma trận phân quyền: `admin`, `chusan`, `user`.
- [ ] **Kiểm thử các trường hợp bảo mật & Nộp bộ kiểm thử:**
  - Kiểm tra trường hợp truy cập hợp lệ (200/201).
  - Kiểm tra trường hợp không gửi token (401 Unauthorized).
  - Kiểm tra trường hợp người dùng đã đăng nhập nhưng không có quyền truy cập (403 Forbidden).
  - Đóng gói file Postman Collection kiểm thử bảo mật.
- [ ] **Bàn giao cấu hình bảo mật cho nhóm (Giai đoạn 4):**
  - Cung cấp chuỗi `JWT_SECRET` dùng chung cho Linh và Nhật.
  - Cung cấp các chuỗi JWT mẫu (token `user`, token `chusan`, token `admin`) để nhóm test.
  - Chia sẻ class `JwtAuthenticationFilter` và `SecurityConfig` chuẩn để Linh và Nhật tích hợp vào Pitch Service và Booking Service.

---

### 📑 C. Phần Viết Báo cáo (Chương 4 & Chương 5)
- [ ] **Biên soạn toàn bộ Chương 4 (Xác thực và bảo mật):**
  - Luồng xác thực đăng nhập, cơ chế cấp phát JWT.
  - Cấu trúc Token, các vai trò (`admin`, `chusan`, `user`) và quy tắc phân quyền RBAC.
  - Cấu hình bộ lọc bảo mật, xử lý phản hồi 401 và 403.
- [ ] **Biên soạn toàn bộ Chương 5 (Kiểm thử, kết quả và tự đánh giá - Chủ trì cùng nhóm):**
  - Bảng tổng hợp các ca kiểm thử (Test Cases) của toàn hệ thống PitchOS.
  - Ảnh chụp màn hình minh chứng kết quả kiểm thử thực tế từ Swagger / Postman.
  - Đánh giá mức độ hoàn thành, các hạn chế và hướng phát triển tiếp theo.

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Hoàng trực tiếp thao tác)
- [ ] **Bước 1 (Đăng nhập & Cấp JWT):**
  - Gửi `POST /api/v1/auth/login` với tài khoản `user` $\rightarrow$ Nhận mã `200 OK` kèm token của `user`.
  - Gửi `POST /api/v1/auth/login` với tài khoản `chusan` $\rightarrow$ Nhận mã `200 OK` kèm token của `chusan`.
  - Mở trang **jwt.io** dán token vào để chỉ rõ cho hội đồng thấy 3 thành phần: Header, Payload (chứa `sub`, `role: chusan`), và Signature băm bí mật.
- [ ] **Bước 2 (Demo 3 Ca bảo mật kinh điển):**
  1. *Ca 1 (401 Unauthorized):* Gọi API yêu cầu bảo mật khi **không truyền Token** $\rightarrow$ Nhận mã chuẩn **401 Unauthorized**.
  2. *Ca 2 (403 Forbidden):* Dùng token của `user` để gọi API thêm sân mới của `chusan` $\rightarrow$ Nhận mã chuẩn **403 Forbidden**.
  3. *Ca 3 (200 OK / 201 Created):* Dùng đúng token của `chusan` gọi lại API thêm sân mới $\rightarrow$ Nhận mã **201 Created**.
- [ ] Sẵn sàng giải thích trực tiếp luồng lọc token trong `JwtAuthenticationFilter` hoặc đổi một tham số quyền nếu thầy cô yêu cầu kiểm tra trực tiếp.
