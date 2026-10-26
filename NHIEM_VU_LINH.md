# 👤 BẢNG NHIỆM VỤ CÁ NHÂN: LINH

> **HỌ VÀ TÊN:** LINH  
> **VAI TRÒ:** Phụ trách Cơ chế JWT, Phân quyền RBAC (401/403) & Code Auth Service  
> **DỊCH VỤ PHỤ TRÁCH:** `pitchos-auth-service` (Cổng: **8081**)  
> **CƠ SỞ DỮ LIỆU SỞ HỮU:** `pitchos_user_db`  
> **TỔNG ĐIỂM BẢO VỆ:** **2,5 / 10,0 Điểm**  
> **BÁO CÁO PHỤ TRÁCH:** **Chương 4 & Chương 5**  
> **THỜI ĐIỂM BẮT ĐẦU:** **Giai đoạn 2 (Nhánh 1)** — Code song song với Hoàng ngay sau khi Hùng bàn giao CSDL.

---

## 🎯 1. BAREM ĐIỂM VÀ ĐẦU VIỆC CHI TIẾT CỦA LINH

### 📘 A. Phần Lý thuyết (1,0 Điểm - Câu 1 Ý 3)
- [ ] **Phân biệt bản chất Xác thực (Authentication) và Phân quyền (Authorization):**
  - *Authentication:* Xác minh danh tính người dùng — "Bạn là ai?" (thông qua username/password).
  - *Authorization:* Kiểm tra quyền hạn của danh tính — "Bạn được phép làm gì?" (dựa vào Role: `admin`, `chusan`, `user`).
- [ ] **Giải thích cấu trúc 3 phần của JSON Web Token (JWT):**
  1. *Header:* Định nghĩa loại token (`typ: "JWT"`) và thuật toán băm chữ ký (`alg: "HS256"`), mã hóa Base64Url.
  2. *Payload (Claims):* Chứa thông tin ngữ cảnh người dùng: Subject `sub` (userId/username), `role` (`admin`, `chusan`, `user`), ngày cấp `iat`, hạn dùng `exp`, mã hóa Base64Url.
  3. *Signature (Chữ ký):* Được tạo bằng thuật toán HMAC-SHA256 kết hợp giữa Header + Payload và `Secret Key`, đảm bảo chống giả mạo token.
- [ ] **Phân biệt chính xác giữa HTTP 401 Unauthorized và HTTP 403 Forbidden:**
  - *401 Unauthorized:* Khi request không gửi kèm token hoặc token sai/hết hạn (chưa xác thực).
  - *403 Forbidden:* Khi token hợp lệ nhưng vai trò người dùng không đủ quyền truy cập (sai quyền, ví dụ tài khoản `user` cố gọi API thêm sân của `chusan`).

---

### 💻 B. Phần Thực nghiệm (1,5 Điểm - Câu 2 Ý 4)
- [ ] **Khởi tạo và lập trình `pitchos-auth-service` chạy trên Port 8081:**
  - Kết nối CSDL `pitchos_user_db` do Hùng bàn giao.
  - Xây dựng Entity `User` (`username`, `email` Gmail, `password`, `full_name`, `phone`, `role`: `admin`, `chusan`, `user`) và `UserRepository`.
  - Cấu hình mã hóa mật khẩu bằng `BCryptPasswordEncoder`.
- [ ] **Xây dựng `JwtTokenProvider`:**
  - Tạo hàm sinh token chứa `sub` (userId/username) và claim `role` (`admin`, `chusan`, `user`).
  - Tạo hàm validate và trích xuất claims từ token.
- [ ] **Xây dựng đầy đủ các API xác thực:**
  1. `POST /api/v1/auth/register`: Đăng ký tài khoản mới (mặc định role `user`), mã hóa mật khẩu bằng BCrypt trước khi lưu.
  2. `POST /api/v1/auth/login`: Xác thực thông tin đăng nhập, sinh và trả về `Bearer <token>`.
  3. `GET /api/v1/users/{id}`: Truy vấn thông tin người dùng theo ID.
- [ ] **Cấu hình Spring Security & JwtAuthenticationFilter:**
  - `JwtAuthenticationFilter`: Lấy token từ header `Authorization: Bearer ...`, giải mã và nạp quyền vào `SecurityContextHolder`.
  - Cấu hình `AuthenticationEntryPoint`: Trả về chuẩn mã **401 Unauthorized** khi chưa đăng nhập / thiếu token.
  - Cấu hình `AccessDeniedHandler`: Trả về chuẩn mã **403 Forbidden** khi truy cập sai quyền.
- [ ] **Bàn giao cấu hình bảo mật cho nhóm (Giai đoạn 4):**
  - Cung cấp chuỗi Secret Key dùng chung cho Hoàng và Nhật.
  - Cung cấp các chuỗi JWT mẫu (token của `user`, token của `chusan`, token của `admin`) để mọi người test.
  - Đóng gói hoặc chia sẻ class `JwtAuthenticationFilter` để Hoàng và Nhật tích hợp vào Pitch Service và Booking Service.

---

### 📑 C. Phần Viết Báo cáo (Chương 4 & Chương 5)
- [ ] **Biên soạn toàn bộ Chương 4:**
  - Cơ chế xác thực phân tán bằng JSON Web Token (JWT).
  - Ma trận phân quyền hệ thống (RBAC) cho 3 vai trò: `admin`, `chusan`, `user`.
  - Cấu hình bộ lọc bảo mật và xử lý phản hồi 401/403.
- [ ] **Biên soạn toàn bộ Chương 5 (Chủ trì & tổng hợp cùng nhóm):**
  - Bảng tổng hợp các ca kiểm thử (Test Cases) của toàn hệ thống.
  - Hình ảnh minh chứng kết quả kiểm thử thực tế.
  - Phần tự đánh giá mức độ hoàn thành dự án.

---

### 🎤 D. Nhiệm vụ Demo trước Hội đồng (Linh trực tiếp thao tác)
- [ ] **Bước 1 (Đăng nhập & Cấp JWT):**
  - Gọi `POST /api/v1/auth/login` với tài khoản `user` $\rightarrow$ Nhận mã `200 OK` kèm token `user`.
  - Gọi `POST /api/v1/auth/login` với tài khoản `chusan` $\rightarrow$ Nhận mã `200 OK` kèm token `chusan`.
  - Dán token vào trang **jwt.io** để chỉ rõ 3 thành phần Header, Payload (chứa `sub` và `role: chusan`), Signature.
- [ ] **Bước 2 (Demo 3 Ca bảo mật kinh điển):**
  1. *Ca 1 (401 Unauthorized):* Gọi API cần bảo mật khi **không truyền Token** $\rightarrow$ Chứng minh nhận mã **401 Unauthorized**.
  2. *Ca 2 (403 Forbidden):* Dùng token của `user` gọi API thêm sân của `chusan` $\rightarrow$ Chứng minh nhận mã **403 Forbidden**.
  3. *Ca 3 (200 OK / 201 Created):* Dùng đúng token của `chusan` gọi lại API thêm sân $\rightarrow$ Nhận mã **201 Created**.
- [ ] Sẵn sàng thay đổi trực tiếp quyền trên code nếu thầy cô yêu cầu kiểm tra.
