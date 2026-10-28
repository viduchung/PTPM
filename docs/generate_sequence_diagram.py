import os
from playwright.sync_api import sync_playwright

SEQUENCE_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Sequence Diagram - Luồng Đặt Sân PitchOS</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body {
      background-color: #ffffff;
      width: 1920px;
      height: 1080px;
      padding: 40px 60px;
      color: #0f172a;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .header { margin-bottom: 20px; }
    .header h1 { font-size: 28px; font-weight: 800; color: #0f172a; }
    .header p { font-size: 15px; color: #64748b; margin-top: 4px; }
    
    .diagram-area {
      flex: 1;
      position: relative;
      background: #fafafa;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px 40px;
    }

    /* Lifelines */
    .lifelines {
      display: flex;
      justify-content: space-between;
      position: relative;
      height: 60px;
    }
    .actor-box {
      width: 180px;
      background: #ffffff;
      border: 2px solid #3b82f6;
      border-radius: 8px;
      text-align: center;
      padding: 10px 8px;
      font-weight: 700;
      font-size: 13px;
      color: #1e3a8a;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      z-index: 10;
    }
    .actor-box.db { border-color: #64748b; color: #334155; }
    .actor-box.service { border-color: #16a34a; color: #15803d; }
    .actor-box.user { border-color: #d97706; color: #b45309; }

    /* SVG overlay for arrows */
    svg.canvas {
      position: absolute;
      top: 90px;
      left: 40px;
      width: calc(100% - 80px);
      height: 780px;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>Sơ đồ tuần tự (Sequence Diagram) — Nghiệp vụ Đặt Sân & Giao tiếp Liên Dịch vụ</h1>
    <p>Minh họa quy trình giao tiếp đồng bộ giữa Khách hàng, Booking Service, Pitch Service qua OpenFeign và Quản trị CSDL phân tán</p>
  </div>

  <div class="diagram-area">
    <!-- Lifelines -->
    <div class="lifelines">
      <div class="actor-box user">👤 Khách hàng (Client)<br><span style="font-size: 11px; font-weight: normal; color: #64748b;">(Next.js App)</span></div>
      <div class="actor-box service">🛡️ Auth Service<br><span style="font-size: 11px; font-weight: normal; color: #64748b;">(Port 8081 - Hoàng)</span></div>
      <div class="actor-box service">📅 Booking Service<br><span style="font-size: 11px; font-weight: normal; color: #64748b;">(Port 8083 - Nhật)</span></div>
      <div class="actor-box db">🗄️ booking_db<br><span style="font-size: 11px; font-weight: normal; color: #64748b;">(MySQL - Hùng)</span></div>
      <div class="actor-box service">🏟️ Pitch Service<br><span style="font-size: 11px; font-weight: normal; color: #64748b;">(Port 8082 - Linh)</span></div>
      <div class="actor-box db">🗄️ pitch_db<br><span style="font-size: 11px; font-weight: normal; color: #64748b;">(MySQL - Hùng)</span></div>
    </div>

    <!-- SVG Content -->
    <svg class="canvas" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
        </marker>
        <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
        </marker>
        <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
        </marker>
        <marker id="arrow-gray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748b" />
        </marker>
        <marker id="arrow-orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ea580c" />
        </marker>
      </defs>

      <!-- Vertical Lifeline Dashed Columns -->
      <!-- Centers: 90, 420, 750, 1080, 1410, 1740 -->
      <line x1="90" y1="0" x2="90" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
      <line x1="420" y1="0" x2="420" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
      <line x1="750" y1="0" x2="750" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
      <line x1="1080" y1="0" x2="1080" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
      <line x1="1410" y1="0" x2="1410" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
      <line x1="1740" y1="0" x2="1740" y2="760" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>

      <!-- STEP 1: Đăng nhập nhận JWT Token -->
      <text x="255" y="35" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">1. POST /api/v1/auth/login { username, password }</text>
      <line x1="90" y1="42" x2="415" y2="42" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>

      <text x="255" y="75" text-anchor="middle" font-size="12" font-weight="600" fill="#166534">2. HTTP 200 OK: Trả về accessToken (Bearer JWT chứa sub, role)</text>
      <line x1="420" y1="82" x2="95" y2="82" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow-green)"/>

      <!-- STEP 2: Tạo yêu cầu đặt sân có đính kèm Bearer Token -->
      <text x="420" y="130" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">3. POST /api/v1/bookings (Header: Authorization: Bearer &lt;Token&gt;, Body: pitchId, bookingDate, startTime, endTime)</text>
      <line x1="90" y1="138" x2="745" y2="138" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>

      <!-- STEP 3: Booking Service kiểm tra trùng lịch trong booking_db -->
      <text x="915" y="175" text-anchor="middle" font-size="12" font-weight="600" fill="#334155">4. SELECT count(*) FROM bookings WHERE pitch_id=? AND booking_date=? AND (trùng khung giờ)</text>
      <line x1="750" y1="182" x2="1075" y2="182" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow-gray)"/>
      <line x1="1080" y1="205" x2="755" y2="205" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow-gray)"/>
      <text x="915" y="200" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b">Trả về: 0 (Khung giờ còn trống)</text>

      <!-- STEP 4: OpenFeign gọi Pitch Service lấy giá & trạng thái -->
      <rect x="710" y="235" width="740" height="70" rx="8" fill="#fff7ed" stroke="#fdba74" stroke-width="1.5"/>
      <text x="1080" y="255" text-anchor="middle" font-size="12" font-weight="800" fill="#c2410c">⚡ Spring Cloud OpenFeign: Booking Service ➔ Pitch Service</text>
      <line x1="750" y1="272" x2="1405" y2="272" stroke="#ea580c" stroke-width="2" marker-end="url(#arrow-orange)"/>
      <text x="1080" y="268" text-anchor="middle" font-size="11" font-weight="600" fill="#ea580c">5. GET /api/v1/pitches/{pitchId} (Header chuyển tiếp token)</text>
      <line x1="1410" y1="292" x2="755" y2="292" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow-orange)"/>
      <text x="1080" y="288" text-anchor="middle" font-size="11" font-weight="600" fill="#ea580c">Trả về: PitchResponseDTO { id, name, pricePerHour, status: 'hoat_dong' }</text>

      <!-- Pitch Service đọc pitch_db -->
      <line x1="1410" y1="272" x2="1735" y2="272" stroke="#64748b" stroke-width="1.5" marker-end="url(#arrow-gray)"/>
      <line x1="1740" y1="290" x2="1415" y2="290" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow-gray)"/>
      <text x="1575" y="265" text-anchor="middle" font-size="10.5" font-weight="600" fill="#475569">SELECT pitches</text>

      <!-- STEP 5: Khối ALT - Xử lý các tình huống lỗi và thành công -->
      <rect x="50" y="330" width="1740" height="390" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="6 4"/>
      <rect x="50" y="330" width="70" height="24" rx="4" fill="#64748b"/>
      <text x="85" y="347" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff">ALT</text>

      <!-- Case A: Pitch Service lỗi / sập (503 Service Unavailable) -->
      <text x="90" y="375" font-size="12" font-weight="700" fill="#dc2626">[Tình huống 1: Pitch Service không khả dụng / ngắt kết nối mạng]</text>
      <line x1="750" y1="395" x2="95" y2="395" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrow-red)"/>
      <text x="420" y="390" text-anchor="middle" font-size="12" font-weight="700" fill="#dc2626">HTTP 503 SERVICE UNAVAILABLE: "Dịch vụ sân bóng tạm thời không khả dụng, vui lòng thử lại sau"</text>

      <line x1="50" y1="425" x2="1790" y2="425" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4 4"/>

      <!-- Case B: Sân bóng đang bảo trì (400 Bad Request) -->
      <text x="90" y="450" font-size="12" font-weight="700" fill="#d97706">[Tình huống 2: Sân bóng có trạng thái 'bao_tri']</text>
      <line x1="750" y1="470" x2="95" y2="470" stroke="#d97706" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrow-orange)"/>
      <text x="420" y="465" text-anchor="middle" font-size="12" font-weight="700" fill="#d97706">HTTP 400 BAD REQUEST: "Sân bóng đang trong thời gian bảo trì, không thể đặt lịch"</text>

      <line x1="50" y1="500" x2="1790" y2="500" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4 4"/>

      <!-- Case C: Trùng khung giờ đã có người đặt (409 Conflict) -->
      <text x="90" y="525" font-size="12" font-weight="700" fill="#ea580c">[Tình huống 3: Tranh chấp khung giờ đặt sân]</text>
      <line x1="750" y1="545" x2="95" y2="545" stroke="#ea580c" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrow-orange)"/>
      <text x="420" y="540" text-anchor="middle" font-size="12" font-weight="700" fill="#ea580c">HTTP 409 CONFLICT: "Khung giờ này đã được đặt bởi người dùng khác"</text>

      <line x1="50" y1="575" x2="1790" y2="575" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4 4"/>

      <!-- Case D: Thành công (201 Created) -->
      <text x="90" y="600" font-size="12" font-weight="700" fill="#16a34a">[Tình huống 4: Dữ liệu hợp lệ & Sân khả dụng (Thành công)]</text>
      <line x1="750" y1="620" x2="1075" y2="620" stroke="#16a34a" stroke-width="2" marker-end="url(#arrow-green)"/>
      <text x="915" y="615" text-anchor="middle" font-size="11.5" font-weight="700" fill="#166534">6. INSERT INTO bookings (pitch_id, user_id, total_price, status='cho_duyet')</text>

      <line x1="1080" y1="645" x2="755" y2="645" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4 4" marker-end="url(#arrow-green)"/>
      <text x="915" y="640" text-anchor="middle" font-size="11" font-weight="600" fill="#166534">Ghi đĩa cứng thành công: Sinh booking_id mới</text>

      <line x1="750" y1="680" x2="95" y2="680" stroke="#16a34a" stroke-width="2" stroke-dasharray="4 4" marker-end="url(#arrow-green)"/>
      <text x="420" y="675" text-anchor="middle" font-size="13" font-weight="800" fill="#166534">HTTP 201 CREATED: Trả về chi tiết đơn đặt sân { id, pitchName, totalPrice, status: 'cho_duyet' }</text>

    </svg>
  </div>
</body>
</html>"""

def generate():
    html_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-sequence.html'
    png_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-sequence-diagram.png'
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(SEQUENCE_HTML)
    print(f'HTML written to {html_path}')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
        page.goto(f'file:///{html_path}')
        page.screenshot(path=png_path)
        browser.close()
    print(f'PNG sequence rendered to {png_path} ({os.path.getsize(png_path)} bytes)')

if __name__ == '__main__':
    generate()
