# KỊCH BẢN QUAY VIDEO — HOÀNG (bản chi tiết theo từng slide)

**Phần phụ trách:** Câu 1 Ý 3 (Lý thuyết) · Câu 2 Ý 4 (Thực nghiệm)
**Độ dài mục tiêu:** 9 – 11 phút · **Slide:** `SLIDE_HOANG_PitchOS.pptx` (15 slide)
**Công cụ quay:** OBS Studio / Camtasia / **Win + G** (Xbox Game Bar)

> **Cách dùng file này:** đọc từ trên xuống, đúng thứ tự slide. Mỗi slide có 3 khối:
> **🗣️ LỜI NÓI** (học thuộc ý, nói tự nhiên) — **🖥️ THAO TÁC** (làm gì trên màn hình) — **✅ KẾT QUẢ** (phải ra đúng mã này, mình đã chạy thật xác nhận).
> Nói đến đâu bấm đến đó. Đừng vừa quay vừa sửa lỗi — chạy trơn một lượt rồi mới bấm quay.

---

## PHẦN 0 — CHUẨN BỊ TRƯỚC KHI BẤM QUAY *(làm trước, KHÔNG quay)*

### B1. Giải phóng cổng bị chiếm (PowerShell)
```
docker stop okr_mysql okr-test-backend-1
```

### B2. Bật MySQL PitchOS về đúng cổng 3306
```
cd E:\DownCodeGit\PTPM
docker compose up -d
```

### B3. Bật Auth Service — mở 1 terminal RIÊNG, để chạy suốt buổi
```
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21.0.11"
cd E:\DownCodeGit\PTPM\pitchos-auth-service
mvn spring-boot:run
```
Đợi tới dòng `Started PitchosAuthServiceApplication`.

### B4. Bật Pitch Service — mở terminal RIÊNG thứ hai
```
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21.0.11"
cd E:\DownCodeGit\PTPM\pitchos-pitch-service
mvn spring-boot:run
```
Đợi tới dòng `Started PitchosPitchServiceApplication`.

### B5. Mở sẵn 5 cửa sổ, sắp xếp gọn
1. **Terminal** đang chạy Auth Service (để khoe log cổng 8081)
2. **Postman** đã import collection `PitchOS - Auth & Security (Hoang) CLEAN`
3. **VS Code** mở sẵn 3 file: `SecurityConfig.java`, `AuthService.java`, `JwtTokenProvider.java`
4. **Trình duyệt** 2 tab: `localhost:8081/swagger-ui.html` và `jwt.io`
5. **DBeaver** kết nối sẵn `pitchos_user_db` — Host `localhost`, Port **`3306`**, User `root`, Password `123456`, Database `pitchos_user_db`. Mở sẵn cửa sổ SQL, dán sẵn câu truy vấn ở Slide 10 (chưa chạy).

### B5.5. Chuẩn bị phần mềm quay + giải phóng tài nguyên
- Đóng các ứng dụng nặng không dùng (trình duyệt thừa, app chat, các container dự án khác) — máy đang chạy 2 JVM + Postman + DBeaver + VS Code nên cần nhẹ RAM, tránh giật khi quay.
- Mở phần mềm quay (OBS / Camtasia / **Win + G**), chọn vùng quay là màn hình chính, **quay thử 10 giây** rồi xem lại: hình nét, chữ đọc được, tiếng rõ.
- (Tùy chọn) Mở PowerPoint ở **Presenter View** để đọc speaker notes đã viết sẵn trong từng slide.

### B6. ⚠️ NẠP SẴN TOKEN — bắt buộc, nếu không demo RBAC sẽ 401
Trong Postman, mở folder **`0. Chuẩn bị`**, bấm **Send** cả 3 request theo thứ tự:
- Đăng nhập admin → **200** · Đăng nhập chusan → **200** · Đăng nhập user → **200**

→ 3 request này nạp token vào biến `tokenAdmin / tokenChusan / tokenUser`. Kiểm tra: bấm tên collection → tab **Variables** → 3 biến token phải có chuỗi dài ở cột **Current value**. Có rồi mới quay.

### B7. Checklist cuối
- [ ] Auth 8081 + Pitch 8082 đều đã in dòng `Started ...Application`
- [ ] Đăng nhập thử `chusan` / `123456` → **200 OK**
- [ ] Mở `localhost:8081/swagger-ui.html` → hiện trang Swagger (tự chuyển sang `/swagger-ui/index.html`)
- [ ] **Diễn thử Slide 5 trên jwt.io:** dán token chusan → bật toggle **BASE64URL ENCODED** → nhập secret → phải ra **Signature Verified**. (Không bật toggle sẽ KHÔNG verified — xem Slide 5.)
- [ ] DBeaver chạy thử câu SELECT ở Slide 10 → ra bảng users
- [ ] Phóng to chữ mọi cửa sổ (`Ctrl` + `+`), cỡ chữ IDE ≥ 16pt
- [ ] Tắt thông báo Windows, Zalo, Messenger
- [ ] Thu âm + quay thử 10 giây nghe/xem lại
- [ ] `SecurityConfig.java` dòng 79 đang là `.hasRole("admin")` (bản gốc)
- [ ] **Diễn thử một lượt KHÔNG quay** từ Slide 1→15, canh thời lượng 9–11 phút, rồi mới quay thật

---

## SLIDE 1 — MỞ ĐẦU *(0:00 – 0:40)*

**🗣️ LỜI NÓI:**
> "Em chào thầy và các bạn. Em là Hoàng, nhóm trưởng nhóm PitchOS. Đề tài của nhóm là hệ thống quản lý đặt sân bóng đá mini, xây dựng theo kiến trúc hướng dịch vụ với ba microservice độc lập. Em phụ trách mảng bảo mật cốt lõi: dịch vụ xác thực chạy trên cổng 8081, cùng cơ chế JWT và phân quyền cho toàn hệ thống. Hôm nay em trình bày hai ý: Câu 1 Ý 3 là lý thuyết về xác thực, phân quyền, cấu trúc JWT; Câu 2 Ý 4 là phần thực nghiệm — em đã cài đặt và kiểm thử thế nào."

**🖥️ THAO TÁC:** chỉ cần hiện slide 1.

---

## SLIDE 2 — LỘ TRÌNH *(0:40 – 1:10)*

**🗣️ LỜI NÓI:**
> "Phần của em chia làm hai nửa. Nửa đầu là lý thuyết, Câu 1 Ý 3: xác thực khác phân quyền ở đâu, một token JWT gồm những gì, vì sao không giả mạo được, và khi nào trả 401 khi nào trả 403. Nửa sau là thực nghiệm, Câu 2 Ý 4: cách nhóm em cài đặt những cơ chế đó vào dịch vụ thật, và kết quả kiểm thử cụ thể. Em bắt đầu với lý thuyết."

**🖥️ THAO TÁC:** hiện slide 2, nói nhanh rồi chuyển.

---

## SLIDE 3 — XÁC THỰC ≠ PHÂN QUYỀN *(1:10 – 1:55)*

**🗣️ LỜI NÓI:**
> "Hai khái niệm này rất hay bị nhầm. **Authentication — xác thực** trả lời 'bạn là ai', đối chiếu tên đăng nhập và mật khẩu, chỉ diễn ra một lần lúc đăng nhập, kết quả là cấp cho bạn một token. **Authorization — phân quyền** trả lời 'bạn được phép làm gì', xét vai trò và quyền sở hữu, diễn ra ở mọi lần gọi API. Điểm mấu chốt: hai tầng này thất bại bằng hai mã lỗi khác nhau — 401 và 403. Xác thực luôn đi trước phân quyền, nhưng đăng nhập thành công không có nghĩa là được phép làm mọi thứ."

**🖥️ THAO TÁC:** slide lý thuyết, chưa demo.

---

## SLIDE 4 — JWT GỒM BA PHẦN *(1:55 – 3:00)*

**🗣️ LỜI NÓI (phần đầu):**
> "Đây là một token thật do hệ thống nhóm em cấp cho tài khoản chủ sân, em copy trực tiếp từ kết quả chạy chứ không lấy trên mạng. Nó chia làm ba phần bởi hai dấu chấm. Phần đầu là **Header** — thuật toán ký HS256. Phần giữa là **Payload** — chứa `sub` là tên đăng nhập, `userId`, `role` là chusan, và `exp` là hạn dùng. Lưu ý: Payload chỉ mã hóa Base64, **không phải mã hóa bảo mật** — ai cầm token cũng đọc được, nên tuyệt đối không để mật khẩu vào đây. Em demo luôn để chứng minh đây là token thật."

**🖥️ THAO TÁC + ✅ KẾT QUẢ:**
1. Postman → folder **`0. Chuẩn bị`** → **Đăng nhập chusan** → **Send** → ✅ **200 OK**, có `accessToken`.
2. Copy chuỗi `accessToken` (chỉ phần trong dấu nháy).
3. Trình duyệt → tab **jwt.io** → dán vào ô **Encoded** bên trái.
4. Rê chuột lần lượt 3 vùng màu, đọc theo slide: **Header** (HS256) → **Payload** (sub, userId, role, exp) → **Signature**.

**🗣️ LỜI CHỐT:**
> "Không cần mật khẩu gì, chỉ cần có token là đọc được hết Payload. Vậy JWT bảo mật ở chỗ nào? Em xin sang slide sau."

> **Giữ nguyên tab jwt.io, slide 5 dùng tiếp.**

---

## SLIDE 5 — VÌ SAO KHÔNG GIẢ MẠO ĐƯỢC *(3:00 – 4:15)* ⭐ ĐOẠN ĂN ĐIỂM NHẤT

**🗣️ LỜI NÓI:**
> "Nếu ai cũng sửa được Payload thì JWT bảo mật ở đâu? Giả sử kẻ tấn công lấy được token khách hàng, sửa `role` từ user thành admin rồi mã hóa lại. Về cú pháp Payload mới hợp lệ. Nhưng chữ ký ở phần ba được tạo bằng cách băm Header cộng Payload cùng với SECRET_KEY — khóa này chỉ server biết. Payload đổi thì chữ ký không còn khớp, token bị từ chối ngay tại bộ lọc, trả về 401. Em chứng minh ngay."

**🖥️ THAO TÁC — PHẦN A (trên jwt.io):**
1. Tìm phần **JWT Signature Verification** (dưới bên phải).
   ⚠️ **BẬT toggle `BASE64URL ENCODED`** ở ngay cạnh tiêu đề — đây là bước nhiều người quên. Hệ thống PitchOS nạp khóa bằng `Decoders.BASE64.decode(secret)`, nên jwt.io phải hiểu secret là chuỗi Base64 thì chữ ký mới khớp. **Không bật toggle → KHÔNG verified.**
2. Dán khóa bí mật vào ô **Secret**:
   ```
   404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970
   ```
   → ✅ hiện dòng xanh **Signature Verified** (và **Valid secret**). Nói: *"Nhập đúng khóa bí mật, trang báo chữ ký hợp lệ."*
3. Vào ô **Decoded Payload** (giữa), sửa `"role": "chusan"` thành `"role": "admin"`.
   → ✅ dòng chữ đổi thành đỏ **Invalid Signature**.
   Nói: *"Em vừa tự phong chức mình lên admin, nhưng chữ ký lập tức báo không hợp lệ — vì Payload đổi thì chữ ký không còn khớp."*

**🖥️ THAO TÁC — PHẦN B (hệ thống thật từ chối token hỏng):**
3. Postman → folder **`3. Test cases Phân quyền`** → **TC07 - Token sai chữ ký** → **Send**.
   → ✅ **401 Unauthorized**.
   Nói: *"Token sai chữ ký, hệ thống trả 401 — từ chối thẳng tại bộ lọc."*

**🗣️ LỜI CHỐT:**
> "Không có khóa bí mật thì không giả mạo được. Đó là giá trị thực sự của JWT."

> **Quay chậm, phóng to màn hình đoạn này.**

---

## SLIDE 6 — STATELESS, VÌ SAO JWT HỢP MICROSERVICES *(4:15 – 5:00)*

**🗣️ LỜI NÓI:**
> "Đặc tính thứ hai của JWT là phi trạng thái — stateless. Mô hình session truyền thống phải lưu phiên đăng nhập ở server. Với ba dịch vụ chạy ba tiến trình riêng như nhóm em, sẽ phát sinh câu hỏi: lưu session ở đâu để cả ba cùng đọc? JWT giải quyết bằng cách server không lưu gì cả — mỗi request client tự gửi kèm token, ba dịch vụ dùng chung một khóa bí mật nên dịch vụ nào cũng tự xác minh chữ ký được, không cần hỏi nhau. Nhờ vậy ba dịch vụ hoàn toàn độc lập; thêm dịch vụ thứ tư chỉ cần cấp khóa bí mật là xong. Em sẽ chứng minh token dùng chung ở slide 13."

**🖥️ THAO TÁC:** slide lý thuyết, chưa demo.

---

## SLIDE 7 — 401 vs 403 *(5:00 – 6:00)*

**🗣️ LỜI NÓI:**
> "Ranh giới rất đơn giản. **401** nghĩa là hệ thống không biết bạn là ai — thất bại ở tầng xác thực. **403** nghĩa là biết rõ bạn là ai nhưng không được phép — thất bại ở tầng phân quyền. Chuyện này không chỉ hình thức: client gặp 401 thì điều người dùng về đăng nhập; gặp 403 thì báo không đủ quyền chứ không bắt đăng nhập lại — vì đăng nhập lại mười lần cũng không thêm quyền. Em demo ba tình huống kinh điển."

**🖥️ THAO TÁC + ✅ KẾT QUẢ:** Postman → folder **`1. Demo hội đồng`**, Send lần lượt:
| Request | Kết quả | Nói |
| :--- | :---: | :--- |
| **Ca 1 - Không gửi token** | ✅ **401** | "Gọi API thêm sân nhưng không gửi header Authorization → 401, hệ thống KHÔNG BIẾT em là ai." |
| **Ca 2 - Token user gọi API chusan** | ✅ **403** | "Vẫn API đó, gửi kèm token khách hàng hợp lệ → 403. Hệ thống BIẾT RÕ em là ai nhưng vai trò user không được thêm sân. Đúng tình huống đề yêu cầu: đã đăng nhập nhưng không có quyền." |
| **Ca 3 - Token chusan gọi lại** | ✅ **201** | "Dùng token chủ sân → 201 Created, sân được tạo." |

**🗣️ LỜI CHỐT:**
> "Ba ca cho thấy ranh giới rất rõ: 401 là chưa biết bạn là ai, 403 là biết rồi nhưng không cho phép."

---

## SLIDE 8 — MA TRẬN PHÂN QUYỀN *(6:00 – 6:45)*

**🗣️ LỜI NÓI:**
> "Hệ thống có ba vai trò lưu bằng ENUM trong CSDL: `user` là khách hàng, `chusan` là chủ sân, `admin` là quản trị. Nhìn hai dòng POST /pitches và POST /bookings: khách hàng không được thêm sân nhưng được đặt sân; chủ sân thì ngược lại. Nghĩa là quyền không bao hàm theo thứ bậc — không phải cứ admin là làm được mọi thứ của cấp dưới. Quyền thiết kế theo đúng chức năng nghiệp vụ — nguyên lý đặc quyền tối thiểu. Em chứng minh một dòng bằng hệ thống thật."

**🖥️ THAO TÁC + ✅ KẾT QUẢ:** Postman → folder **`3. Test cases Phân quyền`**:
| Request | Kết quả | Nói |
| :--- | :---: | :--- |
| **TC09 - role user gọi API admin** | ✅ **403** | "Token khách hàng gọi API danh sách người dùng → 403." |
| **TC10 - role chusan gọi API admin** | ✅ **403** | "Token chủ sân cũng bị từ chối — chủ sân không phải cấp trên của khách hàng." |
| **TC11 - role admin gọi API admin** | ✅ **200** | "Chỉ admin mới xem được danh sách. Đúng như dòng GET /users trong bảng." |

**🗣️ LỜI CHỐT:**
> "Hết phần lý thuyết. Em chuyển sang phần thực nghiệm."

---

## SLIDE 9 — AUTH SERVICE PORT 8081 *(6:45 – 7:45)*

**🗣️ LỜI NÓI:**
> "Dịch vụ em phụ trách là Auth & User Service, cổng 8081, CSDL riêng `pitchos_user_db`. Cung cấp ba API: đăng ký (băm mật khẩu BCrypt rồi mới lưu), đăng nhập (so khớp và cấp token), và tra cứu người dùng (có kiểm tra quyền sở hữu). Một chi tiết quan trọng ở API đăng ký: vai trò tài khoản mới luôn bị ép thành `user`, bất kể client gửi gì — nếu để client tự khai vai trò thì ai cũng tự đăng ký được admin, đó là lỗ hổng leo thang đặc quyền kinh điển. Em cho thầy cô thấy hệ thống đang chạy thật."

**🖥️ THAO TÁC — PHẦN A (Bước 1 của đề: hệ thống đang chạy):**
1. Chuyển sang **Terminal** Auth Service, chỉ vào dòng `Tomcat started on port 8081`.
2. Chuyển terminal Pitch Service → `port 8082`.
3. Mở **DBeaver**, click qua 3 schema: `pitchos_user_db`, `pitchos_pitch_db`, `pitchos_booking_db`.
   Nói: *"Ba CSDL độc lập. Em chỉ phụ trách pitchos_user_db, hai cái kia thuộc dịch vụ khác — đúng nguyên tắc mỗi dịch vụ quản lý dữ liệu của mình."*

**🖥️ THAO TÁC — PHẦN B (Bước 2: dữ liệu hợp lệ & không hợp lệ):**
4. Trình duyệt → `localhost:8081/swagger-ui.html`. Nói: *"Tài liệu API sinh tự động bằng OpenAPI, đủ ba endpoint."*
5. Postman → folder **`2. Test cases Xác thực`** → **TC01 - Đăng ký hợp lệ** → Send.
   → ✅ **201 Created**. Nói: *"Đăng ký hợp lệ → 201. Phản hồi có id, username, role là user, nhưng KHÔNG CÓ trường password. Mật khẩu không bao giờ trả ra ngoài, kể cả đã băm."*
6. **TC03 - Đăng ký sai quy cách** → Send.
   → ✅ **400 Bad Request**, có map `errors`. Nói: *"Dữ liệu sai quy cách → 400, kèm map errors chỉ rõ từng trường: email sai định dạng, mật khẩu phải ít nhất 6 ký tự, họ tên không được trống. Đây là Jakarta Validation kết hợp GlobalExceptionHandler."*

---

## SLIDE 10 — BCRYPT, CSDL KHÔNG LƯU MẬT KHẨU GỐC *(7:45 – 8:30)*

**🗣️ LỜI NÓI:**
> "Nguyên tắc quan trọng nhất: CSDL không bao giờ lưu mật khẩu dạng thuần. Nhóm em chọn BCrypt chứ không dùng MD5 hay SHA-1, vì ba lý do. Một, BCrypt tự sinh salt riêng cho từng mật khẩu — ba tài khoản cùng đặt `123456` nhưng ba chuỗi băm khác hẳn nhau, vô hiệu hóa bảng tra cứu sẵn. Hai, BCrypt cố tình chạy chậm, cost factor 10 là 2 mũ 10 vòng lặp — người dùng chờ vài chục mili giây còn kẻ tấn công dò hàng triệu mật khẩu mất hàng năm. Ba, đây là hàm một chiều — khi đăng nhập hệ thống băm lại rồi so sánh chứ không giải mã ngược. Em mở CSDL cho thầy cô xem."

**🖥️ THAO TÁC — Bước 4 của đề (kiểm chứng dữ liệu):**
1. DBeaver → mở cửa sổ SQL, chạy:
   ```sql
   SELECT id, username, role, LEFT(password, 35) AS hash FROM pitchos_user_db.users;
   ```
2. Chỉ vào cột `hash`. Nói: *"Cột password chỉ chứa chuỗi băm BCrypt tiền tố `$2a$10$`, hoàn toàn không có mật khẩu gốc."*
3. Chỉ ba dòng admin/chusan/user. Nói: *"Ba tài khoản cùng mật khẩu 123456 nhưng ba chuỗi băm khác hẳn — vì BCrypt sinh salt riêng."*
4. Kéo xuống tìm tài khoản vừa đăng ký ở slide 9. Nói: *"Tài khoản em vừa đăng ký lúc nãy đã nằm đây — dữ liệu thực sự ghi xuống đĩa."*

> ⚠️ Khi quay DBeaver chỉ zoom cột `role`, `password/hash`. **Tránh zoom cột `full_name`** (tiếng Việt đang hiển thị lệch mã, không ảnh hưởng demo nhưng tránh lộ).

---

## SLIDE 11 — NƠI 401/403 SINH RA + ĐỔI THAM SỐ *(8:30 – 9:45)* ⭐ YÊU CẦU BẮT BUỘC

**🗣️ LỜI NÓI (đọc code):**
> "Mọi request đi qua một chuỗi lọc. Trạm đầu là `JwtAuthenticationFilter` do em viết: lấy token từ header, xác minh chữ ký, hợp lệ thì nạp vai trò vào SecurityContext. Trạm hai là `AuthorizationFilter` của Spring: đối chiếu vai trò với cấu hình. Qua cả hai mới tới controller. Ở nhánh 401, bộ lọc của em không tự trả lỗi mà chỉ xóa SecurityContext, giao việc sinh mã 401 cho `AuthenticationEntryPoint` — để mọi lỗi bảo mật đi qua đúng một chỗ, khuôn JSON thống nhất. Nhánh 403 do `AccessDeniedHandler` trả về, cùng khuôn JSON với dịch vụ của bạn Linh và Nhật."

**🖥️ THAO TÁC — ĐỌC CODE:**
1. VS Code → **`SecurityConfig.java`** → kéo đến **dòng 79**:
   ```java
   .requestMatchers(HttpMethod.GET, "/api/v1/users").hasRole("admin")
   .anyRequest().authenticated()
   ```
   Nói: *"Dòng này: API danh sách người dùng chỉ cho admin. Dòng dưới: mọi request còn lại đều phải đăng nhập."*
2. Kéo xuống phần `.exceptionHandling` (khoảng dòng 85–87). Nói: *"Hai bean quan trọng: authenticationEntryPoint trả 401, accessDeniedHandler trả 403. Em cố ý tách riêng để khuôn JSON lỗi thống nhất ba dịch vụ."*

**🖥️ THAO TÁC — ĐỔI THAM SỐ (Câu bắt buộc của thầy):**
3. Postman → folder 3 → **TC10 - role chusan gọi API admin** → Send → ✅ **403**. Nói: *"Hiện tại chủ sân gọi API này bị 403."*
4. VS Code → `SecurityConfig.java` **dòng 79**, sửa:
   ```java
   // TRƯỚC:  .requestMatchers(HttpMethod.GET, "/api/v1/users").hasRole("admin")
   // SAU:    .requestMatchers(HttpMethod.GET, "/api/v1/users").hasAnyRole("admin", "chusan")
   ```
   Bấm **Ctrl+S**. Nói: *"Em sửa đúng một chỗ: thêm vai trò chusan vào danh sách được phép."*
5. Terminal Auth Service → **Ctrl+C** → gõ lại `mvn spring-boot:run`, đợi `Started PitchosAuthServiceApplication`.
6. Postman → chạy LẠI **TC10** → Send → ✅ **200 OK** (trước đó 403).
   Nói: *"Kết quả đổi từ 403 thành 200. Em CHỈ đổi một tham số, không sửa gì khác — chứng tỏ phân quyền được điều khiển từ SecurityConfig chứ không hard-code trong controller."*
7. ⚠️ **SỬA LẠI NHƯ CŨ:** đổi `.hasAnyRole("admin", "chusan")` → `.hasRole("admin")`, Ctrl+S, khởi động lại lần nữa. Nói: *"Em đổi lại như ban đầu để hệ thống đúng thiết kế."*

---

## SLIDE 12 — QUYỀN SỞ HỮU TÀI NGUYÊN *(9:45 – 10:45)*

**🗣️ LỜI NÓI (đọc code):**
> "Phân quyền theo vai trò thôi là chưa đủ. Một tài khoản khách hàng gọi xem thông tin của admin — token hợp lệ, vai trò user cũng được phép gọi endpoint này. Nếu chỉ xét vai trò thì request được chấp nhận và dữ liệu người khác bị lộ. Nguyên tắc: không tin tưởng ID do client gửi. Hệ thống tra cả hai bản ghi — bản bị truy cập và bản của người đang đăng nhập — rồi đối chiếu ID; nếu là user mà ID khác nhau thì ném AccessDeniedException, trả 403. Một lưu ý kỹ thuật: ngoại lệ này phải khai báo handler riêng, vì nếu không nó bị gói thành 500 thay vì 403."

**🖥️ THAO TÁC — ĐỌC CODE:**
1. VS Code → **`AuthService.java`** → hàm `getUserById` (dòng 110, phần kiểm tra ở dòng 117–120):
   ```java
   if (current.getRole() == Role.user && !current.getId().equals(target.getId())) {
       throw new AccessDeniedException(...);
   }
   ```
   Nói: *"Em tra cả hai bản ghi rồi đối chiếu ID. User mà ID không trùng thì ném AccessDeniedException."*
2. VS Code → **`GlobalExceptionHandler.java`** → handler của `AccessDeniedException`.
   Nói: *"Ngoại lệ này PHẢI khai báo handler riêng. Vì @RestControllerAdvice chạy bên trong DispatcherServlet, tức bên trong ExceptionTranslationFilter của Spring Security. Không khai báo riêng thì nó bị handler lỗi chung tóm trước và gói thành 500 thay vì 403 — sai hoàn toàn ngữ nghĩa HTTP."*

**🖥️ THAO TÁC — CHẠY THỬ:** Postman → folder 3:
| Request | Kết quả | Nói |
| :--- | :---: | :--- |
| **TC12 - role user xem người khác** | ✅ **403** | "Token hợp lệ, vai trò user được phép gọi endpoint, nhưng vẫn 403 vì không sở hữu tài nguyên." |
| **TC13 - role chusan xem người khác** | ✅ **200** | "Chủ sân xem được mọi tài khoản. Cùng một endpoint, hai vai trò, hai kết quả." |

---

## SLIDE 13 — HỢP ĐỒNG TOKEN DÙNG CHUNG *(10:45 – 11:30)* ⭐ ĐIỂM KIẾN TRÚC

**🗣️ LỜI NÓI (đọc code):**
> "Để token do Auth Service cấp dùng được ở Pitch và Booking, phải thỏa ba điều: cùng khóa bí mật (khai báo một chỗ trong .env, ba dịch vụ cùng nạp); cùng cách nạp khóa (cùng chuỗi secret nhưng nạp khác kiểu thì mảng byte khác, chữ ký vẫn lệch); và cùng hợp đồng claim — chỗ dễ sai nhất. Claim `role` phải viết thường, không tiền tố, vì Spring Security tự ghép `ROLE_` khi so với `hasRole`. Nếu token cấp sẵn tiền tố, quyền thành `ROLE_ROLE_CHUSAN` và mọi API hai dịch vụ kia trả 403. Em nói kỹ vì đây là lỗi suýt xảy ra: hai bạn viết bộ lọc trước khi em xong Auth Service."

**🖥️ THAO TÁC — ĐỌC CODE:**
1. VS Code → **`JwtTokenProvider.java`** → **dòng 63**:
   ```java
   claims.put("role", user.getRole().name().toLowerCase());
   ```
   Nói: *"Nhìn tầm thường, nhưng `toLowerCase()` này chính là hợp đồng ngầm giữa ba dịch vụ. Spring Security tự ghép tiền tố ROLE_ rồi mới so sánh. Nếu em cấp token role là ROLE_CHUSAN, quyền thành ROLE_ROLE_CHUSAN và toàn bộ API hai dịch vụ kia trả 403."*
2. Kéo lên khối chú thích hợp đồng token (dòng 20–35). Nói: *"Em ghi hạn hợp đồng này thành chú thích trong code để sau không ai phá vỡ."*

**🖥️ THAO TÁC — CHỨNG MINH TOKEN DÙNG CHUNG (Bước 3 của đề):**
3. Postman → folder **`4. Bàn giao liên dịch vụ`** → **TC15 - Token Auth dùng được cho Pitch Service** → Send.
   → ✅ **201 Created**.
   Nói: *"Token này do Auth Service cổng 8081 cấp, nhưng API em vừa gọi nằm ở Pitch Service cổng 8082 — tiến trình riêng, CSDL riêng, KHÔNG hề gọi về hỏi Auth Service. Hai dịch vụ dùng chung một khóa nên dịch vụ nào cũng tự xác minh chữ ký được. Đây chính là tính phi trạng thái của JWT."*

> **Demo dự phòng (chỉ làm nếu thầy hỏi):** sửa dòng 63 thành `claims.put("role", "ROLE_" + user.getRole().name().toUpperCase());` → khởi động lại → đăng nhập lại → chạy lại TC15 → sẽ ra **403**. Nói: *"Đúng như em cảnh báo, hợp đồng claim không phải lý thuyết suông."* **NHỚ SỬA LẠI toLowerCase() sau khi demo.**

---

## SLIDE 14 — KẾT QUẢ KIỂM THỬ *(11:30 – 12:15)*

**🗣️ LỜI NÓI:**
> "Toàn bộ số liệu là từ chạy thật. Nhóm em có **36 ca kiểm thử** cho phần bảo mật, chia năm nhóm, và **cả 36 ca đều đạt**. Năm ca cuối — nhóm liên dịch vụ — có ý nghĩa kiến trúc quan trọng nhất: token Auth Service cấp dùng được ở Pitch Service độc lập hoàn toàn. Phần bên phải là điều em thấy đáng giá nhất: ba vấn đề đọc code bằng mắt không thấy, chỉ chạy thật mới lộ — nghiêm trọng nhất là chuỗi băm BCrypt trong script SQL không khớp mật khẩu ghi trong chú thích, nếu không phát hiện cả buổi demo sập ngay bước đăng nhập. Em cũng nói rõ: hai nhóm ca lỗi 503 và chống trùng lịch thuộc phần bạn Nhật, không nằm trong đợt chạy này. Em chạy lại toàn bộ bộ kiểm thử ngay."

**🖥️ THAO TÁC — nộp bộ kiểm thử (yêu cầu của đề):**
1. Postman → bấm tên collection `PitchOS - Auth & Security (Hoang) CLEAN`.
2. Bấm nút **Run** (góc trên phải) → cửa sổ **Collection Runner**.
3. Tick chọn tất cả thư mục → **Run**.
4. Đợi chạy xong (~10–20 giây) → ✅ cột phải toàn **PASS** xanh, không FAIL.
   Nói: *"Mỗi request có Test Script tự kiểm tra mã trạng thái và nội dung phản hồi. Tất cả đều PASS."*

> **Nếu bị hỏi về con số:** báo cáo Chương 5 định nghĩa **36 ca kiểm thử thiết kế** (đăng nhập ba vai trò, cấu trúc JWT, xác thực, phân quyền RBAC, liên dịch vụ). Bộ Postman có 22 request với 49 assertion tự động — nhiều hơn 36 vì một ca thiết kế có thể gồm nhiều assertion. Nói gọn: **"36 ca thiết kế, chạy thật bằng Postman đều đạt."**
> ⚠️ Collection Runner **không bao gồm TC16** (Booking Service cổng 8083 chưa chạy) — nếu bạn chạy cả folder 4 thì TC16 sẽ lỗi kết nối. Trước khi quay, **bỏ tick TC16** trong Runner, hoặc chỉ tick folder 0–3 + TC15.

---

## SLIDE 15 — KẾT LUẬN *(12:15 – 13:00)*

**🗣️ LỜI NÓI:**
> "Em xin nói về hạn chế. Lớn nhất là HS256 — thuật toán đối xứng, cùng một khóa vừa ký vừa xác minh, nên cả ba dịch vụ đều có khả năng tự phát hành token. Nếu Pitch hay Booking bị chiếm quyền, kẻ tấn công có thể tự ký token admin hợp lệ. Hướng khắc phục là chuyển sang RS256 bất đối xứng: Auth Service giữ khóa riêng để ký, hai dịch vụ còn lại chỉ nhận khóa công khai để xác minh. Ngoài ra còn thiếu Refresh Token, chưa thu hồi được token đã lộ, chưa giới hạn số lần đăng nhập sai, chưa chạy HTTPS. Hướng phát triển còn có thêm API Gateway xác thực tập trung. Phần trình bày của em đến đây là hết. Em xin cảm ơn thầy cô và các bạn đã lắng nghe."

**🖥️ THAO TÁC:** hiện slide 15, kết thúc.

---

## SAU KHI QUAY XONG

1. Kiểm tra `SecurityConfig.java` dòng 79 đã về `.hasRole("admin")`.
2. Kiểm tra `JwtTokenProvider.java` dòng 63 vẫn là `toLowerCase()` (nếu có làm demo dự phòng).
3. Bật lại 2 container đã tắt:
   ```
   docker start okr_mysql okr-test-backend-1
   ```

---

## CHECKLIST TRƯỚC KHI NỘP

**Nội dung bắt buộc**
- [ ] Bước 1: thấy rõ dịch vụ + CSDL đang chạy (Slide 9)
- [ ] Bước 2: có request hợp lệ (201) và không hợp lệ (400) (Slide 9)
- [ ] Bước 3: token Auth dùng được ở Pitch Service (Slide 13, TC15)
- [ ] Bước 4: truy vấn CSDL xác minh dữ liệu (Slide 10)
- [ ] Bước 5: đủ 3 ca — 401 / 403 / 201 (Slide 7)
- [ ] **Giải thích code** (Slide 11, 12, 13)
- [ ] **Đổi tham số và chạy lại** (Slide 11)
- [ ] jwt.io sửa Payload → Invalid Signature (Slide 5)

**Kỹ thuật**
- [ ] Độ phân giải ≥ 1080p · chữ đủ to · âm thanh rõ
- [ ] Đã trả lại `SecurityConfig.java` như ban đầu

**Nộp bài**
- [ ] **Không nén zip** — upload thẳng file video hoặc dán link (thầy nói: nén là 0 điểm)
- [ ] Nộp kèm slide `SLIDE_HOANG_PitchOS.pptx`
- [ ] Nộp vào đúng tài khoản đã join Class

---

## PHỤ LỤC — BA CÂU THẦY HAY HỎI NHẤT

**Hỏi: Vì sao không dùng session như bình thường?**
> "Vì hệ thống có ba dịch vụ chạy ba tiến trình riêng. Dùng session thì phải dựng kho session dùng chung, hoặc mỗi request hai dịch vụ kia phải gọi về hỏi Auth Service — cả hai đều tạo điểm nghẽn. JWT thì server không lưu gì, mỗi dịch vụ tự xác minh chữ ký bằng khóa bí mật dùng chung."

**Hỏi: Token bị lộ thì sao?**
> "Đây đúng là hạn chế em nêu ở slide cuối. Hiện token còn hạn 24 giờ thì vẫn dùng được, hệ thống chưa thu hồi được. Hướng khắc phục là thêm Refresh Token vòng đời ngắn kèm cơ chế thu hồi, và chạy HTTPS để token không bị chặn bắt trên đường truyền."

**Hỏi: Vì sao 403 mà không phải 401 ở ca kiểm tra quyền sở hữu?**
> "Vì hệ thống ĐÃ xác thực được danh tính — token hợp lệ, biết rõ người gọi là ai. Chỉ là người đó không sở hữu tài nguyên đang truy cập. 401 dành cho trường hợp chưa biết là ai. Nếu trả 401 ở đây thì client điều người dùng đi đăng nhập lại, mà đăng nhập lại cũng không giải quyết được gì."

---

## PHỤ LỤC — BẢNG TRA NHANH KẾT QUẢ (đã chạy thật, xác nhận đúng)

| Folder | Request | Mã | Folder | Request | Mã |
| :--- | :--- | :---: | :--- | :--- | :---: |
| 0 | Đăng nhập admin/chusan/user | 200 | 3 | TC08 user xem /me | 200 |
| 1 | Ca 1 không token | 401 | 3 | TC09 user → /users | 403 |
| 1 | Ca 2 token user | 403 | 3 | TC10 chusan → /users | 403 |
| 1 | Ca 3 token chusan | 201 | 3 | TC11 admin → /users | 200 |
| 2 | TC01 đăng ký hợp lệ | 201 | 3 | TC12 user xem người khác | 403 |
| 2 | TC02 trùng tên | 400 | 3 | TC13 chusan xem người khác | 200 |
| 2 | TC03 sai quy cách | 400 | 3 | TC14 ID không tồn tại | 404 |
| 2 | TC04 sai mật khẩu | 401 | 4 | TC15 Auth → Pitch | 201 |
| 2 | TC05 không tồn tại | 401 | 4 | TC16 Auth → Booking | *(cần 8083)* |
| 3 | TC06 không token | 401 | | | |
| 3 | TC07 sai chữ ký | 401 | | | |
