# BÁO CÁO MÔ HÌNH KIẾN TRÚC PITCHOS

File trình chiếu PowerPoint:
- Bản mới nhất trong thư mục dự án: [docs/PitchOS-mo-hinh-kien-truc.pptx](file:///c:/Users/viduc/Downloads/PTPM/docs/PitchOS-mo-hinh-kien-truc.pptx)
- Bản mới trong thư mục tải về: [PitchOS-mo-hinh-kien-truc-moi.pptx](file:///c:/Users/viduc/Downloads/PitchOS-mo-hinh-kien-truc-moi.pptx)

---

## 1. SƠ ĐỒ KIẾN TRÚC TỔNG THỂ

![Kiến trúc tổng thể PitchOS](images/pitchos-kien-truc-tong-the.png)

### Các tầng kiến trúc chính:
1. Tầng người dùng:
   - Khách hàng (User): Tra cứu sân bóng, xem bảng giá và tạo yêu cầu đặt sân
   - Chủ sân bóng (Pitch Owner): Quản lý thông tin sân, cập nhật giá thuê và duyệt đơn đặt
   - Quản trị viên (Admin): Quản lý tài khoản, phân quyền và giám sát hệ thống
2. Tầng giao diện web:
   - Ứng dụng web dành cho người dùng, kết nối trực tiếp với các dịch vụ
   - Tự động đính kèm mã xác thực người dùng trong mỗi yêu cầu gửi đi
3. Tầng xác thực và phân quyền:
   - Từng dịch vụ tự thẩm định tính hợp lệ của mã xác thực
   - Tự động chặn các yêu cầu chưa đăng nhập hoặc không đủ quyền hạn
4. Tầng nghiệp vụ:
   - Dịch vụ xác thực (Auth Service): Cổng giao tiếp 8081
   - Dịch vụ sân bóng (Pitch Service): Cổng giao tiếp 8082
   - Dịch vụ đặt sân (Booking Service): Cổng giao tiếp 8083
5. Tầng cơ sở dữ liệu:
   - CSDL người dùng (pitchos_user_db): Bảng tài khoản (users), bảng quyền hạn (roles)
   - CSDL sân bóng (pitchos_pitch_db): Bảng sân bóng (pitches)
   - CSDL đặt sân (pitchos_booking_db): Bảng đơn đặt (bookings), bảng khung giờ (booking_slots)
   - Không tạo khóa ngoại trực tiếp, liên kết dữ liệu hoàn toàn qua mã số định danh
6. Hạ tầng đóng gói:
   - Tất cả dịch vụ và cơ sở dữ liệu được đóng gói độc lập, khởi động bằng một câu lệnh

---

## 2. SƠ ĐỒ TUẦN TỰ NGHIỆP VỤ ĐẶT SÂN

![Sơ đồ tuần tự quy trình đặt lịch](images/pitchos-sequence-diagram.png)

### Các bước trong quy trình:
1. Khách hàng (User) gửi thông tin tài khoản và mật khẩu để đăng nhập hệ thống
2. Dịch vụ xác thực (Auth Service) kiểm tra hợp lệ và cấp mã xác thực cho người dùng
3. Khách hàng (User) gửi yêu cầu đặt sân kèm mã xác thực và khung giờ thi đấu
4. Dịch vụ đặt sân (Booking Service) kiểm tra khung giờ trong bảng đơn đặt (bookings)
5. Dịch vụ đặt sân (Booking Service) gọi sang Dịch vụ sân bóng (Pitch Service) để lấy giá thuê và kiểm tra trạng thái
6. Xử lý các tình huống:
   - Dịch vụ sân bóng (Pitch Service) tạm thời không liên lạc được: Báo lỗi dịch vụ gián đoạn, ngắt kết nối an toàn
   - Sân bóng đang bảo trì sửa chữa: Từ chối yêu cầu do sân đang bảo dưỡng
   - Trùng khung giờ đã có người đặt: Báo lỗi khung giờ bị trùng và gợi ý chọn giờ khác
   - Thông tin hợp lệ: Lưu đơn vào bảng đơn đặt (bookings) ở trạng thái chờ duyệt và thông báo đặt sân thành công

---

## 3. DANH MỤC 12 SLIDE BẢO VỆ ĐỒ ÁN

| Số slide | Tiêu đề slide | Nội dung tóm tắt |
| :---: | :--- | :--- |
| 01 | Bìa báo cáo kiến trúc | Giới thiệu tên hệ thống, kiến trúc và danh sách thành viên |
| 02 | Tác nhân và chức năng | Khách hàng (User), Chủ sân bóng (Pitch Owner), Quản trị viên (Admin) |
| 03 | Mô hình kiến trúc tổng thể | Sơ đồ năm tầng trực quan |
| 04 | Vì sao chia thành các dịch vụ độc lập | Dịch vụ xác thực (Auth Service), Dịch vụ sân bóng (Pitch Service), Dịch vụ đặt sân (Booking Service), CSDL phân tán (Database-per-Service) |
| 05 | Các kiểu giao tiếp trong hệ thống | Giao tiếp trực tiếp (REST API), Giao tiếp giữa các dịch vụ (OpenFeign), Xác thực và phân quyền (JWT & RBAC), Truy cập dữ liệu độc lập (Spring Data JPA) |
| 06 | Quy trình nghiệp vụ đặt sân | Luồng sáu bước từ đăng nhập đến khi lưu đơn hoàn tất |
| 07 | Quản lý trạng thái thực thể | Trạng thái đơn đặt trong bảng bookings và trạng thái sân trong bảng pitches |
| 08 | Kỹ thuật chống đặt trùng khung giờ | Kiểm tra bảng bookings và booking_slots, xử lý yêu cầu gửi cùng lúc (Concurrency) |
| 09 | Xử lý lỗi và phòng thủ sự cố | Các nhóm lỗi Bad Request, Unauthorized, Forbidden, Not Found, Service Unavailable |
| 10 | Bảng phân rã trách nhiệm các dịch vụ | Bảng chi tiết trách nhiệm lý thuyết và thực nghiệm của từng phân hệ |
| 11 | Kịch bản kiểm thử và trình diễn thực tế | Năm bước trình diễn trực tiếp theo đúng yêu cầu đề bài |
| 12 | Phụ lục: Sơ đồ tuần tự | Sơ đồ tuần tự quy trình đặt sân phục vụ giải thích chi tiết |
