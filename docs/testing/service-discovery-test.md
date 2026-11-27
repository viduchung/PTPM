# BIÊN BẢN KIỂM THỬ SERVICE DISCOVERY VÀ CÂN BẰNG TẢI
**Hệ thống:** PitchOS — Hệ thống quản lý đặt lịch sân bóng đá
**Bộ kiểm thử:** TC01 – TC06 (Service Registry & Load Balancing)
**Người thực hiện:** HOÀNG (Nhóm trưởng)
**Ngày thực hiện:** 27/11/2026
**Liên quan:** Mục 2.3 của đề bài (1,5 điểm) — phân tích tại `docs/kt2/PHAN_4_HOANG.md`

---

## 1. MÔI TRƯỜNG KIỂM THỬ

| Hạng mục | Giá trị |
|---|---|
| Hệ điều hành | Windows 11 |
| Docker Engine | 28.3.3 (Docker Desktop, Compose v2) |
| Java | OpenJDK 17 (LTS) — biên dịch bên trong image, không cài trên máy |
| Spring Boot | 3.2.5 |
| Spring Cloud | 2023.0.1 |
| Số container | 8 (3 MySQL + Registry + Auth + Pitch ×2 + Booking) |
| Lệnh khởi chạy | `docker compose up -d --build` |

**Cấu hình rút ngắn độ trễ phục vụ kiểm thử:**

| Tham số | Giá trị dùng khi kiểm thử | Mặc định Eureka |
|---|---|---|
| `eureka.instance.lease-renewal-interval-in-seconds` | 10 | 30 |
| `eureka.instance.lease-expiration-duration-in-seconds` | 30 | 90 |
| `eureka.server.eviction-interval-timer-in-ms` | 5000 | 60000 |
| `eureka.server.enable-self-preservation` | `false` | `true` |

**Trạng thái hệ thống trước khi kiểm thử** (`docker compose ps`): cả 8 container đều đạt `healthy`.

```
mysql-auth                 Up (healthy)
mysql-booking              Up (healthy)
mysql-pitch                Up (healthy)
pitchos-service-registry   Up (healthy)
pitchos-auth-service       Up (healthy)
pitchos-pitch-service-1    Up (healthy)
pitchos-pitch-service-2    Up (healthy)
pitchos-booking-service    Up (healthy)
```

---

## 2. BẢNG TỔNG HỢP KẾT QUẢ

| Mã | Tình huống | Kết quả mong đợi | Kết quả thực tế | Đạt |
|---|---|---|---|---|
| **TC01** | Đăng ký dịch vụ | Đủ 3 Service ID, Pitch có 2 instance | Đủ 3 Service ID, Pitch `UP (2)` ở cổng 8082 và 8084 | ✅ |
| **TC02** | Gọi qua Service ID | `201 Created`, không có URL tĩnh | `201 Created`, `totalPrice` tính từ đơn giá Provider | ✅ |
| **TC03** | Cân bằng tải 20 request | Cả 2 instance đều nhận request | 10 / 10, luân phiên tuyệt đối | ✅ |
| **TC04** | Dừng 1 instance | Vẫn đặt sân thành công | `201 Created`, 100% request dồn sang instance còn sống | ✅ |
| **TC05** | Dừng toàn bộ Provider | `503`, Consumer không sập | `503 Service Unavailable`, Booking vẫn `healthy` và `UP` | ✅ |
| **TC06** | Khởi động lại Provider | Tự đăng ký lại, không restart Consumer | Cả 2 instance trở lại sau 57,5 giây, không restart Consumer | ✅ |

**Kết luận chung:** cả sáu ca kiểm thử đều đạt. Hệ thống chứng minh được đầy đủ bốn tiêu chí của mục 2.3: Eureka Server hoạt động, các dịch vụ tự đăng ký, Consumer định vị Provider bằng Service ID, và hệ thống chịu được việc dừng rồi khởi động lại Provider.

---

## 3. CHI TIẾT TỪNG CA KIỂM THỬ

### TC01 — Đăng ký dịch vụ vào Eureka ✅ ĐẠT

**Mục tiêu:** xác minh mọi dịch vụ tự đăng ký vào Registry khi khởi động, và Pitch Service xuất hiện với đúng 2 instance.

**Lệnh thực hiện:**

```powershell
docker compose up -d --build
docker compose ps
curl http://localhost:8761/eureka/apps -H "Accept: application/json"
```

**Kết quả — danh bạ Eureka trả về HTTP 200:**

| Service ID | Instance ID | Trạng thái | Cổng |
|---|---|---|---|
| `PITCHOS-AUTH-SERVICE` | `pitchos-auth-service:8081` | `UP` | 8081 |
| `PITCHOS-BOOKING-SERVICE` | `pitchos-booking-service:8083` | `UP` | 8083 |
| `PITCHOS-PITCH-SERVICE` | `pitchos-pitch-service:pitch-instance-1` | `UP` | 8082 |
| `PITCHOS-PITCH-SERVICE` | `pitchos-pitch-service:pitch-instance-2` | `UP` | 8084 |

Tổng hợp: `PITCHOS-AUTH-SERVICE` 1 instance, `PITCHOS-BOOKING-SERVICE` 1 instance, **`PITCHOS-PITCH-SERVICE` 2 instance**.

**Nhận xét:** hai instance Pitch Service mang **cùng một Service ID** nhưng **hai Instance ID phân biệt** (`pitch-instance-1` và `pitch-instance-2`). Đây là điều kiện tiên quyết của cân bằng tải: nếu Instance ID trùng nhau, Eureka sẽ coi hai container là một, bản ghi sau ghi đè bản ghi trước, Dashboard chỉ hiện 1 instance và LoadBalancer không có gì để luân phiên.

**Ảnh minh chứng cần chụp:** `docs/architecture/eureka-dashboard-tc01.png` — Dashboard với dòng `PITCHOS-PITCH-SERVICE` hiển thị `UP (2)`.

---

### TC02 — Consumer gọi Provider qua Service ID ✅ ĐẠT

**Mục tiêu:** chứng minh Booking Service định vị Pitch Service bằng tên định danh, không bằng URL cố định. Đây là ca mang nhiều điểm nhất trong barem mục 2.3 (0,5 điểm).

**Điều kiện tiên quyết — kiểm tra mã nguồn:**

```java
// pitchos-booking-service/src/main/java/com/pitchos/booking/client/PitchClient.java:20
@FeignClient(name = "pitchos-pitch-service")   // KHÔNG có thuộc tính url
```

Đã xác minh: Feign Client **không còn** thuộc tính `url`. Cấu hình Booking Service không chứa bất kỳ địa chỉ nào trỏ tới Pitch Service.

**Các bước thực hiện:**

```powershell
# 1. Đăng nhập
curl -X POST http://localhost:8081/api/v1/auth/login -H "Content-Type: application/json" -d "{\"username\":\"user\",\"password\":\"123456\"}"

# 2. Đặt sân (thay <TOKEN>)
curl -X POST http://localhost:8083/api/v1/bookings -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"pitchId\":1,\"startTime\":\"2026-12-20T18:00:00\",\"endTime\":\"2026-12-20T20:00:00\"}"
```

**Kết quả:**

| Hạng mục | Kết quả |
|---|---|
| Feign Client còn thuộc tính `url`? | **Không** |
| Đăng nhập | `HTTP 200`, nhận `accessToken` dài 229 ký tự |
| Đặt sân | **`HTTP 201 Created`** |
| Nội dung phản hồi | `{"id":2, "userId":3, "pitchId":1, "startTime":"2026-12-20T18:00:00", "endTime":"2026-12-20T20:00:00", "totalPrice":600000.0, "status":"cho_duyet"}` |
| Đặt sân không tồn tại (`pitchId=9999`) | `HTTP 404` — *"Không tìm thấy sân bóng với pitchId đã gửi"* |

**Nhận xét:** trường `totalPrice: 600000` là bằng chứng mạnh nhất cho thấy lời gọi liên dịch vụ đã thực sự diễn ra. Booking Service không hề lưu đơn giá sân trong cơ sở dữ liệu của nó; giá trị này chỉ có được bằng cách gọi sang Pitch Service lấy đơn giá rồi nhân với thời lượng 2 giờ. Vì Feign Client không có URL cố định, lời gọi đó bắt buộc phải đi qua cơ chế Service Discovery.

Mã `404` khi đặt sân `9999` cũng cho thấy lỗi từ Provider được Consumer dịch lại đúng ngữ nghĩa thay vì để tràn thành `500`.

**Lỗi gặp phải trong quá trình chạy:** lần gửi đầu tiên trả về `400 Bad Request` — *"Dữ liệu gửi lên không đúng định dạng"*. Nguyên nhân là body gửi sai: `BookingRequest` yêu cầu `startTime` và `endTime` kiểu `LocalDateTime` dạng `2026-12-20T18:00:00`, không có trường `bookingDate` riêng. Đây là lỗi của phía gọi, không phải lỗi hệ thống.

**Ảnh minh chứng cần chụp:** `docs/architecture/postman-tc02-201.png`.

---

### TC03 — Cân bằng tải trên 2 instance ✅ ĐẠT

**Mục tiêu:** chứng minh Spring Cloud LoadBalancer phân bổ request cho cả hai instance Pitch Service.

**Lệnh thực hiện:** gửi 20 request liên tiếp vào `GET /api/v1/bookings/pitch-instance` (endpoint công khai, không cần token nên chạy được bằng Postman Collection Runner).

**Bảng phân phối 20 request:**

| Lần | Instance | Cổng | Lần | Instance | Cổng |
|---|---|---|---|---|---|
| 1 | `pitch-instance-2` | 8084 | 11 | `pitch-instance-2` | 8084 |
| 2 | `pitch-instance-1` | 8082 | 12 | `pitch-instance-1` | 8082 |
| 3 | `pitch-instance-2` | 8084 | 13 | `pitch-instance-2` | 8084 |
| 4 | `pitch-instance-1` | 8082 | 14 | `pitch-instance-1` | 8082 |
| 5 | `pitch-instance-2` | 8084 | 15 | `pitch-instance-2` | 8084 |
| 6 | `pitch-instance-1` | 8082 | 16 | `pitch-instance-1` | 8082 |
| 7 | `pitch-instance-2` | 8084 | 17 | `pitch-instance-2` | 8084 |
| 8 | `pitch-instance-1` | 8082 | 18 | `pitch-instance-1` | 8082 |
| 9 | `pitch-instance-2` | 8084 | 19 | `pitch-instance-2` | 8084 |
| 10 | `pitch-instance-1` | 8082 | 20 | `pitch-instance-1` | 8082 |

**Tổng hợp:**

| Instance | Cổng | Số request | Tỉ lệ |
|---|---|---|---|
| `pitch-instance-1` | 8082 | **10** | 50% |
| `pitch-instance-2` | 8084 | **10** | 50% |
| **Tổng** | | **20** | **100%** |

**Nhận xét:** kết quả đạt tỉ lệ 50/50 tuyệt đối, và quan trọng hơn là **thứ tự luân phiên hoàn hảo** `8084 → 8082 → 8084 → 8082...`. Đây đúng là hành vi của thuật toán Round Robin: biến đếm nguyên tử tăng 1 sau mỗi lời gọi và chọn instance theo phép chia lấy dư cho số instance đang `UP`.

Lưu ý quan trọng khi diễn giải: **tỉ lệ 50/50 không phải tiêu chí bắt buộc**. Tỉ lệ `11/9` hay `12/8` vẫn hợp lệ, vì biến đếm được khởi tạo bằng số ngẫu nhiên và cỡ mẫu 20 là nhỏ. Tiêu chí nghiệm thu đúng là **cả hai instance đều nhận được request**. Lần đo này ra 50/50 là do request được gửi tuần tự từ một luồng duy nhất, không có request đồng thời làm xáo trộn biến đếm. Mục 4 dưới đây trình bày một lần đo cho kết quả **20/0** và lý do tại sao kết quả đó cũng đúng.

**Ảnh minh chứng cần chụp:** `docs/architecture/postman-runner-tc03.png`.

---

### TC04 — Dừng 1 instance Provider ✅ ĐẠT

**Mục tiêu:** chứng minh hệ thống **suy giảm năng lực nhưng không mất chức năng** khi một instance Provider chết.

**Lệnh thực hiện:**

```powershell
docker compose stop pitchos-pitch-service-1
```

**Kết quả đo được:**

| Phép đo | Kết quả |
|---|---|
| Số instance `UP` trước khi dừng | 2 |
| Thời gian từ lúc dừng đến khi Eureka còn 1 instance | **18,2 giây** |
| Phân phối 10 request **ngay sau** khi dừng | 5 × cổng 8084 + **5 × lỗi `503`** |
| Phân phối 10 request **sau khi cache làm mới (+35 giây)** | **10 × cổng 8084**, không còn lỗi |
| Đặt sân khi chỉ còn 1 instance | **`HTTP 201 Created`** (`id=3`, `totalPrice=600000`) |

**Nhận xét — đây là phần cần phân tích kỹ nhất:**

Hiện tượng 5 trên 10 request bị `503` ngay sau khi dừng instance **không phải lỗi lập trình**. Nó là hệ quả trực tiếp của việc Consumer giữ **bản sao danh bạ trong bộ nhớ của chính nó** và chỉ làm mới mỗi 30 giây. Trong cửa sổ thời gian đó, LoadBalancer vẫn thấy 2 instance trong danh sách và vẫn luân phiên gửi một nửa số request sang instance đã chết — đúng tỉ lệ 50% quan sát được.

Sau 35 giây, cache được làm mới, danh sách chỉ còn 1 instance, và **100% request thành công**. Điều này xác nhận hệ thống tự phục hồi mà không cần can thiệp.

Lệnh đặt sân sau đó trả về `201 Created` chứng minh điều quan trọng nhất của ca kiểm thử này: **mất một nửa năng lực xử lý không làm mất chức năng nghiệp vụ**. Ở kiến trúc KT1 với một URL cố định trỏ vào cổng 8082, việc dừng container này sẽ làm chức năng đặt sân chết hoàn toàn.

**Ảnh minh chứng cần chụp:** `docs/architecture/eureka-dashboard-tc04.png` (Dashboard còn `UP (1)`) và `postman-tc04-201.png`.

---

### TC05 — Dừng toàn bộ Provider ✅ ĐẠT

**Mục tiêu:** xác minh Consumer xử lý lỗi gọn gàng khi không còn instance Provider nào, không sập dây chuyền.

**Lệnh thực hiện:**

```powershell
docker compose stop pitchos-pitch-service-2
```

**Kết quả đo được:**

| Phép đo | Kết quả |
|---|---|
| Thời gian từ lúc dừng đến khi Eureka còn 0 instance | **12,1 giây** |
| Mã trạng thái của lệnh đặt sân | **`HTTP 503 Service Unavailable`** |
| Thông điệp lỗi | *"Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!"* |
| Thời gian chờ đến khi nhận phản hồi lỗi | **2,0 giây** |
| Container Booking Service | `Up (healthy)` — vẫn chạy bình thường |
| `GET /actuator/health` của Booking Service | `HTTP 200` → `{"status":"UP"}` |

**Nhận xét — điểm cần làm rõ trong báo cáo:**

Booking Service trả `503` cho nghiệp vụ đặt sân nhưng `/actuator/health` vẫn báo `UP`. Đây **không phải mâu thuẫn**, mà chính là minh họa sống động cho sự phân biệt ba mức trạng thái:

| Mức | Trạng thái | Giải thích |
|---|---|---|
| **Trạng thái container** | `Up` | Tiến trình Java vẫn chạy, không thoát |
| **Sức khỏe ứng dụng** | `UP` | Bản thân Booking Service khỏe mạnh: kết nối được CSDL của nó, xử lý được request |
| **Khả năng nghiệp vụ** | **Không khả dụng** | Không đặt sân được vì phụ thuộc bên ngoài (Pitch Service) đã chết |

Ba mức này được phân tích lý thuyết ở Câu 1.4 (`CAU1_4_HUNG.md`). Kết quả đo ở đây là minh chứng thực nghiệm cho phần lý thuyết đó.

Thời gian chờ 2,0 giây cho thấy Consumer **không treo vô hạn**: nó phát hiện không có instance khả dụng và trả lỗi có nghĩa ngay, thay vì để request chờ đến hết timeout mặc định rồi ném `500`.

**Ảnh minh chứng cần chụp:** `docs/architecture/postman-tc05-503.png`, kèm ảnh `/actuator/health` vẫn `UP`.

---

### TC06 — Khởi động lại Provider ✅ ĐẠT

**Mục tiêu:** chứng minh hệ thống tự phục hồi, Provider tự đăng ký lại **mà không cần khởi động lại Consumer**.

**Lệnh thực hiện:**

```powershell
docker compose start pitchos-pitch-service-1 pitchos-pitch-service-2
```

**Kết quả đo được:**

| Phép đo | Kết quả |
|---|---|
| Thời gian đến khi cả 2 instance xuất hiện lại trên Eureka | **57,5 giây** |
| Đặt sân sau khi 2 instance đã đăng ký lại | **`HTTP 201 Created`** ngay lập tức |
| Có phải khởi động lại Booking Service không? | **KHÔNG** |
| Phân phối 20 request ngay sau khi phục hồi | **20 × cổng 8082**, 0 × cổng 8084 |

**Nhận xét:**

Thời gian 57,5 giây là tổng của thời gian khởi động ứng dụng Spring Boot trong container cộng với một chu kỳ Heartbeat. Trong suốt quá trình này, Booking Service **không hề được khởi động lại** — nó tự phát hiện Provider đã sống lại qua lần làm mới cache tiếp theo. Đây là minh chứng rõ nhất cho tính **lỏng liên kết** mà Service Discovery mang lại.

Kết quả **20/0** của lần đo phân phối ngay sau khi phục hồi cần được giải thích chứ không được bỏ qua: xem Mục 4.

---

## 4. PHÂN TÍCH BỔ SUNG: ĐỘ TRỄ CẬP NHẬT BẢNG ĐỊNH TUYẾN

Sau TC06, phép đo phân phối tải được lặp lại ba lần cách nhau 35 giây để quan sát quá trình Consumer cập nhật danh bạ:

| Thời điểm đo | Phân phối 20 request | Nhận xét |
|---|---|---|
| **Ngay sau khi Provider phục hồi** | `8082: 20` / `8084: 0` | Cache của Consumer mới chỉ thấy 1 instance |
| **Sau +35 giây** | `8082: 10` / `8084: 10` | Cache đã làm mới, luân phiên trở lại bình thường |
| **Sau +70 giây** | `8082: 10` / `8084: 10` | Ổn định |

Đây là **kết quả có giá trị nhất của toàn bộ đợt kiểm thử**, vì nó đo được trực tiếp hiện tượng mà lý thuyết mô tả.

Giải thích: Eureka Server đã biết có 2 instance ở giây thứ 57,5, nhưng Booking Service **không đọc trực tiếp từ Eureka Server mỗi lần gọi**. Nó dùng bản sao danh bạ trong bộ nhớ của chính nó, và bản sao đó chỉ được làm mới theo chu kỳ 30 giây. Trong khoảng giữa hai lần làm mới, LoadBalancer chỉ nhìn thấy instance nào có trong bản sao cũ, nên dồn toàn bộ 20 request sang cổng 8082.

**Tổng hợp các khoảng độ trễ đo được:**

| Tình huống | Độ trễ đo được | Cấu thành |
|---|---|---|
| Instance chết bị loại khỏi danh bạ Eureka | 12–18 giây | Hết hạn lease (30s) rút ngắn nhờ Heartbeat 10s, cộng chu kỳ quét 5s |
| Consumer ngừng gọi vào instance đã chết | ~30 giây | Chu kỳ làm mới cache của Eureka Client |
| Instance sống lại xuất hiện trên danh bạ | 57,5 giây | Thời gian khởi động Spring Boot cộng một chu kỳ Heartbeat |
| Consumer bắt đầu dùng instance mới | ~35 giây sau đó | Chu kỳ làm mới cache |

**Kết luận về mặt kiến trúc:** độ trễ này là **đặc tính cố hữu** của mô hình **AP** (Availability + Partition tolerance) mà Eureka theo đuổi. Eureka chấp nhận trả về dữ liệu *có thể hơi cũ* để đổi lấy việc luôn luôn trả lời được, thay vì khóa toàn hệ thống chờ đồng thuận như mô hình CP. Hệ quả là hệ thống phải được thiết kế để **chịu được** việc gọi vào một instance vừa chết, chứ không thể giả định danh bạ luôn chính xác tuyệt đối.

Trong môi trường sản xuất, khoảng trễ này được xử lý bằng cơ chế **thử lại (Retry)** và **ngắt mạch (Circuit Breaker)** ở phía Consumer — nằm ngoài phạm vi bài kiểm tra số 2 nhưng là hướng phát triển tự nhiên tiếp theo.

---

## 5. DANH MỤC ẢNH MINH CHỨNG CẦN CHỤP

| Tên file | Nội dung | Chú thích phải viết kèm |
|---|---|---|
| `docker-compose-ps.png` | `docker compose ps` với 8 container `healthy` | Phân biệt `Up` và `healthy` |
| `eureka-dashboard-tc01.png` | Dashboard đủ 3 Service ID, Pitch `UP (2)` | Chỉ rõ hai Instance ID khác nhau |
| `postman-tc02-201.png` | Postman đặt sân `201` qua Service ID | Nêu rõ `totalPrice` đến từ Provider |
| `postman-runner-tc03.png` | Postman Runner 20 request | Kèm bảng phân phối 10/10 |
| `eureka-dashboard-tc04.png` | Dashboard còn `UP (1)` | Ghi thời gian 18,2 giây |
| `postman-tc04-201.png` | Đặt sân vẫn `201` khi còn 1 instance | Minh chứng cân bằng tải có giá trị thực |
| `postman-tc05-503.png` | `503` khi dừng cả 2 instance | Kèm ảnh `/actuator/health` vẫn `UP` |

> **Yêu cầu của đề bài về ảnh minh chứng:** mỗi ảnh phải có chú thích và phân tích nội dung, kết quả. Không chèn ảnh chụp màn hình mà không phân tích.
