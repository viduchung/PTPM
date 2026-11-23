# BIÊN BẢN KIỂM THỬ SERVICE DISCOVERY VÀ CÂN BẰNG TẢI
**Hệ thống:** PitchOS — Hệ thống quản lý đặt lịch sân bóng đá
**Bộ kiểm thử:** TC01 – TC06 (Service Registry & Load Balancing)
**Người thực hiện:** HOÀNG (Nhóm trưởng)
**Liên quan:** Mục 2.3 của đề bài (1,5 điểm) — phân tích tại `docs/kt2/PHAN_4_HOANG.md`

---

## 1. MÔI TRƯỜNG KIỂM THỬ

| Hạng mục | Giá trị |
|---|---|
| Hệ điều hành | Windows 11 |
| Docker | Docker Desktop (Compose v2) |
| Java | OpenJDK 17 (LTS) |
| Spring Boot | 3.2.5 |
| Spring Cloud | 2023.0.1 |
| Công cụ gửi request | Postman + Postman Collection Runner |
| Ngày thực hiện | *(điền ngày chạy thật)* |

**Cấu hình rút ngắn độ trễ phục vụ kiểm thử:**

| Tham số | Giá trị dùng khi kiểm thử | Mặc định Eureka |
|---|---|---|
| `eureka.instance.lease-renewal-interval-in-seconds` | 10 | 30 |
| `eureka.instance.lease-expiration-duration-in-seconds` | 30 | 90 |
| `eureka.server.eviction-interval-timer-in-ms` | 5000 | 60000 |
| `eureka.server.enable-self-preservation` | `false` | `true` |

---

## 2. TRẠNG THÁI THỰC HIỆN

| Mã | Tình huống | Trạng thái | Điều kiện còn thiếu |
|---|---|---|---|
| **TC01** | Đăng ký dịch vụ vào Eureka | ⏳ Một phần | Eureka Server đã xác minh chạy được; Pitch và Booking chưa có Eureka Client |
| **TC02** | Consumer gọi Provider qua Service ID | ⏳ Chưa chạy | Booking Service còn gọi bằng URL cố định (Nhật đang xử lý) |
| **TC03** | Cân bằng tải 20 request trên 2 instance | ⏳ Chưa chạy | Cần endpoint `/api/v1/instance-info` của Pitch Service (Linh) |
| **TC04** | Dừng 1 instance Provider | ⏳ Chưa chạy | Cần `docker-compose.yml` đủ 2 instance Pitch (Linh) |
| **TC05** | Dừng toàn bộ Provider | ⏳ Chưa chạy | Như TC04 |
| **TC06** | Khởi động lại Provider | ⏳ Chưa chạy | Như TC04 |

> Biên bản này được lập trước khi chạy, với đầy đủ lệnh thực thi và tiêu chí nghiệm thu cho từng ca, để khi hệ thống hội đủ điều kiện thì chỉ cần chạy và điền kết quả thật vào các ô `(điền)`. **Không ghi kết quả vào biên bản khi chưa thực sự chạy.**

---

## 3. KẾT QUẢ ĐÃ XÁC MINH: EUREKA SERVER

Phần này đã chạy thật trên máy cá nhân bằng JVM (chưa qua Docker, vì Docker Desktop lúc kiểm tra chưa bật).

| Bước | Lệnh | Kết quả thực tế | Đánh giá |
|---|---|---|---|
| 1 | `mvn clean package -DskipTests` trong `pitchos-service-registry/` | `BUILD SUCCESS`, sinh `pitchos-service-registry-0.0.1-SNAPSHOT.jar` | ✅ Đạt |
| 2 | `java -jar target/pitchos-service-registry-0.0.1-SNAPSHOT.jar` | Ứng dụng khởi động, lắng nghe cổng 8761 | ✅ Đạt |
| 3 | `curl http://localhost:8761/actuator/health` | `{"status":"UP"}` | ✅ Đạt |
| 4 | `curl -o /dev/null -w "%{http_code}" http://localhost:8761/` | `200` | ✅ Đạt — Dashboard phục vụ được |
| 5 | `curl http://localhost:8761/eureka/apps` | `<applications>` rỗng | ✅ Đạt — đúng kỳ vọng vì `register-with-eureka=false` |
| 6 | `mvn clean package -DskipTests` trong `pitchos-auth-service/` | `BUILD SUCCESS` sau khi thêm Eureka Client và Actuator | ✅ Đạt |

**Nhận xét bước 5:** danh bạ rỗng ở thời điểm này là kết quả **đúng**, không phải lỗi. Eureka Server được cấu hình `register-with-eureka=false` nên nó không tự đăng ký chính mình, và chưa có dịch vụ nghiệp vụ nào khởi động. Nếu danh bạ có bản ghi ngay khi mới bật Server thì mới là dấu hiệu cấu hình sai.

---

## 4. CHI TIẾT TỪNG CA KIỂM THỬ

### TC01 — Đăng ký dịch vụ vào Eureka

**Mục tiêu:** xác minh mọi dịch vụ tự đăng ký vào Registry khi khởi động, và Pitch Service xuất hiện với đúng 2 instance.

**Các bước thực hiện:**

```powershell
docker compose up -d
docker compose ps
```

Mở trình duyệt tới `http://localhost:8761`, hoặc kiểm tra bằng dòng lệnh:

```powershell
curl http://localhost:8761/eureka/apps -H "Accept: application/json"
```

**Tiêu chí nghiệm thu:** Dashboard hiện đủ 3 Service ID, trong đó `PITCHOS-PITCH-SERVICE` hiển thị `UP (2)` với hai Instance ID khác nhau.

**Kết quả:**

| Service ID | Instance ID | Trạng thái | Cổng | Đạt/Không |
|---|---|---|---|---|
| `PITCHOS-AUTH-SERVICE` | `pitchos-auth-service:8081` | *(điền)* | 8081 | *(điền)* |
| `PITCHOS-PITCH-SERVICE` | `pitchos-pitch-service:8082` | *(điền)* | 8082 | *(điền)* |
| `PITCHOS-PITCH-SERVICE` | `pitchos-pitch-service:8084` | *(điền)* | 8084 | *(điền)* |
| `PITCHOS-BOOKING-SERVICE` | `pitchos-booking-service:8083` | *(điền)* | 8083 | *(điền)* |

**Ảnh minh chứng:** `docs/architecture/eureka-dashboard-tc01.png`

**Lỗi thường gặp và cách xử lý:**

| Hiện tượng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| Pitch Service chỉ hiện 1 instance dù chạy 2 container | Hai instance có cùng Instance ID, bản ghi sau ghi đè bản ghi trước | Đặt `eureka.instance.instance-id=${spring.application.name}:${server.port}` |
| Dịch vụ không xuất hiện trên Dashboard | `EUREKA_URL` trỏ về `localhost` trong container | Đổi thành `http://pitchos-service-registry:8761/eureka/` |
| Dashboard hiện dịch vụ nhưng gọi vào thì `Connection refused` | Đăng ký bằng hostname container (chuỗi hash) mà container khác không phân giải được | Đặt `eureka.instance.prefer-ip-address=true` |

---

### TC02 — Consumer gọi Provider qua Service ID

**Mục tiêu:** chứng minh Booking Service định vị Pitch Service bằng tên định danh, **không** bằng URL cố định. Đây là ca kiểm thử mang nhiều điểm nhất trong barem mục 2.3 (0,5 điểm).

**Điều kiện tiên quyết — phải kiểm tra mã nguồn trước khi chạy:**

```powershell
# Lenh nay PHAI khong tra ve ket qua nao: khong con 'url =' trong Feign Client
Select-String -Path "pitchos-booking-service\src\main\java\**\*.java" -Pattern "@FeignClient" -Context 0,2
```

Feign Client phải ở dạng:

```java
@FeignClient(name = "pitchos-pitch-service")   // KHONG co thuoc tinh url
```

**Các bước thực hiện:**

```powershell
# 1. Dang nhap lay token
curl -X POST http://localhost:8081/api/v1/auth/login -H "Content-Type: application/json" -d "{\"username\":\"user\",\"password\":\"123456\"}"

# 2. Dat san (thay <TOKEN> bang token vua lay)
curl -X POST http://localhost:8083/api/v1/bookings -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"pitchId\":1,\"bookingDate\":\"2026-12-01\",\"startTime\":\"18:00\",\"endTime\":\"20:00\"}"
```

**Tiêu chí nghiệm thu:** trả về `201 Created` kèm thông tin đơn đặt sân, trong khi cấu hình Booking Service **không chứa** bất kỳ URL nào trỏ tới Pitch Service.

**Kết quả:**

| Hạng mục | Kết quả |
|---|---|
| Feign Client còn thuộc tính `url`? | *(điền: Có / Không)* |
| Mã trạng thái HTTP của lệnh đặt sân | *(điền)* |
| Nội dung phản hồi | *(điền)* |
| Đạt / Không đạt | *(điền)* |

---

### TC03 — Cân bằng tải trên 2 instance

**Mục tiêu:** chứng minh Spring Cloud LoadBalancer phân bổ request cho cả hai instance Pitch Service.

**Các bước thực hiện:** dùng Postman Collection Runner với endpoint `GET /api/v1/bookings/pitch-instance`, đặt số lần lặp là **20**. Hoặc bằng PowerShell:

```powershell
$token = "<TOKEN>"
1..20 | ForEach-Object {
    $r = Invoke-RestMethod -Uri "http://localhost:8083/api/v1/bookings/pitch-instance" -Headers @{Authorization="Bearer $token"}
    "$_`t$($r.port)"
}
```

**Tiêu chí nghiệm thu:** **cả hai instance đều nhận được ít nhất một request**. Không yêu cầu tỉ lệ đúng 50/50 — xem lý giải ở `PHAN_4_HOANG.md` Mục 4.3.

**Bảng phân phối 20 request:**

| Lần | Instance phục vụ | Lần | Instance phục vụ |
|---|---|---|---|
| 1 | *(điền)* | 11 | *(điền)* |
| 2 | *(điền)* | 12 | *(điền)* |
| 3 | *(điền)* | 13 | *(điền)* |
| 4 | *(điền)* | 14 | *(điền)* |
| 5 | *(điền)* | 15 | *(điền)* |
| 6 | *(điền)* | 16 | *(điền)* |
| 7 | *(điền)* | 17 | *(điền)* |
| 8 | *(điền)* | 18 | *(điền)* |
| 9 | *(điền)* | 19 | *(điền)* |
| 10 | *(điền)* | 20 | *(điền)* |

**Tổng hợp:**

| Instance | Số request | Tỉ lệ |
|---|---|---|
| `pitch-service-1` (8082) | *(điền)* | *(điền)* |
| `pitch-service-2` (8084) | *(điền)* | *(điền)* |
| **Tổng** | **20** | **100%** |

**Nhận xét cần viết:** nêu rõ cả hai instance đều nhận request nên LoadBalancer hoạt động đúng; giải thích độ lệch so với 50/50 bằng ba nguyên nhân (biến đếm khởi đầu ngẫu nhiên, cache danh bạ làm mới mỗi 30 giây, cỡ mẫu nhỏ). Nếu một instance nhận 0 request thì phải kiểm tra lại Instance ID có trùng không.

---

### TC04 — Dừng 1 instance Provider

**Mục tiêu:** chứng minh hệ thống **suy giảm năng lực nhưng không mất chức năng** khi một instance Provider chết.

**Các bước thực hiện:**

```powershell
docker compose stop pitchos-pitch-service-1
docker compose ps
# Doi va theo doi Dashboard tai http://localhost:8761
# Gui lai request dat san
```

**Tiêu chí nghiệm thu:** đặt sân vẫn trả `201 Created`; Dashboard chuyển `PITCHOS-PITCH-SERVICE` từ `UP (2)` sang `UP (1)`.

**Kết quả:**

| Phép đo | Kết quả |
|---|---|
| Trạng thái Dashboard ngay sau khi dừng | *(điền)* |
| Thời gian đến khi instance biến mất khỏi Dashboard | *(điền, giây)* |
| Mã trạng thái của lệnh đặt sân sau khi dừng | *(điền)* |
| Có request nào lỗi trong giai đoạn chuyển tiếp? | *(điền)* |
| Đạt / Không đạt | *(điền)* |

**Ảnh minh chứng:** `docs/architecture/eureka-dashboard-tc04.png` (Dashboard còn `UP (1)`) và ảnh Postman `201 Created`.

**Lưu ý khi diễn giải:** nếu trong khoảng mấy chục giây đầu có vài request lỗi `Connection refused`, đó là biểu hiện bình thường của độ trễ cập nhật danh bạ, **không phải lỗi lập trình**. Phải ghi lại hiện tượng này và giải thích bằng mô hình AP của Eureka, vì đây chính là nội dung đề bài yêu cầu nhận xét.

---

### TC05 — Dừng toàn bộ Provider

**Mục tiêu:** xác minh Consumer xử lý lỗi gọn gàng khi không còn instance Provider nào, không sập dây chuyền.

**Các bước thực hiện:**

```powershell
docker compose stop pitchos-pitch-service-1 pitchos-pitch-service-2
curl -X POST http://localhost:8083/api/v1/bookings -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d "{\"pitchId\":1,\"bookingDate\":\"2026-12-01\",\"startTime\":\"18:00\",\"endTime\":\"20:00\"}"
curl http://localhost:8083/actuator/health
```

**Tiêu chí nghiệm thu:** trả về `503 Service Unavailable` với thông điệp lỗi có nghĩa; container Booking Service **vẫn chạy**; `/actuator/health` của Booking Service vẫn trả `UP`.

**Kết quả:**

| Phép đo | Kết quả |
|---|---|
| Mã trạng thái của lệnh đặt sân | *(điền)* |
| Thông điệp lỗi trả về | *(điền)* |
| Container Booking còn chạy? | *(điền)* |
| `/actuator/health` của Booking | *(điền)* |
| Thời gian chờ đến khi có phản hồi lỗi | *(điền, giây)* |
| Đạt / Không đạt | *(điền)* |

**Điểm cần làm rõ:** Booking Service trả `503` nhưng `/actuator/health` vẫn `UP` — đây **không** phải nghịch lý. Đó chính là sự phân biệt giữa **sức khỏe ứng dụng** (bản thân Booking Service vẫn hoạt động tốt) và **khả năng thực hiện nghiệp vụ** (không đặt sân được vì phụ thuộc bên ngoài đã chết). Ba mức trạng thái này được phân tích ở Câu 1.4 (`CAU1_4_HUNG.md`).

---

### TC06 — Khởi động lại Provider

**Mục tiêu:** chứng minh hệ thống tự phục hồi, Provider tự đăng ký lại **mà không cần khởi động lại Consumer**.

**Các bước thực hiện:**

```powershell
docker compose start pitchos-pitch-service-1 pitchos-pitch-service-2
# Bam thoi gian, F5 Dashboard moi 5 giay
# Gui lai request dat san
```

**Tiêu chí nghiệm thu:** cả 2 instance xuất hiện lại trên Dashboard; đặt sân thành công `201 Created`; **không** chạy bất kỳ lệnh restart nào trên Booking Service.

**Kết quả:**

| Phép đo | Kết quả |
|---|---|
| Thời gian đến khi instance 1 xuất hiện lại trên Dashboard | *(điền, giây)* |
| Thời gian đến khi instance 2 xuất hiện lại | *(điền, giây)* |
| Thời gian đến khi đặt sân thành công trở lại | *(điền, giây)* |
| Có phải restart Booking Service? | *(điền: Có / Không — kỳ vọng: Không)* |
| Đạt / Không đạt | *(điền)* |

**Nhận xét cần viết:** khoảng thời gian từ lúc Provider sống lại đến lúc Consumer gọi được nó phản ánh chu kỳ làm mới cache danh bạ ở phía Consumer (mặc định 30 giây). Việc không cần restart Consumer là minh chứng rõ ràng nhất cho tính **lỏng liên kết** mà Service Discovery mang lại: ở KT1 với URL cố định, hiện tượng này cũng xảy ra tương tự, nhưng nếu Provider đổi cổng khi khởi động lại thì KT1 sẽ chết hẳn còn KT2 vẫn tự tìm ra.

---

## 5. BẢNG TỔNG HỢP KẾT QUẢ

| Mã | Tình huống | Kết quả mong đợi | Kết quả thực tế | Đạt |
|---|---|---|---|---|
| TC01 | Đăng ký dịch vụ | Đủ 3 Service ID, Pitch có 2 instance | *(điền)* | *(điền)* |
| TC02 | Gọi qua Service ID | `201 Created`, không có URL tĩnh | *(điền)* | *(điền)* |
| TC03 | Cân bằng tải | Cả 2 instance đều nhận request | *(điền)* | *(điền)* |
| TC04 | Dừng 1 instance | Vẫn đặt sân thành công | *(điền)* | *(điền)* |
| TC05 | Dừng toàn bộ | `503`, Consumer không sập | *(điền)* | *(điền)* |
| TC06 | Khởi động lại | Tự đăng ký lại, không restart Consumer | *(điền)* | *(điền)* |

**Kết luận chung:** *(viết sau khi chạy đủ 6 ca)*

---

## 6. DANH MỤC ẢNH MINH CHỨNG CẦN CHỤP

| Tên file | Nội dung | Chú thích phải viết kèm |
|---|---|---|
| `eureka-dashboard-empty.png` | Dashboard ngay sau khi bật Registry, danh bạ trống | Giải thích vì sao trống là đúng |
| `eureka-dashboard-tc01.png` | Dashboard đủ 3 Service ID, Pitch `UP (2)` | Chỉ rõ hai Instance ID khác nhau |
| `docker-compose-ps.png` | Kết quả `docker compose ps`, các container `healthy` | Phân biệt `Up` và `healthy` |
| `postman-tc02-201.png` | Postman đặt sân thành công qua Service ID | Nêu rõ cấu hình không còn URL tĩnh |
| `postman-runner-tc03.png` | Kết quả Postman Runner 20 request | Kèm bảng phân phối |
| `eureka-dashboard-tc04.png` | Dashboard còn `UP (1)` sau khi dừng instance 1 | Ghi thời gian từ lúc dừng đến lúc Dashboard cập nhật |
| `postman-tc04-201.png` | Đặt sân vẫn `201` khi chỉ còn 1 instance | Đây là minh chứng cân bằng tải có giá trị thực |
| `postman-tc05-503.png` | `503` khi dừng cả 2 instance | Kèm ảnh `/actuator/health` của Booking vẫn `UP` |

> **Yêu cầu của đề bài về ảnh minh chứng:** mỗi ảnh phải có chú thích và phân tích nội dung, kết quả. Không chèn ảnh chụp màn hình mà không phân tích.
