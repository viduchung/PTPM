# Nhiệm vụ: Linh — Bảo mật JWT, Phân quyền RBAC & Auth Service

- **Vai trò:** Security Architect & Backend Auth Engineer
- **Tổng điểm phụ trách:** **2,5 Điểm** (1,0đ Lý thuyết + 1,5đ Thực nghiệm)
- **Cổng dịch vụ (Port):** `8081`
- **Cơ sở dữ liệu:** `pitchos_user_db`
- **Báo cáo phụ trách:** **Chương 4 & Chương 5**
- **Thứ tự thực hiện:** **GIAI ĐOẠN 2 (NHÁNH 1)** — Code song song với Hoàng sau khi Hùng bàn giao CSDL.

---

## 📚 1. Yêu cầu Lý thuyết (1,0 Điểm - Câu 1 Ý 3)

- [ ] **Phân biệt bản chất Xác thực (Authentication) và Phân quyền (Authorization):**
  - **Authentication (Xác thực):** Trả lời câu hỏi *"Bạn là ai?"* — Kiểm tra danh tính người dùng thông qua thông tin đăng nhập (`username`/`password`).
  - **Authorization (Phân quyền):** Trả lời câu hỏi *"Bạn được phép làm gì?"* — Kiểm tra vai trò của danh tính đối với tài nguyên (Role: `admin`, `chusan`, `user`).
- [ ] **Giải thích chi tiết cấu trúc 3 phần của JSON Web Token (JWT):**
  1. **Header:** Thuật toán ký (`alg: "HS256"`) và loại token (`typ: "JWT"`).
  2. **Payload (Claims):** Chứa thông tin người dùng: `sub` (userId/username), `role` (`admin`, `chusan`, `user`), `iat`, `exp`.
  3. **Signature (Chữ ký số):** Băm Header + Payload cùng với `Secret Key` qua HMAC-SHA256 để chống giả mạo token.
- [ ] **Phân biệt chính xác giữa HTTP 401 Unauthorized và HTTP 403 Forbidden:**
  - **401 Unauthorized:** Người dùng chưa đăng nhập, không gửi Token hoặc Token không hợp lệ.
  - **403 Forbidden:** Đã đăng nhập nhưng vai trò hiện tại không đủ quyền truy cập (ví dụ tài khoản `user` gọi API của `chusan`).

---

## 🛠️ 2. Yêu cầu Thực nghiệm (1,5 Điểm - Câu 2 Ý 4)

### 2.1. Xây dựng Auth & User Service (Port 8081)
- **Thực thể `User` & `UserRepository`:** Kế thừa `JpaRepository`.
  - Các trường: `username`, `email` (Gmail), `password` (BCrypt), `full_name`, `phone`, `role` (`admin`, `chusan`, `user`).
- **Mã hóa mật khẩu:** Cấu hình bean `BCryptPasswordEncoder`.
- **Xây dựng `JwtTokenProvider`:**
  - Sinh JWT Token chứa `sub` và `role` (`admin`, `chusan`, `user`).
  - Giải mã và trích xuất claims từ token.
- **Xây dựng các Endpoints:**
  - `POST /api/v1/auth/register`: Đăng ký tài khoản mới (mặc định role `user`).
  - `POST /api/v1/auth/login`: Xác thực thông tin đăng nhập và cấp phát `Bearer <JWT_TOKEN>`.
  - `GET /api/v1/users/{id}`: Truy vấn thông tin người dùng theo ID.

### 2.2. Cấu hình Spring Security & JwtAuthenticationFilter
- **`JwtAuthenticationFilter`:** Trích xuất token từ Header `Authorization: Bearer <token>`, xác thực và nạp quyền vào `SecurityContextHolder`.
- **Cấu hình xử lý phản hồi bảo mật:**
  - `AuthenticationEntryPoint` trả về mã lỗi chuẩn **401 Unauthorized** khi không có/sai token.
  - `AccessDeniedHandler` trả về mã lỗi chuẩn **403 Forbidden** khi sai quyền.

### 2.3. Bàn giao cấu hình bảo mật cho nhóm (Giai đoạn 4)
- Gửi cho Hoàng và Nhật:
  - Các chuỗi JWT mẫu (token của `user`, token của `chusan`, token của `admin`).
  - Chuỗi `jwt.secret` dùng chung để đồng bộ giải mã ở các dịch vụ.
  - Class `JwtAuthenticationFilter` và `SecurityConfig` chuẩn để tích hợp vào Pitch Service và Booking Service.

---

## 📝 3. Viết Báo cáo
- **Chương 4:** Kiến trúc bảo mật, luồng cấp phát & xác thực JWT, cấu hình RBAC cho 3 vai trò (`admin`, `chusan`, `user`) và ma trận phân quyền.
- **Chương 5:** Bảng tổng hợp các ca kiểm thử (Test Cases), kết quả thực tế và tự đánh giá.

---

## 🎥 4. Kịch bản Demo Hội đồng (10–15 Phút)
1. **Ca 1 (401 Unauthorized):** Gọi API cần token khi **không truyền Token** $\rightarrow$ Nhận `401 Unauthorized`.
2. **Ca 2 (403 Forbidden):** Đăng nhập bằng tài khoản `user`, dùng token này gọi API thêm sân của `chusan` $\rightarrow$ Nhận `403 Forbidden`.
3. **Ca 3 (200 OK / 201 Created):** Đăng nhập bằng tài khoản `chusan`, gọi lại API thêm sân $\rightarrow$ Nhận `201 Created`.
