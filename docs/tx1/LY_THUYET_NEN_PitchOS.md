# Lý thuyết nền để hiểu hết slide kiến trúc PitchOS

Bản này viết cho người **chưa biết gì** về lập trình web hay kiến trúc hệ thống. Đọc hết là hiểu được từng chữ trên chín slide, và trả lời được câu hỏi của thầy.

Cách đọc: mỗi khái niệm gồm ba phần — **Là gì** (định nghĩa đời thường), **Trong PitchOS** (nó nằm ở đâu trong hệ thống của nhóm), **Slide** (xuất hiện ở slide nào). Không cần đọc theo thứ tự nếu đã biết phần nào.

---

## Phần 1 — Những thứ cơ bản nhất

### 1.1. Client và Server

**Là gì.** Hai vai trong mọi hệ thống phần mềm.

- **Client** (ứng dụng khách) là bên *hỏi*: điện thoại, trình duyệt, hoặc một công cụ thử nghiệm.
- **Server** (máy chủ) là bên *trả lời*: chương trình chạy liên tục, nhận câu hỏi, tra dữ liệu, gửi kết quả về.

Ví dụ đời thường: client là khách ngồi ở bàn gọi món, server là nhà bếp.

**Trong PitchOS.** Nhóm chưa làm giao diện web, nên client là **Swagger UI** và **Postman** (xem mục 7.4 và 7.5). Server là ba chương trình Java chạy trên máy.

**Slide.** 4 — ô trên cùng ghi "Swagger UI · Postman · cURL · ứng dụng khách".

### 1.2. HTTP

**Là gì.** Bộ quy tắc để client và server nói chuyện qua mạng. Mỗi lần nói chuyện gồm đúng hai lượt: client gửi một **request** (yêu cầu), server gửi lại một **response** (phản hồi). Hết. Không có lượt thứ ba.

Một request gồm:

- **Phương thức** (method): hành động muốn làm
- **Đường dẫn** (URL): làm trên cái gì
- **Header**: thông tin kèm theo, ví dụ giấy tờ tùy thân
- **Body**: dữ liệu gửi lên, viết dưới dạng JSON

**Bốn phương thức nhóm dùng:**

| Phương thức | Nghĩa | Ví dụ trong PitchOS |
|---|---|---|
| `GET` | Lấy ra để xem, không đổi gì | `GET /api/v1/pitches` — xem danh sách sân |
| `POST` | Tạo mới | `POST /api/v1/bookings` — đặt một sân |
| `PATCH` | Sửa một phần | `PATCH /api/v1/bookings/5/status` — duyệt đơn số 5 |
| `PUT` | Thay toàn bộ | sửa thông tin một sân |

**Slide.** 5, 6 — mọi dòng kiểu `GET /api/v1/pitches/{id}` là một request HTTP.

### 1.3. API và endpoint

**Là gì.** **API** là danh sách những câu hỏi mà một server chịu trả lời. Giống thực đơn của nhà hàng: ngoài thực đơn thì không gọi được.

Mỗi món trong thực đơn đó là một **endpoint** — một cặp (phương thức + đường dẫn).

**Trong PitchOS.** Ba dịch vụ có ba thực đơn riêng. Ví dụ thực đơn của Booking Service có `POST /api/v1/bookings`, `GET /api/v1/bookings/my-bookings`, `PATCH /api/v1/bookings/{id}/status`.

### 1.4. REST

**Là gì.** Một **phong cách** thiết kế API, không phải một công nghệ. Quy ước chính:

- Mỗi thứ trong hệ thống là một **tài nguyên** có địa chỉ riêng: sân số 1 là `/api/v1/pitches/1`
- Dùng phương thức HTTP để nói hành động, không nhét động từ vào đường dẫn. Viết `POST /bookings` chứ không viết `/taoDonDatSan`
- Server **không nhớ** client là ai giữa hai lần gọi (xem mục 4.5)

**Vì sao nhóm chọn REST.** Dễ thử bằng Postman, dễ đọc log, mọi ngôn ngữ đều gọi được, và thầy có thể gọi thử ngay trên Swagger mà không cần cài gì.

**Slide.** 4 (nhãn "REST / HTTP"), 5 (thẻ "REST — Client hỏi dịch vụ").

### 1.5. JSON

**Là gì.** Cách viết dữ liệu thành chữ để gửi qua mạng, cả người và máy đều đọc được.

```json
{
  "pitchId": 1,
  "startTime": "2026-11-20T09:00:00",
  "endTime": "2026-11-20T10:30:00"
}
```

Đọc là: "sân số 1, từ 9 giờ đến 10 giờ 30 ngày 20/11/2026".

**Trong PitchOS.** Mọi dữ liệu gửi lên và trả về đều là JSON.

### 1.6. Cổng (port)

**Là gì.** Một máy tính chỉ có một địa chỉ mạng, nhưng chạy được nhiều chương trình cùng lúc. **Cổng** là số thứ tự để phân biệt chúng — như số phòng trong một tòa nhà: địa chỉ tòa nhà là một, nhưng phòng 8081 và phòng 8082 là hai nơi khác nhau.

**Trong PitchOS.**

| Cổng | Dịch vụ |
|---|---|
| 8081 | Auth & User Service |
| 8082 | Pitch Service |
| 8083 | Booking Service |
| 3306 | MySQL (cơ sở dữ liệu) |

Gọi `http://localhost:8083/api/v1/bookings` nghĩa là: trên máy này, gõ cửa phòng 8083, hỏi về đơn đặt sân.

**Slide.** 4 — con số `:8081`, `:8082`, `:8083` ở góc mỗi thẻ dịch vụ.

### 1.7. Mã trạng thái HTTP (status code)

**Là gì.** Con số server trả về để nói kết quả. Nhìn chữ số đầu là biết:

- **2xx** — xong việc
- **4xx** — **client sai**, gửi lại y như cũ cũng vẫn sai
- **5xx** — **server sai hoặc hỏng**, client gửi lại sau có thể được

**Bảy mã trong PitchOS:**

| Mã | Tên | Nghĩa trong PitchOS |
|---|---|---|
| `200 OK` | Thành công | Lấy danh sách sân xong |
| `201 Created` | Đã tạo | Đặt sân xong, đơn đã có trong cơ sở dữ liệu |
| `400 Bad Request` | Yêu cầu không hợp lệ | Khung giờ đã có người đặt, hoặc sân đang bảo trì |
| `401 Unauthorized` | Chưa xác thực | Không gửi token, token hết hạn, hoặc token bị sửa |
| `403 Forbidden` | Không đủ quyền | Token hợp lệ nhưng sai vai trò: khách đòi duyệt đơn |
| `404 Not Found` | Không tìm thấy | Đặt sân với `pitchId` không tồn tại |
| `503 Service Unavailable` | Dịch vụ không khả dụng | Pitch Service đã tắt, Booking không hỏi được giá |

**Phân biệt quan trọng nhất: 401 và 403.**

- 401 = "**anh là ai?**" — hệ thống không biết người gọi là ai
- 403 = "**tôi biết anh là ai, nhưng việc này không phải của anh**"

**Slide.** 7 — bốn thẻ lớn ghi 404, 503, 400, 400. Slide 8 — dòng "hai mã 401 và 403".

---

## Phần 2 — Kiến trúc: vì sao chia thành ba dịch vụ

### 2.1. Monolith (khối một cục)

**Là gì.** Cách làm truyền thống: toàn bộ hệ thống là **một chương trình duy nhất**, một cơ sở dữ liệu duy nhất.

**Ưu điểm.** Dễ bắt đầu, gọi hàm nhau trực tiếp, chỉ cần bật một lần.

**Nhược điểm.** Sửa một chỗ nhỏ phải bật lại cả hệ thống. Một lỗi tràn bộ nhớ ở phần quản lý sân làm sập luôn phần đặt sân. Nhiều người cùng sửa thì đụng nhau.

### 2.2. Microservices (nhiều dịch vụ nhỏ)

**Là gì.** Cắt hệ thống thành nhiều chương trình nhỏ, mỗi chương trình:

- Lo **một nhóm nghiệp vụ** duy nhất
- Chạy **riêng một tiến trình**, trên cổng riêng
- Có **cơ sở dữ liệu riêng**
- Nói chuyện với nhau **chỉ qua mạng**, không gọi hàm trực tiếp

**Hình dung.** Monolith là một người làm hết: thu ngân, bếp, phục vụ. Microservices là ba người mỗi người một việc, nói với nhau bằng phiếu order.

**Trong PitchOS.** Ba dịch vụ:

| Dịch vụ | Chịu trách nhiệm | Nếu nó chết |
|---|---|---|
| Auth & User `:8081` | Đăng ký, đăng nhập, cấp token, vai trò | Không ai đăng nhập mới được, nhưng token đã cấp vẫn dùng được |
| Pitch `:8082` | Danh mục sân, đơn giá, bảo trì | Không xem được sân, **không đặt được sân mới** |
| Booking `:8083` | Nhận đơn, tính tiền, chống trùng, duyệt | Không đặt được, nhưng vẫn xem được danh sách sân |

**Giá phải trả.** Chia nhỏ không miễn phí:

- Mã xác thực token **bị lặp ở cả ba** dịch vụ
- Một việc phải gọi qua mạng nhiều lần, chậm hơn gọi hàm
- Lỗi khó lần hơn vì nằm rải ở ba nơi
- Phải bật ba chương trình mới demo được

Trên slide 4 nhóm ghi thẳng cái giá này ở dòng lưu ý màu cam. Nói ra được cái giá là điểm cộng, không phải điểm trừ.

**Slide.** 4, 5.

### 2.3. Database per Service (mỗi dịch vụ một cơ sở dữ liệu)

**Là gì.** Nguyên tắc: dịch vụ nào **chỉ được đọc và ghi cơ sở dữ liệu của mình**. Muốn biết dữ liệu của dịch vụ khác thì **hỏi qua API**, tuyệt đối không tự chọc vào bảng của nó.

**Vì sao nghiêm ngặt vậy.** Nếu Booking được đọc thẳng bảng `pitches`, thì ngày nào Pitch đổi tên cột là Booking vỡ. Ba dịch vụ lúc đó gắn chặt vào nhau — chia nhỏ mà vẫn phụ thuộc, mất hết lợi ích.

**Trong PitchOS.**

| Dịch vụ | Schema | Bảng chính |
|---|---|---|
| Auth & User | `pitchos_user_db` | `users` |
| Pitch | `pitchos_pitch_db` | `pitches` |
| Booking | `pitchos_booking_db` | `bookings` |

Ba schema này nằm trong **cùng một container MySQL** tên `pitchos-mysql` cho dễ chạy trên máy cá nhân, nhưng **tách biệt hoàn toàn về logic** — không dịch vụ nào có quyền chạm vào schema của dịch vụ khác.

**Slide.** 4 (ba ô trắng ghi tên schema), 5 (bảng ba dòng).

### 2.4. Khóa ngoại và Logical ID

**Là gì.**

- **Khóa ngoại** (foreign key) là ràng buộc trong cùng một cơ sở dữ liệu: cột `pitch_id` của bảng `bookings` buộc phải trỏ tới một dòng thật trong bảng `pitches`. Cơ sở dữ liệu tự kiểm, sai là chặn.
- **Logical ID** là khi chỉ **lưu con số** mà **không có ràng buộc** nào. Bảng `bookings` lưu `pitch_id = 1`, nhưng cơ sở dữ liệu không hề biết sân 1 có tồn tại hay không.

**Vì sao PitchOS phải dùng Logical ID.** Vì hai bảng ở hai schema khác nhau, và nguyên tắc 2.3 cấm Booking chạm vào `pitches`. Không thể đặt khóa ngoại xuyên schema theo kiểu đó.

**Hệ quả.** Việc kiểm "sân này có thật không" chuyển từ cơ sở dữ liệu lên **tầng mã nguồn**: Booking phải tự gọi sang Pitch Service hỏi. Sân không tồn tại thì Pitch trả 404, và Booking từ chối ghi đơn. Đây chính là thẻ `404` trên slide 7.

**Slide.** 4 — dòng "liên kết giữa bảng bằng Logical ID, không khóa ngoại".

---

## Phần 3 — Ba dịch vụ nói chuyện với nhau thế nào

### 3.1. Đồng bộ và bất đồng bộ

**Đồng bộ (synchronous).** Gọi rồi **đứng chờ** câu trả lời mới làm tiếp. Như gọi điện thoại: phải có người bắt máy.

- Được: biết ngay kết quả, logic đơn giản, dễ gỡ lỗi
- Mất: bên kia chết là mình tắc; bên kia chậm là mình chậm theo

**Bất đồng bộ (asynchronous).** Gửi một tin nhắn vào **hàng đợi** rồi đi làm việc khác, ai rảnh thì xử lý. Như nhắn tin.

- Được: bên kia chết tin vẫn nằm đó chờ, chịu tải tốt
- Mất: không biết kết quả ngay, phải xử lý chuyện "dữ liệu tạm thời chưa khớp", cần thêm phần mềm hàng đợi như **Kafka** hay **RabbitMQ**

**Trong PitchOS.** **Chỉ dùng đồng bộ.** Vì đặt sân phải biết **ngay** là được hay không — không thể trả lời khách "đơn của anh đang trong hàng đợi, 5 giây nữa biết kết quả". Nhóm **không dùng Kafka**, và trên slide 5 ghi rõ "không có hàng đợi sự kiện".

**Nếu thầy hỏi "sao không dùng Kafka":** vì không có việc nào trong hệ thống chịu được chậm. Cả bốn bước đặt sân đều phải xong trước khi trả lời khách. Thêm Kafka lúc này chỉ thêm phức tạp mà không giải quyết vấn đề nào đang có.

**Slide.** 5 — phụ đề "Chỉ một kiểu giao tiếp: REST đồng bộ, không có hàng đợi sự kiện".

### 3.2. OpenFeign

**Là gì.** Một thư viện của Spring giúp viết lời gọi sang dịch vụ khác cho gọn. Thay vì tự tay mở kết nối, dựng request, đọc chuỗi JSON rồi chuyển thành đối tượng Java, lập trình viên chỉ **khai báo** cái mình muốn:

```java
@FeignClient(name = "pitch-service", url = "${pitch.service.url}")
public interface PitchClient {
    @GetMapping("/api/v1/pitches/{id}")
    PitchResponseDTO getPitchById(@PathVariable Long id);
}
```

Viết xong, trong mã nghiệp vụ chỉ cần `pitchClient.getPitchById(1)` — **trông như gọi một hàm bình thường**, nhưng thực chất bên dưới là một request HTTP đi qua mạng tới cổng 8082.

**Điều phải nhớ.** Nó *trông* như gọi hàm nhưng *không phải*. Nó đi qua mạng, nên **có thể thất bại**: bên kia tắt, mạng nghẽn, trả về lỗi. Vì vậy mới cần Phần 6 bên dưới.

**Trong PitchOS.** Đúng **một** lời gọi liên dịch vụ, **một chiều**:

> Booking Service → `GET /api/v1/pitches/{id}` → Pitch Service

Pitch **không bao giờ** gọi ngược sang Booking. Một chiều nên không có vòng lặp phụ thuộc, dễ suy luận.

**Slide.** 4 (đường cam ghi "OpenFeign"), 5 (thẻ phải), 6 (mũi tên bước 2).

---

## Phần 4 — Bảo mật: xác thực và phân quyền

### 4.1. Xác thực khác phân quyền

Hai việc khác nhau, luôn làm theo thứ tự này:

1. **Xác thực** (authentication) — "**anh là ai?**" Kiểm tra người gọi đúng là người họ khai. Sai thì **401**.
2. **Phân quyền** (authorization) — "**anh được làm gì?**" Biết là ai rồi, mới xét việc này có thuộc quyền họ không. Không thuộc thì **403**.

Ví dụ: vào tòa nhà phải quẹt thẻ (xác thực). Thẻ hợp lệ nhưng là thẻ khách thì không mở được cửa phòng server (phân quyền).

### 4.2. Băm mật khẩu và BCrypt

**Là gì.** Hệ thống **không được** lưu mật khẩu nguyên văn. Nếu cơ sở dữ liệu bị lấy, mật khẩu của tất cả người dùng mất sạch — mà nhiều người dùng chung mật khẩu ở nhiều nơi.

Thay vào đó lưu **giá trị băm** (hash): một chuỗi sinh ra từ mật khẩu theo một chiều — từ mật khẩu tính ra chuỗi thì dễ, từ chuỗi suy lại mật khẩu thì không làm được.

Lúc đăng nhập, hệ thống băm mật khẩu vừa nhập rồi **so hai chuỗi băm**, chứ không bao giờ so mật khẩu.

**BCrypt** là một thuật toán băm được thiết kế **cố tình chạy chậm**, và mỗi lần băm thêm một chuỗi ngẫu nhiên gọi là **salt**. Chậm nên kẻ tấn công không thể thử hàng tỉ mật khẩu mỗi giây; có salt nên hai người dùng cùng mật khẩu `123456` vẫn cho hai chuỗi băm khác nhau.

**Trong PitchOS.** Bảng `users` chỉ lưu chuỗi băm BCrypt, bắt đầu bằng `$2a$10$...`. Số `10` là **độ khó** — mỗi lần tăng 1 thì thời gian băm tăng gấp đôi.

**Slide.** 5 — dòng "Tài khoản, mật khẩu băm BCrypt, vai trò".

### 4.3. Token và JWT

**Vấn đề.** Không thể bắt khách gửi lại mật khẩu ở **mỗi** request. Cần một cái **vé** cấp một lần, dùng cho nhiều lần sau.

**JWT** (JSON Web Token) là cái vé đó. Nó là một chuỗi dài, gồm **ba phần ngăn bởi dấu chấm**:

```
eyJhbGciOiJIUzI1NiJ9 . eyJzdWIiOiJraG...  . 4f2c8a9b1e...
       HEADER               PAYLOAD          SIGNATURE
```

| Phần | Chứa gì | Trong PitchOS |
|---|---|---|
| **Header** | Thuật toán ký | `HS256` |
| **Payload** | Thông tin về người dùng — gọi là **claim** | `sub` (tên đăng nhập), `userId`, `role`, `exp` (thời điểm hết hạn) |
| **Signature** | Chữ ký, tính từ hai phần trên cộng với **khóa bí mật** | chuỗi băm |

**Điều quan trọng nhất về JWT: hai phần đầu KHÔNG được mã hóa.** Chúng chỉ được mã hóa Base64, ai cũng giải ra đọc được. Dán một token lên trang `jwt.io` là thấy hết. Nên **tuyệt đối không bỏ mật khẩu hay dữ liệu nhạy cảm vào payload**.

**Vậy JWT bảo vệ bằng cách nào?** Bằng **chữ ký**, không bằng che giấu. Kẻ tấn công sửa `role` từ `user` thành `admin` thì nội dung đổi, chữ ký cũ không còn khớp, server phát hiện ngay và trả **401**. Muốn ký lại chữ ký đúng thì phải có khóa bí mật — mà khóa đó chỉ server biết.

**Nhóm đã kiểm đúng việc này:** ca kiểm thử "token bị sửa" lấy token thật, đổi một ký tự cuối, gửi lên, nhận về đúng 401.

**Slide.** 4 — dòng "Mỗi yêu cầu mang theo `Authorization: Bearer <JWT>`".

### 4.4. HS256 và RS256

**HS256** — **một khóa bí mật duy nhất**, dùng cả để ký và để xác minh. Giống chìa khóa cửa nhà: ai có chìa cũng mở được **và** khóa được.

**Trong PitchOS hiện tại:** cả ba dịch vụ cùng giữ một chuỗi `SECRET_KEY` giống nhau.

**Hạn chế — đây là điểm yếu nghiêm trọng nhất nhóm tự nhận.** Cả ba dịch vụ đều **có khả năng tự phát hành token**, kể cả token `role = admin`, dù đúng ra chỉ Auth Service được quyền đó. Nếu kẻ tấn công chiếm được Pitch Service — dịch vụ đơn giản nhất, ít được bảo vệ nhất — họ lấy luôn khóa và tự ký token admin, rồi dùng nó đi khắp hệ thống.

**RS256** — **cặp hai khóa**:

- **Khóa riêng** (private key): chỉ Auth Service giữ, dùng để **ký**
- **Khóa công khai** (public key): phát cho Pitch và Booking, **chỉ xác minh được, không ký được**

Giống con dấu: chỉ giám đốc có con dấu, nhưng ai cũng nhìn được dấu thật hay giả.

Chuyển sang RS256 thì Pitch bị chiếm cũng **không tự làm được token admin**, vì nó không có khóa ký. Đây là **ưu tiên số một** ở slide 9.

**Slide.** 9 — mục `01 Bảo mật`.

### 4.5. Stateless (không lưu phiên)

**Là gì.** Server **không nhớ** gì về client giữa hai request. Mỗi request phải **tự mang đủ** thông tin để được xử lý.

**Cách cũ (có phiên).** Đăng nhập xong, server lưu một bản ghi phiên trong bộ nhớ, client giữ một mã phiên. Mỗi request server phải tra lại bản ghi đó.

**Cách JWT (không phiên).** Mọi thông tin đã nằm trong token. Server chỉ cần **xác minh chữ ký** là tin được, không phải tra ở đâu cả — và quan trọng nhất, **không phải hỏi lại Auth Service**.

**Vì sao điều này đáng nói trong hệ nhiều dịch vụ.** Nếu Pitch và Booking phải hỏi Auth mỗi lần có request, thì Auth thành cổ chai: nó chết là cả hệ thống chết. Với JWT, Auth chỉ cần sống lúc **đăng nhập**. Sau đó nó tắt, người đang có token vẫn làm việc bình thường cho tới khi token hết hạn.

**Giá phải trả — nhóm nên chủ động nói nếu bị hỏi.** Vì server không lưu gì, nên **không thu hồi được token** đã cấp. Người dùng bị khóa tài khoản vẫn dùng token cũ cho tới lúc nó hết hạn. Cách khắc phục là **Refresh Token** cộng cơ chế thu hồi — đã ghi ở slide 9.

**Slide.** 5 — "Mỗi dịch vụ tự xác minh chữ ký token, không hỏi lại Auth Service. Không có phiên đăng nhập lưu ở máy chủ."

### 4.6. RBAC — phân quyền theo vai trò

**Là gì.** Không gán quyền cho từng người, mà gán quyền cho **vai trò**, rồi gán vai trò cho người. Thêm 1000 khách mới cũng không phải sửa bảng quyền.

**Ba vai trò trong PitchOS:**

| Vai trò | Là ai | Được làm |
|---|---|---|
| `user` | Khách đặt sân | Xem sân, gửi đơn đặt, xem đơn của mình |
| `chusan` | Chủ sân | Thêm sân, sửa đơn giá, chuyển sân sang bảo trì, **duyệt hoặc từ chối đơn** |
| `admin` | Quản trị | Xem danh sách người dùng, kèm quyền của chủ sân |

**Cách hoạt động.** Vai trò nằm trong claim `role` của token. Mỗi endpoint khai báo mình cần vai trò nào. Ví dụ `POST /api/v1/bookings` yêu cầu vai trò `user` — chủ sân gọi vào đây sẽ nhận **403**, dù token hoàn toàn hợp lệ.

**Chi tiết nhóm nên biết.** Hợp đồng claim của hệ thống là: `role` viết **chữ thường, không có tiền tố** (`user`, không phải `ROLE_USER`), và **bắt buộc** có `userId`. Ba dịch vụ phải thống nhất đúng quy ước này, lệch một chữ là 403 ở chỗ không ngờ.

**Slide.** 3 ("Ba vai trò user, chusan, admin"), 8 ("Phân quyền ba vai trò, hai mã 401 và 403").

---

## Phần 5 — Dữ liệu và chuyện hai người đặt cùng lúc

Đây là phần **khó nhất** và cũng là phần **đáng điểm nhất** của slide 7. Nên đọc kỹ.

### 5.1. Giao dịch (transaction)

**Là gì.** Một nhóm thao tác trên cơ sở dữ liệu được coi là **một việc không chia nhỏ**: hoặc xong hết, hoặc không có gì xảy ra. Không bao giờ dừng ở giữa.

Ví dụ chuyển tiền: trừ tài khoản A và cộng tài khoản B phải cùng một giao dịch. Nếu mất điện sau bước trừ, số tiền đó bốc hơi.

### 5.2. Race condition — tranh chấp

**Là gì.** Hai việc chạy **cùng lúc**, và **kết quả phụ thuộc vào ai nhanh hơn ai**. Chạy mười lần có thể đúng mười lần, lần thứ mười một sai — nên loại lỗi này cực khó phát hiện.

**Trong PitchOS, cụ thể.** Khi có đơn đặt, Booking làm hai việc liên tiếp:

1. Đếm xem khung giờ này đã có đơn nào giữ chưa
2. Nếu chưa, ghi đơn mới

Bây giờ hai khách bấm đặt sân 1, cùng khung 09:00–10:30, cách nhau vài phần nghìn giây:

```
Thời điểm   Khách A                    Khách B
  t1        đếm → 0 đơn
  t2                                   đếm → 0 đơn   (A chưa ghi kịp!)
  t3        ghi đơn #101
  t4                                   ghi đơn #102
```

Cả hai đều thấy "chưa có ai", cả hai đều ghi. **Một khung giờ bị bán hai lần.** Hai khách cùng đến sân, chỉ một người được vào.

Đây đúng là câu hỏi đóng khung ở cuối slide 2: *"Nếu hai khách cùng bấm đặt một khung giờ trong cùng một giây, ai được sân?"*

### 5.3. Khóa (lock) — cách nhóm xử lý

**Là gì.** Buộc các việc tranh chấp phải **xếp hàng lần lượt**, không ai chen vào giữa bước 1 và bước 2 của người khác.

**Cách nhóm làm.** Giữ **một khóa riêng cho từng sân**, và bọc cả hai bước "đếm" + "ghi" vào trong khóa đó:

```java
synchronized (pitchLocks.computeIfAbsent(request.getPitchId(), id -> new Object())) {
    Long overlapping = bookingRepository.countOverlappingBookings(
            request.getPitchId(), request.getStartTime(), request.getEndTime());
    if (overlapping > 0) {
        throw new BadRequestException("Khung giờ này đã có người đặt");
    }
    // ... ghi đơn với trạng thái cho_duyet
}
```

Lúc này dòng thời gian thành:

```
Thời điểm   Khách A                    Khách B
  t1        lấy được khóa sân 1
  t2        đếm → 0 đơn                chờ (khóa đang bị giữ)
  t3        ghi đơn #101, nhả khóa     chờ
  t4                                   lấy được khóa, đếm → 1 đơn
  t5                                   → 400 "Khung giờ này đã có người đặt"
```

**Kết quả: đúng một đơn nhận 201, đơn còn lại nhận 400.** Nhóm đã chạy thật hai request song song và thấy đúng như vậy.

**Hai điểm tinh tế nên nắm, vì thầy có thể hỏi:**

1. **Khóa theo từng sân, không khóa toàn bộ.** Nếu dùng một khóa chung cho cả hệ thống thì mọi đơn đặt phải xếp hàng sau nhau, dù khác sân hoàn toàn — hệ thống chậm vô lý. Khóa theo `pitchId` nên hai khách đặt **hai sân khác nhau** vẫn chạy song song, chỉ người đặt **cùng một sân** mới phải chờ.

2. **Giới hạn: khóa nằm trong bộ nhớ của tiến trình.** `pitchLocks` là một biến trong chương trình Java đang chạy. Nếu chạy **hai bản** Booking Service cùng lúc để chịu tải, mỗi bản có một bộ khóa **riêng**, không ai biết đến ai, và lỗi đặt trùng **quay lại nguyên vẹn**.

   Nhóm ghi thẳng giới hạn này ở dòng cam slide 7, và đề xuất cách khắc phục ở slide 9: **đưa việc chống trùng xuống tầng cơ sở dữ liệu** bằng một ràng buộc duy nhất. Cơ sở dữ liệu là chỗ duy nhất mọi bản Booking đều phải đi qua, nên nó mới là nơi đúng để chặn.

**Slide.** 7 — thẻ "Hai khách đặt cùng một giây" và dòng lưu ý cam.

### 5.4. Ba trạng thái đơn đặt

Đơn đặt sân chỉ có đúng ba trạng thái, không hơn:

| Trạng thái | Nghĩa | Có giữ khung giờ không |
|---|---|---|
| `cho_duyet` | Khách vừa gửi, chủ sân chưa xem | **Có** |
| `da_duyet` | Chủ sân đã nhận | **Có** |
| `tu_choi` | Chủ sân từ chối | **Không** — khung giờ được nhả ra |

**Chi tiết nhóm xử lý thêm.** Vì đơn `tu_choi` đã nhả khung giờ, người khác có thể đã đặt vào đúng chỗ đó. Nên hệ thống **không cho đổi trạng thái** một đơn đã từ chối — nếu cho, sẽ có hai đơn cùng giữ một khung giờ. Thử đổi trạng thái đơn `tu_choi` sẽ nhận **400**.

**Không có trạng thái "đã thanh toán"** — vì hệ thống không thu tiền (slide 3).

### 5.5. Hai trạng thái của sân, và dữ liệu mẫu

Sân chỉ có hai trạng thái:

| Trạng thái | Nghĩa | Đặt được không |
|---|---|---|
| `hoat_dong` | Sân bình thường | **Được** |
| `bao_tri` | Sân đang bảo trì | **Không** — Booking trả 400 "Sân đang bảo trì" |

Sân cũng có ba loại: `san_5`, `san_7`, `san_10` — tức sân 5, 7 và 10 người.

**Dữ liệu mẫu để nhớ.** Sân số 1 giá **300.000đ mỗi giờ**, trạng thái `hoat_dong`. Khách đặt 09:00–10:30, tức **1,5 giờ**, nên tổng tiền là 300.000 × 1,5 = **450.000đ**. Đây đúng là con số trên slide 6 — nhớ ba số này là trình bày được cả slide đó.

---

## Phần 6 — Khi có sự cố

### 6.1. Vì sao phải trả mã lỗi khác nhau

Trả `500` cho mọi lỗi thì client **không biết nên làm gì tiếp**. Mỗi mã khác nhau dẫn tới một hành động khác nhau:

| Mã | Client nên làm gì |
|---|---|
| 400 | Sửa dữ liệu rồi gửi lại — chọn khung giờ khác |
| 401 | Đăng nhập lại |
| 403 | Dừng, việc này không thuộc quyền |
| 404 | Kiểm tra lại mã sân |
| 503 | **Gửi lại sau** — hệ thống đang hỏng, dữ liệu gửi lên vẫn đúng |

Đây là lý do slide 7 có phụ đề: *"Mỗi loại sự cố phải cho một mã lỗi khác nhau, để client biết nên làm gì tiếp"*.

### 6.2. CustomErrorDecoder

**Vấn đề.** Khách gửi `pitchId` không tồn tại. Pitch Service trả `404`. Nhưng về tới Booking, OpenFeign coi mọi phản hồi lỗi là một ngoại lệ chung chung, và nếu không xử lý, Booking sẽ trả về `500` — nghĩa là "server tôi hỏng", trong khi thật ra **client gửi sai**.

**Cách giải.** Một lớp **CustomErrorDecoder** chen vào giữa, đọc mã lỗi Pitch trả về và **dịch lại** thành ngoại lệ tương ứng của Booking. Pitch trả 404 thì khách cũng nhận **404**, đúng bản chất.

**Slide.** 7 — thẻ `404`.

### 6.3. GlobalExceptionHandler

**Là gì.** Một chỗ duy nhất nhận mọi lỗi bất ngờ trong toàn dịch vụ và chuyển thành phản hồi HTTP tử tế. Không có nó, lỗi Java sẽ lòi nguyên **vết gọi hàm** ra cho client — vừa không hiểu được, vừa hở thông tin về mã nguồn.

**Trong PitchOS.** Khi Pitch Service **tắt hẳn**, OpenFeign không kết nối được và ném lỗi. GlobalExceptionHandler bắt lấy, trả về **503** kèm thông báo thử lại sau — thay vì 500 hoặc một đống chữ Java.

**Slide.** 7 — thẻ `503`.

### 6.4. Cô lập lỗi (fault isolation)

**Là gì.** Một bộ phận chết thì chỉ phần việc cần nó bị ảnh hưởng, phần còn lại vẫn chạy.

**Nhóm đã chứng minh bằng thực nghiệm.** Tắt hẳn Pitch Service, rồi gọi hai API của Booking:

| Gọi gì | Kết quả | Vì sao |
|---|---|---|
| `POST /api/v1/bookings` (đặt sân mới) | **503** | Cần hỏi giá, mà Pitch đã chết |
| `GET /api/v1/bookings/my-bookings` (xem đơn cũ) | **200** | Chỉ đọc cơ sở dữ liệu của chính nó, không cần ai |

Đây là điều monolith **không làm được**: trong một khối, phần quản lý sân chết thì cả chương trình chết theo.

**Slide.** 7 — thẻ "Lỗi được cô lập".

---

## Phần 7 — Công cụ và nền tảng

### 7.1. Java, Spring Boot, Maven

- **Java 17** — ngôn ngữ lập trình.
- **Spring Boot 3.2.5** — bộ khung (framework) lo sẵn phần việc lặp lại: mở cổng nghe HTTP, chuyển JSON thành đối tượng Java, nối cơ sở dữ liệu, kiểm tra token. Nhờ nó, lập trình viên chỉ viết phần nghiệp vụ. "Boot" vì mỗi dịch vụ tự chạy được bằng một câu lệnh, không cần cài thêm máy chủ ứng dụng.
- **Maven** — công cụ tải thư viện và đóng gói. Thư viện cần dùng khai trong tệp `pom.xml`, Maven tự tải về.

### 7.2. MySQL và Docker

- **MySQL 8.0** — hệ quản trị cơ sở dữ liệu quan hệ, dữ liệu nằm trong bảng có hàng và cột.
- **Docker** — công cụ chạy phần mềm trong một **container**: một hộp đóng kín, mang theo đủ mọi thứ nó cần. Nhờ vậy MySQL chạy giống nhau trên mọi máy, và không phải cài MySQL trực tiếp vào Windows.

**Trong PitchOS.** Một container tên `pitchos-mysql`, bên trong có ba schema của ba dịch vụ. **Docker phải đang bật** thì ba dịch vụ mới khởi động được — nếu không sẽ báo `Connection refused` ở cổng 3306.

**Slide.** 4 — ô dưới cùng "MySQL 8.0 · Docker".

### 7.3. Giải thích thêm: ORM và Hibernate

Nhóm không ghi lên slide, nhưng nếu thầy hỏi "sao không thấy câu SQL nào":

**ORM** (Object–Relational Mapping) là lớp trung gian ánh xạ **bảng** trong cơ sở dữ liệu thành **lớp** trong Java. Bảng `bookings` ↔ lớp `Booking`; một hàng ↔ một đối tượng. **Hibernate** là bộ ORM Spring Boot dùng sẵn: gọi `bookingRepository.save(booking)` thì Hibernate tự sinh câu `INSERT`.

Chỗ nào logic phức tạp quá — như câu đếm đơn giao nhau khung giờ — nhóm vẫn viết truy vấn tay cho rõ ràng và kiểm soát được.

### 7.4. Swagger UI và OpenAPI

**Là gì.** **OpenAPI** là cách mô tả API thành một tệp chuẩn. **Swagger UI** đọc tệp đó rồi dựng ra một trang web: liệt kê mọi endpoint, và **gọi thử được ngay trên trình duyệt**.

**Vì sao đáng nói.** Tài liệu API thường lạc hậu vì viết tay rồi quên cập nhật. Swagger sinh **tự động từ mã nguồn**, nên không bao giờ lệch. Đổi một endpoint là trang web đổi theo.

**Địa chỉ trong PitchOS:**

```
http://localhost:8081/swagger-ui.html
http://localhost:8082/swagger-ui.html
http://localhost:8083/swagger-ui.html
```

### 7.5. Postman, Collection, Assertion

- **Postman** — công cụ gửi request HTTP bằng tay và xem phản hồi.
- **Collection** — một bộ request đã soạn sẵn, lưu lại thành tệp, chạy lại được nhiều lần.
- **Assertion** (phép kiểm) — câu lệnh kiểm tra tự động viết kèm mỗi request: "mã trả về phải là 201", "`totalPrice` phải bằng 450000", "`status` phải là `cho_duyet`". Chạy xong Postman tự đếm bao nhiêu phép kiểm đạt, bao nhiêu trượt.

**Đây là nguồn của ba con số trên slide 8:**

| Con số | Nghĩa |
|---|---|
| **60 request** | Tổng số lời gọi API trong ba collection |
| **119 phép kiểm** | Tổng số câu kiểm tra tự động — một request có thể có nhiều phép kiểm |
| **115 đã đạt** | Số phép kiểm đúng như mong đợi |

**Bốn phép kiểm còn lại** thuộc nhóm kiểm thử `503`: muốn chạy chúng thì **phải tắt Pitch Service**. Khi chạy cả bộ với hệ thống đầy đủ, chúng đương nhiên không đạt — đó là **điều kiện của chính ca kiểm thử**, không phải lỗi hệ thống. Nói đúng như vậy nếu thầy hỏi.

**Slide.** 8.

---

## Phần 8 — Tra cứu nhanh

| Thuật ngữ | Một câu |
|---|---|
| API | Danh sách câu hỏi mà server chịu trả lời |
| Assertion | Câu kiểm tra tự động kèm mỗi request trong Postman |
| Bất đồng bộ | Gửi vào hàng đợi rồi đi làm việc khác |
| BCrypt | Thuật toán băm mật khẩu, cố tình chạy chậm, có salt |
| Bearer Token | Cách gửi JWT: header `Authorization: Bearer <token>` |
| Claim | Một mẩu thông tin trong phần payload của JWT, ví dụ `role`, `userId` |
| Client | Bên gửi yêu cầu |
| Container | Hộp đóng kín chứa một phần mềm cùng mọi thứ nó cần |
| Database per Service | Mỗi dịch vụ một cơ sở dữ liệu riêng, không ai chạm của ai |
| Docker | Công cụ chạy phần mềm trong container |
| Đồng bộ | Gọi rồi đứng chờ trả lời |
| Endpoint | Một cặp (phương thức + đường dẫn), ví dụ `POST /api/v1/bookings` |
| HS256 | Ký JWT bằng một khóa bí mật dùng chung — ký và xác minh cùng khóa |
| HTTP | Quy tắc hỏi–đáp giữa client và server qua mạng |
| JSON | Cách viết dữ liệu thành chữ để gửi qua mạng |
| JWT | Vé có chữ ký, mang danh tính và vai trò người dùng |
| Khóa (lock) | Cơ chế buộc các việc tranh chấp xếp hàng lần lượt |
| Logical ID | Chỉ lưu con số định danh, không có ràng buộc khóa ngoại |
| Microservices | Nhiều chương trình nhỏ độc lập, nói với nhau qua mạng |
| Monolith | Toàn hệ thống trong một chương trình, một cơ sở dữ liệu |
| OpenFeign | Thư viện Spring giúp gọi dịch vụ khác như gọi hàm |
| ORM | Lớp ánh xạ bảng cơ sở dữ liệu thành lớp trong Java |
| Phân quyền | "Anh được làm gì?" — sai thì 403 |
| Port (cổng) | Số thứ tự phân biệt các chương trình trên cùng một máy |
| Race condition | Hai việc chạy cùng lúc, kết quả phụ thuộc ai nhanh hơn |
| RBAC | Gán quyền theo vai trò, không theo từng người |
| REST | Phong cách thiết kế API quanh tài nguyên và phương thức HTTP |
| RS256 | Ký JWT bằng cặp khóa — chỉ Auth ký được, các dịch vụ khác chỉ xác minh |
| Salt | Chuỗi ngẫu nhiên thêm vào khi băm, để hai mật khẩu giống nhau cho hai chuỗi khác nhau |
| Schema | Một nhóm bảng trong MySQL, như một thư mục |
| Server | Bên nhận và trả lời yêu cầu |
| Stateless | Server không nhớ gì giữa hai request |
| Swagger UI | Trang web tự sinh từ mã nguồn, xem và gọi thử API |
| Transaction | Nhóm thao tác hoặc xong hết hoặc không gì xảy ra |
| Xác thực | "Anh là ai?" — sai thì 401 |

---

## Phần 9 — Mười hai câu thầy có thể hỏi

**1. Vì sao chia ba dịch vụ mà không làm một khối?**
Ba nhóm nghiệp vụ tách bạch rõ, bốn người làm song song không đụng nhau, và một dịch vụ chết không kéo sập cả hệ thống — nhóm đã chứng minh bằng thực nghiệm tắt Pitch Service. Nhóm cũng nhận cái giá: mã xác thực lặp ba lần, phải bật ba chương trình mới demo được.

**2. Sao không dùng API Gateway?**
Với ba dịch vụ thì Gateway thêm một tầng phải chạy và phải gỡ lỗi mà chưa giải quyết vấn đề nào đang có. Nhóm chấp nhận hệ quả là mã JWT lặp ở ba nơi, và đã đưa Gateway vào slide 9 như việc làm tiếp — lúc đó nó sẽ là điểm xác thực tập trung, bỏ được phần lặp.

**3. Sao không dùng Kafka?**
Không có việc nào trong hệ thống chịu được chậm. Đặt sân phải trả lời ngay là được hay không. Cả bốn bước đều phải xong trước khi trả lời khách, nên hàng đợi chỉ thêm phức tạp.

**4. Sao không dùng Eureka hay service discovery?**
Chỉ có đúng một lời gọi liên dịch vụ, địa chỉ cố định, cấu hình trong tệp là đủ. Eureka giải bài toán nhiều bản dịch vụ lên xuống liên tục — bài toán nhóm chưa có.

**5. Dữ liệu ba dịch vụ không khóa ngoại thì làm sao đảm bảo đúng?**
Việc kiểm chuyển từ cơ sở dữ liệu lên tầng mã nguồn: Booking phải gọi Pitch hỏi sân có tồn tại và còn hoạt động không. Sân không tồn tại thì nhận 404, sân bảo trì thì nhận 400, cả hai đều không ghi được đơn.

**6. Hai người đặt cùng lúc thì sao?**
Booking giữ một khóa riêng cho từng sân, bọc cả hai bước kiểm tra trùng và ghi đơn vào trong khóa đó. Đúng một đơn nhận 201, đơn còn lại nhận 400. Nhóm đã chạy thật hai request song song.

**7. Khóa đó chạy nhiều bản Booking có còn đúng không?**
**Không.** Khóa nằm trong bộ nhớ tiến trình, mỗi bản một bộ khóa riêng nên lỗi đặt trùng quay lại. Nhóm ghi rõ giới hạn này trên slide 7 và đề xuất khắc phục ở slide 9: đưa ràng buộc duy nhất xuống tầng cơ sở dữ liệu.

**8. JWT chứa gì, có an toàn không?**
Chứa tên đăng nhập, `userId`, vai trò, thời điểm hết hạn. Nội dung **không được mã hóa**, ai cũng đọc được, nên không bỏ gì nhạy cảm vào. Nó an toàn nhờ **chữ ký**: sửa một ký tự là chữ ký không khớp, server trả 401 — nhóm đã kiểm đúng ca này.

**9. Dùng một khóa bí mật chung cho ba dịch vụ có vấn đề gì?**
Có, và đây là điểm yếu nghiêm trọng nhất. Cả ba đều **có khả năng tự phát hành token admin**, dù chỉ Auth được quyền đó. Pitch bị chiếm là mất cả hệ thống. Vì vậy RS256 là ưu tiên số một ở slide 9.

**10. Vì sao đặt trùng trả 400 chứ không phải 409 Conflict?**
409 đúng về mặt ngữ nghĩa hơn. Nhóm chọn 400 để mọi lỗi vi phạm nghiệp vụ dùng một mã nhất quán, phân biệt bằng nội dung thông báo. Đổi sang 409 là việc nhỏ, chỉ sửa một lớp ngoại lệ.

**11. Có 115 trên 119 phép kiểm, bốn cái còn lại là lỗi gì?**
Không phải lỗi hệ thống. Bốn phép kiểm đó thuộc nhóm kiểm thử 503, **yêu cầu phải tắt Pitch Service mới chạy được**. Chạy với hệ thống đầy đủ thì chúng đương nhiên không đạt — đó là điều kiện của chính ca kiểm thử.

**12. Chưa có giao diện web thì demo thế nào?**
Qua Swagger UI và Postman. Swagger sinh tự động từ mã nguồn nên luôn khớp với API thật, và gọi thử được ngay trên trình duyệt. Giao diện web nằm trong hướng phát triển ở slide 9.
