import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Colors
    C_DARK = RGBColor(15, 23, 42)      # #0f172a
    C_BLUE = RGBColor(30, 64, 175)     # #1e40af
    C_LIGHT_BLUE = RGBColor(224, 242, 254) # #e0f2fe
    C_GREEN = RGBColor(22, 101, 52)    # #166534
    C_GRAY = RGBColor(100, 116, 139)   # #64748b
    C_WHITE = RGBColor(255, 255, 255)
    C_BG_CARD = RGBColor(248, 250, 252)# #f8fafc
    C_BORDER = RGBColor(203, 213, 225) # #cbd5e1
    C_ORANGE = RGBColor(194, 65, 12)   # #c2410c

    def add_header(slide, title_text, page_num_str):
        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10.5), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = C_DARK

        # Page Number
        pb = slide.shapes.add_textbox(Inches(11.5), Inches(0.5), Inches(1.2), Inches(0.4))
        ptf = pb.text_frame
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
        pp = ptf.paragraphs[0]
        pp.alignment = PP_ALIGN.RIGHT
        pp.text = page_num_str
        pp.font.name = "Segoe UI"
        pp.font.size = Pt(13)
        pp.font.bold = True
        pp.font.color.rgb = C_GRAY

    def add_card(slide, left, top, width, height, title, items, subtitle=None, border_color=C_BORDER, bg_color=C_BG_CARD):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = C_BLUE

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_GRAY
            p_sub.space_after = Pt(8)

        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"• {item}"
            p_item.font.name = "Segoe UI"
            p_item.font.size = Pt(12)
            p_item.font.color.rgb = C_DARK
            p_item.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 1: COVER
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    # Background accent
    bg_shape = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(248, 250, 252)
    bg_shape.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "BÁO CÁO KIẾN TRÚC PHẦN MỀM — BÀI KIỂM TRA SỐ 1"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "MÔ HÌNH KIẾN TRÚC TỔNG THỂ"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_DARK

    p2 = tf.add_paragraph()
    p2.text = "Hệ thống Quản lý & Đặt lịch Sân bóng đá (PitchOS)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = C_BLUE
    p2.space_after = Pt(20)

    p3 = tf.add_paragraph()
    p3.text = "Kiến trúc SOA / Microservices · Spring Boot 3 · MySQL 8.0 (Database-per-Service) · JWT Bearer RBAC"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_GRAY
    p3.space_after = Pt(30)

    p4 = tf.add_paragraph()
    p4.text = "Thành viên nhóm: Hoàng (Nhóm trưởng - Auth) · Linh (Pitch API) · Hùng (Database) · Nhật (Booking OpenFeign)"
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = C_GREEN

    # Page number
    pnum = s1.shapes.add_textbox(Inches(11.5), Inches(6.5), Inches(1.2), Inches(0.4))
    pnum.text_frame.paragraphs[0].text = "01 / 12"
    pnum.text_frame.paragraphs[0].font.size = Pt(13)
    pnum.text_frame.paragraphs[0].font.bold = True
    pnum.text_frame.paragraphs[0].font.color.rgb = C_GRAY

    # -------------------------------------------------------------------------
    # SLIDE 2: TÁC NHÂN VÀ PHÂN HỆ CHỨC NĂNG
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Tác nhân và Phân hệ Chức năng", "02 / 12")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(4.5), 
             "👤 Khách hàng (User)", 
             ["Đăng ký tài khoản, đăng nhập hệ thống",
              "Tìm kiếm sân bóng theo loại sân (5, 7, 11)",
              "Tra cứu lịch trống và bảng giá theo giờ",
              "Gửi yêu cầu đặt sân trực tuyến",
              "Xem lịch sử đơn đặt sân của cá nhân",
              "Nhận mã đơn đặt với trạng thái 'cho_duyet'"],
             "Quyền hạn: ROLE_USER")

    add_card(s2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(4.5), 
             "🏟️ Chủ sân / Nhân viên", 
             ["Đăng tải thông tin sân bóng mới",
              "Cập nhật bảng giá, mô tả, địa chỉ sân",
              "Chuyển trạng thái sân (hoat_dong / bao_tri)",
              "Duyệt hoặc từ chối các đơn đặt sân",
              "Theo dõi lịch thi đấu trong ngày",
              "Quản lý doanh thu và tần suất sử dụng sân"],
             "Quyền hạn: ROLE_CHUSAN")

    add_card(s2, Inches(8.8), Inches(1.6), Inches(3.6), Inches(4.5), 
             "👑 Quản trị viên (Admin)", 
             ["Quản lý toàn bộ tài khoản người dùng",
              "Cấp phát và thay đổi quyền truy cập RBAC",
              "Khóa / mở khóa tài khoản vi phạm",
              "Giám sát tình trạng hoạt động các dịch vụ",
              "Xem báo cáo thống kê toàn hệ thống",
              "Kiểm soát tính toàn vẹn dữ liệu"],
             "Quyền hạn: ROLE_ADMIN")

    # Bottom note
    bn = s2.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.6), Inches(0.5))
    bp = bn.text_frame.paragraphs[0]
    bp.text = "💡 Phân quyền tự động qua JWT Bearer: Sau khi đăng nhập, Client tự giải mã claim 'role' để điều hướng đúng giao diện chức năng."
    bp.font.size = Pt(12)
    bp.font.color.rgb = C_GRAY

    # -------------------------------------------------------------------------
    # SLIDE 3: KIẾN TRÚC TỔNG THỂ (IMAGE 4K)
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    arch_img_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-kien-truc-tong-the.png'
    if os.path.exists(arch_img_path):
        s3.shapes.add_picture(arch_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    else:
        add_header(s3, "Kiến trúc tổng thể — PitchOS", "03 / 12")

    # -------------------------------------------------------------------------
    # SLIDE 4: VÌ SAO CHIA THÀNH CÁC SERVICE
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Vì sao phân chia thành các Microservice độc lập?", "04 / 12")
    
    add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.5),
             "🛡️ Identity & Auth Service (:8081)",
             ["Chịu trách nhiệm duy nhất về bảo mật tài khoản & danh tính",
              "Mã hóa mật khẩu một chiều BCrypt và sinh Bearer JWT Token",
              "Tách biệt hoàn toàn để mọi service khác dùng chung cơ chế xác thực"],
             "Hoàng phụ trách (3.0 điểm - Leader)")

    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.5),
             "🏟️ Pitch Service (:8082)",
             ["Chuyên biệt hóa danh mục sân bóng đá và chính sách giá",
              "Tần suất đọc (Read-heavy) cực lớn từ khách hàng tra cứu sân",
              "Được scale độc lập mà không ảnh hưởng tới luồng đặt sân"],
             "Linh phụ trách (2.5 điểm)")

    add_card(s4, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "📅 Booking Service (:8083)",
             ["Chuyên trách xử lý giao dịch đặt lịch (Write-heavy) & chống trùng",
              "Giao tiếp OpenFeign sang Pitch Service để lấy giá thời gian thực",
              "Độc lập giúp bảo toàn tính toàn vẹn nghiệp vụ đơn đặt"],
             "Nhật phụ trách (2.25 điểm)")

    add_card(s4, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "🗄️ Quản trị CSDL Database-per-Service",
             ["3 Database MySQL riêng biệt (pitchos_user, pitch_db, booking_db)",
              "Triệt tiêu hoàn toàn Schema Coupling và Deadlock khóa chéo",
              "Chỉ lưu Logical ID, bảo đảm tính bao đóng tuyệt đối giữa các dịch vụ"],
             "Hùng phụ trách (2.25 điểm)")

    # -------------------------------------------------------------------------
    # SLIDE 5: CÁC KIỂU GIAO TIẾP VÀ BẢO MẬT
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Các Cơ chế Giao tiếp & Mô hình Bảo mật", "05 / 12")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.4),
             "🌐 Giao tiếp HTTP/REST Đồng bộ",
             ["Frontend Client gọi vào các Microservice qua chuẩn RESTful API",
              "Phương thức HTTP rõ ràng: GET, POST, PATCH với mã trạng thái chuẩn",
              "Dữ liệu trao đổi 100% định dạng chuẩn JSON UTF-8"],
             "Giao tiếp ngoài (Client to Service)")

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.4),
             "⚡ Spring Cloud OpenFeign",
             ["Booking Service gọi liên dịch vụ sang Pitch Service (:8082)",
              "Khai báo giao diện @FeignClient trực quan, tự động đóng gói request",
              "Tích hợp xử lý ngắt mạch (Fault Tolerance) trả về mã 503 khi có sự cố"],
             "Giao tiếp liên dịch vụ (Service to Service)")

    add_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "🔑 Xác thực & Phân quyền JWT Bearer",
             ["Auth Service ký số Token bằng thuật toán HMAC-SHA256 bí mật",
              "Các service tự giải mã claims (sub, role) mà không cần truy vấn Auth DB",
              "Tự động chặn truy cập trái phép: HTTP 401 Unauthorized & 403 Forbidden"],
             "Bảo mật Stateless RBAC")

    add_card(s5, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "💾 Truy cập Dữ liệu Độc lập qua JPA",
             ["Mỗi dịch vụ chỉ dùng Spring Data JPA kết nối CSDL thuộc quyền quản lý",
              "Thao tác ghi dữ liệu có Transactional an toàn, kiểm chứng ghi đĩa cứng",
              "Không truy vấn chéo hoặc chia sẻ connection pool giữa các dịch vụ"],
             "Quản trị CSDL Phân tán")

    # -------------------------------------------------------------------------
    # SLIDE 6: LUỒNG NGHIỆP VỤ ĐẶT SÂN
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Quy trình Nghiệp vụ Đặt Sân Từ A đến Z", "06 / 12")

    steps = [
        ("Bước 1: Đăng nhập", "Khách hàng gửi POST /api/v1/auth/login. Auth Service xác thực và trả về Bearer JWT token."),
        ("Bước 2: Tìm kiếm sân", "Client gửi GET /api/v1/pitches lấy danh sách sân khả dụng (status = 'hoat_dong')."),
        ("Bước 3: Gửi yêu cầu đặt", "Khách gửi POST /api/v1/bookings kèm Header: Authorization và thời gian đặt mong muốn."),
        ("Bước 4: Kiểm tra chống trùng", "Booking Service truy vấn booking_db kiểm tra khung giờ đã có người đặt trước chưa."),
        ("Bước 5: OpenFeign gọi giá sân", "Booking Service gọi sang Pitch Service lấy giá thuê/giờ và xác nhận trạng thái sân."),
        ("Bước 6: Ghi nhận & Phản hồi", "Booking Service ghi đơn vào booking_db (status = 'cho_duyet') và trả mã 201 Created.")
    ]

    for idx, (stitle, sdesc) in enumerate(steps):
        col = idx % 3
        row = idx // 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.6 + row * 2.6)
        add_card(s6, x, y, Inches(3.7), Inches(2.3), stitle, [sdesc], f"Giai đoạn {idx+1}")

    # -------------------------------------------------------------------------
    # SLIDE 7: MÁY TRẠNG THÁI (STATE MACHINE)
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Vòng đời & Quản lý Trạng thái Thực thể", "07 / 12")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "📋 Trạng thái Đơn Đặt Sân (Booking)",
             ["⏳ cho_duyet (Pending): Trạng thái khởi tạo sau khi khách đặt sân thành công (201 Created). Đơn chờ chủ sân xác nhận.",
              "✅ da_duyet (Confirmed): Chủ sân kiểm tra và chấp nhận đơn đặt. Khung giờ chính thức được khóa cho khách hàng.",
              "❌ tu_choi (Rejected): Chủ sân từ chối đơn do trùng lịch đột xuất hoặc lý do vận hành sân.",
              "🚫 da_huy (Cancelled): Khách hàng chủ động hủy lịch đặt theo đúng chính sách trước giờ thi đấu."],
             "Lưu tại bảng bookings trong pitchos_booking_db")

    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "🏟️ Trạng thái Sân Bóng (Pitch)",
             ["🟢 hoat_dong (Active): Sân bóng hoạt động bình thường, sẵn sàng hiển thị cho khách hàng tra cứu và đặt lịch.",
              "🟡 bao_tri (Maintenance): Sân bóng đang sửa chữa cỏ, đèn hoặc bảo dưỡng định kỳ.",
              "🚫 Chặn nghiệp vụ tự động: Khi sân ở trạng thái 'bao_tri', Booking Service gọi OpenFeign kiểm tra sẽ lập tức từ chối đơn đặt và trả về HTTP 400 Bad Request.",
              "🛠️ Cập nhật linh hoạt: Chủ sân có thể đổi trạng thái qua API PATCH /api/v1/pitches/{id}/status."],
             "Lưu tại bảng pitches trong pitchos_pitch_db")

    # -------------------------------------------------------------------------
    # SLIDE 8: CHỐNG ĐẶT TRÙNG KHUNG GIỜ
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Cơ chế Kỹ thuật Chống Đặt Trùng Khung Giờ", "08 / 12")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "🔍 Kiểm tra Trùng lịch ở Tầng Dữ liệu",
             ["1. Truy vấn giao thoa thời gian (Time-overlap query):",
              "SELECT count(*) FROM bookings WHERE pitch_id = :pitchId AND booking_date = :date AND status != 'tu_choi' AND (:startTime < end_time AND :endTime > start_time)",
              "2. Ràng buộc Transactional: Thao tác kiểm tra và lưu đơn được bọc trong một @Transactional để ngăn chặn hiện tượng Dirty Read.",
              "3. Phản hồi lỗi chuẩn mực: Nếu có tranh chấp khung giờ, trả về HTTP 409 Conflict hoặc 400 Bad Request kèm thông điệp rõ ràng."],
             "Hùng & Nhật phối hợp triển khai")

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "⚡ Xử lý Yêu cầu Đồng thời (Concurrency)",
             ["• Kịch bản: Hai khách hàng A và B cùng ấn nút Đặt sân cho Sân 5A lúc 18:00 - 19:00 cùng một thời điểm.",
              "• Xử lý: Transaction của khách A hoàn thành trước, ghi bản ghi đơn đặt thành công (HTTP 201 Created).",
              "• Chặn khách B: Transaction của khách B phát hiện xung đột dữ liệu, tự động Rollback và trả về HTTP 409 Conflict.",
              "• Kết quả: Tuyệt đối không thể xảy ra tình trạng 2 khách cùng được cấp một sân trong cùng một khung giờ."],
             "Bảo đảm tính toàn vẹn dữ liệu ACID")

    # -------------------------------------------------------------------------
    # SLIDE 9: XỬ LÝ LỖI VÀ CHỊU LỖI PHÂN TÁN
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Xử lý Lỗi Toàn diện & Phòng thủ Lỗi Mạng", "09 / 12")

    errors = [
        ("400 Bad Request", "Dữ liệu đầu vào sai quy chuẩn (@Valid)", "Tên sân để trống, giá thuê là số âm, định dạng ngày giờ không hợp lệ. GlobalExceptionHandler bắt lỗi và trả về JSON danh sách trường vi phạm."),
        ("401 Unauthorized", "Chưa xác thực danh tính người dùng", "Request thiếu Header Authorization hoặc token JWT sai chữ ký, hết hạn. AuthenticationEntryPoint trả về mã 401 chuẩn JSON."),
        ("403 Forbidden", "Không đủ quyền truy cập tài nguyên (RBAC)", "Khách hàng thông thường (role: user) cố tình gọi API tạo sân mới (POST) hoặc sửa trạng thái sân. AccessDeniedHandler trả về mã 403."),
        ("404 Not Found", "Tài nguyên tra cứu không tồn tại", "Truy vấn ID sân bóng không có trong CSDL. CustomErrorDecoder bắt lỗi từ FeignClient và phản hồi thông báo tài nguyên không tồn tại."),
        ("503 Service Unavailable", "Phòng thủ sụp đổ dây chuyền (Cascading Failure)", "Khi Pitch Service (port 8082) bị tắt hoặc sự cố mạng, Booking Service bắt ngoại lệ kết nối và lập tức trả về mã 503 thay vì bị treo luồng hệ thống."),
        ("Tính bao đóng lỗi", "Tách biệt phạm vi ảnh hưởng giữa các service", "Sự cố ở dịch vụ này không làm hỏng dữ liệu hoặc làm treo các dịch vụ độc lập khác.")
    ]

    for idx, (code, title, desc) in enumerate(errors):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.6 + row * 1.7)
        add_card(s9, x, y, Inches(5.6), Inches(1.5), f"🔴 {code} — {title}", [desc])

    # -------------------------------------------------------------------------
    # SLIDE 10: MA TRẬN PHÂN CÔNG & ĐÁNH GIÁ (10.0 ĐIỂM)
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Bảng Phân công Nhiệm vụ & Barem Điểm Chi tiết", "10 / 12")

    # Add Table
    table_shape = s10.shapes.add_table(5, 5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.5))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.5)

    headers = ["Thành viên", "Nhiệm vụ Lý thuyết (Câu 1)", "Nhiệm vụ Thực nghiệm (Câu 2)", "Dịch vụ phụ trách", "Barem điểm"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    rows_data = [
        ("👑 Hoàng (Nhóm trưởng)", "Ý 3: Phân biệt Auth vs Authz, cấu trúc JWT, HTTP 401 vs 403 (1,0đ)", "Ý 4: Triển khai Auth Service, cấp Bearer Token, kiểm thử bảo mật (2,0đ)", "Auth Service (:8081)", "3,0 / 10,0"),
        ("👤 Linh", "Ý 1: Đặc điểm SOA, phân rã dịch vụ PitchOS, 03 API tiêu biểu (1,5đ)", "Ý 1: Xây dựng 4 REST API Pitch Service, Validation 400, Swagger UI (1,0đ)", "Pitch Service (:8082)", "2,5 / 10,0"),
        ("👤 Hùng", "Ý 2b: Nguyên tắc Database-per-service & rủi ro vi phạm (0,75đ)", "Ý 3: 3 CSDL MySQL độc lập, Entity, Repository JPA, kiểm chứng ghi đĩa (1,5đ)", "Quản trị 3 Database", "2,25 / 10,0"),
        ("👤 Nhật", "Ý 2a: Giao tiếp HTTP/REST, Request/Response, Status code (0,75đ)", "Ý 2: Giao tiếp OpenFeign liên dịch vụ, Sequence Diagram, lỗi 503 (1,5đ)", "Booking Service (:8083)", "2,25 / 10,0")
    ]

    for row_idx, data in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_BG_CARD if row_idx % 2 == 1 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = "Segoe UI"
            p.font.size = Pt(11)
            p.font.color.rgb = C_DARK
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = C_GREEN

    # Bottom note
    bn10 = s10.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.5))
    bn10.text_frame.paragraphs[0].text = "Tổng điểm toàn nhóm: 10,0 / 10,0 Điểm · Các phần việc độc lập hoàn toàn, không ai trùng ai, khớp 100% đề thi."
    bn10.text_frame.paragraphs[0].font.size = Pt(12)
    bn10.text_frame.paragraphs[0].font.bold = True
    bn10.text_frame.paragraphs[0].font.color.rgb = C_GREEN

    # -------------------------------------------------------------------------
    # SLIDE 11: KỊCH BẢN DEMO 5 BƯỚC
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Kịch bản Kiểm thử & Demo Thực nghiệm (10–15 Phút)", "11 / 12")

    demo_steps = [
        ("1. Khởi chạy hệ thống", "Show 3 Microservices (:8081, :8082, :8083) và 3 Database MySQL đang hoạt động bình thường."),
        ("2. Kiểm tra REST API", "Mở Swagger UI gọi API hợp lệ (200/201) và gửi dữ liệu giá âm/tên rỗng chứng minh bắt lỗi 400 Bad Request."),
        ("3. Kiểm tra Giao tiếp", "Gọi đặt sân thành công (OpenFeign hoạt động); sau đó TẮT Pitch Service để chứng minh trả về mã 503 Service Unavailable."),
        ("4. Kiểm tra Ghi đĩa CSDL", "Mở DBeaver/Workbench chạy câu lệnh SELECT chứng minh đơn đặt sân đã được lưu đĩa cứng với trạng thái 'cho_duyet'."),
        ("5. Kiểm tra Bảo mật JWT", "Gọi API khi chưa đăng nhập (401), đăng nhập cấp token, và dùng tài khoản User gọi API của Chủ sân (403 Forbidden).")
    ]

    for idx, (dtitle, ddesc) in enumerate(demo_steps):
        y = Inches(1.6 + idx * 1.0)
        shape = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.733), Inches(0.85))
        shape.fill.solid()
        shape.fill.fore_color.rgb = C_BG_CARD
        shape.line.color.rgb = C_BORDER
        shape.line.width = Pt(1.5)

        tb = s11.shapes.add_textbox(Inches(1.0), y + Inches(0.12), Inches(11.3), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = dtitle
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_BLUE

        p_desc = tf.add_paragraph()
        p_desc.text = ddesc
        p_desc.font.name = "Segoe UI"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = C_DARK

    # -------------------------------------------------------------------------
    # SLIDE 12: PHỤ LỤC: SƠ ĐỒ TUẦN TỰ (SEQUENCE DIAGRAM)
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    seq_img_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-sequence-diagram.png'
    if os.path.exists(seq_img_path):
        s12.shapes.add_picture(seq_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    else:
        add_header(s12, "Phụ lục: Sơ đồ tuần tự (Sequence Diagram)", "12 / 12")

    # Save to both paths
    out_ptpm = r'c:\Users\viduc\Downloads\PTPM\docs\PitchOS-mo-hinh-kien-truc.pptx'
    out_downloads = r'c:\Users\viduc\Downloads\PitchOS-mo-hinh-kien-truc.pptx'

    prs.save(out_ptpm)
    prs.save(out_downloads)
    print(f"Presentation saved successfully to:\n - {out_ptpm}\n - {out_downloads}")

if __name__ == '__main__':
    create_deck()
