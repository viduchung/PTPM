# PHẦN 7: ĐÁNH GIÁ, TỰ CHẤM ĐIỂM VÀ ĐỀ XUẤT HƯỚNG PHÁT TRIỂN
**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices 2026)  
**Sinh viên thực hiện:** HÙNG (Đại diện nhóm tổng kết)  
**Trọng số điểm báo cáo:** Đánh giá tổng thể đề tài PitchOS (Chuẩn đầu ra CĐR L2)

---

## 7.1. BẢNG TỰ ĐÁNH GIÁ ĐIỂM SỐ THEO BAREM CHUẨN CỦA GIẢNG VIÊN

Dựa trên đề cương yêu cầu kỹ thuật và barem điểm chính thức của học phần (Bài kiểm tra số 2 — 10,0 điểm), nhóm tự đánh giá kết quả triển khai như sau:

| Mục Đánh Giá | Nội Dung Chi Tiết | Điểm Tối Đa | Tự Chấm | Minh Chứng Mã Nguồn & Báo Cáo |
|---|---|:---:|:---:|---|
| **Câu 1: Lý thuyết Microservices** | • 1.1: Provider vs Consumer, xử lý lỗi tích hợp (Nhật)<br>• 1.2: Vai trò Service Registry, Eureka vs Gateway, Service ID (Hoàng)<br>• 1.3: Docker Image vs Container, Dockerfile vs Compose (Linh)<br>• 1.4: 3 cấp độ trạng thái, Health Check, Log, Volume (Hùng) | **2,00** | **2,00** | `docs/kt2/CAU1_1_NHAT.md`<br>`docs/kt2/CAU1_2_HOANG.md`<br>`docs/kt2/CAU1_3_LINH.md`<br>`docs/kt2/CAU1_4_HUNG.md` |
| **Mục 2.1: Phân tích & Thiết kế Kiến trúc** | • Sơ đồ kiến trúc tích hợp và triển khai (Trước vs Sau)<br>• Phân tích ranh giới dịch vụ và nguyên tắc Database-per-service<br>• Bảng mô tả chi tiết 4 microservices và triết lý Logical ID | **1,00** | **1,00** | `docs/kt2/PHAN_2_HOANG.md`<br>`docs/kt2/PHAN_2_HUNG.md`<br>`docs/architecture/` |
| **Mục 2.2: Tích hợp & Tiêu thụ Dịch vụ (TH6)** | • Booking Service (Consumer) gọi Pitch Service (Provider) qua OpenFeign<br>• Gọi bằng **Service ID** (loại bỏ hoàn toàn URL cứng)<br>• Kiểm tra tính toàn vẹn dữ liệu đơn giá và trạng thái hoạt động<br>• Xử lý lỗi phân tán: 404 (sân không tồn tại), 502 (đơn giá lỗi), 503 (Provider sập / timeout) | **2,00** | **2,00** | `pitchos-booking-service/`<br>`docs/kt2/PHAN_3_NHAT.md`<br>`docs/testing/integration-test.md`<br>`docs/api/api-contract.md` |
| **Mục 2.3: Service Registry & Cân bằng tải (TH7)** | • Service Registry (Netflix Eureka Server) chạy độc lập cổng 8761<br>• Đăng ký thành công các Eureka Client<br>• **2 instance Pitch Service** chạy song song (cổng 8082 và 8084)<br>• Gửi 20 request liên tiếp qua Consumer chứng minh Spring Cloud LoadBalancer chia tải | **1,50** | **1,50** | `pitchos-service-registry/`<br>`docs/kt2/PHAN_4_HOANG.md`<br>`docs/testing/service-discovery-test.md`<br>`postman/collection.json` |
| **Mục 2.4: Container hóa & Vận hành Docker (TH8)** | • Dockerfile multi-stage cho toàn bộ các dịch vụ (chạy quyền non-root `appuser`)<br>• File `docker-compose.yml` điều phối 8 container trong mạng `pitchos-network`<br>• Cấu hình Healthcheck và `depends_on: condition: service_healthy`<br>• Bảo toàn dữ liệu qua Docker Named Volumes (chứng minh qua lệnh down/up)<br>• Phân tích nhật ký log và phân tích chuyên sâu 1 tình huống sự cố thực tế | **2,00** | **2,00** | `docker-compose.yml`<br>`docs/kt2/PHAN_5_LINH.md`<br>`docs/kt2/PHAN_6_HUNG.md`<br>`scripts/`<br>`docs/testing/operation-test.md` |
| **Chất lượng Báo cáo & Tài liệu** | Báo cáo cấu trúc 7 phần hoàn chỉnh, có ảnh chụp minh chứng thực tế, sơ đồ kiến trúc chuẩn mực, hướng dẫn khởi chạy máy sạch chi tiết | **1,50** | **1,50** | `README.md`, thư mục `docs/` |
| **TỔNG ĐIỂM DỰ KIẾN** | **Toàn bộ hệ thống hoạt động hoàn hảo 100%** | **10,00** | **10,00** | **Xếp loại: XUẤT SẮC** |

---

## 7.2. TỔNG KẾT CÁC BẪY KỸ THUẬT VÀ GIẢI PHÁP KHẮC PHỤC TRONG DỰ ÁN

Trong quá trình hiện thực hóa hệ thống từ KT1 lên KT2, nhóm đã gặp và giải quyết triệt để 6 thách thức kỹ thuật lớn:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. BẪY PHIÊN BẢN (VERSION COMPATIBILITY)                                    │
│    • Vấn đề: Spring Boot 3.2.x không tương thích các bản Spring Cloud cũ    │
│    • Khắc phục: Chuẩn hóa toàn nhóm dùng Spring Cloud bản 2023.0.1          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. BẪY LOCALHOST TRONG CONTAINER                                            │
│    • Vấn đề: Gọi localhost từ container sẽ tự trỏ vào chính nó              │
│    • Khắc phục: Khai báo Service Name mạng Docker (mysql-pitch, registry)   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. BẪY GỌI URL CỨNG TRONG FEIGN CLIENT                                      │
│    • Vấn đề: Feign dùng url = "http://localhost:8082" làm vô hiệu Discovery │
│    • Khắc phục: Xóa bỏ thuộc tính url, chỉ dùng @FeignClient(name = "...")  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. BẪY RACE CONDITION KHI KHỞI TẠO DỮ LIỆU MẪU (2 INSTANCE PITCH)           │
│    • Vấn đề: 2 container Pitch cùng bật, DataInitializer chèn trùng lặp     │
│    • Khắc phục: pitchos-pitch-service-2 chờ pitchos-pitch-service-1 healthy │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. BẪY BẢO MẬT: LỘ MẬT KHẨU VÀ TOKEN TRONG LOG                             │
│    • Vấn đề: DataInitializer in mật khẩu mẫu ra console, vi phạm TH8        │
│    • Khắc phục: Xóa dòng log in pass, gỡ .env khỏi git, chỉ commit mẫu      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 6. BẪY SỤP ĐỔ DÂY CHUYỀN (CASCADING FAILURE)                                │
│    • Vấn đề: Provider chậm làm nghẽn luồng Consumer                         │
│    • Khắc phục: Feign timeout 2s/3s, PitchGateway bắt lỗi trả HTTP 503      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7.3. ĐỀ XUẤT HƯỚNG PHÁT TRIỂN VÀ NÂNG CẤP HỆ THỐNG TRONG TƯƠNG LAI

Để phát triển PitchOS từ một đồ án môn học thành sản phẩm thương mại hoàn chỉnh phục vụ hàng nghìn người dùng đặt sân thực tế, hệ thống có thể mở rộng theo các hướng sau:

### 1. Bổ sung API Gateway (Spring Cloud Gateway)
* **Hiện trạng KT2:** Client đang gọi trực tiếp vào cổng của từng Microservice (8081 cho Auth, 8083 cho Booking).
* **Nâng cấp:** Đặt Spring Cloud Gateway tại cổng biên (cổng `80` hoặc `443`), đóng vai trò là điểm tiếp nhận duy nhất cho toàn bộ Frontend Web và Mobile App. API Gateway sẽ thực hiện:
  * Kiểm tra tập trung JWT Token (Centralized Authentication).
  * Giới hạn tần suất gọi API (Rate Limiting với Redis Token Bucket) để chống tấn công DDoS.
  * Ẩn giấu hoàn toàn cấu trúc mạng và các cổng nội bộ của các microservice phía sau tường lửa.

### 2. Tích hợp Circuit Breaker nâng cao với Resilience4j
* **Hiện trạng KT2:** Sử dụng cơ chế Timeout và Exception Handler cơ bản của OpenFeign để trả về lỗi 503.
* **Nâng cấp:** Tích hợp bộ ngắt mạch **Resilience4j Circuit Breaker**:
  * Khi tỷ lệ lỗi từ Provider vượt quá 50% trong một khoảng thời gian, Circuit Breaker tự động chuyển sang trạng thái `OPEN` (ngắt mạch hoàn toàn), từ chối ngay lập tức các request tiếp theo mà không cần gửi qua mạng.
  * Cung cấp hàm **Fallback** thông minh: khi Pitch Service sập, Booking Service có thể lấy dữ liệu sân bóng từ bộ nhớ đệm (Cache) tạm thời để khách hàng vẫn xem được danh sách sân.

### 3. Giải pháp Khóa Phân Tán (Distributed Lock) khi Scale Booking Service
* **Hiện trạng KT2:** Cơ chế chống trùng lịch (Double Booking) của Booking Service đang sử dụng `synchronized` trên `ConcurrentHashMap` trong bộ nhớ RAM của một tiến trình Java đơn lẻ. Do đó, Booking Service hiện tại bắt buộc phải chạy 1 instance.
* **Nâng cấp:** Khi nhu cầu đặt sân tăng cao và cần mở rộng Booking Service lên 3–5 instances chạy song song, cơ chế khóa RAM cục bộ sẽ không còn tác dụng. Giải pháp tối ưu là sử dụng **Khóa phân tán (Distributed Lock với Redis / Redlock)**:
  * Trước khi kiểm tra trùng lịch và lưu đơn, instance Booking sẽ xin giữ khóa tài nguyên theo `pitch_id` trên máy chủ Redis tập trung.
  * Nhờ đó, ngay cả khi 2 khách hàng gửi request vào 2 instance Booking khác nhau cùng 1 phần nghìn giây, chỉ duy nhất 1 request chiếm được khóa để tạo đơn thành công, loại trừ 100% rủi ro đặt trùng lịch.

### 4. Triển khai Giám sát tập trung (Prometheus & Grafana) và Distributed Tracing (Micrometer Tracing / Zipkin)
* Thu thập toàn bộ số liệu đo lường (Metrics) từ endpoint `/actuator/prometheus` của các container để vẽ biểu đồ trực quan hóa tài nguyên CPU, RAM, thời gian phản hồi (Response Time) và số lượng đơn đặt theo giờ trên Grafana Dashboard.
* Gắn mã định danh tương quan (Correlation ID / Trace ID) xuyên suốt từ Client $\rightarrow$ Gateway $\rightarrow$ Booking $\rightarrow$ Pitch để theo dõi trọn vẹn vòng đời của một request qua các container phân tán.
