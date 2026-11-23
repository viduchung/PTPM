# HƯỚNG DẪN TỪ SỐ 0 — PHẦN VIỆC CỦA HOÀNG

> Tài liệu này viết cho người **chưa biết gì** về Spring Boot, JWT hay microservice.
> Đọc tuần tự từ trên xuống. Chỗ nào không hiểu cứ đọc tiếp, phần sau sẽ giải thích lại bằng code thật.

**Mục lục**
- [Phần 0. Bức tranh toàn cảnh](#phần-0--bức-tranh-toàn-cảnh)
- [Phần 1. Nhiệm vụ của bạn là gì](#phần-1--nhiệm-vụ-của-bạn-là-gì)
- [Phần 2. Kiến thức nền tối thiểu](#phần-2--kiến-thức-nền-tối-thiểu)
- [Phần 3. Đi qua từng file code](#phần-3--đi-qua-từng-file-code)
- [Phần 4. Luồng chạy từ đầu đến cuối](#phần-4--luồng-chạy-từ-đầu-đến-cuối)
- [Phần 5. Cách chạy hệ thống](#phần-5--cách-chạy-hệ-thống)
- [Phần 6. Thầy hỏi thì trả lời thế nào](#phần-6--thầy-hỏi-thì-trả-lời-thế-nào)
- [Phần 7. Checklist hoàn thành bài](#phần-7--checklist-hoàn-thành-bài)
- [Phần 8. JWT chuyên sâu (đọc sau khi nắm Phần 2)](#phần-8--jwt-chuyên-sâu)

---

# PHẦN 0 — BỨC TRANH TOÀN CẢNH

## 0.1. Nhóm bạn đang làm cái gì

Một website **đặt sân bóng đá mini** tên là **PitchOS**. Người dùng vào xem danh sách sân, chọn giờ, đặt sân. Chủ sân duyệt đơn.

Chuyện đặc biệt là: thay vì viết **một** chương trình to làm tất cả, nhóm bạn chia thành **ba chương trình nhỏ chạy riêng**:

| Chương trình | Cổng | Lo việc gì | Ai làm |
| :--- | :---: | :--- | :--- |
| `pitchos-auth-service` | 8081 | Đăng ký, đăng nhập, quản lý tài khoản | **BẠN** |
| `pitchos-pitch-service` | 8082 | Quản lý sân bóng | Linh |
| `pitchos-booking-service` | 8083 | Đặt sân, duyệt đơn | Nhật |

Mỗi chương trình có **cơ sở dữ liệu riêng**, không ai được chọc vào CSDL của ai. Muốn lấy dữ liệu của nhau thì phải **gọi API** qua mạng.

Cách chia này gọi là **kiến trúc microservice** (hay SOA — kiến trúc hướng dịch vụ). Đó là chủ đề của cả môn học này.

## 0.2. "Cổng" (port) là gì

Máy tính chỉ có một địa chỉ (`localhost`), nhưng chạy được nhiều chương trình cùng lúc. Cổng là **số hiệu để phân biệt** chúng.

- `localhost:8081` → gõ vào đây là nói chuyện với chương trình của bạn
- `localhost:8082` → nói chuyện với chương trình của Linh

Giống như chung một tòa nhà (localhost) nhưng khác số phòng (8081, 8082).

## 0.3. Vị trí của bạn trong nhóm

Bạn làm phần **bảo mật** — tức là:

> Ai được vào? Vào rồi thì được làm gì?

Hai service kia lo nghiệp vụ (sân bóng, đơn đặt). Bạn lo **canh cửa** cho cả ba. Đó là lý do phần của bạn được **3,0 điểm**, cao nhất nhóm.

---

# PHẦN 1 — NHIỆM VỤ CỦA BẠN LÀ GÌ

Đề thi chia làm 2 câu. Bạn phụ trách **1 ý ở mỗi câu**.

## 1.1. Câu 1 Ý 3 — Lý thuyết (1,0 điểm)

Đề yêu cầu bạn **nói** được 4 thứ:

1. Phân biệt **xác thực** (authentication) và **phân quyền** (authorization)
2. Trình bày cách dùng **JWT** để bảo vệ API
3. Giải thích khác nhau giữa **HTTP 401** và **HTTP 403**
4. Liên hệ với **ít nhất một vai trò** người dùng trong đề tài

→ Nằm ở **slide 3 đến 8**.

## 1.2. Câu 2 Ý 4 — Thực nghiệm (2,0 điểm)

Đề yêu cầu bạn **làm được** 4 thứ:

1. Triển khai **đăng nhập + JWT**
2. **Bảo vệ API**, phân biệt quyền của ít nhất **2 vai trò**
3. Kiểm tra cả truy cập **hợp lệ và không hợp lệ**, đặc biệt là trường hợp **đã đăng nhập nhưng không có quyền**
4. **Nộp bộ kiểm thử** và kết quả

→ Code đã viết xong, nằm ở **slide 9 đến 14**.

## 1.3. Bạn phải nộp những gì

| Sản phẩm | Nộp ở đâu | Trạng thái |
| :--- | :--- | :--- |
| Slide 15 trang | Tài khoản cá nhân trong Class | ✅ `docs/SLIDE_HOANG_PitchOS.pptx` |
| Video thực hành | Tài khoản cá nhân trong Class | ⬜ **Bạn phải tự quay** |
| Báo cáo Chương 4 & 5 | Nhóm nộp chung | ✅ Đã có trong `docs/` |
| Mã nguồn + Postman | Nhóm nộp chung | ✅ Đã có trong repo |

> **Nhớ:** thầy nói rõ — **không được nén file zip**, nén là 0 điểm. Upload thẳng file hoặc dán link.

---

# PHẦN 2 — KIẾN THỨC NỀN TỐI THIỂU

Phần này giải thích mọi từ chuyên môn bạn sẽ gặp. Đọc một lượt, không cần nhớ hết.

## 2.1. API là gì

**API** là cái "cửa sổ giao dịch" của một chương trình. Bạn gửi yêu cầu vào, nó trả kết quả ra.

Ví dụ thật trong bài của bạn:

```
Gửi đi:  POST http://localhost:8081/api/v1/auth/login
         { "username": "chusan", "password": "123456" }

Nhận về: 200 OK
         { "accessToken": "eyJhbGci...", "role": "chusan" }
```

- `POST` là **phương thức** — kiểu hành động
- `/api/v1/auth/login` là **đường dẫn** — gọi cái gì
- Phần trong `{ }` là **body** — dữ liệu gửi kèm, định dạng **JSON**

## 2.2. Các phương thức HTTP

| Phương thức | Nghĩa | Ví dụ trong bài |
| :--- | :--- | :--- |
| `GET` | Lấy dữ liệu về xem | `GET /api/v1/users/1` — xem user số 1 |
| `POST` | Tạo mới | `POST /api/v1/auth/register` — tạo tài khoản |
| `PUT` | Thay thế toàn bộ | (không dùng trong phần của bạn) |
| `PATCH` | Sửa một phần | `PATCH /api/v1/pitches/1/status` — đổi trạng thái sân |
| `DELETE` | Xóa | (không dùng trong phần của bạn) |

## 2.3. Mã trạng thái HTTP — RẤT QUAN TRỌNG

Mỗi lần trả lời, server kèm theo một con số cho biết chuyện gì đã xảy ra.

| Mã | Tên | Nghĩa | Khi nào gặp trong bài của bạn |
| :---: | :--- | :--- | :--- |
| **200** | OK | Thành công | Đăng nhập đúng, xem thông tin |
| **201** | Created | Tạo mới thành công | Đăng ký xong, tạo sân xong |
| **400** | Bad Request | Dữ liệu gửi lên sai | Email sai định dạng, mật khẩu quá ngắn |
| **401** | Unauthorized | **Chưa biết bạn là ai** | Không gửi token, token sai, sai mật khẩu |
| **403** | Forbidden | **Biết rồi nhưng không cho** | Khách hàng đòi thêm sân |
| **404** | Not Found | Không tìm thấy | Tìm user ID 999999 |
| **500** | Internal Error | Server tự lỗi | Lỗi lập trình (cần tránh) |

> **Phân biệt 401 và 403 là trọng tâm bài bạn.** Nhớ câu này:
> **401 = "Anh là ai?"** · **403 = "À biết anh rồi, nhưng không được."**

## 2.4. Xác thực và Phân quyền

Hai cái này **khác nhau** và **xảy ra ở hai thời điểm khác nhau**.

**Xác thực (Authentication)** — trả lời *"Bạn là ai?"*
- Xảy ra **một lần** lúc đăng nhập
- Đối chiếu username + password
- Thành công → cấp cho bạn một cái **token**
- Thất bại → **401**

**Phân quyền (Authorization)** — trả lời *"Bạn được làm gì?"*
- Xảy ra ở **mọi lần** gọi API sau đó
- Xét **vai trò** của bạn
- Thất bại → **403**

Ví dụ đời thường: vào tòa nhà phải quẹt thẻ (xác thực). Có thẻ rồi nhưng thẻ nhân viên thì không mở được phòng giám đốc (phân quyền).

## 2.5. JWT là gì

**JWT** = JSON Web Token. Là một **chuỗi ký tự dài** mà server cấp cho bạn sau khi đăng nhập thành công. Từ đó về sau, mỗi lần gọi API bạn **đính kèm chuỗi này** để server biết bạn là ai.

Nó trông như thế này (3 phần ngăn bởi dấu chấm):

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjaHVzYW4iLCJyb2xlIjoiY2h1c2FuIn0.4f9a2c7e1b
└──── Header ─────┘ └──────────── Payload ─────────────┘ └─ Signature ─┘
```

**Phần 1 — Header:** khai báo thuật toán ký. Giải mã ra là `{ "alg": "HS256" }`

**Phần 2 — Payload:** thông tin về bạn. Giải mã ra là:
```json
{
  "sub": "chusan",        ← tên đăng nhập
  "userId": 2,            ← mã số người dùng
  "role": "chusan",       ← vai trò
  "exp": 1793422501       ← thời điểm hết hạn
}
```

> ⚠️ **Payload KHÔNG được mã hóa bảo mật**, chỉ mã hóa Base64 — ai cũng đọc được.
> Vì vậy **tuyệt đối không để mật khẩu vào đây.** Đây là câu thầy rất hay hỏi.

**Phần 3 — Signature (chữ ký):** đây là phần bảo mật thật sự.

Nó được tính bằng công thức:
```
Signature = HMAC-SHA256( Header + Payload, SECRET_KEY )
```

`SECRET_KEY` là một chuỗi bí mật **chỉ server biết**. Nếu kẻ xấu sửa Payload (ví dụ đổi `role` từ `user` thành `admin`), thì chữ ký không còn khớp → server từ chối ngay.

**Đây là lý do JWT an toàn dù ai cũng đọc được nội dung.**

> 📖 **Muốn hiểu sâu hơn** — có cả token thật được tính tay từng bước và chứng minh bằng số liệu — xem **[Phần 8](#phần-8--jwt-chuyên-sâu)** ở cuối tài liệu. Nên đọc sau khi đã nắm hết Phần 2.

## 2.6. Stateless — vì sao chọn JWT

Cách cũ (session): server phải **nhớ** ai đang đăng nhập, lưu trong bộ nhớ.

Vấn đề: nhóm bạn có **ba chương trình chạy riêng**. Lưu ở đâu để cả ba cùng biết?

JWT giải quyết: **server không nhớ gì cả**. Mỗi request, client tự mang token theo. Ba service dùng chung một `SECRET_KEY` nên ai cũng tự kiểm tra chữ ký được, **không cần hỏi nhau**.

Tính chất này gọi là **stateless** (phi trạng thái).

## 2.7. BCrypt là gì

Nếu lưu mật khẩu nguyên văn vào CSDL, ai xem được CSDL là biết hết mật khẩu. Nên phải **băm** (hash) nó.

**Băm** = biến đổi một chiều. Từ `123456` ra được chuỗi băm, nhưng từ chuỗi băm **không thể** suy ngược lại `123456`.

Chuỗi băm BCrypt trông như này:
```
$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
└┬┘└┬┘└──────── salt ────────┘└──────── hash ──────────────┘
 │  └── cost factor = 10 (nghĩa là lặp 2^10 = 1024 vòng)
 └───── phiên bản thuật toán
```

**Ba lý do chọn BCrypt thay vì MD5:**

1. **Salt riêng từng mật khẩu** — hai người cùng đặt `123456` vẫn ra hai chuỗi băm khác nhau
2. **Cố tình chạy chậm** — bạn đăng nhập chỉ chờ thêm vài chục mili giây, nhưng kẻ xấu muốn dò hàng triệu mật khẩu thì mất hàng năm
3. **Một chiều** — khi đăng nhập, hệ thống **băm lại rồi so sánh**, chứ không giải mã

> MD5 chạy rất nhanh — mà nhanh chính là thứ kẻ tấn công cần. Đó là lý do không dùng MD5.

## 2.8. Các từ Spring Boot hay gặp

Spring Boot là **khung (framework)** để viết server bằng Java. Nó có cơ chế tự động: bạn gắn **annotation** (mấy chữ bắt đầu bằng `@`) lên class, Spring sẽ tự hiểu và xử lý.

| Annotation | Nghĩa nôm na |
| :--- | :--- |
| `@RestController` | "Class này là cửa ngõ nhận request từ ngoài vào" |
| `@Service` | "Class này chứa logic nghiệp vụ" |
| `@Repository` | "Class này nói chuyện với cơ sở dữ liệu" |
| `@Configuration` | "Class này chứa cấu hình" |
| `@Bean` | "Tạo sẵn một đối tượng để Spring quản lý, chỗ nào cần thì đưa" |
| `@Entity` | "Class này ánh xạ vào một bảng trong CSDL" |
| `@Valid` | "Kiểm tra dữ liệu này có hợp lệ không trước khi xử lý" |
| `@Transactional` | "Cả khối này thành công hết, hoặc hủy hết" |

**Khái niệm "tiêm phụ thuộc" (Dependency Injection):** bạn không tự `new` đối tượng ra, mà khai báo trong constructor, Spring tự đưa vào. Ví dụ:

```java
public AuthService(UserRepository userRepository, ...) {
    this.userRepository = userRepository;   // Spring tự đưa vào đây
}
```

## 2.9. Các tầng trong một ứng dụng Spring Boot

Code được chia thành các **tầng**, mỗi tầng một việc:

```
Client (Postman / trình duyệt)
      ↓  gửi HTTP request
┌─────────────────────────────┐
│  Controller                 │  ← nhận request, trả response
├─────────────────────────────┤
│  Service                    │  ← xử lý nghiệp vụ (nghĩ)
├─────────────────────────────┤
│  Repository                 │  ← nói chuyện với CSDL
├─────────────────────────────┤
│  Entity                     │  ← ánh xạ bảng trong CSDL
└─────────────────────────────┘
      ↓
   MySQL
```

Quy tắc: **Controller không bao giờ gọi thẳng Repository.** Phải đi qua Service.

---

# PHẦN 3 — ĐI QUA TỪNG FILE CODE

## 3.1. Bản đồ thư mục

Toàn bộ code của bạn nằm ở:
```
pitchos-auth-service/src/main/java/com/pitchos/auth/
```

Có **21 file Java, tổng 1321 dòng**. Chia thành 7 nhóm:

```
auth/
├── PitchosAuthServiceApplication.java   (11 dòng)   ← điểm khởi động
│
├── entity/          ← ánh xạ bảng CSDL
│   ├── User.java                        (45 dòng)
│   └── Role.java                        (7 dòng)
│
├── repository/      ← truy vấn CSDL
│   └── UserRepository.java              (23 dòng)
│
├── dto/             ← gói dữ liệu vào/ra
│   ├── RegisterRequest.java             (48 dòng)
│   ├── LoginRequest.java                (24 dòng)
│   ├── LoginResponse.java               (44 dòng)
│   ├── UserResponse.java                (61 dòng)
│   └── ErrorResponse.java               (45 dòng)
│
├── security/        ← ⭐ LÕI BẢO MẬT, phần quan trọng nhất
│   ├── JwtTokenProvider.java            (112 dòng)
│   ├── JwtAuthenticationFilter.java     (73 dòng)
│   └── SecurityConfig.java              (139 dòng)
│
├── service/         ← nghiệp vụ
│   └── AuthService.java                 (146 dòng)
│
├── controller/      ← cửa ngõ API
│   ├── AuthController.java              (77 dòng)
│   └── UserController.java              (96 dòng)
│
├── exception/       ← xử lý lỗi
│   ├── GlobalExceptionHandler.java      (201 dòng)
│   ├── UnauthorizedException.java       (10 dòng)
│   ├── BadRequestException.java         (7 dòng)
│   └── ResourceNotFoundException.java   (7 dòng)
│
└── config/          ← cấu hình phụ
    ├── DataInitializer.java             (103 dòng)
    └── OpenApiConfig.java               (42 dòng)
```

> **Nếu chỉ có thời gian đọc 3 file**, hãy đọc: `JwtTokenProvider`, `SecurityConfig`, `AuthService`. Ba file này là linh hồn bài của bạn.

---

## 3.2. NHÓM 1 — Entity và Repository (tầng dữ liệu)

### `entity/Role.java` — 7 dòng

```java
public enum Role {
    admin,
    chusan,
    user
}
```

**Giải thích:** `enum` là kiểu dữ liệu chỉ nhận một trong các giá trị liệt kê sẵn. Ở đây vai trò chỉ có thể là một trong ba giá trị này, không thể là gì khác.

> **Chú ý:** viết **thường** (`chusan` chứ không phải `CHUSAN`). Chi tiết này cực kỳ quan trọng, giải thích ở mục 3.4.1.

### `entity/User.java` — 45 dòng

Class này **ánh xạ 1-1 với bảng `users`** trong CSDL.

```java
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 50)
    private String username;
    ...
}
```

| Dòng code | Nghĩa |
| :--- | :--- |
| `@Entity` | Nói với Spring: class này là một bảng trong CSDL |
| `@Table(name = "users")` | Tên bảng là `users` |
| `@Id` | Trường này là khóa chính |
| `@GeneratedValue(IDENTITY)` | ID tự tăng, không cần tự gán |
| `@Column(nullable = false)` | Cột bắt buộc có giá trị |
| `@Column(unique = true)` | Không được trùng |
| `@Enumerated(EnumType.STRING)` | Lưu vai trò dưới dạng chữ (`"chusan"`) chứ không phải số |

Các trường: `id`, `username`, `email`, `password`, `fullName`, `phone`, `role`, `createdAt`.

> **File này do bạn Hùng viết** (bạn ấy phụ trách tầng dữ liệu cả 3 service). Bạn chỉ dùng lại.

### `repository/UserRepository.java` — 23 dòng

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByUsername(String username);
    Optional<User> findByEmail(String email);
    Boolean existsByUsername(String username);
    Boolean existsByEmail(String email);
    List<User> findByRole(Role role);
}
```

**Điều kỳ diệu ở đây:** bạn **không viết câu SQL nào cả**. Chỉ cần đặt tên hàm theo quy tắc, Spring Data JPA **tự sinh câu truy vấn**.

- `findByUsername` → Spring tự hiểu: `SELECT * FROM users WHERE username = ?`
- `existsByEmail` → `SELECT COUNT(*) > 0 FROM users WHERE email = ?`

`extends JpaRepository<User, Long>` cho bạn miễn phí các hàm: `save()`, `findById()`, `findAll()`, `delete()`, `count()`.

`Optional<User>` nghĩa là "có thể có user, có thể không" — buộc bạn phải xử lý trường hợp không tìm thấy, tránh lỗi null.

---

## 3.3. NHÓM 2 — DTO (gói dữ liệu vào/ra)

**DTO** = Data Transfer Object. Là các class chỉ để **đóng gói dữ liệu** đi vào hoặc đi ra qua API.

**Vì sao cần DTO mà không dùng thẳng Entity?** Hai lý do:
1. **Bảo mật** — Entity `User` có trường `password`. Nếu trả thẳng Entity ra ngoài, chuỗi băm mật khẩu sẽ lộ.
2. **Linh hoạt** — dữ liệu client gửi lên khác với dữ liệu lưu trong CSDL (ví dụ client gửi mật khẩu thô, CSDL lưu bản đã băm).

### `dto/RegisterRequest.java` — 48 dòng

Dữ liệu client gửi lên khi đăng ký.

```java
@NotBlank(message = "Tên đăng nhập không được để trống")
@Size(min = 4, max = 50, message = "Tên đăng nhập phải từ 4 đến 50 ký tự")
private String username;

@NotBlank(message = "Email không được để trống")
@Email(message = "Email không đúng định dạng")
private String email;

@NotBlank(message = "Mật khẩu không được để trống")
@Size(min = 6, max = 100, message = "Mật khẩu phải có ít nhất 6 ký tự")
private String password;

@Pattern(regexp = "^$|^(0|\\+84)\\d{9}$", message = "Số điện thoại phải gồm 10 chữ số...")
private String phone;
```

| Annotation | Kiểm tra gì |
| :--- | :--- |
| `@NotBlank` | Không được trống hoặc chỉ toàn khoảng trắng |
| `@Size(min, max)` | Độ dài trong khoảng cho phép |
| `@Email` | Phải đúng định dạng email |
| `@Pattern(regexp)` | Phải khớp mẫu (ở đây là SĐT Việt Nam 10 số) |

**Đây chính là phần "kiểm tra dữ liệu đầu vào" mà đề bài yêu cầu.** Khi dữ liệu sai, hệ thống tự trả về **400 Bad Request** kèm danh sách lỗi từng trường.

> **Lưu ý quan trọng:** `RegisterRequest` **không có trường `role`**. Cố ý như vậy — nếu cho client tự khai vai trò thì ai cũng tự đăng ký được tài khoản admin. Đây là lỗ hổng **leo thang đặc quyền** (privilege escalation).

### `dto/LoginRequest.java` — 24 dòng

Đơn giản, chỉ 2 trường `username` và `password`, đều `@NotBlank`.

### `dto/LoginResponse.java` — 44 dòng

Dữ liệu trả về khi đăng nhập thành công:

```java
private String accessToken;   // chuỗi JWT
private String tokenType;     // luôn là "Bearer"
private Long expiresIn;       // sống được bao nhiêu giây
private Long userId;
private String username;
private String fullName;
private Role role;
```

> **Không có trường `password`.** Đúng nguyên tắc.

### `dto/UserResponse.java` — 61 dòng

Thông tin user trả ra ngoài. Có hàm đặc biệt:

```java
public static UserResponse fromEntity(User user) {
    return UserResponse.builder()
            .id(user.getId())
            .username(user.getUsername())
            // ... KHÔNG có .password(...)
            .build();
}
```

Hàm này chuyển từ Entity sang DTO và **cố tình bỏ qua trường password**.

### `dto/ErrorResponse.java` — 45 dòng

Khuôn JSON lỗi dùng chung cho cả ba service:

```json
{
  "timestamp": "2026-10-30T11:55:12.345",
  "status": 401,
  "error": "Unauthorized",
  "message": "Chưa xác thực danh tính...",
  "path": "/api/v1/users/me",
  "errors": { "email": "Email không đúng định dạng" }
}
```

Trường `errors` chỉ xuất hiện khi lỗi validation (400), các lỗi khác thì không có.

---

## 3.4. NHÓM 3 — SECURITY (phần quan trọng nhất)

> ⭐ **Đây là phần ăn điểm. Nếu thầy hỏi code, 90% là hỏi ba file này.**

### 3.4.1. `security/JwtTokenProvider.java` — 112 dòng

Đây là **nhà máy sản xuất token**. Nó làm 2 việc: **sinh** token và **giải mã** token.

#### Phần khởi tạo khóa

```java
public JwtTokenProvider(
        @Value("${jwt.secret:404E6352...}") String secret,
        @Value("${jwt.expiration-ms:86400000}") long expirationMs) {
    this.key = Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    this.expirationMs = expirationMs;
}
```

- `@Value("${jwt.secret}")` — lấy giá trị từ file cấu hình `application.properties`
- `86400000` mili-giây = **24 giờ** (token sống 1 ngày)
- `Keys.hmacShaKeyFor(...)` — biến chuỗi secret thành đối tượng khóa để ký

> ⚠️ **Chi tiết dễ sai:** phải dùng đúng `Decoders.BASE64.decode(secret)` giống hệt hai service kia. Nếu bạn nạp khóa theo cách khác (ví dụ `secret.getBytes()`), thì **cùng một chuỗi secret vẫn ra mảng byte khác nhau** → chữ ký lệch → token bị từ chối.

#### Hàm sinh token — **DÒNG 63 LÀ DÒNG QUAN TRỌNG NHẤT CẢ BÀI**

```java
public String generateToken(User user) {
    Date now = new Date();
    Date expiryDate = new Date(now.getTime() + expirationMs);

    Map<String, Object> claims = new LinkedHashMap<>();
    claims.put("userId", user.getId());
    claims.put("role", user.getRole().name().toLowerCase());   // ← DÒNG 63
    claims.put("fullName", user.getFullName());

    return Jwts.builder()
            .setSubject(user.getUsername())    // sub = tên đăng nhập
            .addClaims(claims)                 // gắn các claim vào
            .setIssuedAt(now)                  // iat = lúc phát hành
            .setExpiration(expiryDate)         // exp = lúc hết hạn
            .signWith(key, SignatureAlgorithm.HS256)   // ký bằng HS256
            .compact();                        // đóng gói thành chuỗi
}
```

**Vì sao dòng 63 quan trọng?**

Spring Security có một **quy ước ngầm**: khi bạn viết `hasRole("chusan")`, nó **tự động ghép thêm tiền tố** `ROLE_` rồi mới so sánh — tức nó đi tìm quyền tên là `ROLE_chusan`.

Mà bộ lọc của cả ba service đều ghép `"ROLE_" + role` lấy từ token.

Nên nếu bạn cấp token với `role = "ROLE_CHUSAN"`, thì quyền sẽ thành:
```
"ROLE_" + "ROLE_CHUSAN" = "ROLE_ROLE_CHUSAN"   ← không khớp gì cả!
```

→ **Toàn bộ API của Pitch Service và Booking Service sẽ trả về 403.**

> Đây là lỗi **suýt xảy ra** với nhóm bạn: Linh và Nhật viết bộ lọc **trước khi** Auth Service hoàn thành. Nếu không thống nhất quy ước từ đầu thì cả hệ thống hỏng mà rất khó tìm ra nguyên nhân.

#### Hàm giải mã token

```java
public Claims parseToken(String token) {
    return Jwts.parserBuilder()
            .setSigningKey(key)
            .build()
            .parseClaimsJws(token)
            .getBody();
}
```

Hàm này **tự động ném lỗi** nếu chữ ký sai hoặc token hết hạn. Không cần tự kiểm tra.

### 3.4.2. `security/JwtAuthenticationFilter.java` — 73 dòng

Đây là **trạm kiểm soát đầu tiên**. Mọi request đều phải đi qua đây trước khi đến controller.

```java
String authHeader = request.getHeader("Authorization");

if (authHeader != null && authHeader.startsWith("Bearer ")) {
    String token = authHeader.substring(7).trim();     // bỏ 7 ký tự "Bearer "
    try {
        Claims claims = jwtTokenProvider.parseToken(token);
        String username = jwtTokenProvider.getUsername(claims);
        String role = jwtTokenProvider.getRole(claims);

        if (role != null) {
            List<SimpleGrantedAuthority> authorities = new ArrayList<>();
            authorities.add(new SimpleGrantedAuthority("ROLE_" + role.toLowerCase()));
            authorities.add(new SimpleGrantedAuthority(role.toLowerCase()));

            SecurityContextHolder.getContext().setAuthentication(
                new UsernamePasswordAuthenticationToken(username, null, authorities));
        }
    } catch (JwtException | IllegalArgumentException ex) {
        SecurityContextHolder.clearContext();     // token hỏng → xóa sạch
    }
}
filterChain.doFilter(request, response);          // cho request đi tiếp
```

**Giải thích từng bước:**

1. Lấy header `Authorization` từ request
2. Nếu có và bắt đầu bằng `"Bearer "` thì cắt lấy phần token
3. Giải mã token, lấy ra username và role
4. Nạp quyền vào `SecurityContextHolder` — đây là "bộ nhớ tạm" của Spring Security cho request này
5. Nếu token hỏng → **xóa context, KHÔNG tự trả lỗi**
6. Cho request đi tiếp

> **Vì sao nạp 2 dạng quyền** (`ROLE_chusan` và `chusan`)?
> Để cấu hình phân quyền viết kiểu `hasRole("chusan")` hay `hasAuthority("chusan")` đều chạy được.

> **Vì sao khi token hỏng lại không tự trả lỗi?**
> Để **mọi phản hồi 401 đi qua đúng một chỗ** (là `AuthenticationEntryPoint` ở file sau). Như vậy khuôn JSON lỗi luôn thống nhất, thay vì mỗi chỗ trả một kiểu.

### 3.4.3. `security/SecurityConfig.java` — 139 dòng

Đây là **bản khai báo luật**: API nào ai được gọi.

#### Bean mã hóa mật khẩu

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```

Khai báo một lần ở đây, chỗ nào cần thì Spring tự đưa vào.

#### Ma trận phân quyền — **DÒNG 79 LÀ DÒNG BẠN SẼ SỬA KHI DEMO**

```java
.authorizeHttpRequests(auth -> auth
        // 1. Hai API này phải công khai, không thì không ai đăng nhập được
        .requestMatchers(HttpMethod.POST, "/api/v1/auth/register", "/api/v1/auth/login").permitAll()

        // 2. Swagger cũng công khai
        .requestMatchers("/swagger-ui/**", "/api-docs/**", ...).permitAll()

        // 3. Danh sách người dùng: CHỈ admin          ← DÒNG 79
        .requestMatchers(HttpMethod.GET, "/api/v1/users").hasRole("admin")

        // 4. Mọi thứ còn lại: phải đăng nhập
        .anyRequest().authenticated()
)
```

| Lệnh | Nghĩa |
| :--- | :--- |
| `permitAll()` | Ai cũng gọi được, không cần token |
| `hasRole("admin")` | Chỉ vai trò admin |
| `hasAnyRole("a", "b")` | Một trong các vai trò liệt kê |
| `authenticated()` | Phải đăng nhập, vai trò nào cũng được |

> **Thứ tự rất quan trọng!** Spring đọc từ trên xuống, **gặp luật nào khớp trước thì dùng luật đó**. Nên `.anyRequest()` luôn đặt cuối cùng.

#### Cấu hình STATELESS

```java
.sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
```

Bắt Spring **không tạo session**. Bắt buộc phải có khi dùng JWT.

#### Hai bộ xử lý lỗi — 401 và 403

```java
.exceptionHandling(ex -> ex
        .authenticationEntryPoint(authenticationEntryPoint())   // → 401
        .accessDeniedHandler(accessDeniedHandler())             // → 403
)
```

Hai bean này nằm cuối file:

```java
@Bean
public AuthenticationEntryPoint authenticationEntryPoint() {
    return (request, response, authException) -> {
        response.setStatus(HttpStatus.UNAUTHORIZED.value());   // 401
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        ErrorResponse errorResponse = ErrorResponse.builder()
                .status(401).error("Unauthorized")
                .message("Chưa xác thực danh tính...")
                .path(request.getRequestURI())
                .build();
        response.getWriter().write(objectMapper.writeValueAsString(errorResponse));
    };
}
```

`AccessDeniedHandler` tương tự nhưng trả **403**.

> **Nhớ:** `AuthenticationEntryPoint` = chưa biết bạn là ai = **401**.
> `AccessDeniedHandler` = biết rồi nhưng không đủ quyền = **403**.

---

## 3.5. NHÓM 4 — Service (tầng nghiệp vụ)

### `service/AuthService.java` — 146 dòng

Đây là nơi chứa **logic nghiệp vụ**. Có 5 hàm.

#### Hàm 1 — `register()` — Đăng ký

```java
@Transactional
public UserResponse register(RegisterRequest request) {
    String username = request.getUsername().trim();
    String email = request.getEmail().trim();

    if (userRepository.existsByUsername(username)) {
        throw new BadRequestException("Tên đăng nhập '" + username + "' đã tồn tại...");
    }
    if (userRepository.existsByEmail(email)) {
        throw new BadRequestException("Email '" + email + "' đã được sử dụng...");
    }

    User user = User.builder()
            .username(username)
            .email(email)
            .password(passwordEncoder.encode(request.getPassword()))   // ← BĂM BCRYPT
            .fullName(request.getFullName().trim())
            .role(Role.user)                                           // ← ÉP CỨNG
            .build();

    User saved = userRepository.save(user);
    return UserResponse.fromEntity(saved);
}
```

**Hai dòng cần nhớ:**
- `passwordEncoder.encode(...)` — băm mật khẩu **trước khi** lưu. CSDL không bao giờ thấy mật khẩu gốc.
- `.role(Role.user)` — **ép cứng** vai trò, bất kể client gửi gì. Chống leo thang đặc quyền.

#### Hàm 2 — `login()` — Đăng nhập

```java
@Transactional(readOnly = true)
public LoginResponse login(LoginRequest request) {
    User user = userRepository.findByUsername(request.getUsername().trim())
            .orElseThrow(() -> new UnauthorizedException("Tên đăng nhập hoặc mật khẩu không đúng"));

    if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
        throw new UnauthorizedException("Tên đăng nhập hoặc mật khẩu không đúng");
    }

    String accessToken = jwtTokenProvider.generateToken(user);
    return LoginResponse.builder()
            .accessToken(accessToken)
            .tokenType("Bearer")
            .expiresIn(jwtTokenProvider.getExpiresInSeconds())
            .userId(user.getId())
            .role(user.getRole())
            .build();
}
```

**`passwordEncoder.matches(mậtKhẩuThô, chuỗiBămTrongDB)`** hoạt động thế nào?
1. Lấy phần **salt** ra khỏi chuỗi băm đã lưu
2. Băm lại mật khẩu vừa nhập **bằng chính salt đó**
3. So sánh hai kết quả

Chứ **không** giải mã ngược chuỗi băm — việc đó không làm được.

> **Chi tiết bảo mật tinh tế:** cả hai trường hợp (sai username, sai password) đều trả về **cùng một thông báo**. Nếu phân biệt, kẻ xấu có thể dùng API đăng nhập để **dò xem tài khoản nào tồn tại** trong hệ thống.

#### Hàm 3 — `getUserById()` — **KIỂM TRA QUYỀN SỞ HỮU**

> ⭐ Đây là phần đề bài yêu cầu riêng: *"trường hợp người dùng đã đăng nhập nhưng không có quyền truy cập tài nguyên"*.

```java
@Transactional(readOnly = true)
public UserResponse getUserById(Long id, String currentUsername) {
    User target = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Không tìm thấy người dùng với mã ID: " + id));

    User current = userRepository.findByUsername(currentUsername)
            .orElseThrow(() -> new UnauthorizedException("Phiên đăng nhập không hợp lệ"));

    if (current.getRole() == Role.user && !current.getId().equals(target.getId())) {
        throw new AccessDeniedException(
            "Truy cập bị từ chối. Tài khoản vai trò 'user' chỉ được xem thông tin của chính mình.");
    }

    return UserResponse.fromEntity(target);
}
```

**Vì sao cần hàm này?**

Xét tình huống: tài khoản `user` có ID 3 gọi `GET /api/v1/users/1` để xem thông tin của admin.
- Token **hợp lệ** ✅
- Vai trò `user` **được phép** gọi endpoint này ✅
- → Nếu chỉ xét vai trò thì **request được chấp nhận, dữ liệu người khác bị lộ!**

Nên phải tra **cả hai** bản ghi rồi đối chiếu ID. Nguyên tắc: **không tin tưởng ID do client gửi lên.**

#### Hàm 4 và 5

- `getCurrentUser(username)` — lấy thông tin chính mình
- `getAllUsers()` — lấy danh sách tất cả (chỉ admin gọi được, đã chặn ở `SecurityConfig`)

---

## 3.6. NHÓM 5 — Controller (cửa ngõ API)

### `controller/AuthController.java` — 77 dòng

```java
@RestController
@RequestMapping("/api/v1/auth")      // mọi API trong class này bắt đầu bằng đường dẫn này
public class AuthController {

    @PostMapping("/register")        // → POST /api/v1/auth/register
    public ResponseEntity<UserResponse> register(@Valid @RequestBody RegisterRequest request) {
        UserResponse created = authService.register(request);
        return ResponseEntity.created(location).body(created);     // trả 201
    }

    @PostMapping("/login")           // → POST /api/v1/auth/login
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));      // trả 200
    }
}
```

| Thành phần | Nghĩa |
| :--- | :--- |
| `@RequestMapping("/api/v1/auth")` | Tiền tố đường dẫn chung |
| `@PostMapping("/register")` | Nhận request `POST` tại `/register` |
| `@RequestBody` | Lấy dữ liệu từ phần body của request |
| `@Valid` | **Chạy kiểm tra validation** — nếu sai tự ném lỗi → 400 |
| `ResponseEntity.created(...)` | Trả mã **201 Created** |
| `ResponseEntity.ok(...)` | Trả mã **200 OK** |

> Để ý: Controller **rất mỏng**, chỉ gọi sang Service rồi trả kết quả. Toàn bộ suy nghĩ nằm ở Service. Đó là thiết kế đúng.

### `controller/UserController.java` — 96 dòng

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @GetMapping("/me")
    public ResponseEntity<UserResponse> getCurrentUser(Authentication authentication) {
        return ResponseEntity.ok(authService.getCurrentUser(authentication.getName()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id,
                                                     Authentication authentication) {
        return ResponseEntity.ok(authService.getUserById(id, authentication.getName()));
    }

    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        return ResponseEntity.ok(authService.getAllUsers());
    }
}
```

**`Authentication authentication`** ở tham số là gì?

Spring **tự động đưa vào** đối tượng này — nó chứa thông tin người đang đăng nhập, lấy từ `SecurityContextHolder` mà `JwtAuthenticationFilter` đã nạp ở bước trước.

`authentication.getName()` trả về **username** của người đang gọi API. Nhờ đó Service biết ai đang hỏi để kiểm tra quyền sở hữu.

**`@PathVariable Long id`** — lấy giá trị từ đường dẫn. Gọi `/api/v1/users/5` thì `id = 5`.

---

## 3.7. NHÓM 6 — Exception (xử lý lỗi)

### Ba class lỗi tùy biến

```java
public class BadRequestException extends RuntimeException { ... }      // → 400
public class UnauthorizedException extends RuntimeException { ... }    // → 401
public class ResourceNotFoundException extends RuntimeException { ... } // → 404
```

Mỗi class chỉ 7–10 dòng. Chúng là **tín hiệu**: Service ném ra, Handler bắt và chuyển thành mã HTTP tương ứng.

### `exception/GlobalExceptionHandler.java` — 201 dòng

Class này **bắt toàn bộ lỗi** trong ứng dụng và biến thành JSON đẹp.

```java
@RestControllerAdvice      // ← "class này canh lỗi cho TOÀN BỘ ứng dụng"
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)   // lỗi @Valid
    public ResponseEntity<ErrorResponse> handleValidationExceptions(...) {
        Map<String, String> fieldErrors = new HashMap<>();
        for (FieldError error : ex.getBindingResult().getFieldErrors()) {
            fieldErrors.put(error.getField(), error.getDefaultMessage());
        }
        // → trả 400 kèm map errors
    }
    ...
}
```

**Bảng các handler trong file:**

| Bắt lỗi gì | Trả về |
| :--- | :---: |
| `MethodArgumentNotValidException` (validation sai) | **400** + map errors |
| `UnauthorizedException` (sai mật khẩu) | **401** |
| `AccessDeniedException` (không đủ quyền) | **403** |
| `ResourceNotFoundException` | **404** |
| `BadRequestException`, `IllegalArgumentException` | **400** |
| `HttpMessageNotReadableException` (JSON sai cú pháp) | **400** |
| `MethodArgumentTypeMismatchException` (`/users/abc`) | **400** |
| `NoResourceFoundException` (URL không tồn tại) | **404** |
| `Exception` (mọi lỗi còn lại) | **500** |

> ⚠️ **Hai cái bẫy trong file này** — thầy rất có thể hỏi:
>
> **Bẫy 1 — `AccessDeniedException` phải khai báo riêng.**
> Nếu không, nó bị handler `Exception.class` bắt trước và gói thành **500** thay vì 403.
> Lý do: `@RestControllerAdvice` chạy **bên trong** `DispatcherServlet`, tức là **bên trong** `ExceptionTranslationFilter` của Spring Security.
>
> **Bẫy 2 — `NoResourceFoundException` cũng phải khai báo riêng.**
> Nếu không, gõ sai URL sẽ ra **500** thay vì 404 — sai hoàn toàn ngữ nghĩa HTTP.
> Lỗi này **thực sự đã xảy ra** khi chạy thử, sau đó mới sửa.

---

## 3.8. NHÓM 7 — Config

### `config/DataInitializer.java` — 103 dòng

Chạy **tự động một lần khi khởi động**. Làm 2 việc:

1. **Nếu CSDL trống** → tạo 3 tài khoản mẫu `admin`, `chusan`, `user` (mật khẩu đều `123456`)
2. **Nếu đã có** → kiểm tra lại mật khẩu 3 tài khoản đó, nếu không khớp `123456` thì **băm lại**

```java
private void repairDemoPasswords() {
    for (String username : List.of("admin", "chusan", "user")) {
        User user = found.get();
        if (!passwordEncoder.matches(DEFAULT_PASSWORD, user.getPassword())) {
            log.warn("Tài khoản '{}' có chuỗi băm BCrypt không khớp mật khẩu mặc định...", username);
            user.setPassword(passwordEncoder.encode(DEFAULT_PASSWORD));
            userRepository.save(user);
        }
    }
}
```

**Vì sao cần đoạn vá này?**

File SQL của Hùng (`pitchos-database/auth-user-service.sql`) ghi chú *"Mật khẩu mặc định: 123456"*, nhưng chuỗi băm nạp sẵn trong đó **không khớp** — đó là chuỗi băm mẫu lấy từ tài liệu Spring Security.

Nếu không có đoạn này, **đăng nhập sẽ thất bại ngay từ bước đầu tiên khi demo**.

Khi khởi động, nếu thấy dòng log `WARN ... không khớp mật khẩu mặc định` thì đúng là lỗi này.

### `config/OpenApiConfig.java` — 42 dòng

Cấu hình trang tài liệu API tự động (Swagger UI) tại `localhost:8081/swagger-ui.html`.

Phần đáng chú ý là khai báo nút **Authorize** (ổ khóa) để dán token vào test trực tiếp trên web.

### `PitchosAuthServiceApplication.java` — 11 dòng

```java
@SpringBootApplication
public class PitchosAuthServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(PitchosAuthServiceApplication.class, args);
    }
}
```

Điểm khởi động. `@SpringBootApplication` bảo Spring tự quét toàn bộ thư mục con, tìm các class có `@RestController`, `@Service`... rồi khởi tạo chúng.

---

## 3.9. File cấu hình

### `src/main/resources/application.properties`

```properties
server.port=${AUTH_SERVICE_PORT:8081}
spring.datasource.url=jdbc:mysql://${MYSQL_HOST:localhost}:${MYSQL_PORT:3306}/${AUTH_DB_NAME:pitchos_user_db}...
spring.jpa.hibernate.ddl-auto=update
jwt.secret=${JWT_SECRET:404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970}
jwt.expiration-ms=${JWT_EXPIRATION_MS:86400000}
```

**Cú pháp `${TÊN:giá_trị_mặc_định}`** nghĩa là: lấy từ biến môi trường, nếu không có thì dùng giá trị sau dấu hai chấm.

Nhờ vậy bạn đổi cổng được mà không sửa code — chỉ cần đặt biến môi trường.

`ddl-auto=update` — Hibernate tự tạo/cập nhật bảng trong CSDL theo Entity.

### `pom.xml`

File khai báo **thư viện** dự án dùng. Các thư viện chính:

| Thư viện | Dùng làm gì |
| :--- | :--- |
| `spring-boot-starter-web` | Xây REST API |
| `spring-boot-starter-data-jpa` | Nói chuyện với CSDL |
| `spring-boot-starter-security` | Bảo mật, phân quyền |
| `spring-boot-starter-validation` | Kiểm tra dữ liệu đầu vào |
| `jjwt` 0.11.5 | Sinh và giải mã JWT |
| `mysql-connector-j` | Driver kết nối MySQL |
| `springdoc-openapi` 2.5.0 | Sinh tài liệu Swagger |
| `lombok` | Tự sinh getter/setter, đỡ phải gõ tay |

---

# PHẦN 4 — LUỒNG CHẠY TỪ ĐẦU ĐẾN CUỐI

## 4.1. Luồng ĐĂNG NHẬP

```
1. Postman gửi:  POST /api/v1/auth/login { username, password }
         ↓
2. SecurityConfig: đường dẫn này permitAll() → cho qua, không cần token
         ↓
3. AuthController.login()  — @Valid kiểm tra không được trống
         ↓  (sai → 400)
4. AuthService.login()
   ├─ userRepository.findByUsername()  → tìm trong CSDL
   │     không thấy → ném UnauthorizedException → 401
   ├─ passwordEncoder.matches()        → so khớp mật khẩu
   │     không khớp → ném UnauthorizedException → 401
   └─ jwtTokenProvider.generateToken() → sinh token
         ↓
5. Trả về 200 OK + { accessToken, role, userId, ... }
```

## 4.2. Luồng GỌI API CÓ BẢO VỆ

```
1. Postman gửi:  GET /api/v1/users
                 Header: Authorization: Bearer eyJhbGci...
         ↓
2. JwtAuthenticationFilter
   ├─ Lấy token từ header
   ├─ parseToken() → kiểm tra chữ ký + hạn dùng
   │     hỏng → xóa context (chưa trả lỗi vội)
   └─ Nạp quyền ROLE_admin vào SecurityContextHolder
         ↓
3. AuthorizationFilter — đối chiếu với SecurityConfig
   ├─ Chưa đăng nhập       → AuthenticationEntryPoint → 401
   ├─ Sai vai trò          → AccessDeniedHandler      → 403
   └─ Đạt → đi tiếp
         ↓
4. UserController.getAllUsers()
         ↓
5. AuthService.getAllUsers() → truy vấn CSDL
         ↓
6. Trả về 200 OK + danh sách
```

## 4.3. Luồng BỊ TỪ CHỐI VÌ QUYỀN SỞ HỮU

```
1. Token của user (ID=3) gọi:  GET /api/v1/users/1
         ↓
2. JwtAuthenticationFilter  → token hợp lệ, nạp ROLE_user  ✅
         ↓
3. AuthorizationFilter → luật .anyRequest().authenticated() → ĐẠT  ✅
         ↓                    (vì user cũng được phép gọi endpoint này)
4. UserController.getUserById(1, "user")
         ↓
5. AuthService.getUserById()
   ├─ target = user ID 1 (admin)
   ├─ current = user ID 3
   └─ role==user && 3 != 1  → ném AccessDeniedException  ❌
         ↓
6. GlobalExceptionHandler bắt → trả 403 Forbidden
```

> **Để ý:** ở bước 3 request đã **vượt qua** tầng phân quyền theo vai trò. Nó chỉ bị chặn ở **tầng nghiệp vụ**. Đó chính là lý do phải có kiểm tra quyền sở hữu.

---

# PHẦN 5 — CÁCH CHẠY HỆ THỐNG

## 5.1. Xử lý xung đột cổng (máy bạn đang bị)

Máy bạn có 2 container của dự án khác chiếm cổng `3306` và `8081`:

```bash
docker stop okr_mysql okr-test-backend-1
```

Dùng xong nhớ bật lại:

```bash
docker start okr_mysql okr-test-backend-1
```

## 5.2. Bật MySQL

```bash
docker compose up -d
```

Lệnh này tạo container `pitchos-mysql`, tự chạy 3 file SQL của Hùng để tạo 3 cơ sở dữ liệu.

## 5.3. Bật Auth Service

```bash
cd pitchos-auth-service && mvn spring-boot:run
```

Chờ đến khi thấy dòng:
```
Started PitchosAuthServiceApplication in 8.142 seconds
```

## 5.4. Bật Pitch Service (cần cho demo liên dịch vụ)

```bash
cd pitchos-pitch-service && mvn spring-boot:run
```

## 5.5. Kiểm tra nhanh

Mở trình duyệt: `http://localhost:8081/swagger-ui.html`

Hoặc trong Postman chạy thư mục **0. Chuẩn bị** → phải ra **200 OK**.

## 5.6. Ba tài khoản có sẵn

| Username | Mật khẩu | Vai trò |
| :--- | :--- | :--- |
| `admin` | `123456` | admin |
| `chusan` | `123456` | chusan |
| `user` | `123456` | user |

---

# PHẦN 6 — THẦY HỎI THÌ TRẢ LỜI THẾ NÀO

## 6.1. Câu chắc chắn bị hỏi

**"Phân biệt 401 và 403?"**
> 401 nghĩa là hệ thống **chưa biết bạn là ai** — thất bại ở tầng xác thực, ví dụ không gửi token hoặc token sai chữ ký. 403 nghĩa là hệ thống **biết rõ bạn là ai rồi nhưng bạn không được phép** — thất bại ở tầng phân quyền. Trong code của em, 401 do `AuthenticationEntryPoint` sinh ra, 403 do `AccessDeniedHandler`.

**"JWT gồm mấy phần?"**
> Ba phần ngăn cách bởi dấu chấm. Header khai báo thuật toán ký là HS256. Payload chứa `sub` là tên đăng nhập, `userId`, `role` và `exp` là hạn dùng. Signature là chữ ký băm từ Header cộng Payload cộng khóa bí mật bằng HMAC-SHA256.

**"Payload có an toàn không?"**
> Không. Payload chỉ mã hóa Base64 chứ không phải mã hóa bảo mật, ai cầm được token đều đọc được. Nên tuyệt đối không để mật khẩu hay dữ liệu nhạy cảm vào đó. Giá trị bảo mật nằm ở phần chữ ký — sửa Payload thì chữ ký không còn khớp.

**"Vì sao không dùng session?"**
> Vì hệ thống có ba dịch vụ chạy trên ba tiến trình riêng. Dùng session thì phải dựng thêm kho session dùng chung, hoặc mỗi request hai dịch vụ kia phải gọi về hỏi Auth Service — cả hai cách đều tạo điểm nghẽn. JWT thì server không lưu gì, mỗi dịch vụ tự xác minh chữ ký bằng khóa bí mật dùng chung.

**"Mật khẩu lưu thế nào?"**
> Băm một chiều bằng BCrypt trước khi lưu, CSDL không bao giờ có mật khẩu gốc. BCrypt tự sinh salt riêng cho từng mật khẩu nên ba tài khoản cùng đặt `123456` vẫn ra ba chuỗi băm khác nhau. Khi đăng nhập hệ thống băm lại rồi so sánh chứ không giải mã ngược.

**"Vì sao không dùng MD5?"**
> MD5 được thiết kế để chạy thật nhanh, mà nhanh chính là thứ kẻ tấn công cần khi dò mật khẩu. BCrypt cố tình chậm, có cost factor điều chỉnh được.

## 6.2. Câu hỏi khó hơn

**"Token bị lộ thì sao?"**
> Đây đúng là hạn chế hiện tại của hệ thống em. Token còn hạn 24 giờ thì vẫn dùng được, hệ thống chưa thu hồi được. Hướng khắc phục là thêm Refresh Token với Access Token vòng đời ngắn, kèm cơ chế thu hồi, và chạy HTTPS để token không bị chặn bắt trên đường truyền.

**"Vì sao claim role phải viết thường?"**
> Vì Spring Security quy ước hàm `hasRole("chusan")` sẽ tự động ghép thêm tiền tố `ROLE_` rồi mới so sánh. Bộ lọc của cả ba dịch vụ đều ghép `"ROLE_" + role` lấy từ token. Nếu em cấp token có sẵn tiền tố thì quyền thành `ROLE_ROLE_CHUSAN`, không khớp gì cả, và toàn bộ API của hai dịch vụ kia sẽ trả 403.

**"Vì sao 403 mà không phải 401 ở trường hợp quyền sở hữu?"**
> Vì hệ thống đã xác thực được danh tính — token hợp lệ, biết rõ người gọi là ai. Chỉ là người đó không sở hữu tài nguyên đang truy cập. 401 dành cho trường hợp chưa biết là ai. Nếu trả 401 ở đây thì client sẽ điều hướng người dùng đi đăng nhập lại, mà đăng nhập lại cũng không giải quyết được gì.

**"Ba dịch vụ dùng chung khóa thì có rủi ro gì?"**
> Có. Thuật toán HS256 là đối xứng, cùng một khóa vừa ký vừa xác minh. Nghĩa là cả ba dịch vụ đều có khả năng **tự phát hành** token chứ không chỉ xác minh. Nếu Pitch Service bị chiếm quyền, kẻ tấn công tự ký được token admin. Hướng khắc phục là chuyển sang RS256 bất đối xứng — Auth Service giữ khóa riêng để ký, hai dịch vụ còn lại chỉ nhận khóa công khai để xác minh.

## 6.3. Nếu thầy bảo sửa code tại chỗ

Chỗ dễ diễn nhất là `SecurityConfig.java` **dòng 79**:

```java
// Hiện tại
.requestMatchers(HttpMethod.GET, "/api/v1/users").hasRole("admin")

// Sửa thành
.requestMatchers(HttpMethod.GET, "/api/v1/users").hasAnyRole("admin", "chusan")
```

Lưu → khởi động lại service → token `chusan` gọi `GET /api/v1/users` sẽ đổi từ **403** thành **200**.

> **Nhớ sửa lại như cũ sau khi demo xong.**

## 6.4. Nếu không trả lời được

Đừng bịa. Nói thật:

> "Chỗ này em chưa nắm chắc, nhưng em biết nó nằm ở file ... và nó làm nhiệm vụ ... Em sẽ tìm hiểu thêm."

Thầy chấm theo mức độ đáp ứng thực tế, và đề cũng ghi rõ: *"Nếu nhóm chưa triển khai đầy đủ một nội dung, cần trình bày rõ phần đã hoàn thành, phần còn thiếu."*

---

# PHẦN 7 — CHECKLIST HOÀN THÀNH BÀI

## 7.1. Những gì đã xong

- [x] Code Auth Service — 21 file, 1321 dòng
- [x] 36 ca kiểm thử, chạy thật đều đạt
- [x] Postman Collection 16 request
- [x] Báo cáo Chương 4 và Chương 5
- [x] Slide 15 trang kèm speaker notes
- [x] Kịch bản quay video

## 7.2. Những gì bạn còn phải làm

- [ ] **Đọc hiểu code** — ít nhất 3 file: `JwtTokenProvider`, `SecurityConfig`, `AuthService`
- [ ] **Tập nói** theo speaker notes trong slide (mở Presenter View)
- [ ] **Quay video** theo notes từng slide
- [ ] **Nộp slide + video** vào tài khoản cá nhân trong Class
- [ ] Nhắc Hùng thêm `Boyngoc` làm collaborator để push được code

## 7.3. Hai lỗi còn tồn tại trong dự án (nên biết để trả lời)

**Lỗi 1 — Hash BCrypt trong file SQL sai.**
File `pitchos-database/auth-user-service.sql` ghi mật khẩu là `123456` nhưng chuỗi băm không khớp. Hiện `DataInitializer` tự vá lúc khởi động nên vẫn chạy được, nhưng gốc rễ chưa sửa.

**Lỗi 2 — Tiếng Việt trong CSDL bị mã hóa hai lần.**
Họ tên hiển thị thành `Tráº§n VÄƒn Chá»§ SÃ¢n` thay vì `Trần Văn Chủ Sân`. Nguyên nhân: file SQL thiếu dòng `SET NAMES utf8mb4;` ở đầu. Không ảnh hưởng chức năng bảo mật, chỉ xấu khi demo.

> Cả hai đều thuộc phần của Hùng. Nếu thầy hỏi, cứ nói thật là nhóm đã phát hiện khi chạy thử và đã ghi vào mục 5.4.2 của báo cáo Chương 5.

## 7.4. Lộ trình học trong 3 buổi

**Buổi 1 — Hiểu khái niệm (1 tiếng)**
Đọc Phần 2 của tài liệu này. Không cần nhớ code, chỉ cần hiểu: JWT là gì, 401 khác 403 ở đâu, BCrypt dùng làm gì.

**Buổi 2 — Đọc code (2 tiếng)**
Mở 3 file chính, đọc song song với mục 3.4 và 3.5. Vừa đọc vừa đối chiếu. Chạy thử hệ thống, dùng Postman bấm thử từng request xem kết quả.

**Buổi 3 — Tập nói và quay (2 tiếng)**
Mở slide ở Presenter View, tập nói theo notes một lượt. Làm thử các bước thực hành. Rồi quay chính thức.

---

# PHẦN 8 — JWT CHUYÊN SÂU

> Phần này đi sâu hơn mục 2.5. Mọi con số dưới đây là **thật**, tính bằng đúng thuật toán trong `JwtTokenProvider.java` của bạn. Cuối phần có script để bạn tự chạy và nghịch.

## 8.1. JWT sinh ra để giải quyết vấn đề gì

HTTP là giao thức **không nhớ gì cả** (stateless). Mỗi request là một lần gặp mặt hoàn toàn mới — server không biết bạn vừa đăng nhập 2 giây trước.

**Cách cũ — session:**
Server ghi vào bộ nhớ *"ai đó tên là abc123 chính là chusan"*, rồi đưa bạn cái mã `abc123`. Lần sau bạn đưa mã đó, server tra sổ.

**Vấn đề với nhóm bạn:** có **ba chương trình chạy riêng biệt**. Sổ ghi ở Auth Service thì Pitch Service đâu đọc được. Muốn dùng chung thì:
- Hoặc dựng thêm một kho session (Redis) — thêm một thứ phải nuôi, hỏng là sập cả ba
- Hoặc mỗi request Pitch Service phải gọi về hỏi Auth Service — chậm và tạo điểm chết

**JWT lật ngược vấn đề:** không ai ghi sổ cả, **cái thẻ tự chứng minh nó thật**.

> Giống hộ chiếu: công an cửa khẩu không gọi về Bộ Ngoại giao hỏi, họ nhìn con dấu và biết nó thật.

## 8.2. Cấu trúc với số liệu thật

### Bước 1 — Header

```
JSON gốc  : {"alg":"HS256"}
Base64url : eyJhbGciOiJIUzI1NiJ9
```

Chỉ khai báo thuật toán ký, ngắn vậy thôi.

### Bước 2 — Payload

```
JSON gốc  : {"sub":"chusan","userId":2,"role":"chusan","fullName":"Tran Van Chu San","iat":1793336101,"exp":1793422501}

Base64url : eyJzdWIiOiJjaHVzYW4iLCJ1c2VySWQiOjIsInJvbGUiOiJjaHVzYW4iLCJmdWxsTmFtZSI6IlRyYW4gVmFuIENodSBTYW4iLCJpYXQiOjE3OTMzMzYxMDEsImV4cCI6MTc5MzQyMjUwMX0
```

| Claim | Giá trị | Ai dùng nó |
| :--- | :--- | :--- |
| `sub` | `chusan` | Auth Service tra cứu user |
| `userId` | `2` | **Booking Service** dùng gán đơn đặt sân |
| `role` | `chusan` | Cả 3 service dùng phân quyền |
| `fullName` | Trần Văn Chủ Sân | Hiển thị trên giao diện |
| `iat` | 1793336101 | Thời điểm phát hành |
| `exp` | 1793422501 | Thời điểm hết hạn |

> **Kiểm chứng:** `1793422501 − 1793336101 = 86400` giây = **đúng 24 giờ**.
> Khớp với `jwt.expiration-ms=86400000` trong `application.properties`.

### Bước 3 — Chữ ký

```
Xfag3YqYfip_2b2gfAD3YCiIXbUzI0tZJNa_Fn1Mu2w
```

### Ghép lại — token hoàn chỉnh, 208 ký tự

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjaHVzYW4iLCJ1c2VySWQiOjIsInJvbGUiOiJjaHVzYW4i...fQ.Xfag3YqYfip_2b2gfAD3YCiIXbUzI0tZJNa_Fn1Mu2w
└──── Header ────┘ └──────────────── Payload ──────────────┘ └────── Signature ──────┘
```

## 8.3. Base64url KHÔNG phải mã hóa — chỗ hiểu sai nhiều nhất

**Base64 chỉ là đổi cách viết**, giống như viết số `10` thành chữ `"mười"`. Không cần mật khẩu gì để đọc ngược:

```
eyJzdWIiOiJjaHVzYW4i...  →  {"sub":"chusan","userId":2,"role":"chusan",...}
```

Script ở mục 8.7 làm đúng điều đó — **không dùng khóa bí mật nào cả**.

**Vậy vì sao vẫn dùng Base64?**
Vì JSON có dấu `{`, `"`, dấu cách — những ký tự này gây lỗi khi nhét vào HTTP header. Base64 biến tất cả thành chữ và số an toàn. Mục đích là **vận chuyển**, không phải **che giấu**.

> ⚠️ **Hệ quả thực tế:** tuyệt đối không để mật khẩu, số thẻ ngân hàng, CMND vào Payload.
> **Đây là câu thầy rất hay hỏi.**

## 8.4. Chữ ký — phần bảo mật thật sự

```
Chữ ký = HMAC-SHA256( base64(header) + "." + base64(payload),  SECRET_KEY )
```

**HMAC-SHA256** là hàm băm có khóa, với hai tính chất quyết định:

**a) Một chiều** — từ chữ ký không suy ngược ra nội dung hay khóa.

**b) Hiệu ứng tuyết lở (avalanche effect)** — đổi 1 ký tự thì chữ ký đổi hoàn toàn:

```
userId = 2  →  Xfag3YqYfip_2b2gfAD3YCiIXbUzI0tZJNa_Fn1Mu2w
userId = 3  →  ze4u-sckdFEWv-OOj7BdP8oba6FjGsvkCLGjwdi8N5I
```

Chỉ đổi **một chữ số** mà hai chuỗi không giống nhau một ký tự nào.

## 8.5. Vì sao không giả mạo được — chứng minh bằng số

Giả sử kẻ xấu lấy được token của `chusan` và muốn nâng mình lên `admin`:

| Bước | Hành động | Làm được? |
| :---: | :--- | :---: |
| 1 | Giải mã Payload để đọc | ✅ Được, không cần khóa |
| 2 | Đổi `"role":"chusan"` → `"role":"admin"`, mã hóa lại | ✅ Được |
| 3 | Tính chữ ký mới cho Payload đã sửa | ❌ **KHÔNG**, vì không có `SECRET_KEY` |

Nên họ đành **giữ nguyên chữ ký cũ**. Khi server nhận được:

```
Chữ ký đính kèm    : Xfag3YqYfip_2b2gfAD3YCiIXbUzI0tZJNa_Fn1Mu2w
Chữ ký server tính : dTGc7IPOtK7d7CHeBKMVZRskiocn1zVcd1oSW9xk8NY
KHỚP KHÔNG? → KHÔNG KHỚP → TỪ CHỐI 401
```

> **Điểm cốt lõi phải nhớ:**
> **Server không "tin" token. Server tự tính lại chữ ký rồi so sánh.**

Trong code của bạn, việc này gói gọn trong `JwtTokenProvider.parseToken()` — thư viện JJWT tự làm và tự ném lỗi nếu lệch:

```java
public Claims parseToken(String token) {
    return Jwts.parserBuilder()
            .setSigningKey(key)        // ← đưa khóa vào
            .build()
            .parseClaimsJws(token)     // ← tự tính lại và so sánh, lệch thì ném JwtException
            .getBody();
}
```

Rồi `JwtAuthenticationFilter` bắt lỗi đó và xóa context:

```java
} catch (JwtException | IllegalArgumentException ex) {
    SecurityContextHolder.clearContext();
}
```

## 8.6. JWT KHÔNG làm được gì

Phần này làm bạn khác với người học thuộc lòng. Nếu trả lời được, thầy sẽ thấy bạn hiểu thật.

| Hiểu sai thường gặp | Sự thật |
| :--- | :--- |
| "JWT mã hóa dữ liệu" | **Không.** Chỉ chống sửa đổi, hoàn toàn không che giấu nội dung |
| "Token lộ thì vô hiệu hóa được" | **Không.** Còn hạn thì vẫn dùng được, trừ khi có danh sách đen |
| "Có JWT là an toàn rồi" | **Không.** Vẫn cần HTTPS, nếu không token bị chặn bắt giữa đường |
| "Token càng nhiều thông tin càng tiện" | **Không.** Payload to làm mọi request nặng thêm, và càng dễ lộ |

### Hạn chế lớn nhất của hệ thống nhóm bạn

**HS256 là thuật toán đối xứng** — cùng một khóa vừa dùng để ký, vừa dùng để xác minh.

Hệ quả: Pitch Service và Booking Service cũng **có khả năng tự phát hành** token, chứ không chỉ kiểm tra. Nếu một trong hai bị chiếm quyền, kẻ tấn công tự ký được token `admin` hợp lệ.

**Cách khắc phục — RS256 (bất đối xứng):**

| | HS256 (hiện tại) | RS256 (nên dùng) |
| :--- | :--- | :--- |
| Số khóa | 1 khóa dùng chung | 2 khóa: riêng + công khai |
| Auth Service | Ký bằng khóa chung | Ký bằng **khóa riêng** |
| Pitch / Booking | Xác minh bằng khóa chung → **ký được luôn** | Xác minh bằng **khóa công khai** → **không ký được** |
| Rủi ro khi 1 service bị chiếm | Tự phát hành token admin | Không làm gì được |

Đây chính là nội dung bạn đã viết ở **slide 15** và mục **5.4.4** báo cáo Chương 5.

## 8.7. Script tự nghịch

Tạo file `jwt-demo.js` ở đâu cũng được, dán code dưới vào, chạy bằng `node jwt-demo.js`.
Không cần cài thư viện gì — `crypto` có sẵn trong Node.

```javascript
const crypto = require("crypto");

const SECRET = "404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970";
// Giống hệt dòng: Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret))
const key = Buffer.from(SECRET, "base64");

const b64url = (buf) =>
  Buffer.from(buf).toString("base64")
    .replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");

function kyToken(header, payload) {
  const h = b64url(JSON.stringify(header));
  const p = b64url(JSON.stringify(payload));
  const phanDuocKy = h + "." + p;
  const sig = b64url(crypto.createHmac("sha256", key).update(phanDuocKy).digest());
  return { h, p, sig, token: phanDuocKy + "." + sig };
}

const header = { alg: "HS256" };
const payload = {
  sub: "chusan",
  userId: 2,
  role: "chusan",
  iat: 1793336101,
  exp: 1793422501,
};

const that = kyToken(header, payload);
console.log("TOKEN:", that.token);

// Chứng minh 1: ai cũng đọc được Payload, không cần khóa
console.log("\nGiải mã Payload (không dùng khóa):");
console.log(JSON.parse(Buffer.from(that.p, "base64").toString("utf8")));

// Chứng minh 2: sửa Payload thì chữ ký lệch
const giaMao = kyToken(header, { ...payload, role: "admin" });
const tokenKeXau = that.h + "." + giaMao.p + "." + that.sig;  // giữ chữ ký cũ
const [h2, p2, sigNhanDuoc] = tokenKeXau.split(".");
const sigServerTinh = b64url(crypto.createHmac("sha256", key).update(h2 + "." + p2).digest());

console.log("\nKẻ xấu đổi role thành admin:");
console.log("  Chữ ký đính kèm   :", sigNhanDuoc);
console.log("  Chữ ký server tính:", sigServerTinh);
console.log("  →", sigNhanDuoc === sigServerTinh ? "KHỚP" : "KHÔNG KHỚP → TỪ CHỐI 401");
```

> **Lưu ý:** chữ ký script này in ra là `k6F0u-URktCdI-Xb9ot9SpOBsQvFr25Hc0OV9cdUYlU`, **khác** với chữ ký `Xfag3YqYfip...` ở mục 8.2. Không phải sai — payload ở đây đã bỏ bớt trường `fullName` cho gọn, mà payload đổi thì chữ ký đổi hoàn toàn. Chính đây là hiệu ứng tuyết lở đã nói ở mục 8.4.

**Gợi ý nghịch để nhớ lâu:**

1. Đổi `userId` từ `2` thành `3` → xem chữ ký đổi hoàn toàn
2. Đổi `SECRET` một ký tự → xem chữ ký đổi hoàn toàn (giả lập hai service không đồng bộ khóa)
3. Đổi `role` thành `"ROLE_CHUSAN"` → token vẫn hợp lệ về chữ ký, nhưng Spring Security sẽ ghép thành `ROLE_ROLE_CHUSAN` và chặn hết (xem lại mục 3.4.1)
4. Dán token sinh ra vào **jwt.io**, nhập `SECRET` vào ô Verify Signature → thấy **Signature Verified**

## 8.8. Tóm tắt một câu

> JWT không giấu thông tin, nó **chứng minh thông tin chưa bị sửa**.
> Ai cũng đọc được Payload, nhưng chỉ ai có `SECRET_KEY` mới tạo được chữ ký hợp lệ.
