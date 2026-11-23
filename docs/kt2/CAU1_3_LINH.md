# CÂU 1.3: DOCKER CONTAINERIZATION TRONG KIẾN TRÚC MICROSERVICES
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices 2026)  
**Sinh viên thực hiện:** LINH  
**Vai trò đề tài:** Kỹ sư Triển khai Container & Provider Pitch Service  
**Mục tiêu điểm số:** 0,5 / 0,5 Điểm Lý thuyết (Câu 1)  
**Minh chứng mã nguồn:** `pitchos-pitch-service/Dockerfile`, `docker-compose.yml`, `.env.example`

---

## 1. PHÂN BIỆT DOCKER IMAGE VÀ DOCKER CONTAINER

Trong kiến trúc hướng dịch vụ hiện đại, việc container hóa (Containerization) là tiêu chuẩn bắt buộc để đảm bảo tính nhất quán môi trường từ khâu phát triển (Development) đến vận hành thực tế (Production). Hai khái niệm nền tảng cấu thành nên công nghệ này là **Docker Image** và **Docker Container**.

```
                           ┌────────────────────────┐
                           │   Dockerfile Kịch bản  │
                           └───────────┬────────────┘
                                       │ docker build
                                       ▼
                           ┌────────────────────────┐
                           │      Docker Image      │
                           │ (Read-Only Blueprint)  │
                           └───────────┬────────────┘
                                       │ docker run (1 Image -> Nhiều Container)
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        ┌───────────────────────┐             ┌───────────────────────┐
        │   Docker Container 1  │             │   Docker Container 2  │
        │ pitchos-pitch-service-1│             │ pitchos-pitch-service-2│
        │      (Port 8082)      │             │      (Port 8084)      │
        │ [Writable Layer: R/W] │             │ [Writable Layer: R/W] │
        │ [Isolated Process PID]│             │ [Isolated Process PID]│
        └───────────────────────┘             └───────────────────────┘
```

### 1.1. Bản chất kỹ thuật của Docker Image
* **Định nghĩa:** Docker Image là một gói phần mềm độc lập, bất biến (Immutable / Read-only Template/Blueprint) chứa toàn bộ các thành phần cần thiết để một ứng dụng có thể thực thi độc lập:
  1. Hệ điều hành tối thiểu (Base OS layer: ví dụ Alpine Linux).
  2. Môi trường thực thi (Runtime environment: ví dụ Eclipse Temurin JRE 17).
  3. Mã nhị phân ứng dụng đã đóng gói (Application JAR file: `pitchos-pitch-service-0.0.1-SNAPSHOT.jar`).
  4. Các biến môi trường, nhãn metadata và lệnh khởi chạy mặc định (`ENTRYPOINT`).
* **Cấu trúc phân lớp (Layered Architecture):** Docker Image được xây dựng từ nhiều lớp chỉ đọc (Read-only Layers) xếp chồng lên nhau thông qua hệ thống tập tin hợp nhất (Union File System - UnionFS / Overlay2). Mỗi chỉ dẫn trong Dockerfile (như `FROM`, `COPY`, `RUN`) sinh ra một layer mới. Các layer này có mã băm định danh duy nhất (SHA256) và được chia sẻ (cache) giữa các image khác nhau để tiết kiệm dung lượng lưu trữ đĩa cứng và băng thông mạng.

### 1.2. Bản chất kỹ thuật của Docker Container
* **Định nghĩa:** Docker Container là một thể hiện đang chạy (Running Instance) được khởi tạo trực tiếp từ một Docker Image.
* **Cơ chế cô lập tiến trình (Process Isolation):** Khác với máy ảo (Virtual Machine) phải mang theo cả một hệ điều hành khách (Guest OS) nặng nề qua Hypervisor, Docker Container chia sẻ chung nhân hệ điều hành máy chủ (Host Linux Kernel) và sử dụng hai tính năng cốt lõi của Linux Kernel để cô lập hoàn toàn:
  * **Namespaces:** Cô lập không gian hiển thị của tiến trình bao gồm: `pid` (cô lập cây tiến trình), `net` (cô lập giao diện mạng và bảng định tuyến), `mnt` (cô lập hệ thống tập tin mount), `ipc` (cô lập bộ nhớ dùng chung), `uts` (cô lập hostname).
  * **Control Groups (Cgroups):** Giới hạn và giám sát tài nguyên phần cứng vật lý mà container được phép sử dụng (CPU quotas, RAM limits, I/O bandwidth).
* **Lớp ghi tạm thời (Writable Container Layer):** Khi container được bật lên, Docker Engine xếp thêm một lớp mỏng cho phép đọc-ghi (Read-Write Layer) trên đỉnh các lớp chỉ đọc của Image. Mọi thao tác tạo file tạm, ghi log cục bộ hoặc sửa đổi cấu hình trong lúc container hoạt động chỉ được lưu trên lớp ghi này. Khi container bị xóa (`docker rm`), lớp ghi này sẽ biến mất hoàn toàn mà không làm thay đổi bản gốc Docker Image bên dưới.

### 1.3. Mối quan hệ tương quan trong hệ thống PitchOS
Mối quan hệ giữa Image và Container là mối quan hệ **Một - Nhiều (1 - N)**, tương đương với mối quan hệ giữa **Lớp (Class)** và **Đối tượng (Object)** trong lập trình hướng đối tượng:
> **Minh chứng thực tế trong PitchOS:**  
> Đề tài yêu cầu dịch vụ Provider `pitchos-pitch-service` phải chạy song song **2 instances** để chứng minh khả năng cân bằng tải (Load Balancing) và chịu lỗi (Fault Tolerance) của Eureka.  
> Nhóm chỉ cần thực hiện `docker build` đúng **một Docker Image duy nhất** (`pitchos-pitch-service:latest`), sau đó Docker Compose khởi tạo thành công **hai Container độc lập**:
> 1. `pitchos-pitch-service-1`: Lắng nghe trên cổng nội bộ `8082`, định danh `INSTANCE_ID=pitch-instance-1`.
> 2. `pitchos-pitch-service-2`: Lắng nghe trên cổng nội bộ `8084`, định danh `INSTANCE_ID=pitch-instance-2`.
> 
> Cả 2 container dùng chung 100% các layer của Image gốc (không tốn thêm dung lượng đĩa cho mã nguồn), nhưng sở hữu tiến trình PID riêng, cổng mạng riêng và lớp ghi riêng.

### 1.4. Bảng so sánh toàn diện Docker Image vs Docker Container

| Tiêu chí so sánh | Docker Image | Docker Container |
|---|---|---|
| **Bản chất kỹ thuật** | Bản thiết kế khuôn mẫu chỉ đọc (Read-only Blueprint / Template) | Thể hiện thực thi động của Image (Running Instance) |
| **Trạng thái (State)** | Bất biến (Immutable, Stateless), đóng băng lúc build | Có trạng thái (Stateful), thay đổi linh hoạt theo thời gian thực |
| **Cấu trúc lưu trữ** | Tập hợp các Read-only Layers (UnionFS / Overlay2) | Các Read-only Layers của Image + 1 Writable Layer trên cùng |
| **Khả năng chỉnh sửa** | Không thể chỉnh sửa trực tiếp (muốn đổi phải build image mới) | Cho phép ghi file, tạo log tạm trên Writable Layer |
| **Tài nguyên chiếm dụng** | Chỉ tiêu tốn dung lượng ổ cứng (Disk Storage) | Chiếm dụng CPU, RAM thực tế của máy chủ và tiến trình PID |
| **Vòng đời (Lifecycle)** | Tồn tại lâu dài (Build ➔ Tag ➔ Push/Pull ➔ Store) | Ngắn hạn, linh hoạt (`create` ➔ `start` ➔ `stop` ➔ `rm`) |
| **Hiện diện trong PitchOS** | `pitchos-pitch-service:latest` (Đóng gói JAR Spring Boot) | `pitchos-pitch-service-1` (:8082) & `pitchos-pitch-service-2` (:8084) |

---

## 2. VAI TRÒ CỦA DOCKERFILE VÀ DOCKER COMPOSE TRONG TRIỂN KHAI MICROSERVICES

Trong một hệ sinh thái phân tán gồm nhiều dịch vụ như PitchOS, việc quản lý triển khai không thể làm thủ công từng câu lệnh đơn lẻ. **Dockerfile** và **Docker Compose** đóng hai vai trò ở hai tầng phạm vi (Scope) bổ trợ chặt chẽ cho nhau.

```
┌────────────────────────────────────────────────────────────────────────┐
│ DOCKERFILE (Phạm vi đơn dịch vụ - Single Service Packaging)             │
│ • Định nghĩa cách đóng gói 1 Microservice thành 1 Docker Image chuẩn     │
│ • Multi-stage Build: Tối ưu dung lượng (loại bỏ Maven khỏi runtime)   │
│ • Security: Tạo và chuyển sang người dùng thường (USER appuser)        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Build ra Image
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ DOCKER COMPOSE (Phạm vi toàn hệ thống - Multi-Service Orchestration)   │
│ • File cấu hình tập trung duy nhất: docker-compose.yml                 │
│ • Điều phối mạng nội bộ (pitchos-network) & phân giải DNS theo tên     │
│ • Kiểm soát sức khỏe (Healthcheck) & Thứ tự khởi động (depends_on)     │
│ • Quản lý biến môi trường (.env) & Lưu trữ bền vững (Named Volumes)   │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1. Vai trò của Dockerfile trong Microservices
Dockerfile là tập tin văn bản chứa các chỉ thị tuần tự hướng dẫn Docker Engine cách tự động hóa quá trình xây dựng một Docker Image cho **từng microservice đơn lẻ**. Trong đề tài PitchOS, Dockerfile của `pitchos-pitch-service` giải quyết 3 bài toán kỹ thuật cốt lõi:

#### a) Kỹ thuật Multi-Stage Build (Tối ưu kích thước Image)
Nếu dùng Dockerfile truyền thống (Single-stage), image cuối cùng sẽ phải chứa toàn bộ Maven CLI, mã nguồn Java thô và kho thư viện đệm `.m2` (dung lượng thường vượt quá 600MB – 800MB). Kỹ thuật Multi-stage build tách quy trình đóng gói thành 2 giai đoạn độc lập:
* **Stage 1 (Builder):** Dùng base image `maven:3.9.6-eclipse-temurin-17-alpine` để biên dịch mã nguồn và đóng gói thành file JAR (`mvn clean package -DskipTests`).
* **Stage 2 (Runtime):** Dùng base image `eclipse-temurin:17-jre-alpine` siêu nhẹ, chỉ sao chép duy nhất file `.jar` hoàn chỉnh từ Stage 1 (`COPY --from=builder`). Toàn bộ Maven và mã nguồn thô bị hủy bỏ.
* **Kết quả:** Dung lượng Image giảm xuống chỉ còn khoảng **150MB**, giúp tiết kiệm băng thông khi kéo thả image và giảm thiểu bề mặt tấn công bảo mật (Attack Surface).

#### b) Tối ưu hóa cơ chế Layer Cache (Tăng tốc độ Build)
Docker lưu vết (cache) kết quả của từng dòng lệnh. Trong `pitchos-pitch-service/Dockerfile`:
```dockerfile
# 1. Copy pom.xml và tải thư viện trước
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 2. Sau đó mới copy mã nguồn nghiệp vụ
COPY src ./src
RUN mvn clean package -DskipTests -B
```
Khi lập trình viên sửa đổi logic trong file Java (nằm ở `src/`), các lớp cache của bước tải thư viện phụ thuộc (`pom.xml`) vẫn được tái sử dụng 100%. Quá trình build lại chỉ mất vài giây thay vì phải tải lại hàng trăm MB thư viện từ Internet.

#### c) Nguyên tắc bảo mật quyền tối thiểu (Least Privilege - Non-root User)
Mặc định, các tiến trình trong container Docker chạy dưới quyền `root`. Nếu ứng dụng Spring Boot xuất hiện lỗ hổng bảo mật (ví dụ Remote Code Execution qua thư viện bên thứ ba), kẻ tấn công chiếm được quyền điều khiển sẽ có quyền root trên container và có nguy cơ thoát khỏi container (Container Escape) để tấn công máy chủ vật lý.
* Trong Dockerfile của Linh, một nhóm và người dùng không có đặc quyền được tạo sẵn:
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app
USER appuser
```
Tiến trình Java Spring Boot luôn thực thi dưới quyền của `appuser`, đáp ứng tiêu chuẩn an toàn bảo mật nghiêm ngặt của bài thực hành TH8.

---

### 2.2. Vai trò của Docker Compose trong Microservices
Trong khi Dockerfile chỉ giải quyết bài toán đóng gói cho một tiến trình đơn lẻ, **Docker Compose** đóng vai trò là **nhà điều phối (Orchestration Engine)** ở môi trường phát triển và kiểm thử. Thay vì kỹ sư phải gõ hàng chục câu lệnh `docker run`, `docker network create`, `docker volume create` với hàng trăm tham số phức tạp, Docker Compose cho phép định nghĩa toàn bộ hạ tầng 8 container của PitchOS trong một file duy nhất: `docker-compose.yml`.

Bốn vai trò hạ tầng quyết định của Docker Compose trong PitchOS gồm:

#### 1. Thiết lập mạng nội bộ cô lập (Docker Network) và Cơ chế phân giải DNS
Docker Compose tự động khởi tạo mạng cầu nối `pitchos-network` (Bridge Network) và tích hợp sẵn máy chủ DNS nội bộ (Embedded DNS Server):
* Các container được gán tên miền nội bộ chính là tên dịch vụ khai báo (`container_name`).
* **Nguyên tắc vàng:** Triệt tiêu hoàn toàn việc dùng `localhost` hay IP cứng. Trong mạng Docker, `localhost` trỏ về chính bản thân container đó. Khi Auth Service hay Booking Service muốn kết nối CSDL, chúng gọi qua tên hostname container: `mysql-auth:3306`, `mysql-booking:3306`. Khi các service đăng ký vào Eureka, chúng trỏ tới `http://pitchos-service-registry:8761/eureka/`.

#### 2. Điều phối thứ tự khởi động và Giám sát sức khỏe (Healthcheck & Dependency Ordering)
Một trong những lỗi phổ biến nhất khi triển khai phân tán là **Race Condition lúc khởi động**: Ứng dụng Java Spring Boot bật lên quá nhanh trong khi MySQL Server đang khởi tạo dữ liệu và chưa mở cổng 3306, dẫn đến crash `CommunicationsException`.
* Docker Compose cho phép kết hợp `healthcheck` (kiểm tra `mysqladmin ping` cho MySQL và `/actuator/health` cho Java) cùng `depends_on: condition: service_healthy`.
* **Đặc biệt trong PitchOS:** `pitchos-pitch-service-2` được cấu hình chờ `pitchos-pitch-service-1` đạt trạng thái `service_healthy`. Nhờ đó, Instance 1 thực hiện xong tiến trình `DataInitializer` (nạp 4 sân bóng mẫu vào MySQL) thì Instance 2 mới khởi động, ngăn chặn triệt để lỗi tranh chấp khóa chính và chèn trùng dữ liệu.

#### 3. Quản trị cấu hình và biến môi trường tập trung (.env)
Tuân thủ nguyên lý số III trong phương pháp luận *The Twelve-Factor App* (Lưu trữ cấu hình trong môi trường):
* Mọi tham số nhạy cảm (mật khẩu CSDL, chuỗi bí mật `JWT_SECRET`) và cổng mạng được tách riêng ra file `.env`.
* Docker Compose tự động nội suy (interpolate) các biến này vào cấu hình container, đảm bảo không có bất kỳ thông tin nhạy cảm nào bị lưu cứng (hardcode) trong mã nguồn hoặc commit lên Git.

#### 4. Quản lý lưu trữ bền vững (Named Volumes)
Vòng đời của container mang tính ngắn hạn (Ephemeral). Để dữ liệu đặt sân không bị mất đi khi container bị khởi động lại hoặc xóa bỏ, Docker Compose cung cấp cơ chế **Named Volume**:
* `mysql_auth_data`, `mysql_pitch_data`, `mysql_booking_data` được gắn trực tiếp vào thư mục `/var/lib/mysql` của các container CSDL.
* Khi thực hiện bảo trì dừng toàn bộ hệ thống bằng `docker compose down`, toàn bộ bản ghi đơn đặt sân trong CSDL vẫn tồn tại vĩnh viễn trên ổ cứng máy chủ vật lý, sẵn sàng phục vụ khi chạy lại `docker compose up -d`.

---

### 2.3. Bảng đối chiếu tổng kết Dockerfile vs Docker Compose

| Tiêu chí | Dockerfile | Docker Compose (`docker-compose.yml`) |
|---|---|---|
| **Mục đích chính** | Đóng gói (Package) và xây dựng (Build) một Docker Image | Điều phối (Orchestrate) và quản lý vòng đời nhiều Container |
| **Phạm vi tác động** | Một Microservice đơn lẻ (`pitchos-pitch-service`) | Toàn bộ hệ sinh thái (8 container trong mạng `pitchos-network`) |
| **Lệnh thực thi cơ bản** | `docker build -t pitchos-pitch-service .` | `docker compose up -d`, `docker compose ps`, `docker compose down` |
| **Quản lý mạng (Network)** | Chỉ khai báo cổng mở dự kiến qua chỉ dẫn `EXPOSE` | Thiết lập mạng nội bộ ảo (`pitchos-network`), kích hoạt DNS container |
| **Thứ tự thực thi** | Thực thi tuần tự các chỉ dẫn biên dịch từ trên xuống dưới | Điều phối thứ tự khởi động phụ thuộc (`depends_on: service_healthy`) |
| **Quản trị dữ liệu** | Không trực tiếp gắn ổ đĩa vật lý của máy chủ | Định nghĩa và gắn kết Named Volumes bền vững cho CSDL |
| **Vai trò của Linh** | Soạn thảo Dockerfile multi-stage, non-root user cho Pitch | Thiết lập file điều phối toàn hệ sinh thái PitchOS hoàn chỉnh |
