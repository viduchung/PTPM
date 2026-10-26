# 🛠️ TÀI LIỆU CÔNG NGHỆ HỆ THỐNG PITCHOS (TECH STACK)

Tài liệu này quy chuẩn toàn bộ ngăn xếp công nghệ (Technology Stack), thư viện, công cụ và kiến trúc được sử dụng trong hệ thống **PitchOS (Football Pitch Booking System)** phục vụ báo cáo và bảo vệ trước hội đồng.

---

## 🏛️ 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG
* **Mô hình kiến trúc:** Kiến trúc hướng dịch vụ (**SOA / Microservices**).
* **Mô hình quản trị dữ liệu:** **Database-per-Service** (Mỗi dịch vụ sở hữu 1 database riêng, chỉ liên kết bằng Logical ID, không khóa ngoại vật lý).
* **Cơ chế xác thực & bảo mật:** Phi tập trung bằng **JSON Web Token (JWT Bearer)** kết hợp **RBAC (Role-Based Access Control)** với 3 vai trò: `admin`, `chusan`, `user`.
* **Giao thức giao tiếp:** Đồng bộ qua **HTTP/REST** (JSON format).

---

## 💻 2. CÔNG NGHỆ BACKEND (SPRING BOOT ECOSYSTEM)

Hệ thống Backend được xây dựng bằng **Java** và nền tảng **Spring Boot**:

| Thành phần | Công nghệ / Thư viện | Phiên bản khuyến nghị | Mục đích sử dụng |
| :--- | :--- | :---: | :--- |
| **Ngôn ngữ chính** | **Java** | 17 LTS / 21 LTS | Nền tảng lập trình hướng đối tượng, đa luồng hiệu năng cao |
| **Core Framework** | **Spring Boot** | 3.2.x / 3.x | Bộ khung phát triển Microservices độc lập |
| **Tầng REST API** | **Spring Web (MVC)** | Built-in | Xây dựng các RESTful endpoints, nhận Request và trả về JSON |
| **Bảo mật & Phân quyền** | **Spring Security 6** | Built-in | Lọc request, cấu hình `SecurityFilterChain`, `AuthenticationEntryPoint` (401), `AccessDeniedHandler` (403) |
| **Cơ chế Token** | **JJWT (io.jsonwebtoken)** | 0.11.5 / 0.12.x | Tạo, ký số HMAC-SHA256 và giải mã JWT token chứa claims (`sub`, `role`) |
| **Mã hóa mật khẩu** | **BCryptPasswordEncoder** | Built-in | Băm mật khẩu người dùng một chiều với salt ngẫu nhiên |
| **Tầng CSDL (ORM)** | **Spring Data JPA / Hibernate** | Built-in | Ánh xạ Object-Relational (ORM), thao tác dữ liệu qua `JpaRepository` |
| **Giao tiếp Liên dịch vụ** | **Spring Cloud OpenFeign** | 2023.x / 4.x | Khai báo HTTP Client gọi liên dịch vụ (Booking Service $\rightarrow$ Pitch Service) |
| **Kiểm tra dữ liệu đầu vào** | **Jakarta Validation** | 3.x (`@Valid`) | Validate dữ liệu DTO (`@NotBlank`, `@Positive`), bắt lỗi trả về **400 Bad Request** |
| **Tài liệu hóa API** | **Springdoc OpenAPI (Swagger UI)** | 2.x | Tự động sinh tài liệu chuẩn OpenAPI v3 tại `/swagger-ui.html` |
| **Tiện ích Code** | **Lombok** | Mới nhất | Giảm thiểu boilerplate code (`@Getter`, `@Setter`, `@Builder`, `@RequiredArgsConstructor`) |

---

## 🗄️ 3. CƠ SỞ DỮ LIỆU & QUẢN TRỊ DỮ LIỆU (DATABASE)

* **Hệ quản trị CSDL:** **MySQL 8.0**
* **Driver kết nối:** `mysql-connector-j`
* **Kiến trúc CSDL phân tán:** 3 CSDL độc lập hoạt động trên cùng máy chủ hoặc độc lập:
  1. `pitchos_user_db` (Auth & User Service - Port 8081 - Hoàng)
  2. `pitchos_pitch_db` (Pitch Service - Port 8082 - Linh)
  3. `pitchos_booking_db` (Booking Service - Port 8083 - Nhật)
* **Công cụ trực quan hóa & kiểm chứng:**
  - **DBeaver Community / MySQL Workbench / Navicat**
  - Hỗ trợ chạy các câu lệnh `SELECT` kiểm chứng đơn lưu đĩa cứng khi demo.

---

## 🌐 4. CÔNG NGHỆ FRONTEND WEB CLIENT (ỨNG DỤNG KHÁCH)

Phục vụ giao diện người dùng đặt sân và chủ sân quản lý:

| Thành phần | Công nghệ sử dụng | Vai trò & Đặc điểm |
| :--- | :--- | :--- |
| **Framework Web** | **Next.js 14+ / React 18** | Server-Side Rendering (SSR) & Client Component, tối ưu SEO |
| **Ngôn ngữ** | **TypeScript** | Định kiểu dữ liệu chặt chẽ, giảm thiểu lỗi runtime |
| **Styling & Giao diện** | **TailwindCSS** + **Vanilla CSS** | Thiết kế giao diện hiện đại, responsive mobile/desktop, hiệu ứng Glassmorphism |
| **Bộ Icon** | **Lucide React** | Bộ icon vector hiện đại, tối giản cho bóng đá, lịch đặt, người dùng |
| **HTTP Client** | **Axios / Fetch API** | Gửi request HTTP lên Backend, tự động đính kèm `Authorization: Bearer <token>` qua Axios Interceptors |
| **Bản đồ** | **Google Maps Embed / Link** | Định vị trực quan địa chỉ các sân bóng trên bản đồ |

---

## 🚀 5. DEVOPS, CÔNG CỤ & MÔI TRƯỜNG PHÁT TRIỂN

* **Quản lý biến môi trường:** File master [`.env`](file:///c:/Users/viduc/Downloads/PTPM/.env) tập trung và các file `application.properties` tự động nạp.
* **Container hóa:** **Docker & Docker Compose** (File [`docker-compose.yml`](file:///c:/Users/viduc/Downloads/PTPM/docker-compose.yml) bật MySQL và tự nạp dữ liệu với 1 lệnh `docker compose up -d`).
* **Công cụ kiểm thử API (Testing):**
  - **Postman:** Tạo bộ sưu tập (Collection) kiểm thử kịch bản thành công và lỗi (400, 401, 403, 503).
  - **Swagger UI:** Giao diện trực quan tích hợp sẵn trên từng dịch vụ (`http://localhost:8082/swagger-ui.html`).
* **Quản lý mã nguồn:** **Git & GitHub** (Phân nhánh theo từng microservice).

---

## 📊 6. MA TRẬN ÁNH XẠ CÔNG NGHỆ VÀO NỘI DUNG BÁO CÁO

* **Chương 1 (Linh):** Trình bày kiến trúc SOA, Spring Web, RESTful API, Jakarta Validation và Swagger UI.
* **Chương 2 (Nhật):** Trình bày Spring Cloud OpenFeign, HTTP Status Code, CustomErrorDecoder và giải pháp ngăn chặn Cascading Failure (503 Service Unavailable).
* **Chương 3 (Hùng):** Trình bày MySQL 8.0, Spring Data JPA, Hibernate, thiết kế Schema không dùng Foreign Key vật lý.
* **Chương 4 (Hoàng):** Trình bày Spring Security 6, JJWT (HMAC-SHA256), BCryptPasswordEncoder, cơ chế xử lý 401/403.
* **Chương 5 (Hoàng & Cả nhóm):** Trình bày bộ Test Cases thực hiện qua Postman / Swagger UI.
