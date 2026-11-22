# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ CHUYÊN ĐỀ 15 PHÚT
## DÀNH RIÊNG CHO: HÙNG (DATABASE ADMINISTRATOR & BACKEND DATA ENGINEER)

> **Dự án:** PitchOS — Football Pitch Booking System (Kiến trúc SOA / Microservices)  
> **Người thực hiện:** HÙNG  
> **Trách nhiệm bảo vệ:** **2,25 / 10,0 Điểm** (Câu 1 Ý 2b: 0,75đ Lý thuyết + Câu 2 Ý 3: 1,50đ Thực nghiệm)  
> **Thời lượng thuyết trình:** **15 Phút** (15 Slides, trung bình ~1 phút / slide)  
> **Tệp PowerPoint:** `Slide_Hung_PitchOS_ChiTiet.pptx` (trong thư mục `docs/`)

---

## BẢNG PHÂN BỔ THỜI GIAN 15 PHÚT

| Slide | Nội dung chính | Thời lượng gợi ý |
| :---: | :--- | :---: |
| **01** | Bìa báo cáo chuyên đề cá nhân | **45 giây** |
| **02** | Vai trò trong nhóm & Nội dung câu hỏi thi cần trả lời | **1 phút** |
| **03** | Phân tích hành vi 3 tác nhân: Admin, Chủ sân, Người thuê | **1 phút 15 giây** |
| **04** | Từ hành vi suy ra 3 CSDL độc lập (Bounded Contexts) | **1 phút** |
| **05** | Lý thuyết: Nguyên tắc Database-per-service (Câu 1 Ý 2b) | **1 phút** |
| **06** | Lý thuyết: 4 Rủi ro kỹ thuật khi dùng chung CSDL (Câu 1 Ý 2b) | **1 phút 15 giây** |
| **07** | Thiết kế Script SQL: `pitchos_user_db` và `pitchos_pitch_db` | **1 phút** |
| **08** | Thiết kế Script SQL: `pitchos_booking_db` & Dữ liệu nạp mẫu | **1 phút** |
| **09** | Sơ đồ Thực thể Quan hệ Phân tán (Distributed ERD) | **1 phút** |
| **10** | Triết lý Khóa Logic (Logical ID) & Toàn vẹn phi tập trung | **1 phút** |
| **11** | Kiến trúc Tầng dữ liệu: Mô hình Thực thể JPA & Hibernate | **1 phút** |
| **12** | Tầng Truy cập Dữ liệu: Spring Data JPA Repository | **1 phút** |
| **13** | Thuật toán & Truy vấn Chống trùng lịch thi đấu (Điểm nhấn) | **1 phút 15 giây** |
| **14** | Thực nghiệm kiểm chứng ghi đĩa cứng & Kịch bản demo (Câu 2 Ý 3) | **1 phút** |
| **15** | Tổng kết đánh giá CĐR L1 & Sẵn sàng trả lời phản biện Q&A | **1 phút 30 giây** |
| **TỔNG** | **15 Slides theo chuẩn Barem đề thi** | **15 PHÚT** |

---

## KỊCH BẢN NÓI CHI TIẾT TỪNG PHÚT (TỪ SLIDE 1 ĐẾN SLIDE 15)

---

### SLIDE 1: BÌA BÁO CÁO CHUYÊN ĐỀ CÁ NHÂN (00:00 - 00:45)
* **Nội dung slide:** Báo cáo chuyên đề Quản trị CSDL Phân tán hệ thống PitchOS; Sinh viên: HÙNG; Vai trò: Database Administrator & Backend Data Engineer; Trọng số: 2,25/10,0 điểm.
* **Lời nói thuyết trình của Hùng:**
  > *"Kính thưa Quý Thầy/Cô trong Hội đồng chấm thi! Em tên là Hùng. Trong dự án Hệ thống Quản lý Đặt sân Bóng đá PitchOS theo kiến trúc hướng dịch vụ SOA và Microservices, em đảm nhận vị trí Quản trị Cơ sở Dữ liệu và Kỹ sư Dữ liệu Backend (Database Administrator & Backend Data Engineer).  
  > Toàn bộ phần việc của em chịu trách nhiệm trực tiếp 2,25 điểm trên thang điểm 10 của đề thi, bao gồm 0,75 điểm lý thuyết ở Câu 1 Ý 2b và 1,50 điểm thực nghiệm ở Câu 2 Ý 3.  
  > Trong 15 phút tới đây, em xin phép trình bày chi tiết hành trình từ phân tích nghiệp vụ thực tế, xây dựng 3 cơ sở dữ liệu phân tán, giải quyết bài toán chống trùng lịch thi đấu cho đến việc kiểm chứng dữ liệu vật lý trên hệ thống."*

---

### SLIDE 2: VAI TRÒ TRONG NHÓM & NỘI DUNG CÂU HỎI THI (00:45 - 01:45)
* **Nội dung slide:** Ánh xạ Câu 1 Ý 2b (0,75đ) và Câu 2 Ý 3 (1,50đ) theo đúng Barem đề bài.
* **Lời nói thuyết trình của Hùng:**
  > *"Về vai trò trong nhóm, em là người thực hiện đầu tiên ở Giai đoạn 1. Bởi vì trong kiến trúc phần mềm, nếu cơ sở dữ liệu và tầng truy cập dữ liệu chưa được hoàn thiện, thì các thành viên phụ trách dịch vụ như Hoàng (Auth), Linh (Pitch), hay Nhật (Booking) sẽ không thể kết nối hay kiểm thử nghiệp vụ khi khởi động Spring Boot.  
  > Cụ thể trong đề thi, em cần giải quyết trọn vẹn hai câu hỏi lớn:  
  > Thứ nhất là Câu 1 Ý 2b phần Lý thuyết: Giải thích nguyên tắc mỗi dịch vụ tự quản lý dữ liệu của mình (Database-per-service), lý giải vì sao không được truy cập chéo DB và phân tích các rủi ro kỹ thuật khi vi phạm.  
  > Thứ hai là Câu 2 Ý 3 phần Thực nghiệm: Cài đặt lưu trữ CSDL MySQL vật lý (không lưu bộ nhớ tạm), thể hiện cấu trúc bảng, tầng Entity/Repository JPA, thực hiện thao tác nghiệp vụ có kiểm chứng ghi đĩa, và đảm bảo tính bao đóng độc lập dữ liệu."*

---

### SLIDE 3: PHÂN TÍCH HÀNH VI 3 NHÓM NGƯỜI DÙNG ĐỂ TẠO CSDL (01:45 - 03:00)
* **Nội dung slide:** Phân tích thực tế: Quản trị viên (Admin) làm gì? Chủ sân làm gì? Người thuê sân làm gì? -> Nhu cầu dữ liệu tương ứng.
* **Lời nói thuyết trình của Hùng:**
  > *"Để thiết kế được một cơ sở dữ liệu chuẩn mực, em không vẽ bảng một cách cảm tính mà bắt đầu từ việc phân tích sâu sắc hành vi thực tế của 3 nhóm tác nhân tương tác với hệ thống PitchOS:  
  > Tác nhân thứ nhất là **Quản trị viên (Admin)**: Admin có nhu cầu quản lý người dùng, phân quyền truy cập, giám sát bảo mật. Hành vi này đòi hỏi hệ thống phải lưu trữ tài khoản, email định danh, mật khẩu được băm an toàn và vai trò quyền hạn (Role). Từ đó, em suy ra yêu cầu phải có bảng `users`.  
  > Tác nhân thứ hai là **Chủ sân (Pitch Owner)**: Chủ sân cần đăng tải các sân bóng mini, phân loại sân 5, sân 7 hay sân 10 người, quy định giá thuê mỗi giờ, cập nhật địa chỉ, tọa độ bản đồ và bật tắt trạng thái bảo trì. Từ đó, em suy ra yêu cầu bắt buộc phải có bảng `pitches`.  
  > Tác nhân thứ ba là **Người thuê sân (User / Player)**: Khách hàng tìm sân, chọn khung giờ đá từ mấy giờ đến mấy giờ, gửi đơn đặt sân và chờ chủ sân phê duyệt. Điều này phát sinh giao dịch đặt sân, đòi hỏi phải lưu người đặt, sân được đặt, thời gian bắt đầu, kết thúc, tổng tiền và trạng thái duyệt. Từ đó, em suy ra yêu cầu phải có bảng `bookings`."*

---

### SLIDE 4: TỪ HÀNH VI SUY RA 3 CƠ SỞ DỮ LIỆU ĐỘC LẬP (03:00 - 04:00)
* **Nội dung slide:** **Sơ đồ đồ họa 3 cột:** Phân tích hành vi thực tế tác nhân ➔ Ngữ cảnh nghiệp vụ (Bounded Contexts) ➔ 3 Cơ sở dữ liệu và bảng SQL vật lý.
* **Lời nói thuyết trình của Hùng:**
  > *"Kính mời Quý Thầy/Cô quan sát trên **Sơ đồ phân tích 3 cột** tại màn hình:  
  > Cột 1 là Hành vi thực tế của 3 tác nhân: Admin giám sát tài khoản, Chủ sân quản lý cơ sở vật chất, và Khách hàng thực hiện giao dịch đặt sân.  
  > Từ 3 nhóm hành vi này, em ánh xạ sang Cột 2 là 3 ranh giới ngữ cảnh nghiệp vụ (Bounded Contexts) và 3 microservice độc lập: Auth Service (Port 8081), Pitch Service (Port 8082) và Booking Service (Port 8083).  
  > Và từ đó, ở Cột 3, em suy ra 3 CSDL vật lý hoàn toàn cách ly trên MySQL 8.0: `pitchos_user_db` với bảng `users`, `pitchos_pitch_db` với bảng `pitches`, và `pitchos_booking_db` với bảng `bookings`.  
  > Đây là bằng chứng cho thấy việc tách 3 database xuất phát 100% từ phân tích nghiệp vụ thực tế, tuân thủ nguyên tắc kiến trúc Microservices."*

---

### SLIDE 5: NGUYÊN TẮC DATABASE-PER-SERVICE (CÂU 1 Ý 2b) (04:00 - 05:00)
* **Nội dung slide:** 3 trụ cột: Exclusive Ownership, Data Encapsulation, API-driven Access; So sánh với Shared DB Monolith.
* **Lời nói thuyết trình của Hùng:**
  > *"Đi vào câu hỏi lý thuyết Câu 1 Ý 2b, hệ thống PitchOS áp dụng triệt để nguyên tắc **Database-per-Service** với 3 trụ cột:  
  > Trụ cột 1 là **Quyền sở hữu độc quyền (Exclusive Data Ownership)**: Mỗi microservice chỉ sở hữu và chịu trách nhiệm toàn bộ đối với CSDL thuộc domain của mình.  
  > Trụ cột 2 là **Tính đóng gói dữ liệu (Data Encapsulation)**: CSDL vật lý là chi tiết cài đặt nội bộ (Private Detail). Tuyệt đối không cấp connection string để dịch vụ khác đọc/ghi trực tiếp vào DB của mình.  
  > Trụ cột 3 là **Truy xuất dữ liệu qua API (API-driven Access)**: Khi Booking Service cần biết đơn giá sân bóng, nó bắt buộc phải gửi HTTP GET request sang API của Pitch Service, không được SELECT chéo.  
  > Khác hoàn toàn với Monolith truyền thống gộp chung mọi bảng vào một DB gây ra mớ bòng bong quan hệ chặt chẽ."*

---

### SLIDE 6: 4 RỦI RO KỸ THUẬT KHI DÙNG CHUNG CSDL (CÂU 1 Ý 2b) (05:00 - 06:15)
* **Nội dung slide:** 4 rủi ro: Schema Coupling, Deadlock chéo, Vỡ bao đóng, Cản trở scale độc lập.
* **Lời nói thuyết trình của Hùng:**
  > *"Đề bài yêu cầu: Vì sao không nên truy cập trực tiếp CSDL của dịch vụ khác và nêu rủi ro? Em đã đúc kết được 4 rủi ro kỹ thuật mang tính sống còn:  
  > Rủi ro thứ nhất là **Ghép nối lược đồ dữ liệu (Schema Coupling)**: Nếu Booking Service SELECT trực tiếp bảng `pitches`, khi Pitch Service đổi tên cột `price_per_hour` thành `hourly_rate`, Booking Service lập tức bị lỗi thời gian chạy RuntimeException. Đội ngũ phát triển buộc phải deploy đồng loạt cả hai dịch vụ, triệt tiêu tính độc lập.  
  > Rủi ro thứ hai là **Khóa tranh chấp và Deadlock chéo**: Các transaction từ hai dịch vụ cùng cạnh tranh row-level lock trên các bảng liên quan sẽ gây ra deadlock, làm cạn kiệt thread pool và treo toàn bộ hệ thống.  
  > Rủi ro thứ ba là **Vỡ tính bao đóng**: Việc viết SQL trực tiếp sẽ bỏ qua toàn bộ logic kiểm tra hợp lệ nghiệp vụ của tầng Service.  
  > Và rủi ro thứ tư là **Nghẽn mở rộng (Bottleneck Scalability)**: Không thể scale riêng DB chịu tải lớn và không thể áp dụng kiến trúc lưu trữ đa dạng Polyglot Persistence."*

---

### SLIDE 7: THIẾT KẾ SCRIPT SQL: USER_DB VÀ PITCH_DB (06:15 - 07:15)
* **Nội dung slide:** Cấu trúc SQL bảng `users` và `pitches`; BCrypt hash; DECIMAL(12,2) cho giá tiền.
* **Lời nói thuyết trình của Hùng:**
  > *"Để hiện thực hóa vào thực nghiệm Câu 2 Ý 3, em đã biên soạn 3 script SQL độc lập:  
  > Đầu tiên là `pitchos_user_db` với bảng `users`: Điểm nhấn ở đây là mật khẩu được băm một chiều an toàn bằng thuật toán BCrypt (`$2a$10$...`), và vai trò người dùng được định nghĩa bằng ENUM (`admin`, `chusan`, `user`) ngay trong SQL để tối ưu hiệu năng.  
  > Thứ hai là `pitchos_pitch_db` với bảng `pitches`: Em sử dụng kiểu `DECIMAL(12, 2)` cho cột `price_per_hour` thay vì Float/Double để triệt tiêu hoàn toàn sai số làm tròn số học dấu phẩy động trong tính toán tài chính. Các loại sân `san_5`, `san_7`, `san_10` và trạng thái `hoat_dong`, `bao_tri` cũng được chuẩn hóa qua ENUM."*

---

### SLIDE 8: THIẾT KẾ SCRIPT SQL: BOOKING_DB & DỮ LIỆU NẠP MẪU (07:15 - 08:15)
* **Nội dung slide:** Bảng `bookings`; Seed data nạp sẵn 3 tài khoản, 4 sân bóng mẫu, 1 đơn mẫu.
* **Lời nói thuyết trình của Hùng:**
  > *"Thứ ba là `pitchos_booking_db` với bảng `bookings`: Bảng này lưu giao dịch đặt sân gồm `start_time`, `end_time`, `total_price` kiểu `DECIMAL(12,2)`, và `status` ENUM với giá trị mặc định là `'cho_duyet'`.  
  > Đặc biệt, em đã soạn thảo sẵn bộ dữ liệu nạp mẫu (Seed Data) chuẩn mực:  
  > - Nạp sẵn 3 tài khoản đại diện cho 3 vai trò: `admin`, `chusan`, `user` với mật khẩu mặc định `123456`.  
  > - Nạp sẵn 4 sân bóng mẫu: Sân 5 Cầu Giấy (300.000đ/h), Sân 7 Mỹ Đình (500.000đ/h), Sân 10 Tây Hồ (800.000đ/h), và Sân Phúc Diễn đang bảo trì để kiểm thử trường hợp từ chối đặt sân.  
  > - Nạp sẵn 1 đơn đặt mẫu để kiểm tra câu truy vấn."*

---

### SLIDE 9: SƠ ĐỒ THỰC THỂ QUAN HỆ PHÂN TÁN (DISTRIBUTED ERD) (08:15 - 09:15)
* **Nội dung slide:** **Sơ đồ đồ họa ERD Phân tán (Distributed ERD)** thể hiện 3 CSDL vật lý với các trường, khóa PK/UK và liên kết Khóa logic (Logical ID).
* **Lời nói thuyết trình của Hùng:**
  > *"Kính mời Thầy Cô quan sát **Sơ đồ Thực thể Quan hệ Phân tán (Distributed ERD)** hiển thị trên màn hình.  
  > Ba schema `pitchos_user_db`, `pitchos_pitch_db` và `pitchos_booking_db` được biểu diễn như 3 hòn đảo dữ liệu độc lập.  
  > Thưa Thầy Cô, điểm kỹ thuật cốt lõi ở đây là: **Giữa 3 bảng `users`, `pitches` và `bookings` hoàn toàn không có đường nối FOREIGN KEY vật lý**.  
  > Trong bảng `bookings`, hai cột `user_id` và `pitch_id` chỉ là kiểu `BIGINT NOT NULL` đóng vai trò là Khóa Logic (Logical ID).  
  > Thiết kế này giúp tầng dữ liệu của từng dịch vụ cách ly tuyệt đối, có thể phân tán trên 3 cụm máy chủ khác nhau mà không bị ràng buộc cơ học bởi Database Engine."*

---

### SLIDE 10: TRIẾT LÝ KHÓA LOGIC & TOÀN VẸN DỮ LIỆU PHI TẬP TRUNG (09:15 - 10:15)
* **Nội dung slide:** Giải thích Logical ID `user_id`, `pitch_id` kiểu `BIGINT NOT NULL`; Toàn vẹn qua JWT và Feign API; Xóa mềm Soft Delete.
* **Lời nói thuyết trình của Hùng:**
  > *"Vậy câu hỏi đặt ra là: Không có Foreign Key vật lý thì làm sao đảm bảo tính toàn vẹn dữ liệu?  
  > Em giải quyết vấn đề này bằng triết lý **Khóa Logic (Logical ID)** và **Toàn vẹn phi tập trung tại tầng ứng dụng (Decentralized Integrity)**:  
  > - Khi tạo đơn, `user_id` được trích xuất an toàn từ chữ ký số trong JWT Token của người dùng đã đăng nhập.  
  > - `pitch_id` được Booking Service gửi HTTP GET sang Pitch Service để xác minh sân có tồn tại và đang hoạt động hay không.  
  > Ngoài ra, hệ thống áp dụng cơ chế **Xóa mềm (Soft Delete)**: Khi một sân ngừng hoạt động, chủ sân chỉ đổi trạng thái sang `bao_tri` chứ không bao giờ DELETE dòng vật lý, giúp lịch sử các đơn đặt sân trong quá khứ không bao giờ bị mồ côi."*

---

### SLIDE 11: KIẾN TRÚC TẦNG DỮ LIỆU JPA ENTITY & HIBERNATE (10:15 - 11:15)
* **Nội dung slide:** Mã nguồn Java `@Entity` `Booking.java`, `@Enumerated(EnumType.STRING)`, `@CreationTimestamp`.
* **Lời nói thuyết trình của Hùng:**
  > *"Chuyển sang tầng lập trình hướng đối tượng, em sử dụng **Spring Data JPA kết hợp Hibernate ORM** để ánh xạ CSDL vào mã nguồn Java:  
  > Trong thực thể `Booking.java`, em khai báo tường minh `@Entity`, `@Table(name = "bookings")`. Hai trường Logical ID được ánh xạ là `Long userId` và `Long pitchId`.  
  > Em sử dụng annotation `@Enumerated(EnumType.STRING)` để lưu giá trị Enum dưới dạng chuỗi chữ trong MySQL ('cho_duyet', 'da_duyet', 'tu_choi'), giúp code không bao giờ bị sai lệch chỉ số khi mở rộng enum. Trường `createdAt` dùng `@CreationTimestamp` tự động gán nhãn thời gian từ máy chủ."*

---

### SLIDE 12: TẦNG TRUY CẬP DỮ LIỆU JPA REPOSITORY (11:15 - 12:15)
* **Nội dung slide:** Interface kế thừa `JpaRepository<T, ID>`; Derived Queries; HikariCP Connection Pool; `@Transactional`.
* **Lời nói thuyết trình của Hùng:**
  > *"Tầng Repository được em thiết kế theo mẫu DAO chuẩn mực thông qua interface `JpaRepository<T, ID>`:  
  > Nhờ kế thừa `JpaRepository`, hệ thống tự động có đầy đủ các hàm CRUD cơ bản mà không cần viết mã thủ công.  
  > Em đã xây dựng các hàm truy vấn dẫn xuất (Derived Queries) như `findByUsername`, `existsByEmail` trong UserRepository, hay lọc sân theo loại trong PitchRepository.  
  > Tầng dữ liệu này được tối ưu hiệu năng nhờ kết nối Connection Pool HikariCP có sẵn trong Spring Boot và quản lý vòng đời transaction bằng `@Transactional`, đảm bảo tự động ROLLBACK nếu có sự cố xảy ra."*

---

### SLIDE 13: THUẬT TOÁN CHỐNG TRÙNG SÂN (ĐIỂM NHẤN CỦA HÙNG) (12:15 - 13:30)
* **Nội dung slide:** **Sơ đồ trực quan 4 trường hợp giao thoa thời gian (Timeline Bars)** và Mã nguồn JPQL `SELECT COUNT(b)`.
* **Lời nói thuyết trình của Hùng:**
  > *"Kính mời Thầy Cô quan sát **Sơ đồ hình học giao thoa thời gian** ở nửa bên trái màn hình:  
  > Em mô phỏng trực quan 4 trường hợp trùng lịch: Bắt đầu trước kết thúc giữa, Bắt đầu giữa kết thúc sau, Nằm lọt bên trong, và Bao trùm toàn bộ.  
  > Cả 4 trường hợp này đều được quy về một công thức toán học tối giản:  
  > `start_old < end_new VÀ end_old > start_new`.  
  > Điểm ưu việt là: Nếu dùng toán tử BETWEEN của SQL, hệ thống sẽ bị sót trường hợp Ca 4 (khung giờ mới bao trùm hoàn toàn khung giờ cũ). Nhưng công thức toán học này bao trùm chính xác 100% các ca xung đột.  
  > Ở nửa bên phải màn hình là câu truy vấn JPQL tối ưu: `SELECT COUNT(b) FROM Booking b ...`. MySQL Engine chỉ cần đếm trên chỉ mục và trả về con số, tuyệt đối không tải toàn bộ Entity lên bộ nhớ RAM. Nếu `count > 0`, hệ thống ném ngoại lệ chặn ngay từ đầu!"*

---

### SLIDE 14: THỰC NGHIỆM KIỂM CHỨNG GHI ĐĨA CỨNG & DEMO (13:30 - 14:30)
* **Nội dung slide:** **Sơ đồ Tuần tự Xử lý Dữ liệu 6 bước (Data Sequence Diagram)** và kiểm chứng DBeaver / tệp `.ibd` InnoDB.
* **Lời nói thuyết trình của Hùng:**
  > *"Để chứng minh tính thực nghiệm theo Câu 2 Ý 3, em kính mời Thầy Cô theo dõi **Sơ đồ Tuần tự Xử lý Dữ liệu** tại màn hình:  
  > Bước 1: Khách hàng gửi request đặt Sân 5 Cầu Giấy (18:00 - 19:30).  
  > Bước 2: Booking Service chạy truy vấn kiểm tra trùng lịch ➔ Kết quả COUNT = 0 (Hợp lệ).  
  > Bước 3: Gửi OpenFeign sang Pitch Service lấy đơn giá: 300.000 VNĐ/h.  
  > Bước 4: Tính tổng tiền 450.000 VNĐ và gọi Repository INSERT vào CSDL `pitchos_booking_db`.  
  > Bước 5: InnoDB Engine COMMIT transaction và ghi dữ liệu bền vững xuống tệp `bookings.ibd` trên ổ đĩa cứng.  
  > Bước 6: Em mở DBeaver chạy lệnh SELECT kiểm chứng độc lập ➔ Bản ghi ID = 2 xuất hiện ngay lập tức trên màn hình với trạng thái `cho_duyet`.  
  > Toàn bộ luồng dữ liệu minh chứng rằng: Dịch vụ chỉ truy cập CSDL của mình; dữ liệu khác phải qua Feign API; và dữ liệu được ghi đĩa bền vững."*

---

### SLIDE 15: TỔNG KẾT ĐÁNH GIÁ & SẴN SÀNG PHẢN BIỆN (14:30 - 15:00)
* **Nội dung slide:** Đối chiếu hoàn thành 100% CĐR L1; Bảng 5 câu hỏi phản biện trọng tâm; Lời cảm ơn.
* **Lời nói thuyết trình của Hùng:**
  > *"Tổng kết lại, phần việc của em đã hoàn thành 100% tất cả các tiêu chí trong barem đề thi: Từ giải thích lý thuyết Database-per-service và 4 rủi ro ở Câu 1 Ý 2b, cho đến thiết kế 3 CSDL MySQL vật lý, mô hình ERD với Logical ID, giải thuật chống trùng sân tối ưu và kiểm chứng ghi đĩa ở Câu 2 Ý 3.  
  > Em tự tin đề xuất đạt điểm tối đa **2,25 / 2,25 Điểm** cho phần phụ trách của mình.  
  > Em đã chuẩn bị sẵn sàng cả về kiến thức lý thuyết lẫn kịch bản demo thực tế trên DBeaver. Em xin chân thành cảm ơn Quý Thầy/Cô đã lắng nghe và em rất mong nhận được những câu hỏi phản biện từ Thầy Cô ạ!"*

---

## BỘ CHÌA KHÓA TRẢ LỜI NHANH 5 CÂU HỎI PHẢN BIỆN CỦA HỘI ĐỒNG

1. **Tại sao không dùng chung 1 database?**  
   $\rightarrow$ Dùng chung DB tạo ra **Schema Coupling** (sửa bảng gây crash runtime dịch vụ khác), nguy cơ **Cross-service Deadlock** treo hệ thống, và cản trở việc scale độc lập.
2. **Không có Foreign Key thì dữ liệu có bị mồ côi?**  
   $\rightarrow$ Áp dụng **Xóa mềm (Soft Delete)** (chỉ đổi status sang `bao_tri`, không xóa cứng khỏi SQL) và kiểm tra tính hợp lệ qua JWT/Feign API trước khi lưu.
3. **Tại sao không dùng BETWEEN cho trùng lịch?**  
   $\rightarrow$ `BETWEEN` bị sót trường hợp khung giờ mới bao trùm hoàn toàn khung giờ cũ. Công thức `start_old < end_new AND end_old > start_new` là điều kiện cần và đủ trong toán học tập hợp.
4. **Nếu 2 người cùng bấm đặt sân tại cùng 1 mili-giây?**  
   $\rightarrow$ Áp dụng `@Transactional` kết hợp Khóa bi quan (**Pessimistic Locking**) hoặc trong hệ phân tán lớn dùng **Redis Distributed Lock (Redisson)** khóa theo `pitch_id`.
5. **Chứng minh dữ liệu ghi xuống đĩa cứng?**  
   $\rightarrow$ Tắt server bật lại dữ liệu vẫn còn; kiểm tra trực tiếp qua client độc lập DBeaver; tệp `bookings.ibd` của InnoDB trên ổ đĩa vật lý tăng kích thước khi transaction COMMIT.

