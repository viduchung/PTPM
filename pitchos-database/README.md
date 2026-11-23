# 🗄️ Quản Trị Cơ Sở Dữ Liệu Phân Tán (Database-per-Service) — PitchOS
## BÀI KIỂM TRA SỐ 2 (TX2) — PTPM HƯỚNG DỊCH VỤ
**Kỹ sư phụ trách:** HÙNG (Database Administrator & Backend Data Engineer)

---

## 📌 1. NGUYÊN TẮC THIẾT KẾ CƠ SỞ DỮ LIỆU
1. **Database-per-Service:** Mỗi Microservice sở hữu hoàn toàn độc quyền một CSDL riêng biệt:
   * `pitchos-auth-service` ➔ CSDL: `pitchos_user_db` *(Volume: `mysql_auth_data`)*
   * `pitchos-pitch-service` ➔ CSDL: `pitchos_pitch_db` *(Volume: `mysql_pitch_data` — dùng chung 2 instances Pitch)*
   * `pitchos-booking-service` ➔ CSDL: `pitchos_booking_db` *(Volume: `mysql_booking_data`)*
2. **Không tạo Foreign Key vật lý:** Bảng `bookings` chỉ lưu trữ **Logical ID** (`user_id`, `pitch_id`) dạng `BIGINT`. Tính toàn vẹn dữ liệu được đảm bảo thông qua tầng ứng dụng (OpenFeign gọi sang Provider để kiểm tra sự tồn tại trước khi tạo đơn).
3. **Bảo toàn dữ liệu bằng Docker Named Volume:** Dữ liệu CSDL ghi xuống ổ đĩa máy chủ ngoài vòng đời container, không bị mất khi chạy lệnh `docker compose down` (chỉ mất nếu cố ý dùng cờ `-v`).

---

## 📂 2. DANH MỤC 3 FILE SQL KHỞI TẠO TỰ ĐỘNG (DOCKER INIT)

Thư mục này chứa đúng 3 file SQL chuẩn hóa phục vụ tự động nạp khi container MySQL khởi động lần đầu qua `/docker-entrypoint-initdb.d/`:

| Tên File SQL | CSDL Khởi tạo | Bảng Dữ liệu | Mô tả & Dữ liệu mẫu |
|---|---|---|---|
| **`auth-init.sql`** | `pitchos_user_db` | `users` | Nạp 3 tài khoản mẫu đại diện cho 3 vai trò (`admin`, `chusan`, `user`), mật khẩu băm BCrypt. |
| **`pitch-init.sql`** | `pitchos_pitch_db` | `pitches` | Nạp danh mục 4 sân bóng mẫu (Sân 5, Sân 7, Sân 10 và 1 sân đang bảo trì để test lỗi 502/400). |
| **`booking-init.sql`** | `pitchos_booking_db` | `bookings` | Tạo bảng đặt sân kèm chỉ mục `idx_booking_pitch_time` tối ưu truy vấn chống trùng lịch, nạp 1 đơn đặt mẫu. |

*(Lưu ý: Các file SQL cũ từ đợt kiểm tra TX1 đã được lưu trữ an toàn trong thư mục `docs/tx1/database/`).*

---

## 🚀 3. HƯỚNG DẪN KIỂM TRA DỮ LIỆU TRÊN DOCKER

### Kiểm tra dữ liệu trực tiếp trong container:
```bash
# Truy vấn danh sách tài khoản
docker exec -it $(docker ps -q -f name=mysql) mysql -u root -e "SELECT id, username, email, role FROM pitchos_user_db.users;"

# Truy vấn danh mục sân bóng
docker exec -it $(docker ps -q -f name=mysql) mysql -u root -e "SELECT id, name, price_per_hour, status FROM pitchos_pitch_db.pitches;"

# Truy vấn các đơn đặt sân
docker exec -it $(docker ps -q -f name=mysql) mysql -u root -e "SELECT id, user_id, pitch_id, total_price, status, created_at FROM pitchos_booking_db.bookings;"
```
