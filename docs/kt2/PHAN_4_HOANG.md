# PHẦN 4: SERVICE REGISTRY VÀ CÂN BẰNG TẢI
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)
**Sinh viên thực hiện:** HOÀNG (Nhóm trưởng)
**Mục tiêu điểm số:** 1,5 / 1,5 Điểm (Mục 2.3 — Microservices và Service Registry)
**Vùng mã nguồn:** `pitchos-service-registry/`, `pitchos-auth-service/`
**Kết quả kiểm thử chi tiết:** `docs/testing/service-discovery-test.md`

---

## 1. BAREM VÀ ĐỐI CHIẾU TRẠNG THÁI THỰC HIỆN

Mục 2.3 được chấm theo bốn tiêu chí. Bảng dưới đây đối chiếu từng tiêu chí với trạng thái hiện tại của mã nguồn:

| Tiêu chí chấm điểm | Điểm | Trạng thái | Minh chứng |
|---|---|---|---|
| Eureka Server hoạt động | 0,3 | ✅ **Đạt** | `pitchos-service-registry/`, Mục 2 |
| Các dịch vụ đăng ký thành công vào Registry | 0,3 | ✅ **Đạt** — 3 Service ID, Pitch có 2 instance | Mục 3, TC01 |
| **Consumer dùng Service Discovery để gọi Provider** | **0,5** | ✅ **Đạt** — `201 Created`, Feign không còn `url` | Mục 4, TC02 |
| Kiểm thử dừng và khởi động lại Provider | 0,4 | ✅ **Đạt** — TC04, TC05, TC06 | Mục 6, `service-discovery-test.md` |

Toàn bộ sáu ca kiểm thử TC01–TC06 đã chạy thật trên Docker ngày 27/11/2026 và đều đạt. Số liệu chi tiết trong `docs/testing/service-discovery-test.md`.

> **Lưu ý về điều kiện nghiệm thu quan trọng nhất:** tiêu chí 0,5 điểm lớn nhất của mục này **không phải** là việc Eureka Dashboard hiển thị danh sách dịch vụ, mà là việc Consumer thật sự tra cứu địa chỉ Provider qua Service ID. Nếu Booking Service vẫn giữ `@FeignClient(url = "...")` thì dù Dashboard hiện đủ dịch vụ, yêu cầu Service Discovery vẫn **chưa đạt**. Phép thử dứt khoát: xóa thuộc tính `url` khỏi Feign Client và hệ thống vẫn gọi được Provider.

---

## 2. CẤU HÌNH EUREKA SERVER

### 2.1. Lựa chọn phiên bản và lý do

Service Registry được hiện thực bằng **Netflix Eureka Server** thông qua Spring Cloud. Việc chọn phiên bản không tùy ý: Spring Boot và Spring Cloud có ma trận tương thích chặt chẽ, ghép sai sẽ gây lỗi khởi động do xung đột `spring-core` và `spring-context`.

| Thành phần | Phiên bản | Căn cứ lựa chọn |
|---|---|---|
| Java | 17 (LTS) | Phiên bản tối thiểu của Spring Boot 3.x |
| Spring Boot | 3.2.5 | Giữ nguyên phiên bản đã dùng ở KT1 cho toàn bộ 4 service |
| Spring Cloud | **2023.0.1** | Dòng 2023.0.x là dòng tương thích với Spring Boot 3.2.x |

Khai báo trong `pitchos-service-registry/pom.xml`:

```xml
<properties>
    <java.version>17</java.version>
    <spring-cloud.version>2023.0.1</spring-cloud.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Khối `<dependencyManagement>` với `<scope>import</scope>` là bắt buộc: nó nạp toàn bộ BOM (Bill of Materials) của Spring Cloud để các dependency con không cần ghi phiên bản riêng, nhờ đó mọi thành phần Spring Cloud trong dự án luôn cùng một dòng phiên bản.

### 2.2. Bật Service Registry bằng annotation

```java
@SpringBootApplication
@EnableEurekaServer
public class PitchosServiceRegistryApplication {
    public static void main(String[] args) {
        SpringApplication.run(PitchosServiceRegistryApplication.class, args);
    }
}
```

`@EnableEurekaServer` bật ba thành phần đồng thời: bảng đăng ký lưu trong bộ nhớ (in-memory registry), tập REST API để Eureka Client gửi đăng ký và Heartbeat, và trang Dashboard quản trị.

### 2.3. Phân tích từng tham số cấu hình

File `pitchos-service-registry/src/main/resources/application.properties`:

```properties
server.port=${REGISTRY_PORT:8761}
spring.application.name=pitchos-service-registry

eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false

eureka.server.enable-self-preservation=false
eureka.server.eviction-interval-timer-in-ms=5000

management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=never
```

| Tham số | Giá trị | Vì sao phải đặt như vậy |
|---|---|---|
| `server.port` | `8761` | Cổng mặc định theo quy ước của Netflix Eureka. Giữ đúng quy ước giúp người đọc mã nguồn nhận ra ngay vai trò của module |
| `register-with-eureka` | `false` | Eureka Server **tự nó cũng là một Eureka Client**. Nếu để mặc định `true`, nó sẽ cố đăng ký chính mình vào một Registry khác; hệ thống chỉ có một node duy nhất nên log sẽ tràn lỗi `Connect refused` khi khởi động |
| `fetch-registry` | `false` | Tương tự: không có node Registry nào khác để kéo bản sao danh bạ về. Tham số này chỉ bật khi triển khai Eureka theo cụm (peer-aware cluster) |
| `enable-self-preservation` | `false` | Xem phân tích ở Mục 2.4 |
| `eviction-interval-timer-in-ms` | `5000` | Mặc định 60 giây. Giảm xuống 5 giây để chu kỳ quét loại bỏ instance chết diễn ra nhanh, phục vụ kịch bản kiểm thử dừng Provider |
| `management.endpoints.web.exposure.include` | `health,info` | Chỉ mở hai endpoint cần thiết cho Docker healthcheck. Không mở toàn bộ vì `/actuator/env` sẽ phơi bày chuỗi kết nối CSDL và biến môi trường ra ngoài |
| `management.endpoint.health.show-details` | `never` | Chỉ trả về `{"status":"UP"}`, không liệt kê chi tiết thành phần nội bộ cho người gọi bên ngoài |

### 2.4. Phân tích riêng về chế độ Self-Preservation

Chế độ **Self-Preservation** là một cơ chế bảo vệ của Eureka. Nguyên lý: Eureka đếm số Heartbeat nhận được mỗi phút và so với số lượng kỳ vọng. Nếu tỉ lệ nhận được tụt dưới ngưỡng (mặc định khoảng 85%), Eureka kết luận rằng **mạng** đang có sự cố chứ không phải **các dịch vụ** đồng loạt chết, nên nó **ngừng loại bỏ bản ghi** và giữ nguyên toàn bộ danh bạ cũ.

Trong môi trường sản xuất với hàng trăm instance, đây là hành vi đúng đắn: thà giữ lại vài bản ghi cũ còn hơn xóa oan toàn bộ danh bạ vì một sự cố mạng tạm thời.

Nhưng ở môi trường học tập, hệ thống PitchOS chỉ có 4 instance. Khi kiểm thử dừng 1 instance Pitch Service, tỉ lệ Heartbeat tụt 25% — vượt ngưỡng ngay lập tức. Eureka chuyển sang chế độ tự bảo vệ, hiển thị cảnh báo đỏ trên Dashboard và **giữ instance đã chết trong danh bạ vô thời hạn**. Hệ quả là kịch bản kiểm thử "dừng một Provider rồi quan sát" không bao giờ cho kết quả đúng.

Vì vậy nhóm tắt chế độ này ở môi trường học tập, kèm ghi chú rõ: **đây là cấu hình dành riêng cho môi trường phát triển và kiểm thử, không phải cấu hình khuyến nghị cho môi trường sản xuất.**

### 2.5. Kết quả kiểm tra Eureka Server (đã xác minh)

Lần kiểm tra đầu chạy trực tiếp bằng JVM trên máy cá nhân (`java -jar target/pitchos-service-registry-0.0.1-SNAPSHOT.jar`). Lần kiểm thử chính thức chạy trong Docker cùng toàn hệ thống 8 container:

| Kiểm tra | Lệnh | Kết quả thực tế |
|---|---|---|
| Biên dịch và đóng gói | `mvn clean package -DskipTests` | `BUILD SUCCESS`, sinh file `pitchos-service-registry-0.0.1-SNAPSHOT.jar` |
| Sức khỏe ứng dụng | `curl http://localhost:8761/actuator/health` | `{"status":"UP"}` |
| Eureka Dashboard | `curl -o /dev/null -w "%{http_code}" http://localhost:8761/` | `200` |
| Danh bạ khi chưa có client | `curl http://localhost:8761/eureka/apps` | `<applications>` rỗng — đúng kỳ vọng, vì `register-with-eureka=false` nên Server không tự đăng ký chính nó |

**📷 Vị trí chèn ảnh 1:** Ảnh chụp Eureka Dashboard tại `http://localhost:8761` ngay sau khi khởi động, cho thấy mục *Instances currently registered with Eureka* đang trống và khối *General Info* hiển thị thông tin node.

*Chú thích ảnh cần viết kèm:* Dashboard trống ở thời điểm này là kết quả đúng chứ không phải lỗi, vì chưa có dịch vụ nào khởi động và bản thân Eureka Server không tự đăng ký. Ảnh này làm mốc so sánh với Ảnh 2 ở Mục 3.4.

---

## 3. CƠ CHẾ ĐĂNG KÝ CỦA EUREKA CLIENT

### 3.1. Thêm Eureka Client vào một dịch vụ

Mỗi dịch vụ nghiệp vụ cần hai dependency:

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

Từ Spring Cloud 2020 trở đi, **không cần** annotation `@EnableEurekaClient` hay `@EnableDiscoveryClient`: chỉ cần có starter trong classpath, Spring Boot tự động cấu hình (auto-configuration) và dịch vụ tự đăng ký khi khởi động.

### 3.2. Cấu hình Eureka Client trong Auth Service

```properties
eureka.client.service-url.defaultZone=${EUREKA_URL:http://localhost:8761/eureka/}
eureka.client.register-with-eureka=true
eureka.client.fetch-registry=true

eureka.instance.prefer-ip-address=true
eureka.instance.instance-id=${spring.application.name}:${server.port}

eureka.instance.lease-renewal-interval-in-seconds=10
eureka.instance.lease-expiration-duration-in-seconds=30
```

| Tham số | Vì sao cần thiết |
|---|---|
| `service-url.defaultZone` | Địa chỉ Registry. Dùng dạng `${EUREKA_URL:...}` để **cùng một file jar** chạy được cả trên máy thật (mặc định `localhost:8761`) và trong Docker (biến môi trường trỏ tới `http://pitchos-service-registry:8761/eureka/`). Đây là nguyên tắc *build một lần, chạy mọi môi trường* |
| `prefer-ip-address=true` | Mặc định Eureka đăng ký bằng hostname. Trong Docker, hostname của container là một chuỗi hash ngẫu nhiên mà các container khác **không phân giải được** → lời gọi thất bại dù danh bạ hiển thị đầy đủ. Đặt `true` buộc đăng ký bằng địa chỉ IP, luôn gọi được trong cùng network |
| `instance-id` có kèm cổng | Khi chạy 2 instance Pitch Service, nếu Instance ID trùng nhau thì Eureka coi chúng là **một** instance và bản ghi sau ghi đè bản ghi trước — mất hoàn toàn khả năng cân bằng tải. Gắn thêm `${server.port}` đảm bảo hai bản ghi phân biệt được |
| `lease-renewal` = 10s | Mặc định 30 giây. Giảm xuống 10 giây để thời gian phát hiện instance chết ngắn hơn, phù hợp kịch bản demo |
| `lease-expiration` = 30s | Mặc định 90 giây. Theo quy tắc kinh nghiệm, giá trị này nên bằng khoảng 3 lần chu kỳ Heartbeat để chịu được việc mất 2 nhịp liên tiếp do mạng chậm mà không bị loại oan |

### 3.3. Vòng đời một bản ghi đăng ký

```
  Dịch vụ khởi động
         │
         ▼
  ┌──────────────────────┐
  │ STARTING             │  Ứng dụng đang nạp context, chưa nhận request
  └──────────┬───────────┘
             │  POST /eureka/apps/{serviceId}   (gửi bản ghi đăng ký)
             ▼
  ┌──────────────────────┐
  │ UP                   │  Có trong danh bạ, Consumer tra cứu thấy
  └──────────┬───────────┘
             │  PUT /eureka/apps/{id}/{instanceId}  mỗi 10 giây (Heartbeat)
             │  ─── vòng lặp duy trì sự sống ───
             │
    ┌────────┴─────────┐
    │                  │
    ▼                  ▼
 Dừng êm            Dừng đột ngột
 (SIGTERM)          (kill -9 / mất điện)
    │                  │
    │ DELETE            │ Không gửi được gì
    │ hủy đăng ký       │
    ▼                  ▼
┌─────────┐    ┌─────────────────────────────────┐
│ Bị xóa  │    │ Hết hạn lease sau 30 giây       │
│ ngay    │    │ → chu kỳ eviction quét (5 giây) │
│         │    │ → bị xóa khỏi danh bạ           │
└─────────┘    └─────────────────────────────────┘
```

Sự khác biệt giữa **dừng êm** và **dừng đột ngột** là điểm cần nhấn mạnh khi trình bày: `docker compose stop` gửi `SIGTERM`, Spring Boot bắt được tín hiệu và kịp gọi hủy đăng ký nên bản ghi mất ngay; còn `docker kill` hoặc máy mất điện thì không kịp, và hệ thống phải chờ hết thời hạn lease. Chính khoảng chờ này tạo ra **độ trễ cập nhật bảng định tuyến** phân tích ở Mục 6.

### 3.4. Minh chứng các dịch vụ đã đăng ký

**📷 Vị trí chèn ảnh 2:** Ảnh chụp Eureka Dashboard sau khi `docker compose up -d` hoàn tất, cho thấy bảng *Instances currently registered with Eureka* có đủ ba Service ID, trong đó `PITCHOS-PITCH-SERVICE` hiển thị **2 instance** (cổng 8082 và 8084).

*Chú thích ảnh cần viết kèm:* Cần chỉ rõ cột `Availability Zones` của dòng `PITCHOS-PITCH-SERVICE` hiện số `2`, và cột `Status` hiện hai liên kết `UP (2)` tương ứng hai Instance ID khác nhau. Đây là điều kiện tiên quyết để có cân bằng tải: nếu Instance ID bị trùng, Dashboard chỉ hiện 1 instance và LoadBalancer không có gì để luân phiên.

**Kết quả đo thực tế ngày 27/11/2026** (TC01, danh bạ trả về `HTTP 200`):

| Service ID trên Dashboard | Instance ID | Trạng thái | Cổng |
|---|---|---|---|
| `PITCHOS-AUTH-SERVICE` | `pitchos-auth-service:8081` | `UP` | 8081 |
| `PITCHOS-BOOKING-SERVICE` | `pitchos-booking-service:8083` | `UP` | 8083 |
| `PITCHOS-PITCH-SERVICE` | `pitchos-pitch-service:pitch-instance-1` | `UP` | 8082 |
| `PITCHOS-PITCH-SERVICE` | `pitchos-pitch-service:pitch-instance-2` | `UP` | 8084 |

Hai instance Pitch Service mang cùng Service ID nhưng hai Instance ID phân biệt — đúng điều kiện cần của cân bằng tải.

Có thể kiểm tra bằng dòng lệnh thay cho Dashboard để đưa vào báo cáo dạng văn bản:

```powershell
curl http://localhost:8761/eureka/apps -H "Accept: application/json"
```

---

## 4. CƠ CHẾ SPRING CLOUD LOADBALANCER

### 4.1. Vị trí của LoadBalancer trong luồng gọi

Spring Cloud LoadBalancer là thư viện **cân bằng tải phía client** (Client-side Load Balancing). Khác biệt căn bản so với cân bằng tải phía server (như Nginx):

| | **Cân bằng tải phía server** (Nginx, HAProxy) | **Cân bằng tải phía client** (Spring Cloud LoadBalancer) |
|---|---|---|
| Vị trí đặt | Một thành phần riêng đứng trước các Provider | Một thư viện **nằm trong** tiến trình Consumer |
| Request đi qua | Consumer → Load Balancer → Provider (2 chặng) | Consumer → Provider (1 chặng) |
| Biết danh sách Provider từ đâu | Cấu hình thủ công trong file của Load Balancer | Tự động từ danh bạ Eureka |
| Điểm lỗi đơn (SPOF) | Có: Load Balancer sập thì mất hết | Không: mỗi Consumer tự quyết định |

Trong PitchOS, LoadBalancer được kích hoạt tự động khi `spring-cloud-starter-netflix-eureka-client` có trong classpath của Booking Service, và được OpenFeign sử dụng ngầm.

### 4.2. Thuật toán Round Robin

Thuật toán mặc định của Spring Cloud LoadBalancer là **Round Robin**: duy trì một biến đếm nguyên tử (atomic counter), mỗi lời gọi tăng biến đếm lên 1 và chọn instance theo công thức:

```
chỉ số instance được chọn = (giá trị biến đếm) % (số instance đang UP)
```

Với 2 instance Pitch Service, dãy lựa chọn lý thuyết là: `8082, 8084, 8082, 8084, ...`

### 4.3. Lưu ý quan trọng khi nhận xét kết quả đo

Có ba lý do khiến tỉ lệ phân phối thực tế **không phải lúc nào cũng đúng 50/50**, cần nêu rõ trong báo cáo để tránh bị cho là kết quả sai:

1. **Biến đếm khởi đầu ở giá trị bất kỳ:** biến đếm được khởi tạo bằng một số ngẫu nhiên để tránh mọi Consumer cùng dồn vào instance đầu tiên khi khởi động đồng thời. Do đó instance nào nhận request đầu tiên là không xác định trước.
2. **Cache danh bạ làm mới mỗi 30 giây:** nếu instance thứ 2 đăng ký sau khi Consumer đã tải bản sao danh bạ, thì trong tối đa 30 giây đầu Consumer chỉ thấy 1 instance và dồn toàn bộ request vào đó.
3. **Số lượng mẫu nhỏ:** với 20 request, tỉ lệ `11/9` hay `12/8` vẫn hoàn toàn hợp lệ.

Tiêu chí nghiệm thu đúng là: **cả hai instance đều phải nhận được ít nhất một request**, chứng minh LoadBalancer thật sự luân phiên. Không được đặt tiêu chí phải đúng 10/10.

### 4.4. Bảng số liệu 20 request

Cách thu số liệu: Booking Service cung cấp endpoint `GET /api/v1/bookings/pitch-instance` — endpoint này gọi xuống Pitch Service qua Service ID và trả về thông tin instance đã phục vụ (lấy từ endpoint `/api/v1/instance-info` của Pitch Service, do Linh bổ sung). Dùng **Postman Collection Runner** với số lần lặp 20, hoặc dòng lệnh:

```powershell
1..20 | ForEach-Object { (Invoke-RestMethod -Uri "http://localhost:8083/api/v1/bookings/pitch-instance" -Headers @{Authorization="Bearer $env:TOKEN"}).port }
```

**Kết quả đo thực tế ngày 27/11/2026** (TC03, 20 request tuần tự):

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

**Nhận xét:** cả hai instance đều nhận được request, kết luận Spring Cloud LoadBalancer hoạt động đúng. Đáng chú ý hơn con số 50/50 là **thứ tự luân phiên hoàn hảo** `8084 → 8082 → 8084 → 8082…`, đúng hành vi của thuật toán Round Robin: biến đếm nguyên tử tăng 1 sau mỗi lời gọi rồi chia lấy dư cho số instance đang `UP`. Lần đo này ra tỉ lệ tuyệt đối vì 20 request được gửi tuần tự từ một luồng duy nhất, không có request đồng thời làm xáo trộn biến đếm.

Tuy vậy, một lần đo khác ngay sau khi hai instance vừa khởi động lại (TC06) cho kết quả **20/0 — toàn bộ dồn vào cổng 8082**, rồi trở lại 10/10 sau 35 giây. Kết quả đó cũng đúng, và được phân tích ở Mục 6.3. Nó cho thấy vì sao tiêu chí nghiệm thu phải là *cả hai instance đều nhận được request* chứ không phải *tỉ lệ đúng 50/50*.

---

## 5. BẢO MẬT VÀ VẬN HÀNH LIÊN QUAN ĐẾN REGISTRY

### 5.1. Actuator: chỉ mở hai endpoint

Cả Service Registry và Auth Service đều cấu hình:

```properties
management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=never
```

Lý do không mở toàn bộ: `/actuator/env` liệt kê mọi biến môi trường, bao gồm `spring.datasource.password` và `jwt.secret`; `/actuator/beans` và `/actuator/mappings` phơi bày toàn bộ cấu trúc nội bộ cho người tấn công dò tìm. `show-details=never` khiến endpoint chỉ trả về `{"status":"UP"}` thay vì liệt kê tên database, dung lượng ổ đĩa và các thành phần nội bộ.

Trong `SecurityConfig` của Auth Service, hai endpoint này được mở `permitAll` vì Docker healthcheck và các công cụ giám sát gọi tới khi chưa có token:

```java
.requestMatchers("/actuator/health", "/actuator/health/**", "/actuator/info").permitAll()
```

Việc mở `permitAll` chỉ an toàn **vì** danh sách endpoint được expose đã bị giới hạn ở `health,info` trong `application.properties`. Hai cấu hình này phải đi cùng nhau.

### 5.2. Gỡ log in mật khẩu khỏi Auth Service

Trong `DataInitializer.java` của Auth Service tồn tại hai câu lệnh ghi log in thẳng mật khẩu mặc định ra console:

```java
// Mã nguồn cũ - đã gỡ bỏ
log.info("Khởi tạo thành công {} tài khoản mẫu (mật khẩu dùng chung: {})",
        initialUsers.size(), DEFAULT_PASSWORD);

log.warn("Tài khoản '{}' có chuỗi băm BCrypt không khớp mật khẩu mặc định '{}'. ...",
        username, DEFAULT_PASSWORD);
```

Đây là lỗi bảo mật thực sự, không phải lỗi hình thức: log của container được thu thập bởi `docker logs`, thường được chuyển tiếp sang hệ thống tập trung, lưu trữ dài hạn và chia sẻ cho nhiều người khi gỡ lỗi. Mật khẩu nằm trong log đồng nghĩa với việc nó bị sao chép ra nhiều nơi ngoài tầm kiểm soát.

Mã nguồn sau khi sửa chỉ ghi lại *sự kiện*, không ghi *giá trị bí mật*:

```java
log.info("Khởi tạo thành công {} tài khoản mẫu cho 3 vai trò (admin, chusan, user).",
        initialUsers.size());

log.warn("Tài khoản '{}' có chuỗi băm BCrypt không khớp mật khẩu mặc định. "
        + "Đang băm lại để phục vụ kiểm thử và demo.", username);
```

Mật khẩu mặc định của ba tài khoản mẫu được ghi trong `README.md` — nơi dành cho tài liệu hướng dẫn, không phải trong luồng log thời gian chạy.

### 5.3. Quản lý bí mật bằng biến môi trường

| Hạng mục | Trước | Sau |
|---|---|---|
| File `.env` thật (chứa mật khẩu MySQL và `JWT_SECRET`) | Bị commit lên Git | Đã gỡ khỏi Git bằng `git rm --cached .env`, thêm vào `.gitignore` |
| File khuôn mẫu | Không rõ ràng | Chỉ commit `.env.example`, có quy tắc `!.env.example` trong `.gitignore` để không bị loại oan |
| Bí mật trong Dockerfile | — | Không ghi bất kỳ bí mật nào vào Dockerfile; truyền qua `environment` của Docker Compose lúc chạy |

Lưu ý còn tồn đọng cần xử lý trước khi nộp: các file `application.properties` của ba dịch vụ hiện vẫn đặt giá trị `JWT_SECRET` thật làm **giá trị mặc định** trong biểu thức `${JWT_SECRET:404E63...}`. Gỡ `.env` khỏi Git nhưng vẫn để bí mật trong file cấu hình đã commit thì mục tiêu bảo mật chưa đạt trọn vẹn — cần thay bằng `${JWT_SECRET}` không có giá trị mặc định, để ứng dụng báo lỗi rõ ràng khi thiếu biến môi trường thay vì âm thầm dùng khóa đã bị lộ.

### 5.4. Dockerfile multi-stage không chạy quyền root

`Dockerfile` của Service Registry và Auth Service dùng hai giai đoạn:

```dockerfile
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /build
COPY pom.xml .
RUN mvn -B dependency:go-offline
COPY src ./src
RUN mvn -B clean package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=build /build/target/*.jar app.jar
RUN chown appuser:appgroup /app/app.jar
USER appuser
EXPOSE 8761
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

Ba quyết định thiết kế:

1. **Tách hai giai đoạn:** giai đoạn build cần Maven và toàn bộ JDK; giai đoạn chạy chỉ cần một file `.jar` và một JRE. Ảnh cuối cùng không mang theo Maven, mã nguồn và cache `.m2` — nhỏ hơn nhiều lần và giảm bề mặt tấn công.
2. **Copy `pom.xml` trước `src`:** Docker cache theo từng lớp. Khi chỉ sửa mã nguồn mà `pom.xml` không đổi, lớp tải dependency được tái sử dụng, rút ngắn thời gian build đáng kể.
3. **`USER appuser`:** mặc định container chạy bằng `root`. Nếu kẻ tấn công khai thác được lỗ hổng trong tiến trình Java, họ sẽ có quyền `root` trong container và có thêm cơ hội leo thang ra ngoài. Chạy bằng người dùng thường là nguyên tắc đặc quyền tối thiểu.

---

## 6. KIỂM THỬ DỪNG VÀ KHỞI ĐỘNG LẠI PROVIDER

Phần này chiếm 0,4 điểm trong barem mục 2.3. Kết quả chi tiết của bộ kiểm thử **TC01–TC06** được ghi trong `docs/testing/service-discovery-test.md`; mục này chỉ phân tích hiện tượng cần quan sát.

### 6.1. Ba kịch bản và hành vi kỳ vọng

| Kịch bản | Lệnh | Hành vi kỳ vọng | Giải thích cơ chế |
|---|---|---|---|
| **Dừng 1 trong 2 instance Provider** | `docker compose stop pitchos-pitch-service-1` | Đặt sân **vẫn thành công** `201 Created` | LoadBalancer còn 1 instance UP trong danh sách và dồn toàn bộ request sang đó. Hệ thống **suy giảm năng lực** nhưng **không mất chức năng** |
| **Dừng cả 2 instance Provider** | `docker compose stop pitchos-pitch-service-1 pitchos-pitch-service-2` | Trả về `503 Service Unavailable`, Booking Service **không sập** | Danh sách instance rỗng, LoadBalancer không có gì để chọn. Điều quan trọng là Consumer phải xử lý lỗi và trả mã lỗi có nghĩa, không được để lỗi tràn ra thành `500` hoặc treo vô hạn |
| **Khởi động lại Provider** | `docker compose start pitchos-pitch-service-1` | Sau một khoảng trễ, đặt sân thành công trở lại **mà không cần restart Consumer** | Instance tự đăng ký lại vào danh bạ; Consumer nhận instance mới ở lần làm mới cache tiếp theo |

### 6.2. Nhận xét về độ trễ cập nhật bảng định tuyến

Đây là nội dung đề bài yêu cầu nhận xét rõ. Khi một instance dừng, hệ thống **không** nhận biết ngay lập tức. Tổng độ trễ là tổng dồn của ba thành phần:

| Thành phần độ trễ | Mặc định Eureka | Cấu hình PitchOS |
|---|---|---|
| (a) Registry chờ hết thời hạn lease | 90 giây | **30 giây** |
| (b) Chu kỳ quét loại bỏ instance chết (eviction) | 60 giây | **5 giây** |
| (c) Consumer làm mới bản sao danh bạ | 30 giây | 30 giây |
| **Tổng xấu nhất** | **~180 giây** | **~65 giây** |

**Số liệu đo thực tế ngày 27/11/2026:**

| Phép đo | Giá trị đo được |
|---|---|
| Từ lúc `docker compose stop` một instance đến khi Eureka còn 1 instance | **18,2 giây** |
| Từ lúc dừng cả hai instance đến khi Eureka còn 0 instance | **12,1 giây** |
| Từ lúc `docker compose start` đến khi cả 2 instance đăng ký lại | **57,5 giây** |
| Từ lúc Eureka có đủ 2 instance đến khi Consumer dùng lại cả hai | **khoảng 35 giây** |
| Thời gian Consumer trả lỗi `503` khi không còn Provider | **2,0 giây** (không treo) |

### 6.3. Quan sát quan trọng nhất: cache của Consumer, không phải danh bạ của Server

Ngay sau khi dừng một instance, 10 request thử nghiệm cho kết quả **5 thành công trên cổng 8084 và 5 lỗi `503`** — đúng tỉ lệ 50%. Sau 35 giây, cùng phép đo cho **10/10 thành công**.

Chiều ngược lại cũng vậy. Sau khi hai instance khởi động lại, phép đo phân phối được lặp ba lần cách nhau 35 giây:

| Thời điểm đo | Phân phối 20 request |
|---|---|
| Ngay sau khi Provider phục hồi | `8082: 20` / `8084: 0` |
| Sau +35 giây | `8082: 10` / `8084: 10` |
| Sau +70 giây | `8082: 10` / `8084: 10` |

Hai phép đo này chỉ ra cùng một nguyên nhân: Booking Service **không đọc trực tiếp từ Eureka Server mỗi lần gọi**. Nó dùng bản sao danh bạ trong bộ nhớ của chính nó, làm mới theo chu kỳ 30 giây. Eureka Server đã biết sự thật mới từ giây thứ 12 hoặc 57, nhưng Consumer chỉ biết ở lần làm mới cache kế tiếp.

**Kết luận:** hiện tượng gọi vào instance đã chết và nhận lỗi **không phải lỗi lập trình**, mà là hệ quả trực tiếp của mô hình **AP** (Availability + Partition tolerance) mà Eureka theo đuổi: chấp nhận dữ liệu có thể hơi cũ để luôn trả lời được, thay vì khóa hệ thống chờ đồng thuận như mô hình CP. Hệ thống phải được thiết kế để **chịu được** điều này. Môi trường sản xuất bổ sung cơ chế **thử lại (Retry)** và **ngắt mạch (Circuit Breaker)** ở phía Consumer — ngoài phạm vi bài kiểm tra số 2 nhưng là hướng phát triển tiếp theo.

**Kết quả ba ca kiểm thử:**

| Ca | Kết quả thực tế |
|---|---|
| **TC04** dừng 1 instance | Đặt sân vẫn `201 Created` (`id=3`, `totalPrice=600000`) |
| **TC05** dừng cả 2 instance | `503 Service Unavailable` — *"Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!"*; container Booking vẫn `healthy`, `/actuator/health` vẫn trả `{"status":"UP"}` |
| **TC06** khởi động lại | Cả 2 instance đăng ký lại sau 57,5 giây, đặt sân `201 Created` ngay sau đó, **không phải restart Booking Service** |

Kết quả TC05 đáng chú ý: Booking Service trả `503` cho nghiệp vụ nhưng `/actuator/health` vẫn `UP`. Đây không phải mâu thuẫn mà là minh chứng thực nghiệm cho sự phân biệt **sức khỏe ứng dụng** (Booking vẫn khỏe) và **khả năng nghiệp vụ** (không đặt sân được vì phụ thuộc bên ngoài đã chết) — nội dung lý thuyết ở Câu 1.4.

**📷 Vị trí chèn ảnh 3:** Dashboard sau khi dừng instance 1, `PITCHOS-PITCH-SERVICE` còn `UP (1)`.

**📷 Vị trí chèn ảnh 4:** Postman đặt sân `201 Created` khi chỉ còn 1 instance.

---

## 7. ĐÁNH GIÁ VÀ HƯỚNG PHÁT TRIỂN

### 7.1. Những gì Service Registry đã mang lại cho PitchOS

| Trước (KT1) | Sau (KT2) |
|---|---|
| Địa chỉ Provider gắn cứng trong cấu hình Consumer | Consumer chỉ biết tên logic; địa chỉ do danh bạ cấp lúc chạy |
| Chỉ chạy được 1 instance Provider | Chạy 2 instance, phân bổ luân phiên tự động |
| Thêm instance phải sửa cấu hình và build lại | Thêm instance chỉ cần bật container mới |
| Provider chết thì chức năng chết theo | Provider chết 1 trong 2 thì hệ thống suy giảm năng lực, vẫn phục vụ |

### 7.2. Hạn chế còn lại của hệ thống

1. **Eureka Server là node đơn lẻ:** nếu nó sập, các lời gọi hiện có vẫn chạy nhờ cache nhưng không đăng ký được instance mới. Môi trường sản xuất cần triển khai Eureka theo cụm nhiều node (peer-aware).
2. **Chưa có API Gateway:** Client hiện gọi trực tiếp vào từng cổng dịch vụ. Hệ thống hoàn chỉnh cần một cổng duy nhất ở tầng biên.
3. **Chưa có Circuit Breaker:** khi Provider chậm, Consumer vẫn chờ hết timeout thay vì ngắt mạch sớm.
4. **Tắt Self-Preservation là cấu hình cho môi trường kiểm thử**, phải bật lại khi triển khai thật.
5. **`JWT_SECRET` vẫn còn làm giá trị mặc định trong các file `application.properties` đã commit** — cần xử lý trước khi nộp (xem Mục 5.3).
