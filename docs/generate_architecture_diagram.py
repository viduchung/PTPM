import os
from playwright.sync_api import sync_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Mô hình Kiến trúc Tổng thể PitchOS</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    body {
      background-color: #f8fafc;
      width: 1920px;
      height: 1080px;
      padding: 40px 50px;
      color: #0f172a;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    
    /* Header */
    .header {
      margin-bottom: 25px;
    }
    .header h1 {
      font-size: 32px;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .header h1 .badge {
      font-size: 14px;
      font-weight: 600;
      background: #e0f2fe;
      color: #0369a1;
      padding: 4px 10px;
      border-radius: 6px;
      border: 1px solid #bae6fd;
    }
    .header p {
      font-size: 16px;
      color: #64748b;
      margin-top: 4px;
      font-weight: 500;
    }

    /* Main Container */
    .main-grid {
      display: grid;
      grid-template-columns: 1460px 330px;
      gap: 30px;
      flex: 1;
    }

    /* Left Content (5 Layers) */
    .layers-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
      justify-content: space-between;
    }

    .layer-row {
      display: flex;
      align-items: stretch;
      gap: 20px;
      position: relative;
    }

    .layer-label {
      width: 140px;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .layer-number-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      font-size: 16px;
      color: #0f172a;
    }
    .num-circle {
      width: 24px;
      height: 24px;
      background: #0f172a;
      color: #fff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 700;
    }
    .layer-sub {
      font-size: 11px;
      color: #64748b;
      margin-top: 4px;
      line-height: 1.3;
    }

    .layer-content {
      flex: 1;
      display: flex;
      gap: 16px;
      align-items: stretch;
    }

    /* Layer 1: Actors */
    .actor-pill {
      flex: 1;
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      border-radius: 24px;
      padding: 10px 18px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      font-weight: 700;
      font-size: 15px;
      color: #1e293b;
      box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .actor-pill .role-tag {
      font-size: 11px;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 12px;
      text-transform: uppercase;
    }
    .role-user { background: #dbeafe; color: #1e40af; }
    .role-chusan { background: #fef3c7; color: #92400e; }
    .role-admin { background: #fee2e2; color: #991b1b; }

    /* Layer 2: Frontend App */
    .frontend-container {
      flex: 1;
      background: #ffffff;
      border: 2px solid #93c5fd;
      border-radius: 14px;
      padding: 12px 18px;
      box-shadow: 0 2px 5px rgba(59, 130, 246, 0.05);
      position: relative;
    }
    .frontend-badge {
      position: absolute;
      top: -10px;
      left: 20px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1d4ed8;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .frontend-cards {
      display: flex;
      gap: 16px;
      height: 100%;
    }
    .frontend-card {
      flex: 1;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 8px 14px;
    }
    .frontend-card h4 {
      font-size: 14px;
      font-weight: 700;
      color: #1e3a8a;
      margin-bottom: 3px;
    }
    .frontend-card p {
      font-size: 11px;
      color: #64748b;
    }

    /* Connection Banner */
    .flow-connector {
      text-align: center;
      font-size: 11px;
      font-weight: 700;
      color: #2563eb;
      background: #eff6ff;
      border: 1px dashed #93c5fd;
      padding: 4px 12px;
      border-radius: 6px;
      margin: 0 auto;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Layer 3: API & Security */
    .gateway-box {
      flex: 1;
      background: #ffffff;
      border: 2px solid #3b82f6;
      border-radius: 12px;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .gateway-info h4 {
      font-size: 15px;
      font-weight: 800;
      color: #1d4ed8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .gateway-info p {
      font-size: 12px;
      color: #475569;
      margin-top: 2px;
    }
    .gateway-status {
      display: flex;
      gap: 10px;
    }
    .gw-tag {
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 6px;
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #cbd5e1;
    }
    .gw-tag.success { background: #dcfce7; color: #166534; border-color: #86efac; }
    .gw-tag.error { background: #fee2e2; color: #991b1b; border-color: #fca5a5; }

    /* Layer 4: Microservices */
    .services-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr) 240px;
      gap: 14px;
      flex: 1;
    }
    .service-card {
      background: #ffffff;
      border: 2px solid #22c55e;
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 2px 5px rgba(34, 197, 94, 0.06);
      position: relative;
    }
    .service-card.external {
      border: 2px dashed #a855f7;
      background: #faf5ff;
    }
    .service-owner-badge {
      position: absolute;
      top: -9px;
      right: 12px;
      background: #f0fdf4;
      border: 1px solid #86efac;
      color: #15803d;
      font-size: 10px;
      font-weight: 700;
      padding: 1px 7px;
      border-radius: 4px;
    }
    .service-header h4 {
      font-size: 14px;
      font-weight: 800;
      color: #15803d;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .service-card.external .service-header h4 {
      color: #7e22ce;
    }
    .service-port {
      font-size: 11px;
      font-weight: 600;
      background: #dcfce7;
      color: #166534;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .service-card.external .service-port {
      background: #f3e8ff;
      color: #6b21a8;
    }
    .service-tech {
      font-size: 10px;
      color: #64748b;
      margin-top: 1px;
      margin-bottom: 8px;
    }
    .service-chips {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .chip {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 4px 6px;
      font-size: 10px;
      font-weight: 600;
      color: #334155;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .service-feign-banner {
      margin-top: 6px;
      background: #fff7ed;
      border: 1px dashed #fdba74;
      color: #c2410c;
      font-size: 9.5px;
      font-weight: 700;
      padding: 3px 6px;
      border-radius: 4px;
      text-align: center;
    }

    /* Layer 5: Databases */
    .databases-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr) 240px;
      gap: 14px;
      flex: 1;
    }
    .db-card {
      background: #ffffff;
      border: 2px solid #64748b;
      border-radius: 10px;
      padding: 10px 14px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      position: relative;
    }
    .db-badge {
      position: absolute;
      top: -9px;
      right: 12px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #475569;
      font-size: 10px;
      font-weight: 700;
      padding: 1px 7px;
      border-radius: 4px;
    }
    .db-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 800;
      color: #1e293b;
    }
    .db-icon {
      font-size: 15px;
    }
    .db-meta {
      font-size: 10px;
      color: #64748b;
      margin-top: 2px;
    }
    .db-tables {
      display: flex;
      gap: 5px;
      margin-top: 6px;
      flex-wrap: wrap;
    }
    .db-tag {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      font-size: 9.5px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      color: #334155;
    }
    .db-card.external-sandbox {
      border: 2px dashed #cbd5e1;
      background: #fafafa;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
    }

    /* Infrastructure Bar */
    .infra-banner {
      background: #0f172a;
      border-radius: 10px;
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #ffffff;
    }
    .infra-title {
      font-size: 14px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
      color: #38bdf8;
    }
    .infra-desc {
      font-size: 12px;
      color: #cbd5e1;
    }
    .infra-tags {
      display: flex;
      gap: 8px;
    }
    .infra-pill {
      background: #1e293b;
      border: 1px solid #334155;
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      color: #94a3b8;
    }

    /* Right Sidebar */
    .sidebar {
      display: flex;
      flex-direction: column;
      gap: 16px;
      justify-content: space-between;
    }
    .legend-card {
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .legend-title {
      font-size: 14px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 6px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
      font-size: 11.5px;
      color: #334155;
    }
    .legend-line {
      width: 32px;
      height: 4px;
      border-radius: 2px;
      position: relative;
    }
    .line-rest { background: #2563eb; }
    .line-feign { background: #ea580c; border: 1px dashed #c2410c; height: 3px; }
    .line-sql { background: #475569; }
    .line-ext { background: #9333ea; border: 1px dotted #7e22ce; height: 3px; }

    /* Rationale Card */
    .rationale-card {
      background: #f0fdf4;
      border: 1.5px solid #86efac;
      border-radius: 12px;
      padding: 16px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .rationale-title {
      font-size: 13px;
      font-weight: 800;
      color: #166534;
      margin-bottom: 8px;
    }
    .rationale-item {
      font-size: 11px;
      color: #14532d;
      margin-bottom: 8px;
      line-height: 1.4;
    }
    .rationale-item strong {
      color: #052e16;
    }
    
    .team-badge-box {
      background: #ffffff;
      border: 1px solid #bbf7d0;
      border-radius: 8px;
      padding: 8px 10px;
      font-size: 10.5px;
      color: #1e293b;
    }
    .team-badge-box h5 {
      font-weight: 800;
      color: #166534;
      margin-bottom: 4px;
    }
    .team-member-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 2px;
    }
    .team-member-row span.score {
      font-weight: 700;
      color: #0284c7;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <h1>
      Kiến trúc tổng thể — Hệ thống quản lý & đặt lịch sân bóng đá (PitchOS)
      <span class="badge">Kiến trúc SOA / Microservices</span>
    </h1>
    <p>Quy mô đồ án kiểm tra: 3 Microservices độc lập, mỗi service sở hữu dữ liệu riêng (Database-per-Service) & Bảo mật JWT Bearer RBAC</p>
  </div>

  <!-- Main Grid -->
  <div class="main-grid">
    
    <!-- Left 5 Layers -->
    <div class="layers-container">
      
      <!-- Layer 1: Actors -->
      <div class="layer-row">
        <div class="layer-label">
          <div class="layer-number-title">
            <div class="num-circle">1</div>
            <span>Người dùng</span>
          </div>
          <div class="layer-sub">Tác nhân hệ thống phân theo 3 vai trò</div>
        </div>
        <div class="layer-content">
          <div class="actor-pill">
            <span>👤 Khách hàng</span>
            <span class="role-tag role-user">Role: user</span>
          </div>
          <div class="actor-pill">
            <span>🏟️ Chủ sân / Nhân viên</span>
            <span class="role-tag role-chusan">Role: chusan</span>
          </div>
          <div class="actor-pill">
            <span>👑 Quản trị viên</span>
            <span class="role-tag role-admin">Role: admin</span>
          </div>
        </div>
      </div>

      <!-- Layer 2: Frontend Client -->
      <div class="layer-row">
        <div class="layer-label">
          <div class="layer-number-title">
            <div class="num-circle">2</div>
            <span>Giao diện</span>
          </div>
          <div class="layer-sub">Next.js · TypeScript Tailwind CSS · Axios</div>
        </div>
        <div class="layer-content">
          <div class="frontend-container">
            <div class="frontend-badge">Next.js Web Client · Single Page Application (SPA)</div>
            <div class="frontend-cards">
              <div class="frontend-card">
                <h4>Website Khách hàng</h4>
                <p>Xem danh mục sân · Lọc sân 5/7/11 · Đặt sân & tra cứu lịch sử</p>
              </div>
              <div class="frontend-card">
                <h4>Trang Quản lý sân</h4>
                <p>Quản lý sân bóng · Điều chỉnh giá/giờ · Bật tắt bảo trì · Duyệt đơn</p>
              </div>
              <div class="frontend-card">
                <h4>Bảng Quản trị Admin</h4>
                <p>Quản lý tài khoản · Phân quyền RBAC · Theo dõi toàn bộ đơn đặt</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Flow Connector -->
      <div style="text-align: center; margin: -6px 0;">
        <span class="flow-connector">
          ⬇ Giao thức HTTP / REST (JSON) + Header: Authorization: Bearer &lt;JWT Token&gt;
        </span>
      </div>

      <!-- Layer 3: API & Security -->
      <div class="layer-row">
        <div class="layer-label">
          <div class="layer-number-title">
            <div class="num-circle">3</div>
            <span>API & Security</span>
          </div>
          <div class="layer-sub">Spring Security 6 JJWT HMAC-SHA256</div>
        </div>
        <div class="layer-content">
          <div class="gateway-box">
            <div class="gateway-info">
              <h4>🛡️ Cơ chế Bảo mật Phi tập trung (Decentralized JWT Security Filter)</h4>
              <p>Trích xuất claims (sub, role) · Xác thực tính toàn vẹn chữ ký số · Chặn truy cập trái phép ở từng service độc lập</p>
            </div>
            <div class="gateway-status">
              <span class="gw-tag success">HTTP 200/201 (Hợp lệ)</span>
              <span class="gw-tag error">HTTP 401 Unauthorized</span>
              <span class="gw-tag error">HTTP 403 Forbidden</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Layer 4: Microservices -->
      <div class="layer-row">
        <div class="layer-label">
          <div class="layer-number-title">
            <div class="num-circle">4</div>
            <span>Nghiệp vụ</span>
          </div>
          <div class="layer-sub">Spring Boot 3.2.5 Java 17 Microservices</div>
        </div>
        <div class="layer-content">
          <div class="services-grid">
            
            <!-- Auth Service -->
            <div class="service-card">
              <div class="service-owner-badge">Hoàng phụ trách (3.0đ)</div>
              <div>
                <div class="service-header">
                  <h4>Identity & Auth</h4>
                  <span class="service-port">:8081</span>
                </div>
                <div class="service-tech">Spring Boot · Spring Security 6</div>
              </div>
              <div class="service-chips">
                <div class="chip">Đăng ký (BCrypt)</div>
                <div class="chip">Đăng nhập (JWT)</div>
                <div class="chip">Cấp Bearer Token</div>
                <div class="chip">Phân quyền RBAC</div>
              </div>
            </div>

            <!-- Pitch Service -->
            <div class="service-card">
              <div class="service-owner-badge">Linh phụ trách (2.5đ)</div>
              <div>
                <div class="service-header">
                  <h4>Pitch Service</h4>
                  <span class="service-port">:8082</span>
                </div>
                <div class="service-tech">Spring Boot · OpenAPI Swagger</div>
              </div>
              <div class="service-chips">
                <div class="chip">RESTful Endpoints</div>
                <div class="chip">Validation 400</div>
                <div class="chip">Swagger UI / Docs</div>
                <div class="chip">Lọc & Trạng thái sân</div>
              </div>
            </div>

            <!-- Booking Service -->
            <div class="service-card">
              <div class="service-owner-badge">Nhật phụ trách (2.25đ)</div>
              <div>
                <div class="service-header">
                  <h4>Booking Service</h4>
                  <span class="service-port">:8083</span>
                </div>
                <div class="service-tech">Spring Boot · Spring Cloud Feign</div>
              </div>
              <div class="service-chips">
                <div class="chip">POST /bookings 201</div>
                <div class="chip">Chống trùng lịch</div>
                <div class="chip">OpenFeign Client</div>
                <div class="chip">Fault 503 Fallback</div>
              </div>
              <div class="service-feign-banner">
                ⇄ OpenFeign gọi Pitch Service (:8082)
              </div>
            </div>

            <!-- Payment Sandbox -->
            <div class="service-card external">
              <div>
                <div class="service-header">
                  <h4>Payment Sandbox</h4>
                  <span class="service-port">:8084</span>
                </div>
                <div class="service-tech">Mở rộng · VNPAY / MoMo</div>
              </div>
              <div class="service-chips">
                <div class="chip">Tạo giao dịch</div>
                <div class="chip">IPN Webhook</div>
                <div class="chip">Xác thực chữ ký</div>
                <div class="chip">Hoàn tiền</div>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- Layer 5: Databases -->
      <div class="layer-row">
        <div class="layer-label">
          <div class="layer-number-title">
            <div class="num-circle">5</div>
            <span>Dữ liệu</span>
          </div>
          <div class="layer-sub">MySQL 8.0 · JPA Database-per-Service</div>
        </div>
        <div class="layer-content">
          <div class="databases-grid">
            
            <!-- User DB -->
            <div class="db-card">
              <div class="db-badge">Hùng phụ trách</div>
              <div class="db-header">
                <span class="db-icon">🗄️</span>
                <span>pitchos_user_db</span>
              </div>
              <div class="db-meta">Sở hữu bởi Auth Service (:8081)</div>
              <div class="db-tables">
                <span class="db-tag">users</span>
                <span class="db-tag">roles</span>
                <span class="db-tag">user_roles</span>
              </div>
            </div>

            <!-- Pitch DB -->
            <div class="db-card">
              <div class="db-badge">Hùng phụ trách</div>
              <div class="db-header">
                <span class="db-icon">🗄️</span>
                <span>pitchos_pitch_db</span>
              </div>
              <div class="db-meta">Sở hữu bởi Pitch Service (:8082)</div>
              <div class="db-tables">
                <span class="db-tag">pitches</span>
                <span class="db-tag">pitch_types</span>
                <span class="db-tag">pricing</span>
              </div>
            </div>

            <!-- Booking DB -->
            <div class="db-card">
              <div class="db-badge">Hùng phụ trách</div>
              <div class="db-header">
                <span class="db-icon">🗄️</span>
                <span>pitchos_booking_db</span>
              </div>
              <div class="db-meta">Sở hữu bởi Booking Service (:8083)</div>
              <div class="db-tables">
                <span class="db-tag">bookings</span>
                <span class="db-tag">booking_slots</span>
                <span class="db-tag">audit_log</span>
              </div>
            </div>

            <!-- External DB Sandbox -->
            <div class="db-card external-sandbox">
              <div>
                <div style="font-size: 13px; font-weight: 700; color: #64748b;">payment_db</div>
                <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Sandbox / Cổng thanh toán</div>
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- Infrastructure Banner -->
      <div class="infra-banner">
        <div class="infra-title">
          <span>🐳 Docker & Docker Compose</span>
          <span style="font-size: 11px; font-weight: normal; color: #94a3b8;">(Hạ tầng container hóa chuẩn môi trường)</span>
        </div>
        <div class="infra-desc">
          Mỗi Microservice và MySQL Database chạy trong container riêng biệt · Cấu hình biến môi trường qua .env · Tự động seed dữ liệu mẫu khi khởi động
        </div>
        <div class="infra-tags">
          <span class="infra-pill">MySQL 8.0 Containers</span>
          <span class="infra-pill">Spring Boot JAR Containers</span>
          <span class="infra-pill">Bridge Network</span>
        </div>
      </div>

    </div>

    <!-- Right Sidebar: Legend & Decisions -->
    <div class="sidebar">
      
      <!-- Legend Card -->
      <div class="legend-card">
        <div class="legend-title">📌 Chú giải kết nối</div>
        
        <div class="legend-item">
          <div class="legend-line line-rest"></div>
          <div>
            <strong>REST / HTTP</strong>
            <div style="font-size: 10px; color: #64748b;">Frontend gọi Backend, JSON</div>
          </div>
        </div>

        <div class="legend-item">
          <div class="legend-line line-feign"></div>
          <div>
            <strong>Spring Cloud OpenFeign</strong>
            <div style="font-size: 10px; color: #64748b;">Booking gọi Pitch, có lỗi 503</div>
          </div>
        </div>

        <div class="legend-item">
          <div class="legend-line line-sql"></div>
          <div>
            <strong>SQL / Spring Data JPA</strong>
            <div style="font-size: 10px; color: #64748b;">Chỉ đọc ghi DB của chính mình</div>
          </div>
        </div>

        <div class="legend-item">
          <div class="legend-line line-ext"></div>
          <div>
            <strong>External / Sandbox API</strong>
            <div style="font-size: 10px; color: #64748b;">VNPAY Sandbox / Webhook IPN</div>
          </div>
        </div>
      </div>

      <!-- Rationale Card -->
      <div class="rationale-card">
        <div>
          <div class="rationale-title">💡 Quyết định kiến trúc cốt lõi</div>
          
          <div class="rationale-item">
            <strong>1. Database-per-Service:</strong><br>
            Triệt tiêu hoàn toàn Schema Coupling và Deadlock khóa chéo. Mỗi service tự do nâng cấp cấu trúc bảng.
          </div>

          <div class="rationale-item">
            <strong>2. Không khóa ngoại vật lý:</strong><br>
            Liên kết bảng qua Logical ID (kiểu số nguyên). Kiểm tra toàn vẹn bằng REST API thay vì FK vật lý.
          </div>

          <div class="rationale-item">
            <strong>3. Phòng thủ lỗi 503:</strong><br>
            Khi Pitch Service tắt, Booking Service ngắt mạch trả về 503 Service Unavailable, ngăn Cascading Failure.
          </div>
        </div>

        <!-- Team Breakdown Box -->
        <div class="team-badge-box">
          <h5>👥 Phân công nhiệm vụ (10.0đ)</h5>
          <div class="team-member-row">
            <span>👑 <strong>Hoàng (Lead)</strong>: Auth & JWT</span>
            <span class="score">3.0đ</span>
          </div>
          <div class="team-member-row">
            <span>👤 <strong>Linh</strong>: Pitch REST API</span>
            <span class="score">2.5đ</span>
          </div>
          <div class="team-member-row">
            <span>👤 <strong>Hùng</strong>: Distributed DB</span>
            <span class="score">2.25đ</span>
          </div>
          <div class="team-member-row">
            <span>👤 <strong>Nhật</strong>: OpenFeign & 503</span>
            <span class="score">2.25đ</span>
          </div>
        </div>

      </div>

    </div>

  </div>

</body>
</html>"""

def generate():
    html_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-architecture.html'
    png_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-kien-truc-tong-the.png'
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f'HTML written to {html_path}')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
        page.goto(f'file:///{html_path}')
        page.screenshot(path=png_path)
        browser.close()
    print(f'PNG diagram rendered to {png_path} ({os.path.getsize(png_path)} bytes)')

if __name__ == '__main__':
    generate()
