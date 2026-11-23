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

## 3. BẢNG GHI KẾT QUẢ (ĐIỀN KHI CHẠY TRÊN DOCKER)

| Mã | Mã mong đợi | Mã thực tế | Thời gian phản hồi | Ảnh minh chứng | Nhận xét |
|:-:|:-:|:-:|:-:|---|---|
| IT01 | `201` |  |  | `docs/testing/img/it01.png` | Kiểm tra `totalPrice` = số giờ × đơn giá |
| IT02 | `404` |  |  | `docs/testing/img/it02.png` | Thông báo tiếng Việt rõ ràng |
| IT03a | `400` |  |  | `docs/testing/img/it03a.png` | Sân `bao_tri` |
| IT03b | `502` |  |  | `docs/testing/img/it03b.png` | Nhớ trả lại giá cũ sau khi chụp |
| IT04 | `503` |  |  | `docs/testing/img/it04.png` | Chụp kèm `docker compose ps` |
| IT04b | `200` |  |  | `docs/testing/img/it04b.png` | Chứng minh Booking không sập theo |
| IT05 | `503` |  |  | `docs/testing/img/it05.png` | Ghi rõ thời gian phản hồi ≈ 3s |
| IT06a | `201` |  |  | `docs/testing/img/it06a.png` | — |
| IT06b | `400` |  |  | `docs/testing/img/it06b.png` | "Khung giờ này đã có người đặt" |
| IT07 | `400` |  |  | `docs/testing/img/it07.png` | Chặn tại validation |

**Log cần thu kèm (phục vụ Phần 6 của Hùng — đối soát log liên dịch vụ):**

```bash
docker compose logs --tail=50 pitchos-booking-service pitchos-pitch-service-1 > docs/testing/log-it01-it07.txt
```

Trong log của Booking Service phải thấy dòng do Consumer ghi lại sau khi gọi Provider:

```
Pitch Service trả về sân 1: giá 300000.00 /giờ, trạng thái hoat_dong
```

Và khi Provider sập:

```
Không gọi được Pitch Service (status Feign = -1): ...
```

---

## 4. KẾT QUẢ BỘ KIỂM THỬ TỰ ĐỘNG (ĐÃ CHẠY THỰC TẾ)

Toàn bộ 8 ca IT01–IT07 (và 2 ca TC03, TC05) đã được mã hóa thành bộ kiểm thử tự động trong dự án, chạy trên H2 in-memory, thay `PitchClient` bằng mock để mô phỏng mọi kiểu phản hồi của Provider. Bộ test này **không cần** Docker, Eureka hay MySQL.

### 4.1. Lệnh chạy

```bash
cd pitchos-booking-service
mvn test
```

### 4.2. Kết quả thực tế (ngày 22/11/2026)

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
