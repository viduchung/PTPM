# CÂU 1.2: VAI TRÒ CỦA SERVICE REGISTRY VÀ SERVICE DISCOVERY
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices)
**Sinh viên thực hiện:** HOÀNG (Nhóm trưởng)
**Mục tiêu điểm số:** 0,5 / 0,5 Điểm Lý thuyết (Câu 1)
**Minh chứng mã nguồn:** `pitchos-service-registry/`, `pitchos-auth-service/src/main/resources/application.properties`

---

## 1. SERVICE REGISTRY: CUỐN DANH BẠ TRUNG TÂM CỦA HỆ THỐNG

### 1.1. Vấn đề mà Service Registry giải quyết

Trong kiến trúc đơn khối (Monolithic), mọi lời gọi hàm diễn ra trong cùng một tiến trình, địa chỉ của hàm được trình biên dịch giải quyết ngay lúc build. Khi tách thành nhiều microservice chạy trên nhiều tiến trình, nhiều container, mỗi lời gọi trở thành một lời gọi qua mạng, và câu hỏi mới xuất hiện: **"dịch vụ tôi cần gọi hiện đang nằm ở địa chỉ nào?"**

Ở bài kiểm tra số 1, nhóm giải quyết câu hỏi này bằng cách gắn cứng địa chỉ vào cấu hình:

```properties
# Cách làm ở KT1 - gắn cứng địa chỉ Provider
pitch.service.url=http://localhost:8082
```

Cách này hoạt động được trên một máy tính duy nhất, nhưng sụp đổ ngay khi hệ thống được container hóa, vì ba lý do sẽ phân tích ở Mục 4.

### 1.2. Định nghĩa và cấu trúc bản ghi

**Service Registry** là một dịch vụ hạ tầng đóng vai trò *cuốn danh bạ điện thoại* trung tâm: nó lưu trữ thông tin mạng của toàn bộ các **service instance** đang sống trong hệ thống. Mỗi bản ghi trong danh bạ gồm:

| Thành phần bản ghi | Ý nghĩa | Ví dụ trong PitchOS |
|---|---|---|
| **Service ID** (Application Name) | Tên định danh logic của dịch vụ, không đổi theo thời gian | `PITCHOS-AUTH-SERVICE` |
| **Instance ID** | Định danh duy nhất của từng bản chạy cụ thể | `pitchos-pitch-service:8082` |
| **Host / IP Address** | Địa chỉ mạng thực tế tại thời điểm hiện tại | `172.18.0.5` |
| **Port** | Cổng ứng dụng đang lắng nghe | `8082` |
| **Status** | Trạng thái vòng đời | `UP`, `DOWN`, `STARTING`, `OUT_OF_SERVICE` |
| **Health Check URL** | Địa chỉ để kiểm tra sức khỏe | `/actuator/health` |

Trong PitchOS, Service Registry được hiện thực bằng **Netflix Eureka Server**, đặt trong module `pitchos-service-registry`, chạy ở cổng `8761`. Toàn bộ hạ tầng danh bạ được bật bằng một annotation duy nhất:

```java
@SpringBootApplication
@EnableEurekaServer     // Bật bảng đăng ký, REST API cho client và Dashboard
public class PitchosServiceRegistryApplication { ... }
```

### 1.3. Hai chiều hoạt động: Đăng ký và Tra cứu

Danh bạ chỉ có giá trị khi có cả người ghi tên vào và người tra cứu. Tương ứng, có hai chiều hoạt động:

**Chiều 1 — Service Registration (Đăng ký):** Dịch vụ tự khai báo mình với Registry khi khởi động. Trong PitchOS, Auth Service đăng ký bằng cấu hình sau:

```properties
eureka.client.service-url.defaultZone=${EUREKA_URL:http://localhost:8761/eureka/}
eureka.client.register-with-eureka=true
eureka.instance.prefer-ip-address=true
```

**Chiều 2 — Service Discovery (Tra cứu):** Dịch vụ tiêu thụ (Consumer) hỏi Registry để biết Provider đang ở đâu, rồi mới phát lời gọi thật. Đây là nội dung Mục 2.

---

## 2. SERVICE DISCOVERY: CƠ CHẾ TRA CỨU VÀ ĐỊNH VỊ

### 2.1. Luồng tra cứu đầy đủ trong PitchOS

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      SERVICE REGISTRY (Eureka :8761)                     │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  PITCHOS-AUTH-SERVICE    -> 172.18.0.3:8081  [UP]                  │  │
│  │  PITCHOS-PITCH-SERVICE   -> 172.18.0.5:8082  [UP]                  │  │
│  │                          -> 172.18.0.6:8084  [UP]   <- 2 instance  │  │
│  │  PITCHOS-BOOKING-SERVICE -> 172.18.0.7:8083  [UP]                  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└────────▲────────────────────────▲──────────────────────────▲─────────────┘
         │ (1) Đăng ký            │ (2) Tải bản sao          │ (1) Đăng ký
         │     + Heartbeat 10s    │     danh bạ về cache     │     + Heartbeat
         │                        │                          │
┌────────┴─────────┐    ┌─────────┴──────────┐     ┌─────────┴─────────┐
│  Auth Service    │    │  Booking Service   │     │  Pitch Service    │
│  (Provider)      │    │  (CONSUMER)        │     │  (PROVIDER)       │
│  :8081           │    │  :8083             │     │  :8082 và :8084   │
└──────────────────┘    └─────────┬──────────┘     └─────────▲─────────┘
                                  │                          │
                                  └──────────────────────────┘
                             (3) Gọi trực tiếp bằng IP lấy từ cache
                                 (KHÔNG đi qua Eureka Server)
```

Năm bước của một lời gọi có Service Discovery:

| Bước | Hành động | Thành phần thực hiện |
|---|---|---|
| **1** | Provider khởi động, gửi bản ghi `{Service ID, IP, Port}` lên Registry | Eureka Client trong Pitch Service |
| **2** | Consumer tải bản sao toàn bộ danh bạ về bộ nhớ đệm cục bộ (local cache), làm mới mỗi 30 giây | Eureka Client trong Booking Service |
| **3** | Consumer cần gọi Provider: tra cứu Service ID `pitchos-pitch-service` **trong cache của chính nó**, nhận về danh sách 2 instance | Spring Cloud LoadBalancer |
| **4** | LoadBalancer chọn 1 instance theo thuật toán Round Robin, trả về địa chỉ cụ thể | Spring Cloud LoadBalancer |
| **5** | Consumer phát request HTTP trực tiếp tới instance đã chọn | OpenFeign Client |

**Điểm kỹ thuật quan trọng cần nhấn mạnh:** Eureka Server **không nằm trên đường đi của request nghiệp vụ**. Nó chỉ tham gia ở bước 1–2 (đăng ký và cấp bản sao danh bạ). Đến bước 5, Booking Service gọi **trực tiếp** tới Pitch Service. Nhờ thiết kế này, nếu Eureka Server tạm thời sập, các lời gọi hiện có **vẫn hoạt động bình thường** vì mỗi Consumer đã giữ bản sao danh bạ trong bộ nhớ của mình. Mô hình này gọi là **Client-side Discovery**.

### 2.2. Cơ chế Heartbeat và độ trễ cập nhật

Registry phải luôn biết instance nào còn sống. Cơ chế được dùng là **Heartbeat** (nhịp tim): mỗi Eureka Client định kỳ gửi một request gia hạn hợp đồng thuê (lease) lên Registry để báo "tôi vẫn còn sống".

Hai tham số điều khiển cơ chế này:

| Tham số | Mặc định Eureka | Cấu hình trong PitchOS | Ý nghĩa |
|---|---|---|---|
| `lease-renewal-interval-in-seconds` | 30 giây | **10 giây** | Chu kỳ gửi Heartbeat |
| `lease-expiration-duration-in-seconds` | 90 giây | **30 giây** | Không nhận Heartbeat quá hạn này thì bị loại khỏi danh bạ |

**Phân tích độ trễ cập nhật:**

Khi một instance Provider dừng đột ngột (ví dụ `docker compose stop pitchos-pitch-service-1`), nó **không kịp** gửi tín hiệu hủy đăng ký. Instance đó biến mất khỏi hệ thống nhưng vẫn còn trong danh bạ, và tổng độ trễ để toàn hệ thống nhận biết là tổng dồn của ba khoảng thời gian:

```
  (a) Registry chờ hết thời hạn lease                -> tối đa 90 giây (mặc định)
+ (b) Chu kỳ quét loại bỏ instance chết (eviction)   -> 60 giây (mặc định)
+ (c) Consumer làm mới cache danh bạ                 -> 30 giây (mặc định)
--------------------------------------------------------------------------
  Tổng độ trễ trường hợp xấu nhất                    -> có thể lên tới ~3 phút
```

**Hệ quả thực tế:** trong khoảng độ trễ này, Consumer vẫn có thể chọn một instance đã chết và nhận lỗi `Connection refused`. Đây **không phải lỗi lập trình** mà là đặc tính kiến trúc của mô hình **AP** (Availability + Partition tolerance) mà Eureka theo đuổi: Eureka chấp nhận trả về dữ liệu *có thể hơi cũ* để đổi lấy việc luôn luôn trả lời được, thay vì khóa toàn hệ thống chờ đồng thuận như mô hình CP.

**Hai biện pháp nhóm đã áp dụng để rút ngắn độ trễ phục vụ kiểm thử:**

1. Giảm nhịp Heartbeat và thời hạn lease xuống `10s / 30s` ở phía Client (`pitchos-auth-service/src/main/resources/application.properties`).
2. Tắt chế độ **Self-Preservation** và giảm chu kỳ quét ở phía Server:

```properties
eureka.server.enable-self-preservation=false
eureka.server.eviction-interval-timer-in-ms=5000
```

*Lý do tắt Self-Preservation:* cơ chế này được thiết kế cho môi trường sản xuất hàng trăm instance — khi tỉ lệ Heartbeat nhận được tụt dưới ngưỡng (khoảng 85%), Eureka cho rằng **mạng** bị lỗi chứ không phải **dịch vụ** bị lỗi, nên nó giữ lại toàn bộ bản ghi cũ để tránh xóa oan hàng loạt. Ở môi trường học tập chỉ có 3–4 instance, việc dừng 1 instance đã vượt ngưỡng ngay lập tức, khiến Eureka chuyển sang chế độ tự bảo vệ và **không loại instance đã chết ra khỏi danh bạ** — làm kịch bản kiểm thử "dừng một instance" không phản ánh đúng thực tế.

---

## 3. PHÂN BIỆT EUREKA SERVER VỚI API GATEWAY

Đây là hai thành phần **khác nhau về tầng hoạt động, về hướng luồng dữ liệu và về trách nhiệm**. Gộp lẫn hai khái niệm dẫn tới thiết kế sai: hoặc để Client gọi thẳng vào Eureka để lấy địa chỉ (phơi bày topology nội bộ ra ngoài), hoặc kỳ vọng Eureka tự lọc bảo mật request (điều nó không hề làm).

### 3.1. Bảng so sánh

| Tiêu chí | **Eureka Server** (Service Registry) | **API Gateway** |
|---|---|---|
| **Tầng hoạt động** | Tầng nội bộ (Internal / Service Layer) | Tầng biên (Edge / Perimeter) |
| **Câu hỏi nó trả lời** | "Dịch vụ tên X đang ở những địa chỉ nào?" | "Request này nên chuyển tới dịch vụ nào, và người gửi có quyền không?" |
| **Ai gọi nó** | Các microservice nội bộ (Eureka Client) | Client bên ngoài: trình duyệt, ứng dụng di động, Postman |
| **Có nằm trên đường đi của request nghiệp vụ?** | **KHÔNG.** Chỉ cấp địa chỉ, không trung chuyển dữ liệu | **CÓ.** Mọi byte dữ liệu nghiệp vụ đều đi xuyên qua nó |
| **Trách nhiệm chính** | Lưu danh bạ, nhận Heartbeat, loại bỏ instance chết | Định tuyến (Routing), xác thực, Rate Limiting, SSL Termination, tổng hợp API |
| **Nếu thành phần này sập** | Các lời gọi hiện có **vẫn chạy** (Consumer dùng cache); chỉ không đăng ký / phát hiện được instance mới | **Toàn bộ hệ thống mất lối vào** từ bên ngoài, Client không gọi được gì |
| **Hiện thực trong Spring Cloud** | `spring-cloud-starter-netflix-eureka-server` | `spring-cloud-starter-gateway` |
| **Trong PitchOS** | Đã triển khai: `pitchos-service-registry` :8761 | Chưa triển khai (ngoài phạm vi KT2) |

### 3.2. Sơ đồ phân định vị trí hai thành phần

```
   NGƯỜI DÙNG / POSTMAN / TRÌNH DUYỆT
                 │
                 │  (A) Request nghiệp vụ từ bên ngoài
                 ▼
     ╔═══════════════════════════╗
     ║       API GATEWAY         ║   <-- TẦNG BIÊN
     ║  Routing · Auth · Limit   ║       Dữ liệu nghiệp vụ ĐI XUYÊN QUA
     ╚═══════════╦═══════════════╝
                 │  (B) Chuyển tiếp vào trong
    ┌────────────┼────────────┬─────────────┐
    ▼            ▼            ▼             │
┌────────┐  ┌────────┐  ┌─────────┐         │ (C) Tra cứu địa chỉ
│  Auth  │  │ Pitch  │  │ Booking │─────────┘      (chỉ metadata)
│ :8081  │  │ :8082  │  │  :8083  │                      │
└───┬────┘  └───┬────┘  └────┬────┘                      ▼
    │           │            │                ╔════════════════════╗
    └───────────┴────────────┴───────────────► ║   EUREKA SERVER    ║
              (C) Đăng ký + Heartbeat          ║   Danh bạ :8761    ║
                                               ╚════════════════════╝
                                                  <-- TẦNG NỘI BỘ
                                                KHÔNG có dữ liệu nghiệp
                                                vụ nào đi xuyên qua đây
```

Đọc sơ đồ theo luồng: mũi tên **(A)** và **(B)** là luồng dữ liệu nghiệp vụ, đi *xuyên qua* API Gateway. Mũi tên **(C)** là luồng metadata quản trị, chỉ chạm tới Eureka. Hai luồng này không giao nhau — đó chính là lý do không thể dùng thành phần này thay cho thành phần kia.

### 3.3. Cách ghi nhớ ngắn gọn

> **Eureka Server** là *cuốn danh bạ điện thoại*: nó cho bạn biết số của người cần gọi, nhưng cuộc gọi là bạn tự thực hiện — giọng nói không đi qua cuốn danh bạ.
>
> **API Gateway** là *tổng đài lễ tân*: mọi cuộc gọi từ bên ngoài đều phải qua tổng đài; tổng đài kiểm tra bạn là ai, có quyền gặp ai, rồi mới nối máy — toàn bộ nội dung cuộc gọi đi xuyên qua tổng đài.

---

## 4. VÌ SAO CONSUMER PHẢI GỌI PROVIDER QUA SERVICE ID

### 4.1. Lý do 1: Địa chỉ trong môi trường container là phù du (Ephemeral)

Khi container hóa, Docker cấp địa chỉ IP cho container từ dải mạng nội bộ của network `pitchos-network` theo thứ tự khởi động. Địa chỉ này **thay đổi sau mỗi lần `docker compose down` rồi `up`**:

| Lần khởi chạy | IP của Pitch instance 1 | IP của Pitch instance 2 |
|---|---|---|
| Lần 1 | `172.18.0.5` | `172.18.0.6` |
| Lần 2 (sau `down` / `up`) | `172.18.0.7` | `172.18.0.4` |

Nếu Booking Service gắn cứng `http://172.18.0.5:8082`, chỉ cần khởi động lại hệ thống một lần là toàn bộ chức năng đặt sân chết. Ngược lại, tên định danh `pitchos-pitch-service` **không bao giờ đổi**, vì nó là tên logic do lập trình viên đặt trong `spring.application.name`, không phải địa chỉ do hạ tầng cấp.

Trường hợp đặc biệt nguy hiểm là **bẫy `localhost` trong container**: cấu hình `http://localhost:8082` chạy đúng trên máy thật, nhưng khi đóng gói vào Docker, `localhost` trỏ về **chính container đang chạy mã đó** (Booking Service), nơi không có cổng 8082 nào lắng nghe. Kết quả là `Connection refused` — và lỗi này không xuất hiện trong lúc phát triển, chỉ bùng ra khi triển khai.

### 4.2. Lý do 2: Một Service ID có thể trỏ tới nhiều instance (điều kiện cần của cân bằng tải)

Một URL cố định về bản chất chỉ mô tả được **một** điểm đích. Trong khi đó, PitchOS chạy **2 instance Pitch Service** song song (cổng `8082` và `8084`) để tăng khả năng chịu tải và chịu lỗi.

```
Gọi bằng URL cứng:     Booking ──────────────► Pitch :8082 (duy nhất)
                                                Pitch :8084 không bao giờ được dùng

Gọi bằng Service ID:   Booking ──► LoadBalancer ──┬──► Pitch :8082
                                   (Round Robin)  └──► Pitch :8084
```

Chỉ khi gọi qua Service ID, `Spring Cloud LoadBalancer` mới có **danh sách** instance để lựa chọn và phân bổ luân phiên. Với URL cứng, instance thứ hai tồn tại nhưng vô dụng — đồng nghĩa mất hoàn toàn khả năng cân bằng tải phía client (Client-side Load Balancing).

### 4.3. Lý do 3: Lỏng liên kết và khả năng tự phục hồi

Gọi qua Service ID đưa vào hệ thống một lớp gián tiếp (indirection) giữa *tên* và *địa chỉ*. Lớp gián tiếp này mang lại ba hệ quả:

| Hệ quả | Giải thích |
|---|---|
| **Lỏng liên kết (Loose Coupling)** | Consumer chỉ cần biết *tên* của Provider, không cần biết Provider chạy ở máy nào, cổng nào, có mấy bản. Thay đổi hạ tầng của Provider không buộc sửa và build lại Consumer |
| **Mở rộng co giãn (Elastic Scaling)** | Thêm instance thứ 3 của Pitch Service chỉ cần khởi động container mới; nó tự đăng ký vào danh bạ và được LoadBalancer đưa vào vòng luân phiên. Không ai phải sửa cấu hình |
| **Tự phục hồi (Self-healing)** | Khi một instance chết, nó bị loại khỏi danh bạ sau thời hạn lease, Consumer tự động chỉ còn chọn các instance sống. Hệ thống **suy giảm năng lực** (còn 1 instance) chứ **không ngừng hoạt động** |

### 4.4. Minh chứng trong mã nguồn PitchOS

Khác biệt giữa hai cách gọi nằm ở duy nhất thuộc tính `url` của Feign Client:

```java
// CÁCH LÀM Ở KT1 - gắn cứng địa chỉ, KHÔNG có Service Discovery
@FeignClient(name = "pitch-service", url = "${pitch.service.url}")
public interface PitchServiceClient { ... }

// CÁCH LÀM Ở KT2 - tra cứu qua Service ID trong danh bạ Eureka
@FeignClient(name = "pitchos-pitch-service")   // chính là spring.application.name của Provider
public interface PitchServiceClient { ... }
```

> **Tiêu chí tự nghiệm thu:** việc dựng được Eureka Server và thấy danh sách dịch vụ hiện trên Dashboard **chưa đủ** để kết luận hệ thống đã có Service Discovery. Nếu Consumer vẫn gọi Provider bằng URL cố định thì Eureka chỉ là một trang web hiển thị danh sách, còn cơ chế tra cứu động hoàn toàn không được dùng. Phép thử đúng là: **xóa thuộc tính `url` khỏi Feign Client, hệ thống vẫn gọi được Provider**.

---

## 5. KẾT LUẬN

Service Registry và Service Discovery là cặp cơ chế giải quyết bài toán định vị dịch vụ trong môi trường mà địa chỉ mạng thay đổi liên tục. Service Registry (Eureka Server) giữ danh bạ; Service Discovery là cơ chế tra cứu danh bạ đó để thay một *tên logic* bằng một *địa chỉ cụ thể* ngay tại thời điểm gọi.

Ba điểm cần giữ đúng về mặt nhận thức kiến trúc:

1. Eureka Server hoạt động ở **tầng nội bộ** và **không trung chuyển dữ liệu nghiệp vụ**; nhiệm vụ tiếp nhận, định tuyến và bảo vệ request từ bên ngoài thuộc về **API Gateway** — một thành phần khác, ở tầng khác.
2. Cơ chế Heartbeat khiến danh bạ luôn **trễ hơn thực tế một khoảng hữu hạn**; hệ thống phải được thiết kế để chịu được việc gọi vào một instance vừa chết, không thể giả định danh bạ chính xác tuyệt đối.
3. Gọi qua **Service ID** là điều kiện bắt buộc để có cân bằng tải phía client, mở rộng co giãn và lỏng liên kết. Gọi qua URL cố định vô hiệu hóa cả ba lợi ích này, dù Eureka Server vẫn đang chạy.
