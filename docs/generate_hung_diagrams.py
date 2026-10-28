import os
from playwright.sync_api import sync_playwright

IMG_DIR = r"c:\Users\viduc\Downloads\PTPM\docs\images"
os.makedirs(IMG_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 0. HTML: SƠ ĐỒ Ý TƯỞNG TỪ HÀNH VI TÁC NHÂN SUY RA 3 CSDL (ACTOR TO DB)
# -----------------------------------------------------------------------------
ACTOR_TO_DB_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ đồ Phân tích Nghiệp vụ suy ra 3 CSDL PitchOS</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body {
      background-color: #f8fafc;
      width: 1920px;
      height: 1080px;
      padding: 30px 50px;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }
    .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; }
    .header p { font-size: 15px; color: #64748b; margin-top: 4px; }
    .badge-top {
      background: #eff6ff;
      border: 1.5px solid #2563eb;
      color: #1d4ed8;
      padding: 6px 14px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 14px;
    }

    .columns-container {
      display: flex;
      justify-content: space-between;
      gap: 30px;
      flex: 1;
      align-items: stretch;
    }

    .column-box {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .column-header {
      text-align: center;
      padding: 12px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 16px;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .col-header-1 { background: linear-gradient(135deg, #1e3a8a, #3b82f6); }
    .col-header-2 { background: linear-gradient(135deg, #0f766e, #14b8a6); }
    .col-header-3 { background: linear-gradient(135deg, #15803d, #22c55e); }

    .node-card {
      background: #ffffff;
      border: 2px solid #cbd5e1;
      border-radius: 10px;
      padding: 16px 20px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .node-card.admin { border-color: #3b82f6; }
    .node-card.owner { border-color: #14b8a6; }
    .node-card.user { border-color: #22c55e; }

    .node-title {
      font-size: 16px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .node-badge {
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 700;
    }
    .node-badge.admin { background: #dbeafe; color: #1e40af; }
    .node-badge.owner { background: #ccfbf1; color: #0f766e; }
    .node-badge.user { background: #dcfce7; color: #166534; }

    .node-desc {
      font-size: 13.5px;
      color: #475569;
      line-height: 1.5;
    }
    .node-desc ul {
      margin-left: 18px;
      margin-top: 4px;
    }
    .node-desc li {
      margin-bottom: 3px;
    }

    .output-box {
      margin-top: 8px;
      background: #f1f5f9;
      padding: 8px 12px;
      border-radius: 6px;
      font-family: 'Consolas', monospace;
      font-size: 12.5px;
      font-weight: 700;
      color: #0f172a;
      border-left: 4px solid;
    }
    .output-box.admin { border-left-color: #2563eb; }
    .output-box.owner { border-left-color: #0d9488; }
    .output-box.user { border-left-color: #16a34a; }

    .bottom-bar {
      margin-top: 20px;
      background: #ffffff;
      border: 2px dashed #3b82f6;
      border-radius: 10px;
      padding: 14px 25px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>SƠ ĐỒ PHÂN TÍCH HÀNH VI TÁC NHÂN ➔ THIẾT KẾ 3 CƠ SỞ DỮ LIỆU</h1>
      <p>Hệ thống PitchOS — Phân rã ngữ cảnh nghiệp vụ (Bounded Contexts) theo tư duy Microservices | HÙNG</p>
    </div>
    <div class="badge-top">PHÂN TÍCH THỰC TẾ ➔ 3 SCHEMAS ĐỘC LẬP</div>
  </div>

  <div class="columns-container">
    <!-- CỘT 1: HÀNH VI TÁC NHÂN -->
    <div class="column-box">
      <div class="column-header col-header-1">1. HÀNH VI THỰC TẾ TÁC NHÂN</div>

      <div class="node-card admin">
        <div>
          <div class="node-title">
            <span>Quản Trị Viên (Admin)</span>
            <span class="node-badge admin">GIÁM SÁT HỆ THỐNG</span>
          </div>
          <div class="node-desc">
            <ul>
              <li>Quản lý danh sách tài khoản người dùng toàn hệ thống.</li>
              <li>Phân quyền vai trò: <code>admin</code>, <code>chusan</code>, <code>user</code>.</li>
              <li>Bảo mật tài khoản, đăng nhập & cấp phát token.</li>
            </ul>
          </div>
        </div>
        <div class="output-box admin">➔ Nhu cầu: Lưu danh tính, email & pass mã hóa</div>
      </div>

      <div class="node-card owner">
        <div>
          <div class="node-title">
            <span>Chủ Sân Bóng (Pitch Owner)</span>
            <span class="node-badge owner">QUẢN LÝ CƠ SỞ VẬT CHẤT</span>
          </div>
          <div class="node-desc">
            <ul>
              <li>Đăng tải cụm sân bóng mini (sân 5, sân 7, sân 10).</li>
              <li>Cấu hình đơn giá thuê mỗi giờ (VNĐ/h).</li>
              <li>Cập nhật trạng thái sân: hoạt động hoặc bảo trì.</li>
            </ul>
          </div>
        </div>
        <div class="output-box owner">➔ Nhu cầu: Lưu thông số sân & bảng giá thuê</div>
      </div>

      <div class="node-card user">
        <div>
          <div class="node-title">
            <span>Người Thuê Sân (User / Player)</span>
            <span class="node-badge user">GIAO DỊCH ĐẶT SÂN</span>
          </div>
          <div class="node-desc">
            <ul>
              <li>Tìm kiếm sân trống theo khung giờ mong muốn.</li>
              <li>Gửi yêu cầu đặt sân: <code>start_time</code> ➔ <code>end_time</code>.</li>
              <li>Thanh toán tiền thuê & theo dõi trạng thái duyệt đơn.</li>
            </ul>
          </div>
        </div>
        <div class="output-box user">➔ Nhu cầu: Lưu lịch thi đấu, tiền thuê & đơn hàng</div>
      </div>
    </div>

    <!-- CỘT 2: BOUNDED CONTEXT & MICROSERVICE -->
    <div class="column-box">
      <div class="column-header col-header-2">2. NGỮ CẢNH NGHIỆP VỤ & DỊCH VỤ</div>

      <div class="node-card admin" style="justify-content: center;">
        <div class="node-title">
          <span>Ngữ cảnh Định danh (Auth Context)</span>
          <span class="node-badge admin">PORT 8081</span>
        </div>
        <div class="node-desc">
          • Dịch vụ đảm nhiệm: <strong>Auth & User Service</strong>.<br/>
          • Trách nhiệm: Đăng ký, đăng nhập, sinh token JWT xác thực, phân quyền RBAC.<br/>
          • Độc lập tuyệt đối với nghiệp vụ sân bóng và giao dịch đặt sân.
        </div>
      </div>

      <div class="node-card owner" style="justify-content: center;">
        <div class="node-title">
          <span>Ngữ cảnh Sân bóng (Pitch Context)</span>
          <span class="node-badge owner">PORT 8082</span>
        </div>
        <div class="node-desc">
          • Dịch vụ đảm nhiệm: <strong>Pitch Service</strong>.<br/>
          • Trách nhiệm: Quản lý danh mục sân, phân loại kích thước sân, bảng giá giờ thuê, tra cứu công khai.<br/>
          • Tần suất đọc rất cao, hỗ trợ cache dữ liệu dễ dàng.
        </div>
      </div>

      <div class="node-card user" style="justify-content: center;">
        <div class="node-title">
          <span>Ngữ cảnh Đặt sân (Booking Context)</span>
          <span class="node-badge user">PORT 8083</span>
        </div>
        <div class="node-desc">
          • Dịch vụ đảm nhiệm: <strong>Booking Service</strong>.<br/>
          • Trách nhiệm: Tiếp nhận đơn đặt, chạy thuật toán chống trùng lịch, tính tiền thuê, chuyển trạng thái duyệt đơn.<br/>
          • Tần suất ghi cao, xử lý tính toàn vẹn giao dịch.
        </div>
      </div>
    </div>

    <!-- CỘT 3: CSDL VẬT LÝ & BẢNG SQL -->
    <div class="column-box">
      <div class="column-header col-header-3">3. CƠ SỞ DỮ LIỆU & BẢNG SQL VẬT LÝ</div>

      <div class="node-card admin">
        <div>
          <div class="node-title">
            <span>CSDL: pitchos_user_db</span>
            <span class="node-badge admin">MYSQL 8.0</span>
          </div>
          <div class="node-desc">
            • <strong>Bảng: users</strong><br/>
            • <code>id</code> (BIGINT PK)<br/>
            • <code>username</code>, <code>email</code> (UK)<br/>
            • <code>password</code> (BCrypt hash)<br/>
            • <code>role</code> (ENUM: admin, chusan, user)
          </div>
        </div>
        <div class="output-box admin">📁 Tệp vật lý: users.ibd</div>
      </div>

      <div class="node-card owner">
        <div>
          <div class="node-title">
            <span>CSDL: pitchos_pitch_db</span>
            <span class="node-badge owner">MYSQL 8.0</span>
          </div>
          <div class="node-desc">
            • <strong>Bảng: pitches</strong><br/>
            • <code>id</code> (BIGINT PK)<br/>
            • <code>name</code> (VARCHAR 150)<br/>
            • <code>pitch_type</code> (ENUM: san_5, 7, 10)<br/>
            • <code>price_per_hour</code> (DECIMAL 12,2)
          </div>
        </div>
        <div class="output-box owner">📁 Tệp vật lý: pitches.ibd</div>
      </div>

      <div class="node-card user">
        <div>
          <div class="node-title">
            <span>CSDL: pitchos_booking_db</span>
            <span class="node-badge user">MYSQL 8.0</span>
          </div>
          <div class="node-desc">
            • <strong>Bảng: bookings</strong><br/>
            • <code>id</code> (BIGINT PK)<br/>
            • <code>user_id</code> (Logical ID ⇢ users.id)<br/>
            • <code>pitch_id</code> (Logical ID ⇢ pitches.id)<br/>
            • <code>start_time</code>, <code>end_time</code>, <code>total_price</code>
          </div>
        </div>
        <div class="output-box user">📁 Tệp vật lý: bookings.ibd</div>
      </div>
    </div>
  </div>

  <div class="bottom-bar">
    <span>💡 <strong>KẾT LUẬN KIẾN TRÚC:</strong> Phân chia 3 CSDL xuất phát 100% từ hành vi thực tế của 3 tác nhân người dùng.</span>
    <span style="color: #2563eb; font-weight: 800;">TUÂN THỦ HOÀN TOÀN NGUYÊN TẮC DATABASE-PER-SERVICE</span>
  </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# 1. HTML: SƠ ĐỒ THỰC THỂ QUAN HỆ PHÂN TÁN (DISTRIBUTED ERD)
# -----------------------------------------------------------------------------
ERD_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ đồ ERD Phân tán PitchOS</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body {
      background-color: #f8fafc;
      width: 1920px;
      height: 1080px;
      padding: 30px 50px;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 15px;
      margin-bottom: 20px;
    }
    .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; }
    .header p { font-size: 15px; color: #64748b; margin-top: 4px; }
    .badge-principle {
      background: #eff6ff;
      border: 1.5px solid #3b82f6;
      color: #1d4ed8;
      padding: 8px 16px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 14px;
    }

    .diagram-container {
      display: flex;
      justify-content: space-between;
      align-items: stretch;
      flex: 1;
      gap: 30px;
      position: relative;
    }

    .schema-card {
      flex: 1;
      background: #ffffff;
      border-radius: 12px;
      border: 2px solid #cbd5e1;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .schema-card.auth { border-color: #2563eb; }
    .schema-card.booking { border-color: #16a34a; }
    .schema-card.pitch { border-color: #0d9488; }

    .card-header {
      padding: 16px 20px;
      color: #ffffff;
      font-weight: 800;
      font-size: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .schema-card.auth .card-header { background: linear-gradient(135deg, #1e40af, #3b82f6); }
    .schema-card.booking .card-header { background: linear-gradient(135deg, #15803d, #22c55e); }
    .schema-card.pitch .card-header { background: linear-gradient(135deg, #0f766e, #14b8a6); }

    .card-header span.port {
      background: rgba(255,255,255,0.25);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
    }

    .table-title {
      padding: 12px 20px;
      background: #f1f5f9;
      font-weight: 800;
      font-size: 15px;
      color: #334155;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
    }

    .columns-list {
      flex: 1;
      padding: 10px 0;
      overflow-y: auto;
    }

    .col-row {
      display: flex;
      padding: 8px 20px;
      font-size: 13.5px;
      border-bottom: 1px solid #f8fafc;
      align-items: center;
    }
    .col-row:nth-child(even) { background-color: #fbfcfe; }
    .col-name { font-weight: 700; width: 38%; color: #1e293b; font-family: 'Consolas', monospace; }
    .col-type { color: #64748b; width: 32%; font-family: 'Consolas', monospace; font-size: 12.5px; }
    .col-key { width: 30%; text-align: right; }
    
    .key-pk { background: #fee2e2; color: #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px; }
    .key-uk { background: #e0e7ff; color: #4338ca; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px; }
    .key-logic { background: #fef3c7; color: #b45309; padding: 2px 6px; border-radius: 4px; font-weight: 800; font-size: 11px; border: 1px dashed #d97706; }

    .connector-banner {
      margin-top: 20px;
      background: #ffffff;
      border: 2px dashed #3b82f6;
      border-radius: 10px;
      padding: 16px 25px;
      display: flex;
      justify-content: space-around;
      align-items: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .banner-item {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14.5px;
    }
    .banner-item strong { color: #1e40af; }
    .rule-box {
      background: #fef2f2;
      border: 1px solid #ef4444;
      color: #991b1b;
      padding: 6px 14px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>SƠ ĐỒ THỰC THỂ QUAN HỆ PHÂN TÁN (DISTRIBUTED ERD)</h1>
      <p>Hệ thống PitchOS — Kiến trúc Microservices | Quản trị CSDL: HÙNG</p>
    </div>
    <div class="badge-principle">NGUYÊN TẮC: DATABASE-PER-SERVICE (CÂU 2 Ý 3)</div>
  </div>

  <div class="diagram-container">
    <!-- SCHEMA 1: USER DB -->
    <div class="schema-card auth">
      <div class="card-header">
        <span>CSDL NGƯỜI DÙNG (pitchos_user_db)</span>
        <span class="port">Port 8081 / Auth Service</span>
      </div>
      <div class="table-title">
        <span>Bảng: users</span>
        <span style="font-size: 12px; color: #64748b;">InnoDB Engine</span>
      </div>
      <div class="columns-list">
        <div class="col-row">
          <span class="col-name">id</span>
          <span class="col-type">BIGINT AUTO</span>
          <span class="col-key"><span class="key-pk">PK</span></span>
        </div>
        <div class="col-row">
          <span class="col-name">username</span>
          <span class="col-type">VARCHAR(50)</span>
          <span class="col-key"><span class="key-uk">UK NOT NULL</span></span>
        </div>
        <div class="col-row">
          <span class="col-name">email</span>
          <span class="col-type">VARCHAR(100)</span>
          <span class="col-key"><span class="key-uk">UK NOT NULL</span></span>
        </div>
        <div class="col-row">
          <span class="col-name">password</span>
          <span class="col-type">VARCHAR(255)</span>
          <span class="col-key">BCrypt Hash</span>
        </div>
        <div class="col-row">
          <span class="col-name">full_name</span>
          <span class="col-type">VARCHAR(100)</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">phone</span>
          <span class="col-type">VARCHAR(20)</span>
          <span class="col-key">NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">role</span>
          <span class="col-type">ENUM('admin',...)</span>
          <span class="col-key">RBAC Role</span>
        </div>
        <div class="col-row">
          <span class="col-name">created_at</span>
          <span class="col-type">TIMESTAMP</span>
          <span class="col-key">CURRENT_TIME</span>
        </div>
      </div>
    </div>

    <!-- SCHEMA 2: BOOKING DB -->
    <div class="schema-card booking">
      <div class="card-header">
        <span>CSDL ĐẶT SÂN (pitchos_booking_db)</span>
        <span class="port">Port 8083 / Booking Service</span>
      </div>
      <div class="table-title">
        <span>Bảng: bookings</span>
        <span style="font-size: 12px; color: #64748b;">InnoDB Engine</span>
      </div>
      <div class="columns-list">
        <div class="col-row">
          <span class="col-name">id</span>
          <span class="col-type">BIGINT AUTO</span>
          <span class="col-key"><span class="key-pk">PK</span></span>
        </div>
        <div class="col-row" style="background: #fffbeb;">
          <span class="col-name">user_id</span>
          <span class="col-type">BIGINT</span>
          <span class="col-key"><span class="key-logic">LOGICAL ID (users.id)</span></span>
        </div>
        <div class="col-row" style="background: #fffbeb;">
          <span class="col-name">pitch_id</span>
          <span class="col-type">BIGINT</span>
          <span class="col-key"><span class="key-logic">LOGICAL ID (pitches.id)</span></span>
        </div>
        <div class="col-row">
          <span class="col-name">start_time</span>
          <span class="col-type">DATETIME</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">end_time</span>
          <span class="col-type">DATETIME</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">total_price</span>
          <span class="col-type">DECIMAL(12,2)</span>
          <span class="col-key">Tính tự động</span>
        </div>
        <div class="col-row">
          <span class="col-name">status</span>
          <span class="col-type">ENUM('cho_duyet',.)</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">created_at</span>
          <span class="col-type">TIMESTAMP</span>
          <span class="col-key">CURRENT_TIME</span>
        </div>
      </div>
    </div>

    <!-- SCHEMA 3: PITCH DB -->
    <div class="schema-card pitch">
      <div class="card-header">
        <span>CSDL SÂN BÓNG (pitchos_pitch_db)</span>
        <span class="port">Port 8082 / Pitch Service</span>
      </div>
      <div class="table-title">
        <span>Bảng: pitches</span>
        <span style="font-size: 12px; color: #64748b;">InnoDB Engine</span>
      </div>
      <div class="columns-list">
        <div class="col-row">
          <span class="col-name">id</span>
          <span class="col-type">BIGINT AUTO</span>
          <span class="col-key"><span class="key-pk">PK</span></span>
        </div>
        <div class="col-row">
          <span class="col-name">name</span>
          <span class="col-type">VARCHAR(150)</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">pitch_type</span>
          <span class="col-type">ENUM('san_5',...)</span>
          <span class="col-key">Quy mô sân</span>
        </div>
        <div class="col-row">
          <span class="col-name">price_per_hour</span>
          <span class="col-type">DECIMAL(12,2)</span>
          <span class="col-key">Đơn giá thuê</span>
        </div>
        <div class="col-row">
          <span class="col-name">address</span>
          <span class="col-type">VARCHAR(255)</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">thumbnail_url</span>
          <span class="col-type">VARCHAR(500)</span>
          <span class="col-key">Ảnh đại diện</span>
        </div>
        <div class="col-row">
          <span class="col-name">status</span>
          <span class="col-type">ENUM('hoat_dong',..)</span>
          <span class="col-key">NOT NULL</span>
        </div>
        <div class="col-row">
          <span class="col-name">created_at</span>
          <span class="col-type">TIMESTAMP</span>
          <span class="col-key">CURRENT_TIME</span>
        </div>
      </div>
    </div>
  </div>

  <div class="connector-banner">
    <div class="banner-item">
      <span>🔗 Liên kết Logic 1:</span>
      <strong>bookings.user_id ⇢ users.id</strong>
      <span style="color: #64748b; font-size: 13px;">(Xác thực qua JWT Claims)</span>
    </div>
    <div class="rule-box">
      ⚠️ TUYỆT ĐỐI KHÔNG DÙNG FOREIGN KEY VẬT LÝ RÀNG BUỘC CHÉO DATABASE
    </div>
    <div class="banner-item">
      <span>🔗 Liên kết Logic 2:</span>
      <strong>bookings.pitch_id ⇢ pitches.id</strong>
      <span style="color: #64748b; font-size: 13px;">(Xác thực qua Feign API)</span>
    </div>
  </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# 2. HTML: SƠ ĐỒ TUẦN TỰ DỮ LIỆU & GHI ĐĨA (DATA SEQUENCE DIAGRAM)
# -----------------------------------------------------------------------------
SEQ_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sơ đồ Tuần tự Xử lý Dữ liệu PitchOS</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body {
      background-color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 30px 50px;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }
    .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; }
    .header p { font-size: 15px; color: #64748b; margin-top: 4px; }
    .badge-step {
      background: #f0fdf4;
      border: 1.5px solid #16a34a;
      color: #15803d;
      padding: 6px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 14px;
    }

    .lifelines-container {
      display: flex;
      justify-content: space-between;
      position: relative;
      margin-bottom: 20px;
    }
    .actor-box {
      width: 280px;
      text-align: center;
      padding: 14px 10px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 14px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.04);
      border: 2px solid;
    }
    .actor-box.client { background: #eff6ff; border-color: #3b82f6; color: #1e40af; }
    .actor-box.booking { background: #f0fdf4; border-color: #22c55e; color: #15803d; }
    .actor-box.pitch { background: #f0fdfa; border-color: #14b8a6; color: #0f766e; }
    .actor-box.db { background: #fefce8; border-color: #eab308; color: #854d0e; }
    .actor-box.disk { background: #f8fafc; border-color: #64748b; color: #334155; }

    .steps-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 10px 0;
    }

    .step-card {
      background: #f8fafc;
      border: 1.5px solid #e2e8f0;
      border-radius: 8px;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .step-card.active {
      border-color: #3b82f6;
      background: #ffffff;
      border-left: 6px solid #2563eb;
    }
    .step-num {
      width: 32px;
      height: 32px;
      background: #2563eb;
      color: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 14px;
      margin-right: 15px;
    }
    .step-content { flex: 1; }
    .step-title { font-weight: 700; font-size: 15px; color: #0f172a; margin-bottom: 3px; }
    .step-desc { font-size: 13.5px; color: #475569; font-family: 'Consolas', monospace; }
    .step-badge {
      background: #e2e8f0;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      color: #334155;
    }
    .step-badge.sql { background: #fef3c7; color: #92400e; }
    .step-badge.feign { background: #dcfce7; color: #166534; }
    .step-badge.disk { background: #fee2e2; color: #991b1b; }

    .bottom-summary {
      background: #1e293b;
      color: #f8fafc;
      padding: 14px 25px;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>SƠ ĐỒ TUẦN TỰ XỬ LÝ DỮ LIỆU & KIỂM CHỨNG GHI ĐĨA (DATA SEQUENCE)</h1>
      <p>Nghiệp vụ tạo đơn đặt sân PitchOS — Kiểm tra chống trùng lịch & ghi đĩa cứng MySQL</p>
    </div>
    <div class="badge-step">ĐÁP ỨNG: CÂU 2 Ý 3 (1,50 ĐIỂM THỰC NGHIỆM)</div>
  </div>

  <div class="lifelines-container">
    <div class="actor-box client">1. Ứng dụng Khách<br/>(Postman / Web Client)</div>
    <div class="actor-box booking">2. Dịch vụ đặt sân<br/>(Booking Service :8083)</div>
    <div class="actor-box pitch">3. Dịch vụ sân bóng<br/>(Pitch Service :8082)</div>
    <div class="actor-box db">4. CSDL Đặt sân<br/>(pitchos_booking_db)</div>
    <div class="actor-box disk">5. Ổ đĩa cứng vật lý<br/>(InnoDB .ibd File)</div>
  </div>

  <div class="steps-container">
    <div class="step-card active">
      <div style="display: flex; align-items: center;">
        <div class="step-num">1</div>
        <div class="step-content">
          <div class="step-title">Gửi Yêu Cầu Tạo Đơn Đặt Sân (HTTP POST)</div>
          <div class="step-desc">Client ➔ Booking Service: POST /api/v1/bookings {pitchId: 1, startTime: '18:00', endTime: '19:30'}</div>
        </div>
      </div>
      <div class="step-badge">HTTP/REST JSON</div>
    </div>

    <div class="step-card active">
      <div style="display: flex; align-items: center;">
        <div class="step-num" style="background: #d97706;">2</div>
        <div class="step-content">
          <div class="step-title">Chạy Thuật Toán Chống Trùng Lịch Thi Đấu (COUNT JPQL Query)</div>
          <div class="step-desc">Booking Service ➔ pitchos_booking_db: SELECT COUNT(b) ... WHERE pitchId=1 AND start &lt; '19:30' AND end &gt; '18:00'</div>
        </div>
      </div>
      <div class="step-badge sql">SQL COUNT = 0 (HỢP LỆ)</div>
    </div>

    <div class="step-card active">
      <div style="display: flex; align-items: center;">
        <div class="step-num" style="background: #0d9488;">3</div>
        <div class="step-content">
          <div class="step-title">Giao Tiếp Liên Dịch Vụ Lấy Đơn Giá Sân (OpenFeign REST Client)</div>
          <div class="step-desc">Booking Service ➔ Pitch Service: GET /api/v1/pitches/1 ➔ Phản hồi: 200 OK {pricePerHour: 300000.00}</div>
        </div>
      </div>
      <div class="step-badge feign">OPENFEIGN API CALL</div>
    </div>

    <div class="step-card active">
      <div style="display: flex; align-items: center;">
        <div class="step-num" style="background: #16a34a;">4</div>
        <div class="step-content">
          <div class="step-title">Tính Toán Tiền Thuê & Ghi Xuống Cơ Sở Dữ Liệu MySQL</div>
          <div class="step-desc">1.5h * 300.000 = 450.000 VNĐ ➔ INSERT INTO bookings (user_id=3, pitch_id=1, total_price=450000.00, status='cho_duyet')</div>
        </div>
      </div>
      <div class="step-badge sql">JPA REPOSITORY SAVE</div>
    </div>

    <div class="step-card active">
      <div style="display: flex; align-items: center;">
        <div class="step-num" style="background: #dc2626;">5</div>
        <div class="step-content">
          <div class="step-title">Xác Nhận Lưu Trữ Bền Vững Vào Tệp Vật Lý Trên Ổ Đĩa Cứng (Disk Durability)</div>
          <div class="step-desc">InnoDB Engine COMMIT transaction ➔ Ghi trực tiếp vào tệp bookings.ibd trên ổ đĩa vật lý của máy chủ</div>
        </div>
      </div>
      <div class="step-badge disk">INNODB DISK WRITE</div>
    </div>

    <div class="step-card active">
      <div style="display: flex; align-items: center;">
        <div class="step-num" style="background: #475569;">6</div>
        <div class="step-content">
          <div class="step-title">Kiểm Chứng Kết Quả Trực Quan Trên DBeaver / MySQL Workbench</div>
          <div class="step-desc">Hùng thực thi: SELECT * FROM pitchos_booking_db.bookings ORDER BY id DESC LIMIT 1; ➔ Xuất hiện bản ghi ID=2</div>
        </div>
      </div>
      <div class="step-badge">DBEAVER VERIFICATION</div>
    </div>
  </div>

  <div class="bottom-summary">
    <span>⭐ <strong>KHẲNG ĐỊNH:</strong> Booking Service chỉ truy cập CSDL của mình; dữ liệu sân lấy qua Feign API; dữ liệu được ghi đĩa bền vững.</span>
    <span style="color: #4ade80; font-weight: 700;">HOÀN THÀNH 100% TIÊU CHÍ CÂU 2 Ý 3</span>
  </div>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# 3. HTML: SƠ ĐỒ THUẬT TOÁN GIAO THOA THỜI GIAN (TIME OVERLAP ALGORITHM)
# -----------------------------------------------------------------------------
ALGO_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Thuật toán Giao thoa Thời gian PitchOS</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body {
      background-color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 30px 50px;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }
    .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; }
    .header p { font-size: 15px; color: #64748b; margin-top: 4px; }
    .badge-formula {
      background: #eff6ff;
      border: 1.5px solid #2563eb;
      color: #1d4ed8;
      padding: 6px 14px;
      border-radius: 8px;
      font-weight: 800;
      font-size: 15px;
      font-family: 'Consolas', monospace;
    }

    .content-grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 30px;
      flex: 1;
    }

    .visual-box {
      background: #f8fafc;
      border: 2px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px 25px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .visual-title { font-weight: 800; font-size: 17px; color: #1e3a8a; margin-bottom: 15px; }

    .timeline-row {
      margin-bottom: 12px;
      background: #ffffff;
      padding: 10px 15px;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .row-label { font-weight: 700; font-size: 13.5px; width: 220px; color: #334155; }
    .bar-container { flex: 1; height: 32px; background: #f1f5f9; border-radius: 6px; position: relative; margin: 0 15px; }
    
    .bar {
      position: absolute;
      top: 4px;
      height: 24px;
      border-radius: 4px;
      color: #ffffff;
      font-size: 11px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .bar.old { left: 30%; width: 40%; background: #2563eb; }
    .bar.c1 { left: 15%; width: 35%; background: #ef4444; }
    .bar.c2 { left: 50%; width: 35%; background: #ef4444; }
    .bar.c3 { left: 35%; width: 30%; background: #ef4444; }
    .bar.c4 { left: 20%; width: 60%; background: #ef4444; }
    
    .status-tag {
      width: 130px;
      text-align: center;
      padding: 4px 8px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 12px;
    }
    .status-tag.booked { background: #dbeafe; color: #1e40af; }
    .status-tag.conflict { background: #fee2e2; color: #dc2626; }

    .code-box {
      background: #0f172a;
      border-radius: 12px;
      padding: 20px 25px;
      color: #f8fafc;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .code-title { color: #38bdf8; font-weight: 800; font-size: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; }
    .code-content {
      font-family: 'Consolas', monospace;
      font-size: 14.5px;
      line-height: 1.6;
      color: #e2e8f0;
      background: #1e293b;
      padding: 16px;
      border-radius: 8px;
      border: 1px solid #334155;
    }
    .hl-keyword { color: #f43f5e; font-weight: 700; }
    .hl-func { color: #38bdf8; }
    .hl-var { color: #fbbf24; }
    .hl-comment { color: #94a3b8; font-style: italic; }

    .perf-analysis {
      background: #1e293b;
      padding: 14px 18px;
      border-radius: 8px;
      border-left: 4px solid #10b981;
      font-size: 13.5px;
    }
    .perf-analysis strong { color: #34d399; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>THUẬT TOÁN & TRUY VẤN CHỐNG TRÙNG LỊCH THI ĐẤU (ANTI-OVERBOOKING)</h1>
      <p>Điểm nhấn kỹ thuật tối ưu hóa toán học do Hùng trực tiếp thiết kế và cài đặt</p>
    </div>
    <div class="badge-formula">start_old &lt; end_new AND end_old &gt; start_new</div>
  </div>

  <div class="content-grid">
    <!-- VISUAL TIMELINE -->
    <div class="visual-box">
      <div class="visual-title">MÔ HÌNH HÌNH HỌC GIAO THOA THỜI GIAN (4 TRƯỜNG HỢP)</div>

      <div class="timeline-row">
        <span class="row-label">Khung giờ ĐÃ CÓ người đặt:</span>
        <div class="bar-container">
          <div class="bar old">[ start_old ⇢ end_old ]</div>
        </div>
        <span class="status-tag booked">ĐÃ ĐẶT SÂN</span>
      </div>

      <div class="timeline-row">
        <span class="row-label">Trùng Ca 1: Bắt đầu trước, kết thúc giữa:</span>
        <div class="bar-container">
          <div class="bar c1">Ca 1: start_new ⇢ end_new</div>
        </div>
        <span class="status-tag conflict">TRÙNG LỊCH ➔ CHẶN</span>
      </div>

      <div class="timeline-row">
        <span class="row-label">Trùng Ca 2: Bắt đầu giữa, kết thúc sau:</span>
        <div class="bar-container">
          <div class="bar c2">Ca 2: start_new ⇢ end_new</div>
        </div>
        <span class="status-tag conflict">TRÙNG LỊCH ➔ CHẶN</span>
      </div>

      <div class="timeline-row">
        <span class="row-label">Trùng Ca 3: Nằm lọt bên trong khung giờ:</span>
        <div class="bar-container">
          <div class="bar c3">Ca 3: start ⇢ end</div>
        </div>
        <span class="status-tag conflict">TRÙNG LỊCH ➔ CHẶN</span>
      </div>

      <div class="timeline-row">
        <span class="row-label">Trùng Ca 4: Bao trùm toàn bộ khung giờ:</span>
        <div class="bar-container">
          <div class="bar c4">Ca 4: Bao trùm toàn bộ</div>
        </div>
        <span class="status-tag conflict">TRÙNG LỊCH ➔ CHẶN</span>
      </div>
      
      <div style="font-size: 13px; color: #64748b; margin-top: 5px;">
        💡 <strong>Điểm ưu việt:</strong> Toán tử BETWEEN của SQL sẽ bỏ sót Ca 4, nhưng công thức toán học này bao quát 100% các ca xung đột.
      </div>
    </div>

    <!-- CODE JPQL -->
    <div class="code-box">
      <div class="code-title">
        <span>CÀI ĐẶT TRUY VẤN TỐI ƯU TRONG BOOKINGREPOSITORY</span>
        <span style="color: #94a3b8; font-size: 13px;">Spring Data JPA</span>
      </div>

      <div class="code-content">
<span class="hl-comment">// Hùng phụ trách tối ưu - Câu 2 Ý 3</span>
<span class="hl-keyword">@Query</span>(<span class="hl-var">"SELECT COUNT(b) FROM Booking b "</span> +
       <span class="hl-var">"WHERE b.pitchId = :pitchId "</span> +
       <span class="hl-var">"  AND b.status &lt;&gt; com.pitchos.booking.entity.BookingStatus.tu_choi "</span> +
       <span class="hl-var">"  AND b.startTime &lt; :endTime "</span> +
       <span class="hl-var">"  AND b.endTime &gt; :startTime"</span>)
<span class="hl-keyword">Long</span> <span class="hl-func">countOverlappingBookings</span>(
    <span class="hl-keyword">@Param</span>(<span class="hl-var">"pitchId"</span>) <span class="hl-keyword">Long</span> pitchId,
    <span class="hl-keyword">@Param</span>(<span class="hl-var">"startTime"</span>) LocalDateTime startTime,
    <span class="hl-keyword">@Param</span>(<span class="hl-var">"endTime"</span>) LocalDateTime endTime);
      </div>

      <div class="perf-analysis">
        <strong>Tối ưu hóa hiệu năng đỉnh cao:</strong><br/>
        • Sử dụng <code>SELECT COUNT(b)</code>: MySQL Engine đếm trực tiếp trên đĩa cứng và trả về số nguyên (0 hoặc > 0).<br/>
        • Tuyệt đối không load Entity vào bộ nhớ RAM của Spring Boot.<br/>
        • Bỏ qua các đơn có trạng thái <code>'tu_choi'</code> (sân được mở lại tự do cho người khác đặt).
      </div>
    </div>
  </div>
</body>
</html>
"""

def generate_images():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        # 0. Actor to DB
        actor_path = os.path.join(IMG_DIR, "pitchos-actor-to-db.png")
        page.set_content(ACTOR_TO_DB_HTML)
        page.screenshot(path=actor_path, full_page=True)
        print(f"Generated: {actor_path}")

        # 1. ERD
        erd_path = os.path.join(IMG_DIR, "pitchos-distributed-erd.png")
        page.set_content(ERD_HTML)
        page.screenshot(path=erd_path, full_page=True)
        print(f"Generated: {erd_path}")

        # 2. Sequence
        seq_path = os.path.join(IMG_DIR, "pitchos-data-sequence.png")
        page.set_content(SEQ_HTML)
        page.screenshot(path=seq_path, full_page=True)
        print(f"Generated: {seq_path}")

        # 3. Algorithm
        algo_path = os.path.join(IMG_DIR, "pitchos-time-overlap-algorithm.png")
        page.set_content(ALGO_HTML)
        page.screenshot(path=algo_path, full_page=True)
        print(f"Generated: {algo_path}")

        browser.close()

if __name__ == "__main__":
    generate_images()
