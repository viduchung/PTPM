# TÀI LIỆU HƯỚNG DẪN THUYẾT TRÌNH & NỘI DUNG SLIDE CHI TIẾT
# DÀNH CHO: HÙNG (DATABASE ADMINISTRATOR & BACKEND DATA ENGINEER)

**Học phần:** Kiến trúc phần mềm / Phát triển phần mềm  
**Đề tài:** PitchOS — Football Pitch Booking System (Kiến trúc SOA / Microservices)  
**Thành viên:** HÙNG  
**Vai trò:** Quản trị Cơ sở Dữ liệu & Kỹ sư Dữ liệu Backend (Database Administrator & Backend Data Engineer)  
**Trọng số đánh giá:** **2,25 / 10,0 Điểm** (Câu 1 Ý 2b: 0,75đ Lý thuyết + Câu 2 Ý 3: 1,50đ Thực nghiệm)  
**File trình chiếu:** `docs/PitchOS-Bao-Cao-Hung.pptx` (hoặc `Downloads/PitchOS-Bao-Cao-Hung.pptx`)

---

## MỤC LỤC TÀI LIỆU
1. [Khung phân bổ thời gian & Phong thái thuyết trình](#1-khung-phân-bổ-thời-gian--phong-thái-thuyết-trình)
2. [Chi tiết từng Slide & Kịch bản thuyết trình từng chữ](#2-chi-tiết-từng-slide--kịch-bản-thuyết-trình-từng-chữ)
   - [Slide 1: Bìa Báo Cáo Chuyên Đề Cá Nhân](#slide-1-bìa-báo-cáo-chuyên-đề-cá-nhân)
   - [Slide 2: Mục Tiêu & Phạm Vi Nhiệm Vụ (Barem Điểm)](#slide-2-mục-tiêu--phạm-vi-nhiệm-vụ-barem-điểm)
   - [Slide 3: Nguyên Tắc Database-per-Service](#slide-3-nguyên-tắc-database-per-service)
   - [Slide 4: 4 Rủi Ro Kỹ Thuật Khi Dùng Chung CSDL](#slide-4-4-rủi-ro-kỹ-thuật-khi-dùng-chung-csdl)
   - [Slide 5: Lược Đồ 3 CSDL Phân Tán Của PitchOS](#slide-5-lược-đồ-3-csdl-phân-tán-của-pitchos)
   - [Slide 6: Mô Hình ERD Phân Tán & Triết Lý Khóa Logic](#slide-6-mô-hình-erd-phân-tán--triết-lý-khóa-logic)
   - [Slide 7: Kiến Trúc Tầng Dữ Liệu JPA Entity & Repository](#slide-7-kiến-trúc-tầng-dữ-liệu-jpa-entity--repository)
   - [Slide 8: Thuật Toán & Truy Vấn Chống Trùng Lịch Thi Đấu](#slide-8-thuật-toán--truy-vấn-chống-trùng-lịch-thi-đấu)
   - [Slide 9: Thực Nghiệm Kiểm Chứng Ghi Đĩa Cứng & Kịch Bản Demo](#slide-9-thực-nghiệm-kiểm-chứng-ghi-đĩa-cứng--kịch-bản-demo)
   - [Slide 10: Tổng Kết Đánh Giá & Khẳng Định Kết Quả](#slide-10-tổng-kết-đánh-giá--khẳng-định-kết-quả)
3. [Kịch bản Demo trực tiếp trên DBeaver / Workbench (Step-by-step)](#3-kịch-bản-demo-trực-tiếp-trên-dbeaver--workbench)
4. [Bộ 5 Câu hỏi phản biện thường gặp của Hội đồng & Câu trả lời điểm 10](#4-bộ-5-câu-hỏi-phản-biện-thường-gặp-của-hội-đồng)

---

## 1. KHUNG PHÂN BỔ THỜI GIAN & PHONG THÁI THUYẾT TRÌNH

* **Tổng thời gian trình bày của Hùng:** 3 — 5 phút (khi nhóm bảo vệ chung hoặc khi Thầy/Cô gọi riêng từng người).
* **Phân bổ thời gian gợi ý:**
  - Slide 1 & 2 (Mở đầu & Mục tiêu): 30 giây.
  - Slide 3 & 4 (Lý thuyết C1 Ý 2b - 0,75đ): 1 phút.
  - Slide 5, 6, 7 (Kiến trúc CSDL & Tầng JPA): 1 phút 15 giây.
  - Slide 8 (Điểm nhấn Thuật toán chống trùng lịch): 45 giây.
  - Slide 9 & 10 (Kiểm chứng ghi đĩa & Kết luận C2 Ý 3 - 1,50đ): 45 giây.
* **Phong thái kỹ sư chuyên nghiệp:**
  - Tự tin, nói to, rõ ràng, gãy gọn.
  - Sử dụng chính xác thuật ngữ kỹ thuật chuyên ngành: *Bounded Context, Exclusive Ownership, Schema Coupling, Cross-service Deadlock, Logical ID, Decentralized Data Integrity, Overlapping Time-intervals, COUNT Query Optimization, InnoDB Disk Storage*.
  - Nhấn mạnh vào sản phẩm thực tế: Không chỉ nói lý thuyết suông, mà đã cài đặt hoàn chỉnh 3 CSDL MySQL, chạy thực tế và kiểm chứng bằng SQL.

---

## 2. CHI TIẾT TỪNG SLIDE & KỊCH BẢN THUYẾT TRÌNH TỪNG CHỮ

---

### SLIDE 1: BÌA BÁO CÁO CHUYÊN ĐỀ CÁ NHÂN

* **Tiêu đề chính:** BÁO CÁO CHUYÊN ĐỀ QUẢN TRỊ CƠ SỞ DỮ LIỆU PHÂN TÁN
* **Đề tài:** Hệ thống quản lý đặt sân bóng đá PitchOS (Kiến trúc SOA / Microservices)
* **Thành viên:** HÙNG
* **Vai trò:** Quản trị Cơ sở Dữ liệu & Kỹ sư Dữ liệu Backend (Database Administrator & Backend Data Engineer)
* **Trọng số:** 2,25 / 10,0 Điểm (Câu 1 Ý 2b: 0,75đ + Câu 2 Ý 3: 1,50đ)

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Kính thưa Quý Thầy/Cô trong Hội đồng chấm thi! Em là Hùng, phụ trách vai trò Quản trị Cơ sở dữ liệu và Kỹ sư Dữ liệu Backend của dự án PitchOS.  
> Hôm nay, em xin phép đại diện nhóm trình bày chuyên đề kỹ thuật chuyên sâu về Thiết kế Cơ sở dữ liệu Phân tán và Quản lý dữ liệu trong kiến trúc hướng dịch vụ.  
> Toàn bộ phần việc của em chịu trách nhiệm trực tiếp 2,25 điểm trên thang điểm 10 của đề thi, bao gồm 0,75 điểm lý thuyết ở Câu 1 Ý 2b và 1,50 điểm thực nghiệm ở Câu 2 Ý 3."*

---

### SLIDE 2: MỤC TIÊU & PHẠM VI NHIỆM VỤ (BAREM ĐIỂM)

* **Nội dung hiển thị:**
  - **Cột trái - Câu 1 Ý 2b (0,75đ):** Nguyên tắc Database-per-service, giải thích vì sao cấm truy cập chéo DB, phân tích 4 rủi ro kỹ thuật (Schema Coupling, Deadlock chéo, vỡ bao đóng, cản trở scale).
  - **Cột phải - Câu 2 Ý 3 (1,50đ):** Lưu trữ CSDL MySQL vật lý (không lưu RAM), mô hình Entity/Repository JPA, 3 schemas độc lập, mô hình ERD với Logical ID, thuật toán chống trùng sân, kiểm chứng ghi đĩa trên DBeaver.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Trước khi đi vào chi tiết, em xin phép điểm nhanh qua các yêu cầu trong barem đề thi mà phần báo cáo của em sẽ giải quyết trọn vẹn:  
> Thứ nhất, ở phần Lý thuyết (Câu 1 Ý 2b), em sẽ phân tích bản chất của nguyên tắc Database-per-service và chỉ ra 4 rủi ro sống còn nếu một hệ thống vi phạm nguyên tắc này.  
> Thứ hai, ở phần Thực nghiệm (Câu 2 Ý 3), em đã xây dựng hoàn chỉnh 3 cơ sở dữ liệu MySQL độc lập, thiết kế tầng JPA Entity - Repository, sử dụng mô hình khóa logic không Foreign Key vật lý, và cài đặt một thuật toán kiểm tra chống trùng lịch thi đấu tối ưu về toán học và hiệu năng câu truy vấn. Cuối cùng là chứng minh dữ liệu đã được ghi bền vững xuống đĩa cứng."*

---

### SLIDE 3: NGUYÊN TẮC DATABASE-PER-SERVICE

* **Nội dung hiển thị:** 3 trụ cột thiết kế dữ liệu độc lập
  1. *Quyền sở hữu độc quyền (Exclusive Data Ownership):* Mỗi dịch vụ chỉ sở hữu CSDL thuộc Bounded Context của mình.
  2. *Tính đóng gói dữ liệu (Data Encapsulation):* CSDL là thành phần nội bộ (private detail), tuyệt đối không cấp quyền truy cập chéo.
  3. *Truy xuất qua RESTful API (API-driven Access):* Khi dịch vụ khác cần dữ liệu, bắt buộc phải gọi qua HTTP/REST công khai.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Thưa Thầy Cô, trong kiến trúc nguyên khối truyền thống, các dịch vụ thường dùng chung một CSDL (Shared Database). Điều này dẫn đến sự phụ thuộc ràng buộc lẫn nhau.  
> Vì vậy, trong PitchOS, nhóm em áp dụng nghiêm ngặt nguyên tắc **Database-per-Service** với 3 trụ cột:  
> 1. Quyền sở hữu độc quyền: Dịch vụ xác thực (Auth Service) độc quyền quản lý CSDL người dùng (pitchos_user_db); Dịch vụ sân bóng (Pitch Service) quản lý CSDL sân bóng (pitchos_pitch_db); Dịch vụ đặt sân (Booking Service) quản lý CSDL đặt sân (pitchos_booking_db).  
> 2. Tính đóng gói: CSDL là private detail của dịch vụ. Không có dịch vụ nào được cấp connection string để chọc trực tiếp vào DB của dịch vụ khác.  
> 3. Truy xuất qua API: Khi Dịch vụ đặt sân (Booking Service) cần biết giá sân, dịch vụ này bắt buộc phải gửi một HTTP GET request sang API `/api/v1/pitches/{id}` của Dịch vụ sân bóng (Pitch Service), tuyệt đối không SELECT chéo sang bảng sân bóng (pitches)."*

---

### SLIDE 4: 4 RỦI RO KỸ THUẬT KHI DÙNG CHUNG CSDL

* **Nội dung hiển thị:** Trả lời trực diện câu hỏi *"Vì sao một dịch vụ không nên truy cập trực tiếp CSDL của dịch vụ khác? Nêu rủi ro..."*
  1. *Ghép nối lược đồ dữ liệu (Schema Coupling):* Sửa cột, xóa cột gây lỗi RuntimeException dây chuyền, phá hỏng khả năng phát hành độc lập.
  2. *Khóa tranh chấp và Deadlock chéo (Cross-service Deadlock):* Tranh chấp khóa dòng giữa các transaction từ nhiều service gây treo thread pool toàn hệ thống.
  3. *Phá vỡ tính bao đóng (Breaking Business Encapsulation):* Service ngoài tự ý sửa DB bỏ qua các tầng kiểm tra nghiệp vụ hợp lệ.
  4. *Cản trở mở rộng độc lập (Hindering Scalability):* Tắc nghẽn I/O tại một máy chủ DB chung, tước đoạt cơ hội dùng lưu trữ đa dạng (Polyglot Persistence).

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Đề bài có đặt câu hỏi: Vì sao một dịch vụ không nên truy cập trực tiếp CSDL của dịch vụ khác và rủi ro xảy ra là gì?  
> Qua nghiên cứu và thực nghiệm, em đúc kết được 4 rủi ro kỹ thuật nghiêm trọng:  
> Rủi ro thứ nhất là **Schema Coupling**: Nếu Dịch vụ đặt sân (Booking Service) SELECT trực tiếp bảng sân bóng (pitches), khi Dịch vụ sân bóng (Pitch Service) đổi tên cột `price_per_hour` thành `hourly_rate`, Dịch vụ đặt sân lập tức bị crash runtime. Cả hai đội ngũ buộc phải phối hợp deploy cùng lúc, làm mất hoàn toàn tính phát hành độc lập.  
> Rủi ro thứ hai là **Deadlock chéo**: Hai transaction từ hai service khác nhau tranh chấp khóa dòng trên hai bảng liên quan sẽ gây ra deadlock, làm treo toàn bộ luồng xử lý của hệ thống.  
> Rủi ro thứ ba là **Vỡ tính bao đóng**: Một service ngoài tự ý INSERT dữ liệu mà không qua tầng Service Layer sẽ bỏ qua toàn bộ logic xác thực nghiệp vụ.  
> Và rủi ro thứ tư là **Nghẽn mở rộng (Bottleneck Scalability)**: Không thể scale riêng DB chịu tải cao và không thể áp dụng Polyglot Persistence."*

---

### SLIDE 5: LƯỢC ĐỒ 3 CSDL PHÂN TÁN CỦA PITCHOS

* **Nội dung hiển thị:**
  - `CSDL người dùng (pitchos_user_db)`: Bảng người dùng (users) — id, username, email, password (BCrypt), role (ENUM), created_at.
  - `CSDL sân bóng (pitchos_pitch_db)`: Bảng sân bóng (pitches) — id, name, pitch_type (ENUM), price_per_hour (DECIMAL 12,2), status (ENUM).
  - `CSDL đặt sân (pitchos_booking_db)`: Bảng đơn đặt (bookings) — id, user_id (Logical ID), pitch_id (Logical ID), start_time, end_time, total_price (DECIMAL 12,2), status (ENUM).

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Để hiện thực hóa lý thuyết trên vào thực nghiệm (Câu 2 Ý 3), em đã xây dựng 3 CSDL MySQL độc lập tương ứng với 3 Bounded Context:  
> CSDL thứ nhất là `pitchos_user_db` gồm bảng `users`, lưu trữ tài khoản, mật khẩu được băm một chiều an toàn bằng BCrypt và phân quyền người dùng qua ENUM.  
> CSDL thứ hai là `pitchos_pitch_db` gồm bảng `pitches`, quản lý thông số kỹ thuật sân. Ở đây, em đặc biệt sử dụng kiểu `DECIMAL(12,2)` cho cột `price_per_hour` để triệt tiêu hoàn toàn sai số làm tròn số học dấu phẩy động khi tính tiền.  
> CSDL thứ ba là `pitchos_booking_db` gồm bảng `bookings`, quản lý toàn bộ giao dịch đặt sân và trạng thái phê duyệt của chủ sân."*

---

### SLIDE 6: MÔ HÌNH ERD PHÂN TÁN & TRIẾT LÝ KHÓA LOGIC

* **Nội dung hiển thị:**
  - Khẳng định kỹ thuật: **TUYỆT ĐỐI KHÔNG DÙNG FOREIGN KEY VẬT LÝ**.
  - Bảng đơn đặt (bookings) lưu `user_id` và `pitch_id` dưới dạng `BIGINT NOT NULL` thông thường (Logical ID).
  - Toàn vẹn dữ liệu được đảm bảo tại tầng ứng dụng (Decentralized Data Integrity) thông qua JWT Claims và HTTP RESTful Call.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Một điểm nhấn then chốt trong thiết kế ERD phân tán của em là: **Trong bảng `bookings`, tuyệt đối không có bất kỳ một ràng buộc FOREIGN KEY vật lý nào sang bảng `users` hay `pitches`**.  
> Cột `user_id` và `pitch_id` chỉ được khai báo là kiểu `BIGINT NOT NULL` - đóng vai trò là **Logical ID**.  
> Vậy hệ thống đảm bảo toàn vẹn tham chiếu như thế nào?  
> Đó là thông qua **Toàn vẹn phi tập trung tại tầng ứng dụng (Decentralized Integrity)**:  
> Khi tạo đơn, `user_id` được trích xuất an toàn từ chữ ký số JWT của người dùng đã đăng nhập.  
> Còn `pitch_id` được Dịch vụ đặt sân (Booking Service) gửi HTTP GET sang Dịch vụ sân bóng (Pitch Service) để kiểm tra xem sân có tồn tại và đang hoạt động hay không.  
> Thiết kế này giúp tầng lưu trữ của các service độc lập hoàn toàn, sẵn sàng tách ra các máy chủ vật lý riêng biệt trong tương lai."*

---

### SLIDE 7: KIẾN TRÚC TẦNG DỮ LIỆU JPA ENTITY & REPOSITORY

* **Nội dung hiển thị:**
  - Mô hình Thực thể (JPA Entity): `@Entity`, `@Table(name = "...")`, `@Enumerated(EnumType.STRING)`, `@CreationTimestamp`, `@Column(precision = 12, scale = 2)`.
  - Tầng Repository: Kế thừa `JpaRepository<T, ID>`, các hàm Derived Queries (`findByUsername`, `existsByEmail`, `findByPitchTypeAndStatus`).
  - Quản lý Transaction và HikariCP Connection Pool tự động.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Về kiến trúc lập trình truy cập dữ liệu, em áp dụng mẫu thiết kế DAO và ORM bằng Spring Data JPA kết hợp Hibernate:  
> Các thực thể `User`, `Pitch`, `Booking` được ánh xạ tường minh bằng các annotation của JPA. Em dùng `@Enumerated(EnumType.STRING)` để đảm bảo tính nhất quán tuyệt đối giữa mã nguồn Java và kiểu ENUM trong MySQL.  
> Tầng Repository kế thừa interface `JpaRepository`, giúp tự động hóa toàn bộ các thao tác thêm, sửa, xóa, tìm kiếm theo khóa chính mà không cần viết SQL thủ công. Đồng thời, Spring Data JPA tự động quản lý Transaction và Connection Pool qua HikariCP, đảm bảo hiệu năng và tính ổn định cao."*

---

### SLIDE 8: THUẬT TOÁN & TRUY VẤN CHỐNG TRÙNG LỊCH THI ĐẤU

* **Nội dung hiển thị:**
  - Bài toán nghiệp vụ: Chống Overbooking / Double-booking.
  - Công thức toán học kiểm tra giao thoa:
    $$\begin{cases} T_{\text{start\_old}} < T_{\text{end\_new}} \\ T_{\text{end\_old}} > T_{\text{start\_new}} \end{cases}$$
  - Loại trừ các đơn có trạng thái `tu_choi`.
  - Cài đặt JPQL tối ưu:
    ```java
    @Query("SELECT COUNT(b) FROM Booking b " +
           "WHERE b.pitchId = :pitchId " +
           "  AND b.status <> com.pitchos.booking.entity.BookingStatus.tu_choi " +
           "  AND b.startTime < :endTime " +
           "  AND b.endTime > :startTime")
    Long countOverlappingBookings(@Param("pitchId") Long pitchId,
                                  @Param("startTime") LocalDateTime start,
                                  @Param("endTime") LocalDateTime end);
    ```
  - Tối ưu hiệu năng: Đếm `COUNT` trực tiếp tại MySQL Engine, không load Entity lên RAM.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Đến với phần điểm nhấn kỹ thuật quan trọng nhất của em: **Thuật toán chống trùng lịch thi đấu (Anti-Double Booking)**.  
> Trong nghiệp vụ thuê sân bóng, rủi ro lớn nhất là hai đội bóng cùng đặt một sân trong cùng một khung giờ.  
> Em đã giải quyết bài toán này bằng công thức toán học kiểm tra giao thoa khoảng thời gian: Đơn cũ và đơn mới giao nhau khi và chỉ khi: `start_old < end_new VÀ end_old > start_new`. Công thức này bao quát trọn vẹn cả 4 trường hợp trùng lịch. Đồng thời, nếu đơn cũ đã bị từ chối (`status = 'tu_choi'`), khung giờ đó được mở lại tự do.  
> Về mặt triển khai trong code, em viết trực tiếp câu truy vấn JPQL tối ưu trong `BookingRepository`. Em sử dụng hàm `SELECT COUNT(b)` để Database Engine chỉ cần trả về số lượng xung đột (`0` hoặc `> 0`), tuyệt đối không load toàn bộ bản ghi lên RAM của Spring Boot.  
> Nếu kết quả `> 0`, hệ thống ném ra ngoại lệ từ chối ngay lập tức, bảo vệ tính đúng đắn của dữ liệu."*

---

### SLIDE 9: THỰC NGHIỆM KIỂM CHỨNG GHI ĐĨA CỨNG & KỊCH BẢN DEMO

* **Nội dung hiển thị:**
  - Kịch bản nghiệp vụ: User ID = 3 đặt Sân ID = 1 (18:00 - 19:30).
  - Luồng: Kiểm tra trùng sân (count = 0) -> Lấy giá sân qua OpenFeign (300.000đ/h) -> Tính tổng tiền (450.000đ) -> Lưu đĩa `cho_duyet`.
  - Câu lệnh SQL kiểm chứng trực tiếp trên DBeaver / Workbench:
    ```sql
    SELECT id, user_id, pitch_id, start_time, end_time, total_price, status, created_at 
    FROM pitchos_booking_db.bookings 
    ORDER BY id DESC LIMIT 1;
    ```
  - Xác nhận lưu bền vững xuống tệp `.ibd` của InnoDB Storage Engine trên đĩa cứng.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Để chứng minh dữ liệu được lưu bền vững vào đĩa cứng thay vì chỉ lưu tạm trên RAM (theo đúng yêu cầu Câu 2 Ý 3), em đã xây dựng kịch bản kiểm chứng thực nghiệm:  
> Khách hàng `user` đặt Sân 5 Cầu Giấy từ 18:00 đến 19:30.  
> Dịch vụ kiểm tra trùng lịch trả về 0, gọi API sang Pitch Service lấy đơn giá 300.000đ, tính ra tổng tiền 450.000đ và lưu đơn với trạng thái `cho_duyet`.  
> Ngay sau đó, em mở DBeaver và chạy câu lệnh `SELECT ... FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1;`.  
> Kết quả hiển thị rõ ràng bản ghi mới nhất với đầy đủ các trường dữ liệu, được ghi bền vững vào tệp dữ liệu vật lý `.ibd` của InnoDB Engine trên ổ cứng máy chủ."*

---

### SLIDE 10: TỔNG KẾT ĐÁNH GIÁ & KHẲNG ĐỊNH KẾT QUẢ

* **Nội dung hiển thị:**
  - Đối chiếu hoàn thành 100% tiêu chí đề thi:
    + Câu 1 Ý 2b (0,75đ): Lý giải Database-per-service & 4 rủi ro kỹ thuật.
    + Câu 2 Ý 3 (1,50đ): Lưu MySQL, JPA Entity/Repository, kiểm chứng ghi đĩa, cách ly dữ liệu.
  - Khẳng định kết quả: Đạt tuyệt đối 2,25 / 2,25 điểm.
  - Sẵn sàng phản biện trước Hội đồng.

> **KỊCH BẢN NÓI (SPEECH SCRIPT):**  
> *"Tổng kết lại, phần báo cáo của em đã giải quyết trọn vẹn 100% các tiêu chí trong barem: từ phân tích lý thuyết chuyên sâu đến cài đặt thực tế 3 CSDL phân tán, giải thuật chống trùng sân tối ưu và minh chứng dữ liệu vật lý.  
> Em tự tin rằng phần thực hiện này hoàn toàn xứng đáng đạt điểm tối đa **2,25 / 2,25 Điểm**.  
> Em xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe và em sẵn sàng trả lời các câu hỏi phản biện của Thầy Cô ạ!"*

---

## 3. KỊCH BẢN DEMO TRỰC TIẾP TRÊN DBEAVER / WORKBENCH

Khi Thầy/Cô yêu cầu: *"Em hãy demo chứng minh phần quản trị CSDL của em"*, Hùng thực hiện đúng 4 bước sau trên màn hình:

### Bước 1: Mở DBeaver / MySQL Workbench (Show 3 Database độc lập)
* Chỉ chuột vào cây thư mục Databases trên DBeaver:
  - `pitchos_user_db`
  - `pitchos_pitch_db`
  - `pitchos_booking_db`
* **Nói với Thầy Cô:** *"Thưa Thầy Cô, đây là 3 database hoàn toàn độc lập của 3 microservice, chạy trên port 3306."*

### Bước 2: Chứng minh không có Foreign Key vật lý
* Chạy lệnh trên DBeaver:
  ```sql
  SHOW CREATE TABLE pitchos_booking_db.bookings;
  ```
* **Chỉ vào màn hình:** *"Thầy Cô có thể thấy ở đây, cột `user_id` và `pitch_id` chỉ là `BIGINT NOT NULL`, hoàn toàn không có mệnh đề `CONSTRAINT ... FOREIGN KEY`. Toàn vẹn dữ liệu được đảm bảo qua tầng ứng dụng và API."*

### Bước 3: Thực hiện thao tác đặt sân (Gọi API qua Swagger / Postman)
* Mở Swagger UI của Booking Service (`http://localhost:8083/swagger-ui.html`) hoặc Postman.
* Gửi request `POST /api/v1/bookings`:
  ```json
  {
    "pitchId": 1,
    "startTime": "2026-10-29T18:00:00",
    "endTime": "2026-10-29T19:30:00"
  }
  ```
* Nhận về kết quả `201 Created` với `totalPrice = 450000.0` và `status = "cho_duyet"`.

### Bước 4: Chạy câu lệnh SQL kiểm tra ghi đĩa
* Quay lại DBeaver chạy lệnh:
  ```sql
  SELECT id, user_id, pitch_id, start_time, end_time, total_price, status, created_at 
  FROM pitchos_booking_db.bookings 
  ORDER BY id DESC LIMIT 1;
  ```
* **Chỉ vào kết quả:** *"Bản ghi ID mới nhất vừa được thêm vào bảng, `total_price` được tính chuẩn 450.000 VNĐ, trạng thái là `cho_duyet`. Dữ liệu đã được ghi bền vững xuống ổ đĩa vật lý."*

### Bước 5 (Bonus điểm cộng): Thử đặt trùng giờ để show thuật toán bắt lỗi
* Gửi lại request với khung giờ giao thoa (ví dụ: `18:30:00` đến `20:00:00` cùng sân ID 1).
* Hệ thống trả về `400 Bad Request` hoặc `409 Conflict` kèm thông báo: *"Khung giờ này sân đã có người đặt!"*.
* **Nói với Thầy Cô:** *"Hệ thống đã chặn ngay lập tức nhờ câu truy vấn JPQL kiểm tra giao thoa thời gian mà em đã trình bày trong slide."*

---

## 4. BỘ 5 CÂU HỎI PHẢN BIỆN THƯỜNG GẶP CỦA HỘI ĐỒNG

---

### Câu hỏi 1: *"Tại sao nhóm em không dùng chung một Database rồi phân quyền user hoặc tạo các bảng chung cho dễ JOIN dữ liệu?"*
> **Câu trả lời chuẩn của Hùng:**  
> *"Dạ thưa Thầy/Cô, việc dùng chung Database là tư duy của kiến trúc Monolith. Trong kiến trúc SOA/Microservices, nếu dùng chung DB, hệ thống sẽ rơi vào cái bẫy **Schema Coupling** (Ghép nối lược đồ). Chỉ cần một team sửa cấu trúc cột của bảng `pitches`, service của team khác sẽ lập tức bị lỗi runtime. Hơn nữa, việc dùng chung DB tạo ra nguy cơ **Deadlock chéo** giữa các transaction của các dịch vụ khác nhau và tước bỏ khả năng scale độc lập của từng dịch vụ. Do đó, việc tách 3 database độc lập là nguyên tắc sống còn để bảo đảm tính tự chủ của microservice ạ."*

---

### Câu hỏi 2: *"Không có Foreign Key vật lý thì nếu lỡ một sân bóng trong bảng `pitches` bị xóa, các đơn booking cũ trong bảng `bookings` có bị biến thành bản ghi rác (mồ côi) không? Nhóm xử lý thế nào?"*
> **Câu trả lời chuẩn của Hùng:**  
> *"Dạ thưa Thầy/Cô, đây là vấn đề Toàn vẹn dữ liệu phi tập trung (Decentralized Data Integrity) trong Microservices. Nhóm em xử lý bằng 2 cơ chế:  
> 1. **Về mặt nghiệp vụ:** Nhóm áp dụng **Xóa mềm (Soft Delete)**. Sân bóng không bao giờ bị `DELETE` vật lý khỏi database mà chỉ chuyển `status` sang `bao_tri` hoặc `ngung_hoat_dong`. Do đó lịch sử đơn đặt sân vẫn luôn toàn vẹn.  
> 2. **Về mặt kỹ thuật:** Khi có thao tác hủy tài nguyên quan trọng, hệ thống có thể áp dụng mô hình Saga hoặc Event-driven thông qua Message Broker (như RabbitMQ/Kafka) để gửi sự kiện đồng bộ trạng thái giữa các dịch vụ ạ."*

---

### Câu hỏi 3: *"Tại sao công thức chống trùng lịch của em là `start_old < end_new AND end_old > start_new` mà không dùng toán tử `BETWEEN` trong SQL?"*
> **Câu trả lời chuẩn của Hùng:**  
> *"Dạ thưa Thầy/Cô, nếu dùng `BETWEEN`, chúng ta chỉ bắt được trường hợp một mốc thời gian rơi vào giữa hai mốc khác. Nhưng nó sẽ bị sót trường hợp thứ 4: **Khung giờ mới bao trùm hoàn toàn khung giờ cũ** (Ví dụ đơn cũ từ 18:00 - 19:00, đơn mới từ 17:00 - 20:00 thì cả 18:00 và 19:00 đều không `BETWEEN` 17:00 và 20:00 theo chiều ngược lại nếu không viết điều kiện kép phức tạp).  
> Công thức `start_old < end_new AND end_old > start_new` là điều kiện cần và đủ trong toán học tập hợp để hai đoạn thẳng thời gian giao nhau, bao quát được toàn bộ 4 trường hợp giao thoa với độ phức tạp tối thiểu và thực thi nhanh nhất trên database engine ạ."*

---

### Câu hỏi 4: *"Nếu tại cùng một tích tắc (mili-giây), có hai khách hàng cùng ấn nút Đặt sân cho cùng một khung giờ thì hệ thống có bị đặt trùng (Overbooking) không?"*
> **Câu trả lời chuẩn của Hùng:**  
> *"Dạ thưa Thầy/Cô, trong môi trường đa luồng có tính cạnh tranh cao (Concurrency), việc chỉ kiểm tra bằng câu lệnh `SELECT COUNT` thông thường có thể dẫn đến hiện tượng Race Condition (hai luồng cùng đọc count = 0 rồi cùng ghi). Để xử lý triệt để bài toán này trong sản xuất, nhóm có các giải pháp:  
> 1. Đặt annotation `@Transactional(isolation = Isolation.SERIALIZABLE)` hoặc dùng Khóa bi quan (Pessimistic Locking `SELECT ... FOR UPDATE`).  
> 2. Tạo một Unique Index trên cặp `(pitch_id, start_time)` đối với các khung giờ cố định.  
> 3. Trong hệ thống phân tán quy mô lớn, giải pháp tối ưu nhất là sử dụng **Distributed Lock** bằng Redis (Redisson) theo `pitch_id` để tuần tự hóa các yêu cầu đặt sân cho cùng một sân ạ."*

---

### Câu hỏi 5: *"Em hãy chỉ ra bằng chứng chứng minh dữ liệu này được ghi xuống đĩa cứng chứ không phải biến tĩnh trong bộ nhớ RAM?"*
> **Câu trả lời chuẩn của Hùng:**  
> *"Dạ thưa Thầy/Cô, minh chứng thể hiện ở 3 điểm:  
> 1. Khi em tắt hoàn toàn ứng dụng Spring Boot và khởi động lại, toàn bộ dữ liệu đơn đặt sân vẫn còn nguyên vẹn.  
> 2. Câu truy vấn được thực hiện trực tiếp từ một client độc lập bên ngoài là DBeaver/Workbench kết nối tới cổng 3306 của MySQL Server.  
> 3. Trong thư mục dữ liệu của MySQL (`C:\ProgramData\MySQL\MySQL Server 8.0\Data\pitchos_booking_db\`), file vật lý `bookings.ibd` của InnoDB Engine liên tục tăng kích thước khi các transaction được COMMIT thành công xuống ổ đĩa ạ."*

---

## 5. LỜI KẾT DÀNH CHO HÙNG

Tài liệu này và slide trình chiếu `PitchOS-Bao-Cao-Hung.pptx` được thiết kế tương thích 100% với barem chấm thi của giảng viên. Hùng chỉ cần:
1. Mở file PowerPoint `PitchOS-Bao-Cao-Hung.pptx` tập dượt trước 1-2 lần theo kịch bản nói.
2. Mở sẵn DBeaver với 3 tab SQL cho 3 database.
3. Khi đến lượt, tự tin trình bày theo cấu trúc trên. Chắc chắn bạn sẽ đạt điểm tuyệt đối **2,25 / 2,25 điểm**! Chúc Hùng bảo vệ thành công rực rỡ!

