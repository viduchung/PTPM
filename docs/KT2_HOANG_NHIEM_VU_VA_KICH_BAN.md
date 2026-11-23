# 👑 HOÀNG – NHIỆM VỤ, HƯỚNG DẪN LÀM VÀ KỊCH BẢN QUAY VIDEO (BÀI KIỂM TRA SỐ 2)

> Đi kèm [KE_HOACH_KIEM_TRA_2.md](KE_HOACH_KIEM_TRA_2.md). File này chỉ dành cho Hoàng: **làm gì → làm thế nào → quay gì, nói gì**.
> Vai trò: **Trưởng nhóm · Service Registry (Eureka) · Auth Service · kiến trúc tổng thể · gộp báo cáo**.

---

# PHẦN A — HOÀNG CẦN LÀM GÌ

| # | Việc | Loại | Sản phẩm | Ngày |
|---|---|---|---|---|
| A1 | Đồng bộ nhánh `hoang`, xử lý thay đổi chưa commit | Git | nhánh sạch | 1 |
| A2 | **PR1**: tạo `pitchos-service-registry` (Eureka) + gỡ `.env` khỏi Git | Code | module mới, `.gitignore` | 1 |
| A3 | Họp nhóm 30': chốt chuẩn chung (mục 4.0 kế hoạch) + hợp đồng `instance-info` | Điều phối | biên bản ngắn trong Issue | 1 |
| A4 | **PR2**: Auth Service thành Eureka Client + Actuator + Dockerfile + sửa log lộ mật khẩu | Code | auth chạy trong Docker | 2 |
| A5 | Vẽ sơ đồ **trước/sau**, sơ đồ tích hợp, sơ đồ triển khai | Tài liệu | 3–4 file `.png` + `.drawio` | 2–3 |
| A6 | `deployment-design.md` + bảng mô tả dịch vụ | Tài liệu | `docs/architecture/deployment-design.md` | 3 |
| A7 | Review/merge PR của Linh, Nhật, Hùng theo thứ tự | Điều phối | `main` chạy được | 2–4 |
| A8 | README triển khai trên máy sạch, **tự thử bằng một bản clone mới** | Tài liệu | `README.md` | 4 |
| A9 | Chạy **TC01–TC06** + **bảng 20 request** trên Docker | Kiểm thử | `docs/testing/service-discovery-test.md` + ảnh | 5 |
| A10 | Viết **Câu 1.2**, **Phần 2**, **Phần 4** | Báo cáo | `docs/kt2/CAU1_2_HOANG.md`, `PHAN_2_HOANG.md`, `PHAN_4_HOANG.md` | 3–6 |
| A11 | Gộp báo cáo → `docs/report.docx` → `docs/report.pdf` | Báo cáo | báo cáo hoàn chỉnh | 6 |
| A12 | **Quay video cá nhân** (Phần C) | Demo | video 12–14' | 7 |

Điểm Hoàng “gánh” trực tiếp trên barem: **2.1 (1,0đ) + 2.3 (1,5đ) + Câu 1.2 (0,5đ)**, cộng phần README/gộp báo cáo ảnh hưởng 60% điểm báo cáo.

---

# PHẦN B — HƯỚNG DẪN LÀM TỪNG VIỆC

## B1. Đồng bộ nhánh (A1)

Máy Hoàng đang có thay đổi chưa commit ở `docs/BAO_CAO_CHUONG_1_LINH.md` và `docs/BAO_CAO_CHUONG_3_HUNG.md` (file của Linh và Hùng),
và nhánh `hoang` đang thiếu commit của Linh đã merge vào `main`.

1. Xem mình đã sửa gì: `git diff docs/BAO_CAO_CHUONG_1_LINH.md docs/BAO_CAO_CHUONG_3_HUNG.md`
2. Nếu cần giữ → commit riêng rồi báo Linh/Hùng. Nếu không cần → bỏ: `git restore docs/BAO_CAO_CHUONG_1_LINH.md docs/BAO_CAO_CHUONG_3_HUNG.md`
3. Đồng bộ:
```bash
git checkout main
git pull origin main
git checkout hoang
git merge main
```

## B2. PR1 — Eureka Server + gỡ `.env` (A2)

### B2.1. Tạo thư mục `pitchos-service-registry/` với 4 file

**`pitchos-service-registry/pom.xml`**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.5</version>
        <relativePath/>
    </parent>
    <groupId>com.pitchos</groupId>
    <artifactId>pitchos-service-registry</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>pitchos-service-registry</name>
    <description>PitchOS Service Registry (Eureka Server)</description>

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

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

**`pitchos-service-registry/src/main/java/com/pitchos/registry/PitchosServiceRegistryApplication.java`**
```java
package com.pitchos.registry;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

/** Service Registry của PitchOS: chỉ quản lý đăng ký/khám phá dịch vụ, không xử lý nghiệp vụ. */
@SpringBootApplication
@EnableEurekaServer
public class PitchosServiceRegistryApplication {
    public static void main(String[] args) {
        SpringApplication.run(PitchosServiceRegistryApplication.class, args);
    }
}
```

**`pitchos-service-registry/src/main/resources/application.properties`**
```properties
server.port=${EUREKA_PORT:8761}
spring.application.name=pitchos-service-registry

# Eureka Server không tự đăng ký và không lấy danh sách từ chính nó
eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false

# Môi trường demo: tắt self-preservation để instance chết bị loại nhanh, quét 5 giây/lần.
# (Production nên để bật — phải giải thích điều này trong báo cáo Phần 4)
eureka.server.enable-self-preservation=false
eureka.server.eviction-interval-timer-in-ms=5000

management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=never
```

**`pitchos-service-registry/Dockerfile`**
```dockerfile
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -B dependency:go-offline
COPY src ./src
RUN mvn -B clean package -DskipTests

FROM eclipse-temurin:17-jre
RUN useradd -r -u 1001 appuser
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
USER appuser
EXPOSE 8761
ENTRYPOINT ["java","-jar","app.jar"]
```
Kiểm tra image `eclipse-temurin:17-jre` có `curl` không (Linh cần cho healthcheck):
```bash
docker run --rm eclipse-temurin:17-jre sh -c "which curl wget"
```
Nếu không có, thêm `RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*` **trước** dòng `USER`, và báo cả nhóm sửa theo.

### B2.2. Chạy thử ở máy
```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21.0.11"
cd E:\DownCodeGit\PTPM\pitchos-service-registry
mvn spring-boot:run
```
Mở `http://localhost:8761` → thấy trang Eureka, mục *Instances currently registered* đang trống. Mở `http://localhost:8761/actuator/health` → `{"status":"UP"}`.
Thử Docker:
```bash
docker build -t pitchos-service-registry ./pitchos-service-registry
docker run --rm -p 8761:8761 pitchos-service-registry
```
→ chụp 2 ảnh (Dashboard trống, health UP) vào `docs/kt2/images/hoang/`.

### B2.3. Gỡ `.env` khỏi Git
1. Thêm dòng `.env` vào `.gitignore`.
2. `git rm --cached .env` (file vẫn còn trên máy, chỉ không còn được Git theo dõi).
3. ⚠️ **Báo cả nhóm TRƯỚC khi merge**: khi họ `git pull`, Git sẽ **xoá file `.env` trên máy họ**. Mỗi người sao lưu `.env` trước khi pull, hoặc tạo lại bằng cách copy `.env.example` → `.env`.
4. `JWT_SECRET` cũ vẫn nằm trong lịch sử Git → ghi vào báo cáo Phần 7 (hạn chế): môi trường thật phải đổi secret mới.

### B2.4. Commit + PR
```bash
git add pitchos-service-registry .gitignore
git rm --cached .env
git commit -m "[KT2][registry] Tạo Eureka Server, gỡ .env khỏi Git"
git push origin hoang
```
Mở PR `hoang → main` trên GitHub, ghi rõ trong mô tả việc `.env` bị xoá khi pull.

## B3. PR2 — Auth Service (A4)

Sửa **chỉ trong `pitchos-auth-service/`**:

1. **`pom.xml`**: thêm vào `<properties>` dòng `<spring-cloud.version>2023.0.1</spring-cloud.version>`; thêm 2 dependency
   `spring-cloud-starter-netflix-eureka-client` và `spring-boot-starter-actuator`; thêm khối `<dependencyManagement>` y như ở pom Eureka.
2. **`src/main/resources/application.properties`** — thêm cuối file:
```properties
# Eureka Client
eureka.client.service-url.defaultZone=${EUREKA_URL:http://localhost:8761/eureka/}
eureka.instance.prefer-ip-address=true
eureka.instance.instance-id=${spring.application.name}:${INSTANCE_ID:${server.port}}

# Actuator
management.endpoints.web.exposure.include=health,info
management.endpoint.health.show-details=never
```
3. **`SecurityConfig.java`** — trong khối `requestMatchers(... "/error").permitAll()` thêm `"/actuator/health"`, `"/actuator/info"`.
4. **`DataInitializer.java`** — bỏ mật khẩu khỏi 2 dòng log (TH8 trừ điểm nếu log lộ dữ liệu nhạy cảm):
```java
log.info("Khởi tạo thành công {} tài khoản mẫu cho 3 vai trò", initialUsers.size());
```
```java
log.warn("Tài khoản '{}' có chuỗi băm BCrypt không khớp mật khẩu mặc định. "
        + "Đang băm lại để phục vụ kiểm thử và demo.", username);
```
5. **`Dockerfile`** — giống registry, đổi `EXPOSE 8081`.
6. Xoá file thừa `pitchos-auth-service/application.properties` (bản ở gốc thư mục service).
7. Chạy thử: bật Eureka → bật Auth → Dashboard có `PITCHOS-AUTH-SERVICE` → `http://localhost:8081/actuator/health` = UP → đăng nhập bằng Postman vẫn 200 (đảm bảo không làm hỏng JWT).
8. Commit `[KT2][auth] Eureka client, Actuator, Dockerfile, bỏ mật khẩu khỏi log` → PR.

## B4. Họp chốt chuẩn chung (A3)

Chốt và ghi vào 1 Issue “Chuẩn chung KT2”:
- Bảng Service ID / container / port (mục 3 kế hoạch).
- Khối properties mục 4.0(b) + Dockerfile mục 4.0(d).
- Hợp đồng `GET /api/v1/instance-info` → `{ "serviceName", "instanceId", "port" }` (Linh làm, Nhật gọi).
- Endpoint của Booking để test cân bằng tải: `GET /api/v1/bookings/pitch-instance` (Nhật làm), cần token `user`.
- **Đề xuất thêm để demo nhanh** (Eureka mặc định mất 30–90 giây mới cập nhật):
  - ở mọi client: `eureka.instance.lease-renewal-interval-in-seconds=5`, `eureka.instance.lease-expiration-duration-in-seconds=15`
  - ở Booking: `eureka.client.registry-fetch-interval-seconds=5`, `spring.cloud.loadbalancer.cache.ttl=5s`
  - Ghi trong báo cáo: đây là cấu hình cho môi trường demo, giá trị mặc định lớn hơn để giảm tải cho Registry.

## B5. Sơ đồ (A5)

Vẽ bằng draw.io (app.diagrams.net), lưu cả `.drawio` và `.png` vào `docs/architecture/`:

| File | Nội dung bắt buộc |
|---|---|
| `architecture-before.png` | Sau TH6/KT1: 3 service chạy tay bằng `mvn spring-boot:run`, Booking gọi Pitch bằng **URL cứng `http://localhost:8082`**, 1 MySQL |
| `architecture-after.png` = `integration-architecture.png` | Eureka ở giữa, mũi tên “đăng ký/heartbeat” từ 4 service, Booking → Pitch ghi “OpenFeign + LoadBalancer, Service ID `pitchos-pitch-service`”, 2 instance Pitch, mỗi service nối DB riêng |
| `deployment-architecture.png` | Khung lớn “Docker host” → khung “pitchos-network” → các container (ghi tên container + port nội bộ), 3 container MySQL kèm biểu tượng volume, port map ra host (8761, 8081–8084), file `.env` cấp biến môi trường |

Mẹo: dùng 3 màu cố định — xanh dương cho service nghiệp vụ, cam cho Eureka, xám cho DB; mũi tên nét liền = gọi API, nét đứt = đăng ký/heartbeat.

## B6. `deployment-design.md` + bảng mô tả dịch vụ (A6)

| Service ID | Trách nhiệm | API chính | Database | Consumer (ai gọi nó) | Provider (nó gọi ai) | Số instance |
|---|---|---|---|---|---|---|
| `pitchos-service-registry` | Đăng ký, khám phá dịch vụ | Dashboard `/` | – | tất cả service | – | 1 |
| `pitchos-auth-service` | Đăng ký, đăng nhập, phát JWT, RBAC | `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/users/me`, `GET /api/v1/users/{id}`, `GET /api/v1/users` | `pitchos_user_db` (`mysql-auth`) | Client | – | 1 |
| `pitchos-pitch-service` | Quản lý sân, giá, trạng thái | `GET /api/v1/pitches`, `GET /api/v1/pitches/{id}`, `POST /api/v1/pitches`, `PATCH /api/v1/pitches/{id}/status`, `GET /api/v1/instance-info` | `pitchos_pitch_db` (`mysql-pitch`, dùng chung cho 2 instance) | Booking, Client | – | **2** |
| `pitchos-booking-service` | Đặt sân, duyệt đơn | `POST /api/v1/bookings`, `GET /api/v1/bookings/my-bookings`, `PATCH /api/v1/bookings/{id}/status`, `GET /api/v1/bookings/pitch-instance` | `pitchos_booking_db` (`mysql-booking`) | Client | **Pitch** | 1 |

Thêm 3 đoạn giải thích ngắn bên dưới bảng:
- **Vì sao Pitch chạy 2 instance**: là Provider được gọi nhiều nhất (mỗi lần đặt sân), không giữ trạng thái trong RAM, 2 instance dùng chung 1 DB nên dữ liệu nhất quán.
- **Vì sao Booking chỉ 1 instance**: khoá chống đặt trùng (`synchronized`) nằm trong bộ nhớ một tiến trình; chạy 2 instance sẽ có thể đặt trùng → cần khoá ở DB trước khi scale (thầy: “cân bằng tải ≠ nhất quán giao dịch”).
- **Vì sao không có API Gateway**: không bắt buộc ở TH7/TH8/KT2; đưa vào hướng phát triển.

## B7. README (A8)

Cấu trúc README gốc (viết cho người chưa từng thấy dự án):
1. Giới thiệu 3 dòng + ảnh `deployment-architecture.png`.
2. Yêu cầu: Docker Desktop, RAM ≥ 8GB, cổng 8081–8084, 8761 đang trống. **Không cần cài Java/Maven** (image tự build).
3. Các bước: `git clone` → `copy .env.example .env` → `docker compose up -d --build` → chờ `docker compose ps` báo healthy (2–5 phút lần đầu).
4. Bảng địa chỉ: Eureka `http://localhost:8761`, Swagger auth/pitch, health của từng service.
5. Tài khoản mẫu: tên đăng nhập `admin`, `chusan`, `user` (mật khẩu ghi trong `DataInitializer`, chỉ dùng để demo).
6. Lệnh vận hành: logs, stop, start, restart, down; **cảnh báo `down -v` xoá dữ liệu**.
7. Import `postman/collection.json` và chạy theo thứ tự folder.
8. Xử lý lỗi thường gặp: cổng 3306/8081 bị chiếm, service chưa lên Eureka (chờ), hết RAM.

**Bắt buộc tự thử**: clone repo vào một thư mục mới (vd. `E:\test-clone`), làm đúng README từ đầu. Chạy được mới coi là xong (thầy sẽ làm đúng như vậy).

## B8. Kiểm thử TC01–TC06 + bảng 20 request (A9)

Làm sau khi PR của Linh (compose) và Nhật (`pitch-instance`) đã merge. Tên container dưới đây theo kế hoạch; nếu Linh đặt khác thì đổi theo.

**Lấy token và gửi 20 request (PowerShell)** — kết quả in ra đúng dạng bảng:
```powershell
$pw = Read-Host "Mat khau tai khoan user mau"
$body = @{ username = "user"; password = $pw } | ConvertTo-Json
$token = (Invoke-RestMethod -Method Post -Uri http://localhost:8081/api/v1/auth/login -ContentType "application/json" -Body $body).accessToken
$h = @{ Authorization = "Bearer $token" }
$rows = foreach ($i in 1..20) {
  try {
    $r = Invoke-RestMethod -Uri http://localhost:8083/api/v1/bookings/pitch-instance -Headers $h
    [pscustomobject]@{ Lan = $i; Instance = $r.instanceId; KetQua = "Thanh cong" }
  } catch {
    [pscustomobject]@{ Lan = $i; Instance = "-"; KetQua = "Loi $($_.Exception.Response.StatusCode.value__)" }
  }
}
$rows | Format-Table
$rows | Group-Object Instance | Select-Object Name, Count
```
(Có thể làm tương tự bằng Postman Runner với 20 iterations.)

| Mã | Thao tác | Kết quả mong đợi | Minh chứng cần chụp |
|---|---|---|---|
| TC01 | `docker compose up -d` | Eureka hiện AUTH, BOOKING, PITCH (2 instance: `pitch-service-1`, `pitch-service-2`) | Dashboard + `docker compose ps` |
| TC02 | Đặt sân qua Booking | 201, `totalPrice` đúng | Postman + code `@FeignClient(name = "pitchos-pitch-service")` không có `url` + log Booking |
| TC03 | Chạy script 20 request | Cả 2 instance đều xuất hiện | Bảng kết quả + `Group-Object` + log 2 container Pitch |
| TC04 | `docker compose kill pitchos-pitch-service-1` (mô phỏng sập đột ngột), chạy lại script | Instance 2 phục vụ; **ghi lại số request lỗi lúc đầu** do Eureka/LoadBalancer chưa cập nhật | Bảng kết quả + Dashboard |
| TC05 | `docker compose stop pitchos-pitch-service-2` (lúc này cả 2 đã dừng), đặt sân | 503 “Dịch vụ quản lý sân hiện không khả dụng…”, trả về nhanh, không treo | Postman + log `Không gọi được Pitch Service` |
| TC06 | `docker compose start pitchos-pitch-service-1 pitchos-pitch-service-2`, chờ ~15–30s | 2 instance đăng ký lại, đặt sân thành công | Dashboard + Postman |
| TC07 *(mở rộng)* | `docker compose stop pitchos-service-registry`, đặt sân | Vẫn đặt được vì Booking còn bản sao danh sách instance trong bộ nhớ; service mới thì không đăng ký được → **chạy thử trước, ghi đúng kết quả thật** | Postman + giải thích |

Phân biệt khi viết báo cáo: `docker compose stop` → service tắt êm, **tự huỷ đăng ký** nên biến khỏi Dashboard ngay;
`docker compose kill` → tắt đột ngột, **không kịp huỷ đăng ký**, Eureka chỉ loại sau khi hết hạn heartbeat → đây là “độ trễ” thầy nói ở TH7.

## B9. Báo cáo (A10, A11)

**Câu 1.2 — bản nháp đủ ý (chỉnh lời văn của mình):**
- *Service Registry* là “danh bạ” của hệ thống: mỗi instance khi khởi động gửi tên dịch vụ, địa chỉ, cổng tới Registry, sau đó gửi heartbeat định kỳ; instance ngừng heartbeat quá hạn sẽ bị loại. Danh bạ vì vậy luôn **có độ trễ** so với thực tế.
- *Service Discovery* là việc Consumer tra danh bạ theo **tên dịch vụ** để lấy danh sách instance còn sống, rồi LoadBalancer chọn một instance để gửi request. Trong PitchOS: Booking tra `pitchos-pitch-service`, nhận 2 instance, LoadBalancer luân phiên chọn.
- *Eureka Server vs API Gateway*:

| | Eureka Server | API Gateway |
|---|---|---|
| Câu hỏi trả lời | “Dịch vụ X đang ở đâu?” | “Request của client nên đi vào dịch vụ nào?” |
| Ai dùng | Các service (Consumer) | Client bên ngoài |
| Request nghiệp vụ có đi qua không | **Không** — chỉ trả địa chỉ | **Có** — mọi request đi qua |
| Việc thường làm | Đăng ký, heartbeat, danh sách instance | Định tuyến, xác thực tập trung, giới hạn tốc độ, CORS |
| PitchOS | Có (bắt buộc) | Chưa có (hướng phát triển) |

  Hai thành phần bổ trợ nhau: Gateway thường cũng hỏi Eureka để biết định tuyến tới đâu.
- *Vì sao gọi bằng Service ID*: địa chỉ IP container thay đổi mỗi lần tạo lại; một dịch vụ có thể có nhiều instance; URL cứng buộc phải sửa và build lại Consumer mỗi khi Provider đổi cổng/chuyển máy; gọi bằng tên thì thêm/bớt instance không phải sửa Consumer và có cân bằng tải.
- *Lưu ý thầy nhấn mạnh*: tìm thấy dịch vụ không có nghĩa được phép gọi (vẫn cần JWT); dịch vụ có trên Dashboard chưa chứng minh nó phục vụ được (cần health check và request thật).

**Phần 2 — Thiết kế kiến trúc:** 2.1 Kế thừa từ KT1 (phân rã dịch vụ, SRP, database-per-service — chép từ Ch1 §1.3 và Ch3 §3.1) → 2.2 Kiến trúc trước KT2 (sơ đồ before, nêu hạn chế: URL cứng, chạy tay, 1 instance) → 2.3 Kiến trúc sau (sơ đồ after + triển khai) → 2.4 Bảng mô tả dịch vụ (B6) → 2.5 Consumer/Provider và quy trình đặt sân.

**Phần 4 — Service Registry:** 4.1 Thiết kế Eureka Server (code, cấu hình, lý do tắt self-preservation khi demo) → 4.2 Đăng ký các service (cấu hình client, `instance-id`, ảnh Dashboard) → 4.3 Consumer gọi bằng Service ID (code Feign trước/sau, LoadBalancer) → 4.4 Hai instance và phân phối request (bảng 20 request + nhận xét tỉ lệ) → 4.5 Kiểm thử TC01–TC07 → 4.6 Nhận xét: độ trễ cập nhật, stop vs kill, giới hạn 1 Eureka.

**Gộp báo cáo (ngày 6):** thứ tự Bìa → Mục lục → Câu 1 (1.1→1.4) → Phần 1→7 → Phụ lục (link GitHub, Postman). Kiểm tra: mỗi ảnh có số hình + chú thích + 1–2 câu phân tích; mỗi phần có mục “Kế thừa” và “Bổ sung cho KT2”.

---

# PHẦN C — KỊCH BẢN QUAY VIDEO (12–14 phút)

> Đề KT2 bắt mọi thành viên trình diễn đủ **8 nội dung** (mục 3.3). Hoàng làm đủ 8, **nói sâu ở bước 3 (Eureka) và bước 7 (dừng/khởi động lại Provider)** vì đó là phần mình phụ trách.
> Mỗi cảnh: **🗣️ LỜI NÓI** (thuộc ý, nói tự nhiên) — **🖥️ THAO TÁC** — **✅ KẾT QUẢ PHẢI THẤY**.
> Chạy thử trọn kịch bản một lần trước khi bấm quay; kết quả thật khác kịch bản thì **nói theo kết quả thật**.

## C0. Chuẩn bị (không quay)

1. Giải phóng cổng: `docker ps` → dừng container dự án khác đang chiếm 3306/8081–8084/8761 (lần trước là `okr_mysql`, `okr-test-backend-1`).
2. **Build image trước** để lúc quay không phải chờ: `docker compose build`.
3. Đảm bảo có dữ liệu sạch: nếu cần làm lại từ đầu thì `docker compose down -v` **bây giờ** (không làm trong lúc quay).
4. Mở sẵn: Terminal PowerShell ở `E:\DownCodeGit\PTPM` (chữ to, nền tối) · Trình duyệt tab `localhost:8761` · Postman (collection KT2, đã có biến `tokenUser`) · VS Code mở `PitchClient.java`, `PitchosServiceRegistryApplication.java`, `application.properties` của Booking, `docker-compose.yml` · ảnh `architecture-after.png`.
5. Dán sẵn script 20 request (B8) vào một file `demo-lb.ps1` để ngoài repo (không commit).
6. Quay thử 10 giây kiểm tra tiếng và chữ.

## C1. Mở đầu — 0:00–0:30

🗣️ “Em là Hoàng, nhóm trưởng nhóm PitchOS – hệ thống đặt sân bóng mini. Trong bài kiểm tra 2 em phụ trách Service Registry với Eureka, Auth Service và kiến trúc triển khai. Video này em trình diễn đủ 8 nội dung của đề, tập trung vào phần đăng ký và khám phá dịch vụ.”

🖥️ Mở ảnh sơ đồ kiến trúc.

## C2. Kiến trúc + quy trình nghiệp vụ — 0:30–2:00 *(nội dung 1)*

🗣️ “Hệ thống có 3 dịch vụ nghiệp vụ: Auth quản lý tài khoản và phát JWT, Pitch quản lý sân, Booking quản lý đơn đặt sân. Mỗi dịch vụ có database riêng, chạy ở container MySQL riêng.
Quy trình em chọn là **khách đặt sân**: Booking là **Consumer**, nó phải gọi Pitch – **Provider** – để lấy giá và trạng thái sân rồi mới tính tiền và lưu đơn. Booking không bao giờ đọc thẳng database của Pitch.
So với bài thực hành 6, trước đây Booking gọi Pitch bằng URL cố định localhost:8082. Bây giờ có thêm Eureka ở giữa: mọi dịch vụ tự đăng ký, Booking tìm Pitch theo tên. Pitch chạy 2 instance để chịu tải và dự phòng; Booking chỉ chạy 1 instance vì khoá chống đặt trùng của nó nằm trong bộ nhớ – nếu nhân bản phải chuyển khoá xuống database trước.”

🖥️ Chỉ chuột theo mũi tên trên sơ đồ.

## C3. Khởi động bằng Docker Compose — 2:00–3:00 *(nội dung 2)*

🗣️ “Toàn bộ hệ thống khởi động bằng một lệnh. Cấu hình database, JWT secret, địa chỉ Eureka đều đọc từ biến môi trường trong file .env, không nằm trong mã nguồn.”

🖥️
```bash
docker compose up -d
docker compose ps
```
(Chờ đến khi tất cả `healthy` — cắt đoạn chờ khi dựng video.)

✅ 9 container: registry, auth, pitch-1, pitch-2, booking, 3 MySQL, tất cả `healthy`.

🗣️ “Cột healthy không chỉ nghĩa là container đang chạy, mà là endpoint actuator health của ứng dụng bên trong đã trả UP. Compose dùng healthcheck này để đợi database và Eureka sẵn sàng rồi mới bật các service phụ thuộc.”

## C4. Eureka — 3:00–5:00 *(nội dung 3 – phần chính của Hoàng)*

🖥️ Mở `http://localhost:8761`.

✅ Thấy `PITCHOS-AUTH-SERVICE` (1), `PITCHOS-BOOKING-SERVICE` (1), `PITCHOS-PITCH-SERVICE` (**2**: `pitch-service-1`, `pitch-service-2`).

🗣️ “Đây là Eureka Server, cổng 8761. Nó là project riêng, chỉ có annotation @EnableEurekaServer, không xử lý nghiệp vụ, và tự nó không đăng ký vào chính nó.
Các dịch vụ khi khởi động gửi tên, địa chỉ, cổng tới đây và gửi heartbeat định kỳ. Pitch có hai dòng cùng một Service ID – đó là hai instance của cùng một dịch vụ, cùng image, cùng API, cùng database.”

🖥️ VS Code: `PitchosServiceRegistryApplication.java` → `application.properties` của registry → `PitchClient.java` → `application.properties` của Booking (dòng `EUREKA_URL`).

🗣️ “Phía Booking, Feign client chỉ khai báo name là pitchos-pitch-service, không có url. Khi gọi, Booking hỏi Eureka danh sách instance của tên này, Spring Cloud LoadBalancer chọn một instance. Địa chỉ Eureka cũng lấy từ biến môi trường: trong Docker là tên service pitchos-service-registry, không phải localhost, vì localhost trong container là chính container đó.
Em lưu ý: Dashboard chỉ cho biết dịch vụ đã đăng ký, chưa chứng minh gọi được – nên tiếp theo em gọi thật.”

## C5. Nghiệp vụ Consumer gọi Provider — 5:00–6:30 *(nội dung 4)*

🖥️ Postman: đăng nhập `user` → 200. Gửi `POST http://localhost:8083/api/v1/bookings`:
```json
{ "pitchId": 1, "startTime": "2026-12-20T18:00:00", "endTime": "2026-12-20T19:30:00" }
```
✅ **201**, `status: cho_duyet`, `totalPrice` = giá/giờ × 1,5.

🖥️ Terminal: `docker compose logs --tail 5 pitchos-booking-service pitchos-pitch-service-1 pitchos-pitch-service-2`

🗣️ “Log của Booking ghi ‘Pitch Service trả về sân 1, giá …’ – đây là dữ liệu Booking nhận qua API. Log Pitch có tên container ở đầu dòng nên em biết instance nào vừa xử lý.”

🖥️ Chạy `demo-lb.ps1` (20 request).

✅ Bảng 20 dòng, cột Instance có cả `pitch-service-1` và `pitch-service-2`; bảng đếm, ví dụ 10/10.

🗣️ “20 request đi qua Booking, LoadBalancer phân phối luân phiên cho hai instance. Không cần đúng 50/50, quan trọng là cả hai đều được chọn. Booking không hề biết cổng hay IP của từng instance.”

## C6. Lỗi tích hợp — 6:30–7:30 *(nội dung 5)*

🖥️ Postman: đặt sân với `"pitchId": 999`.

✅ **404** “Không tìm thấy sân bóng với pitchId đã gửi”.

🗣️ “Lỗi thứ nhất: Provider trả 404, Booking dịch lại thành 404 có thông báo rõ, không tạo đơn. Lỗi thứ hai là Provider không khả dụng – em sẽ minh hoạ ngay trong phần dừng dịch vụ.”

## C7. Health và log — 7:30–8:30 *(nội dung 6)*

🖥️
```bash
curl http://localhost:8761/actuator/health
curl http://localhost:8081/actuator/health
curl http://localhost:8082/actuator/health
curl http://localhost:8083/actuator/health
docker compose logs --tail 20 pitchos-booking-service
```
✅ 4 lần `{"status":"UP"}`.

🗣️ “Health chỉ trả UP hoặc DOWN, không lộ chi tiết cấu hình hay database – đúng khuyến nghị bảo mật. Nếu database của service mất kết nối, trạng thái sẽ chuyển DOWN.
Em phân biệt ba mức: container đang chạy, ứng dụng khoẻ, và nghiệp vụ thực hiện được. Ngay sau đây em sẽ cho thấy Booking vẫn UP nhưng nghiệp vụ đặt sân không làm được khi Pitch dừng.”

## C8. Dừng và khởi động lại Provider — 8:30–11:30 *(nội dung 7 – phần chính của Hoàng)*

**Cảnh 1 — một instance sập đột ngột**
🖥️ `docker compose kill pitchos-pitch-service-1` → mở Dashboard → chạy lại `demo-lb.ps1`.

✅ Phần lớn request do `pitch-service-2` xử lý; có thể vài request đầu lỗi trước khi Eureka loại instance 1.

🗣️ “Em dùng kill để mô phỏng sập đột ngột – instance không kịp huỷ đăng ký nên Eureka vẫn còn liệt kê nó vài giây, đến khi hết hạn heartbeat mới loại. [Nếu có request lỗi:] Mấy request lỗi đầu chính là độ trễ đó. Sau đó toàn bộ request chuyển sang instance 2, khách vẫn đặt được sân.”

**Cảnh 2 — mất toàn bộ Provider**
🖥️ `docker compose stop pitchos-pitch-service-2` → Postman đặt sân.

✅ **503** “Dịch vụ quản lý sân hiện không khả dụng. Vui lòng thử lại sau!”, trả về ngay.
🖥️ `curl http://localhost:8083/actuator/health` → vẫn UP; `docker compose logs --tail 5 pitchos-booking-service` → dòng `Không gọi được Pitch Service`.

🗣️ “Khi không còn instance nào, Booking trả 503 rõ ràng, không treo và không lỗi 500. Booking vẫn UP – container chạy, ứng dụng khoẻ, nhưng nghiệp vụ đặt sân thì không thực hiện được. Đó là sự khác nhau giữa application health và business availability.”

**Cảnh 3 — phục hồi**
🖥️ `docker compose start pitchos-pitch-service-1 pitchos-pitch-service-2` → chờ healthy → Dashboard → Postman đặt sân khung giờ mới.

✅ Dashboard lại có 2 instance; đặt sân **201**.

🗣️ “Hai instance khởi động lại, tự đăng ký vào Eureka, Booking tìm thấy và gọi được lại – không phải sửa cấu hình hay khởi động lại Booking.”

## C9. Bảo toàn dữ liệu — 11:30–12:45 *(nội dung 8)*

🖥️
```bash
docker compose down
docker compose ps
docker compose up -d
```
Chờ healthy → Postman `GET http://localhost:8083/api/v1/bookings/my-bookings` (token user, đăng nhập lại nếu cần).

✅ Hai đơn vừa tạo vẫn còn.

🗣️ “Lệnh down xoá container nhưng không xoá named volume. Dữ liệu MySQL nằm trong volume nên sau khi tạo lại container, đơn đặt sân vẫn còn. Nếu dùng down -v thì volume bị xoá và mất dữ liệu – nên nhóm không dùng lệnh đó khi vận hành.”

## C10. Kết — 12:45–13:15

🗣️ “Tóm lại: các dịch vụ tự đăng ký vào Eureka, Booking tìm Pitch theo Service ID và được phân phối tới hai instance, hệ thống vẫn phục vụ khi một instance dừng, báo lỗi rõ khi mất hết và tự phục hồi khi bật lại, dữ liệu bền vững nhờ volume. Hạn chế: chỉ có một Eureka, chưa có API Gateway và Circuit Breaker – đó là hướng phát triển tiếp theo. Em cảm ơn thầy.”

---

# PHẦN D — CÂU HỎI THẦY CÓ THỂ HỎI (chuẩn bị trả lời)

| Câu hỏi | Ý trả lời |
|---|---|
| Eureka khác API Gateway thế nào? | Eureka trả lời “dịch vụ ở đâu”, request nghiệp vụ không đi qua nó; Gateway là cửa vào cho client, request đi qua và được định tuyến (xem bảng B9) |
| Dùng Service ID là tự có cân bằng tải à? | Không. Cần LoadBalancer: `eureka-client` kéo theo Spring Cloud LoadBalancer, Feign dùng nó để chọn instance (mặc định luân phiên) |
| Sao dừng instance mà vẫn có request lỗi? | Eureka cập nhật theo heartbeat, Booking giữ bản sao danh sách có thời hạn → có khoảng trễ; giảm bằng heartbeat/cache ngắn hơn, retry có giới hạn |
| Sao tắt self-preservation? | Để demo thấy instance chết bị loại nhanh. Production nên bật để không xoá nhầm hàng loạt khi mạng chập chờn |
| Eureka chết thì sao? | Service đang chạy vẫn gọi nhau được một thời gian nhờ bản sao danh sách đã lưu; service mới/khởi động lại không đăng ký được → vì vậy production cần nhiều Eureka (HA) |
| Hai instance Pitch có dùng 2 DB riêng không? | Không — dùng chung `mysql-pitch`; 2 DB riêng thì hai instance trả dữ liệu sân khác nhau |
| Sao Booking không chạy 2 instance? | Khoá chống đặt trùng là `synchronized` trong RAM, chỉ có hiệu lực trong 1 tiến trình; muốn scale phải chuyển sang khoá/ràng buộc ở DB |
| Có Eureka rồi thì còn cần JWT không? | Có. Tìm thấy dịch vụ ≠ được phép gọi; Eureka không xác thực ai cả |
| Trong Docker sao không dùng `localhost:8761`? | `localhost` trong container là chính nó; phải dùng tên service Docker `pitchos-service-registry` (Docker DNS trong network) |
| `depends_on` có đủ không? | Không, chỉ đợi container chạy; phải có healthcheck + `condition: service_healthy`, và ứng dụng vẫn phải tự kết nối lại được |
| Dashboard có đủ làm minh chứng? | Không; phải kèm request thật, response và log (thầy nhấn mạnh ở TH7) |
| `.env` có lên GitHub không? | Không, chỉ `.env.example`; `.env` đã gỡ khỏi Git và nằm trong `.gitignore` |

---

## Checklist trước khi nộp (của Hoàng)

- [ ] PR1, PR2 đã merge; `main` chạy `docker compose up -d --build` từ bản clone mới
- [ ] Ảnh: Dashboard (2 instance Pitch), code Feign không `url`, bảng 20 request, TC04–TC06, health
- [ ] `docs/architecture/` đủ sơ đồ + `deployment-design.md`
- [ ] `docs/testing/service-discovery-test.md` đủ TC01–TC06 (+ TC07 nếu làm)
- [ ] `docs/kt2/CAU1_2_HOANG.md`, `PHAN_2_HOANG.md`, `PHAN_4_HOANG.md`
- [ ] README thử trên máy sạch OK
- [ ] `docs/report.pdf` đã gộp, ảnh có chú thích + phân tích
- [ ] Video 12–14', đủ 8 nội dung
