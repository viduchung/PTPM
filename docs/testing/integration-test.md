# BIÊN BẢN KIỂM THỬ TÍCH HỢP IT01 – IT07 (CONSUMER → PROVIDER)
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)  
**Người thực hiện:** NHẬT — `pitchos-booking-service` (Consumer)  
**Đối tượng kiểm thử:** Luồng Booking Service gọi Pitch Service qua Service ID, cân bằng tải và xử lý lỗi tích hợp  
**Bộ test Postman:** [`postman/collection.json`](../../postman/collection.json) — thư mục *2. Integration & Error Handling (IT01–IT07)*

---

## 1. ĐIỀU KIỆN TIỀN ĐỀ

### 1.1. Phụ thuộc vào công việc của thành viên khác

| Thành phần cần có | Người phụ trách | Phục vụ ca test |
|---|---|---|
| `pitchos-service-registry` (Eureka Server :8761) | Hoàng | Tất cả (Consumer tra cứu Service ID) |
| `docker-compose.yml` toàn hệ thống + 2 instance Pitch | Linh | IT04, IT05, TC01–TC06 |
| `GET /api/v1/instance-info` trên Pitch Service | Linh | TC03 (bảng phân phối 20 request) |
| 3 file SQL init dữ liệu sạch | Hùng | IT01 (sân 1 giá 300.000), IT03a (sân 4 `bao_tri`) |

### 1.2. Khởi động hệ thống và kiểm tra trạng thái

```bash
docker compose up -d
docker compose ps                 # toàn bộ 7 container phải ở trạng thái healthy
curl http://localhost:8083/actuator/health          # {"status":"UP"}
curl -H "Accept: application/json" http://localhost:8761/eureka/apps   # Pitch phải có 2 instance
```

### 1.3. Lấy token trước khi chạy

Trong Postman, chạy lần lượt thư mục **1. Authentication & RBAC** (các request 1.2, 1.3, 1.4). Script `test` tự lưu `userToken`, `chusanToken`, `adminToken` vào biến collection.

---

## 2. KỊCH BẢN VÀ LỆNH CHUẨN BỊ CHO TỪNG CA

| Mã | Tình huống | Lệnh / thao tác chuẩn bị | Request Postman | Mã mong đợi |
|:-:|---|---|---|:-:|
| **IT01** | Đặt sân hợp lệ | Không cần (hệ thống chạy đủ) | `IT01 - Dat san thanh cong` | `201` |
| **IT02** | Sân không tồn tại | Không cần | `IT02 - San khong ton tai pitchId=9999` | `404` |
| **IT03a** | Sân đang bảo trì | Dữ liệu mẫu đã có sân 4 `bao_tri` | `IT03a - San dang bao tri (pitchId=4)` | `400` |
| **IT03b** | Đơn giá Provider không hợp lệ | `docker compose exec mysql-pitch mysql -uroot -p123456 pitchos_pitch_db -e "UPDATE pitches SET price_per_hour = 0 WHERE id = 3;"` | `IT03b - Don gia Provider <= 0` | `502` |
| **IT04** | Provider sập hoàn toàn | `docker compose stop pitchos-pitch-service-1 pitchos-pitch-service-2` rồi **chờ 15–30 giây** | `IT04` và `IT04b` | `503` và `200` |
| **IT05** | Timeout mạng | `docker compose pause pitchos-pitch-service-1 pitchos-pitch-service-2` | `IT05 - Timeout mang` | `503` sau 2–3s |
| **IT06** | Gửi lặp yêu cầu | Không cần | `IT06a` rồi `IT06b` (giữ nguyên khung giờ) | `201` rồi `400` |
| **IT07** | Dữ liệu đầu vào sai | Không cần | `IT07 - endTime truoc startTime` | `400` |

### Lệnh khôi phục bắt buộc sau khi chụp minh chứng

```bash
# Sau IT03b: trả lại đơn giá đúng cho sân 3
docker compose exec mysql-pitch mysql -uroot -p123456 pitchos_pitch_db \
  -e "UPDATE pitches SET price_per_hour = 800000 WHERE id = 3;"

# Sau IT04
docker compose start pitchos-pitch-service-1 pitchos-pitch-service-2

# Sau IT05
docker compose unpause pitchos-pitch-service-1 pitchos-pitch-service-2
```

> ⚠️ **Tuyệt đối không dùng `docker compose down -v`** trong suốt quá trình kiểm thử: cờ `-v` xóa sạch named volume, mất toàn bộ dữ liệu đơn đặt sân đã tạo và không thể minh chứng bảo toàn dữ liệu (DEP06, Bước 8 video demo).

---

## 3. KẾT QUẢ CHẠY THẬT QUA HTTP (MÔI TRƯỜNG CỤC BỘ, CHƯA CẦN DOCKER)

Toàn bộ 7 ca IT01–IT07 đã được **chạy thật bằng request HTTP** trên một hệ thống đầy đủ gồm
Eureka Server + 2 instance Provider + Consumer, dựng trực tiếp trên máy (không qua Docker vì
`docker-compose.yml` của nhóm chưa hoàn thiện). Đây là minh chứng mạnh hơn bộ test đơn vị ở
mục 4: request đi qua mạng thật, qua Eureka thật và qua Spring Cloud LoadBalancer thật.

### 3.1. Môi trường chạy

| Thành phần | Cách chạy | Cổng | Ghi chú |
|---|---|:-:|---|
| `pitchos-service-registry` | `java -jar` (build từ mã nguồn của Hoàng) | 8761 | Eureka Server |
| `pitchos-pitch-service` instance 1 | `java -jar --spring.profiles.active=h2 --server.port=8082`, `INSTANCE_ID=pitch-instance-1` | 8082 | Provider |
| `pitchos-pitch-service` instance 2 | `java -jar --spring.profiles.active=h2 --server.port=8084`, `INSTANCE_ID=pitch-instance-2` | 8084 | Provider, **dùng chung một H2 file DB** với instance 1 (mô phỏng `mysql-pitch` dùng chung trong Docker) |
| `pitchos-booking-service` | `mvn spring-boot:run` + file cấu hình H2 đặt ngoài repo | 8083 | Consumer |
| Token JWT | Ký HS256 bằng đúng `jwt.secret` dùng chung (`userId=3`, `role=user`) | — | Thay cho Auth Service vì máy chạy thử không có MySQL |

> ⚠️ **Lưu ý về mã sân:** môi trường cục bộ nạp dữ liệu bằng `DataInitializer` của Pitch Service,
> nên **sân `bao_tri` là `id = 3`**. Khi chạy bằng Docker, dữ liệu nạp từ `pitchos-database/pitch-init.sql`
> và **sân `bao_tri` là `id = 4`**. Phải đổi `pitchId` cho đúng môi trường khi chạy lại.

Kiểm tra danh bạ trước khi chạy — Provider đã có **đủ 2 instance UP**, Consumer cũng đã tự đăng ký:

```
PITCHOS-PITCH-SERVICE     2 instance: pitchos-pitch-service:pitch-instance-1 (UP)
                                      pitchos-pitch-service:pitch-instance-2 (UP)
PITCHOS-BOOKING-SERVICE   1 instance: pitchos-booking-service:8083
    DiscoveryClient_PITCHOS-BOOKING-SERVICE/pitchos-booking-service:8083 - registration status: 204
```

### 3.2. Bảng kết quả thực tế — 23/11/2026

| Mã | Tình huống | Mã mong đợi | **Mã thực tế** | Thời gian | Kết luận |
|:-:|---|:-:|:-:|:-:|:-:|
| **IT01** | Đặt sân hợp lệ (sân 1, 18:00–19:30, đơn giá 300.000) | `201` | **`201`** | 0,32s | ✅ Đạt — `totalPrice = 450000.00` |
| **IT02** | Sân không tồn tại (`pitchId = 9999`) | `404` | **`404`** | 0,08s | ✅ Đạt |
| **IT03a** | Sân đang bảo trì (`pitchId = 3`) | `400` | **`400`** | 0,03s | ✅ Đạt |
| **IT03b** | Đơn giá Provider `= 0` (sửa trực tiếp DB của Provider) | `502` | **`502`** | 0,08s | ✅ Đạt |
| **IT04** | Dừng hẳn cả 2 instance Provider | `503` | **`503`** | 2,02s | ✅ Đạt — đúng `connect-timeout = 2000ms` |
| **IT05** | Treo cả 2 instance Provider (tương đương `docker compose pause`) | `503` sau 2–3s | **`503`** | **3,03s** | ✅ Đạt — đúng `read-timeout = 3000ms` |
| **IT06** | Gửi lặp cùng khung giờ (sân 2, 18:00–20:00) | `201` rồi `400` | **`201`** rồi **`400`** | 0,15s | ✅ Đạt |
| **IT07** | `endTime` trước `startTime` | `400` | **`400`** | 0,01s | ✅ Đạt — chặn tại validation, không gọi Provider |

**Phản hồi nguyên văn của từng ca:**

```json
IT01 → HTTP 201
{"id":1,"userId":3,"pitchId":1,"startTime":"2027-05-01T18:00:00","endTime":"2027-05-01T19:30:00",
 "totalPrice":450000.00,"status":"cho_duyet","createdAt":"2026-11-23T20:31:03.919175"}
   → 1,5 giờ × 300.000 = 450.000 ✔ đúng đơn giá do Provider công bố

IT02 → HTTP 404
{"status":404,"error":"Not Found","message":"Không tìm thấy sân bóng với pitchId đã gửi"}

IT03a → HTTP 400
{"status":400,"error":"Bad Request","message":"Sân bóng hiện không hoạt động hoặc đang bảo trì"}

IT03b → HTTP 502
{"status":502,"error":"Bad Gateway","message":"Dữ liệu đơn giá từ Pitch Service không hợp lệ"}

IT04 và IT05 → HTTP 503
{"status":503,"error":"Service Unavailable",
 "message":"Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!"}

IT06 lần 2 → HTTP 400
{"status":400,"error":"Bad Request","message":"Khung giờ này đã có người đặt"}

IT07 → HTTP 400
{"status":400,"error":"Bad Request","message":"endTime phải sau startTime"}
```

### 3.3. Chứng minh Consumer KHÔNG sập theo Provider (IT04)

Ngay sau khi dừng cả 2 instance Provider:

```
POST /api/v1/bookings             → HTTP 503   (lỗi được xử lý sạch sẽ, không phải 500)
GET  /api/v1/bookings/my-bookings → HTTP 200   (vẫn trả đủ 2 đơn đã đặt trước đó)
GET  /actuator/health             → HTTP 200   {"status":"UP"}
```

Booking Service vẫn `UP` và vẫn phục vụ các nghiệp vụ không phụ thuộc Provider — **không xảy ra
sụp đổ dây chuyền (Cascading Failure)**.

**IT04c — gọi lại sau khi Eureka đã xóa sạch bản ghi (chờ hết hạn lease):**

```
Sau ~145 giây: so instance UP cua PITCHOS-PITCH-SERVICE = 0
POST /api/v1/bookings → HTTP 503  (2,04s)
Log: Không gọi được Pitch Service (status Feign = -1):
     Connect timed out executing GET http://pitchos-pitch-service/api/v1/pitches/1
```

> 📌 **Ghi nhận trung thực về đường đi của lỗi:** ngay cả khi danh bạ Eureka đã rỗng, lần gọi này
> vẫn đi theo nhánh **timeout của Feign** (`Connect timed out`) chứ không rơi vào nhánh
> `IllegalStateException` của Spring Cloud LoadBalancer, vì bộ nhớ đệm danh sách instance phía
> Consumer còn giữ địa chỉ cũ và vẫn thử kết nối. Cả hai nhánh đều cho ra `503` đúng yêu cầu.
> Riêng nhánh "hết instance trong danh bạ" được bao phủ bằng bộ test tự động
> (`it04_providerSapHoanToan`, `tc05_pitchInstanceKhiProviderSap` — xem mục 4), nơi lớp
> `PitchGateway` chuyển `IllegalStateException` thành `503`. Đây là lớp phòng vệ dự phòng, không
> phải nhánh chạy thường xuyên.

### 3.4. Log liên dịch vụ thu được (trích nguyên văn log Consumer)

Hai dòng dưới đây là bằng chứng gọi **theo Service ID**, không còn URL cứng — đường dẫn trong log
là `http://pitchos-pitch-service/...` chứ không phải `http://localhost:8082/...`:

```
c.p.b.exception.GlobalExceptionHandler : Không gọi được Pitch Service (status Feign = -1):
    Read timed out executing GET http://pitchos-pitch-service/api/v1/pitches/1      ← IT05
c.p.b.exception.GlobalExceptionHandler : Không gọi được Pitch Service (status Feign = -1):
    Connect timed out executing GET http://pitchos-pitch-service/api/v1/pitches/1   ← IT04
```

Log của luồng thành công và luồng kiểm tra dữ liệu nhận về từ Provider:

```
c.p.booking.service.BookingService     : Pitch Service trả về sân 1: giá 300000.00 /giờ, trạng thái hoat_dong
c.p.booking.service.BookingService     : Pitch Service trả về sân 3: giá 250000.00 /giờ, trạng thái bao_tri
c.p.booking.service.BookingService     : Pitch Service trả về sân 4: giá 0.00 /giờ, trạng thái hoat_dong
c.p.b.exception.GlobalExceptionHandler : Dữ liệu nhận từ Pitch Service không hợp lệ:
                                         Dữ liệu đơn giá từ Pitch Service không hợp lệ
```

### 3.5. Bảng phân phối tải 20 request qua Consumer (số liệu thật)

Gửi 20 request `GET /api/v1/bookings/pitch-instance` liên tiếp:

| Instance Provider | Số request nhận được | Tỉ lệ |
|---|:-:|:-:|
| `pitch-instance-1` (cổng 8082) | **10** | 50% |
| `pitch-instance-2` (cổng 8084) | **10** | 50% |
| **Tổng** | **20** | **100%** |

Log Consumer cho thấy LoadBalancer luân phiên **tuyệt đối đều** theo Round-Robin:

```
LoadBalancer phân phối request sang instance Pitch: {instanceId=pitch-instance-2, port=8084}
LoadBalancer phân phối request sang instance Pitch: {instanceId=pitch-instance-1, port=8082}
LoadBalancer phân phối request sang instance Pitch: {instanceId=pitch-instance-2, port=8084}
LoadBalancer phân phối request sang instance Pitch: {instanceId=pitch-instance-1, port=8082}
...  (lặp đúng quy luật cho đủ 20 request)
```

### 3.6. Phần còn phải chụp ảnh khi hệ thống Docker hoàn thiện

Bảng dưới đây giữ nguyên để dán ảnh Postman khi `docker-compose.yml` chạy được. Mã trạng thái
mong đợi đã được chứng minh ở mục 3.2, nên bước này chỉ còn là thu ảnh minh chứng.

| Mã | Mã mong đợi | Ảnh minh chứng | Ghi chú khi chụp |
|:-:|:-:|---|---|
| IT01 | `201` | `docs/testing/img/it01.png` | Chụp kèm `totalPrice` |
| IT02 | `404` | `docs/testing/img/it02.png` | — |
| IT03a | `400` | `docs/testing/img/it03a.png` | Trên Docker dùng `pitchId = 4` |
| IT03b | `502` | `docs/testing/img/it03b.png` | Nhớ trả lại giá cũ sau khi chụp |
| IT04 | `503` | `docs/testing/img/it04.png` | Chụp kèm `docker compose ps` |
| IT05 | `503` | `docs/testing/img/it05.png` | Ghi rõ thời gian phản hồi ≈ 3s |
| IT06 | `201` → `400` | `docs/testing/img/it06.png` | — |
| IT07 | `400` | `docs/testing/img/it07.png` | — |

```bash
# Thu log 2 dịch vụ phục vụ Phần 6 của Hùng
docker compose logs --tail=50 pitchos-booking-service pitchos-pitch-service-1 > docs/testing/log-it01-it07.txt
```

## 4. KẾT QUẢ BỘ KIỂM THỬ TỰ ĐỘNG (ĐÃ CHẠY THỰC TẾ)

Toàn bộ 8 ca IT01–IT07 (và 2 ca TC03, TC05) đã được mã hóa thành bộ kiểm thử tự động trong dự án, chạy trên H2 in-memory, thay `PitchClient` bằng mock để mô phỏng mọi kiểu phản hồi của Provider. Bộ test này **không cần** Docker, Eureka hay MySQL.

### 4.1. Lệnh chạy

```bash
cd pitchos-booking-service
mvn test
```

### 4.2. Kết quả thực tế (chạy lại ngày 23/11/2026 trên JDK 21 + Maven 3.9.16)

```
[INFO] Tests run: 11, Failures: 0, Errors: 0, Skipped: 0 -- in com.pitchos.booking.IntegrationErrorHandlingTest
[INFO] Tests run:  3, Failures: 0, Errors: 0, Skipped: 0 -- in com.pitchos.booking.SecurityRbacTest
[INFO] Tests run:  3, Failures: 0, Errors: 0, Skipped: 0 -- in com.pitchos.booking.unit.CustomErrorDecoderTest
[INFO] Tests run: 17, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

### 4.3. Ánh xạ ca kiểm thử sang phương thức test

| Mã | Phương thức test | Cách mô phỏng Provider |
|:-:|---|---|
| IT01 | `it01_datSanHopLe` | Mock trả `pricePerHour = 300000`, `status = hoat_dong` |
| IT02 | `it02_sanKhongTonTai` | Mock ném `ResourceNotFoundException` (kết quả của `CustomErrorDecoder`) |
| IT03a | `it03a_donGiaKhongHopLe` | Mock trả `pricePerHour = 0` → `502` |
| IT03b | `it03b_donGiaNull` | Mock trả `pricePerHour = null` → `502` |
| IT03c | `it03c_sanBaoTri` | Mock trả `status = bao_tri` → `400` |
| IT04 | `it04_providerSapHoanToan` | Mock ném `IllegalStateException("No instances available...")`, sau đó kiểm tra `GET /my-bookings` vẫn `200` |
| IT05 | `it05_timeoutMang` | Mock ném `RetryableException` (`SocketTimeoutException`) → `503` |
| IT06 | `it06_guiLapYeuCau` | Gọi 2 lần cùng khung giờ → `201` rồi `400` |
| IT07 | `it07_duLieuDauVaoSai` | Kèm `verifyNoInteractions(pitchClient)` — chứng minh không gọi Provider |
| TC03 | `tc03_pitchInstance` | Mock `getInstanceInfo()` trả `{instanceId, port}` → `200` |
| TC05 | `tc05_pitchInstanceKhiProviderSap` | Mock ném `IllegalStateException` → `503` |
| RBAC | `SecurityRbacTest` | Không token → `401`; token `chusan` đặt sân → `403`; `/actuator/health` → `200 UP` |
| Decoder | `CustomErrorDecoderTest` | `404` của `getPitchById` → `404`; `404` của endpoint khác và `500` → `503` |

### 4.4. Giá trị của bộ test tự động

1. **Kiểm chứng được ngay** khi Eureka, Docker hoặc Pitch Service của nhóm chưa sẵn sàng.
2. **Bao phủ cả hai ca khó tạo bằng tay**: timeout mạng và hết instance trong danh bạ Eureka.
3. **Chống hồi quy**: mọi lần sửa mã nguồn về sau đều phải chạy qua 17 ca test này.
4. **Không thay thế** minh chứng Postman trên Docker — hai bộ bổ sung cho nhau: test tự động chứng minh *logic đúng*, Postman trên Docker chứng minh *hệ thống thật chạy đúng*.

---

## 5. KIỂM THỬ CÂN BẰNG TẢI QUA CONSUMER (PHỤC VỤ TC03)

1. Chạy request `TC03b - Xoa bo dem phan phoi tai` một lần để reset biến `lbStats`.
2. Mở **Collection Runner**, chỉ chọn request `TC03 - Can bang tai`, đặt **Iterations = 20**, nhấn Run.
3. Mở tab **Console** của Postman, dòng log cuối cùng in bảng phân phối, ví dụ:

```
Phan phoi tai sau 20 request: {"pitchos-pitch-service:8082":10,"pitchos-pitch-service:8084":10}
```

4. Chụp ảnh Console và điền vào bảng dưới đây (bảng tổng hợp đầy đủ thuộc Phần 4 của Hoàng):

| Instance Provider | Số request nhận được | Tỉ lệ |
|---|:-:|:-:|
| `pitchos-pitch-service:8082` |  |  |
| `pitchos-pitch-service:8084` |  |  |
| **Tổng** | **20** | **100%** |

> Nếu một instance nhận 0 request: kiểm tra Eureka Dashboard xem instance đó đã đăng ký chưa, hoặc chờ thêm 30 giây cho LoadBalancer cập nhật danh sách rồi chạy lại.

---

## 6. KẾT LUẬN

* Bộ kiểm thử tự động 17/17 ca **đã chạy thành công**, xác nhận logic tích hợp Consumer → Provider: gọi theo Service ID, kiểm tra dữ liệu nhận về, phân loại chính xác 5 nhóm lỗi (`400`, `404`, `502`, `503` do sập, `503` do timeout) và không sụp đổ dây chuyền khi Provider chết.
* Bộ minh chứng Postman trên Docker **cần chạy lại và chụp ảnh** sau khi Eureka Server, `docker-compose.yml` và endpoint `/api/v1/instance-info` của nhóm hoàn thành; các ô trong bảng mục 3 và mục 5 được giữ trống để điền số liệu thật, không ghi khống.
