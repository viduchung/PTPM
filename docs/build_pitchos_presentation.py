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
    blank_layout = prs.slide_layouts[6]

    # Bảng màu tối giản hiện đại
    C_DARK = RGBColor(15, 23, 42)          # Slate 900
    C_BLUE = RGBColor(30, 64, 175)         # Blue 700
    C_GREEN = RGBColor(22, 101, 52)        # Green 800
    C_GRAY = RGBColor(100, 116, 139)       # Slate 500
    C_WHITE = RGBColor(255, 255, 255)
    C_BG_CARD = RGBColor(248, 250, 252)    # Slate 50
    C_BORDER = RGBColor(203, 213, 225)     # Slate 300

    def add_header(slide, title_text, page_num_str):
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
            p_sub.font.size = Pt(11.5)
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
    # SLIDE 1: BÌA
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(248, 250, 252)
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BÁO CÁO KIẾN TRÚC PHẦN MỀM"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "MÔ HÌNH KIẾN TRÚC TỔNG THỂ"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_DARK

    p2 = tf1.add_paragraph()
    p2.text = "Hệ thống quản lý và đặt lịch sân bóng đá PitchOS"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = C_BLUE
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "Kiến trúc hướng dịch vụ, cơ sở dữ liệu phân tán và phân quyền bảo mật"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_GRAY
    p3.space_after = Pt(30)

    p4 = tf1.add_paragraph()
    p4.text = "Thành viên nhóm: Hoàng, Linh, Hùng, Nhật"
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = C_GREEN

    pnum1 = s1.shapes.add_textbox(Inches(11.5), Inches(6.5), Inches(1.2), Inches(0.4))
    pnum1.text_frame.paragraphs[0].text = "01 / 12"
    pnum1.text_frame.paragraphs[0].font.size = Pt(13)
    pnum1.text_frame.paragraphs[0].font.bold = True
    pnum1.text_frame.paragraphs[0].font.color.rgb = C_GRAY

    # -------------------------------------------------------------------------
    # SLIDE 2: TÁC NHÂN VÀ PHÂN HỆ CHỨC NĂNG
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Tác nhân và chức năng", "02 / 12")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(4.5), 
             "👤 Khách hàng", 
             ["Đăng ký tài khoản và đăng nhập",
              "Tìm kiếm sân bóng và xem bảng giá",
              "Xem giờ trống và gửi yêu cầu đặt sân",
              "Theo dõi lịch sử đơn đặt của bản thân",
              "Nhận thông báo mã đơn chờ duyệt"],
             "Vai trò người dùng thông thường")

    add_card(s2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(4.5), 
             "🏟️ Chủ sân bóng", 
             ["Thêm mới và quản lý danh sách sân",
              "Cập nhật giá thuê theo từng khung giờ",
              "Chuyển trạng thái hoạt động hoặc bảo trì",
              "Tiếp nhận duyệt hoặc từ chối các đơn đặt",
              "Theo dõi lịch thi đấu hàng ngày"],
             "Vai trò quản lý sân bãi")

    add_card(s2, Inches(8.8), Inches(1.6), Inches(3.6), Inches(4.5), 
             "👑 Quản trị viên", 
             ["Quản lý người dùng và cấp phát quyền hạn",
              "Giám sát trạng thái hoạt động của hệ thống",
              "Khóa các tài khoản vi phạm quy định",
              "Kiểm soát tính nhất quán của dữ liệu",
              "Xem báo cáo thống kê toàn bộ hệ thống"],
             "Vai trò quản trị cao cấp")

    bn2 = s2.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.6), Inches(0.5))
    bp2 = bn2.text_frame.paragraphs[0]
    bp2.text = "💡 Người dùng sau khi đăng nhập thành công sẽ truy cập đúng khu vực chức năng theo quyền hạn được cấp."
    bp2.font.size = Pt(12)
    bp2.font.color.rgb = C_GRAY

    # -------------------------------------------------------------------------
    # SLIDE 3: KIẾN TRÚC TỔNG THỂ (IMAGE ĐƠN GIẢN HÓA)
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    arch_img_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-kien-truc-tong-the.png'
    if os.path.exists(arch_img_path):
        s3.shapes.add_picture(arch_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    else:
        add_header(s3, "Kiến trúc tổng thể PitchOS", "03 / 12")

    # -------------------------------------------------------------------------
    # SLIDE 4: VÌ SAO CHIA THÀNH CÁC DỊCH VỤ ĐỘC LẬP
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Vì sao phân chia thành các dịch vụ độc lập?", "04 / 12")
    
    add_card(s4, Inches(0.8), Inches(1.5), Inches(5.6), Inches(2.5),
             "🛡️ Dịch vụ xác thực",
             ["Chuyên trách quản lý danh tính và bảo mật",
              "Cấp phát mã xác thực cho toàn bộ hệ thống",
              "Tách biệt để mọi dịch vụ dùng chung cơ chế bảo mật"],
             "Hoàng phụ trách")

    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.6), Inches(2.5),
             "🏟️ Dịch vụ sân bóng",
             ["Quản lý thông tin sân và chính sách giá thuê",
              "Đáp ứng lượng tra cứu lớn từ khách hàng",
              "Vận hành độc lập mà không ảnh hưởng tới việc đặt sân"],
             "Linh phụ trách")

    add_card(s4, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "📅 Dịch vụ đặt sân",
             ["Xử lý các giao dịch đặt lịch và kiểm tra trùng giờ",
              "Chuyên trách đảm bảo tính nhất quán của đơn đặt",
              "Độc lập giúp bảo toàn dữ liệu nghiệp vụ quan trọng"],
             "Nhật phụ trách")

    add_card(s4, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "🗄️ Cơ sở dữ liệu phân tán",
             ["Mỗi dịch vụ sở hữu một kho dữ liệu riêng biệt",
              "Tránh tranh chấp tài nguyên và khóa chéo dữ liệu",
              "Cho phép nâng cấp cấu trúc bảng độc lập"],
             "Hùng phụ trách")

    # -------------------------------------------------------------------------
    # SLIDE 5: CÁC KIỂU GIAO TIẾP VÀ BẢO MẬT
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Các kiểu giao tiếp trong hệ thống", "05 / 12")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.4),
             "🌐 Giao tiếp trực tiếp",
             ["Ứng dụng web gửi yêu cầu và nhận kết quả tức thì",
              "Các phương thức rõ ràng cho tra cứu, tạo mới và sửa đổi",
              "Dữ liệu trao đổi theo định dạng chuẩn rõ ràng"],
             "Giao tiếp người dùng với dịch vụ")

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.6), Inches(2.4),
             "⚡ Giao tiếp giữa các dịch vụ",
             ["Dịch vụ đặt sân tự động gọi sang dịch vụ sân bóng",
              "Lấy giá thuê thực tế và kiểm tra trạng thái hoạt động",
              "Tự động ngắt kết nối an toàn khi dịch vụ đích gặp sự cố"],
             "Giao tiếp nội bộ giữa các dịch vụ")

    add_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "🔑 Xác thực và phân quyền",
             ["Dịch vụ xác thực tạo mã chứng nhận danh tính",
              "Các dịch vụ tự kiểm tra quyền mà không cần gọi lại",
              "Bảo đảm an toàn và không làm quá tải dịch vụ xác thực"],
             "Bảo mật quyền truy cập")

    add_card(s5, Inches(6.8), Inches(4.3), Inches(5.6), Inches(2.5),
             "💾 Truy cập dữ liệu độc lập",
             ["Mỗi dịch vụ chỉ kết nối với cơ sở dữ liệu của mình",
              "Tuyệt đối không truy vấn chéo vào dữ liệu của dịch vụ khác",
              "Bảo đảm tính độc lập của từng phân hệ"],
             "Quản trị dữ liệu phân tán")

    # -------------------------------------------------------------------------
    # SLIDE 6: LUỒNG NGHIỆP VỤ ĐẶT SÂN
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Quy trình nghiệp vụ đặt sân từ đầu đến cuối", "06 / 12")

    steps = [
        ("Bước 1: Đăng nhập", "Khách hàng đăng nhập vào hệ thống và nhận mã xác thực người dùng."),
        ("Bước 2: Tìm kiếm sân", "Khách hàng xem danh mục các sân đang ở trạng thái sẵn sàng hoạt động."),
        ("Bước 3: Gửi yêu cầu đặt", "Khách hàng chọn sân và khung giờ thi đấu rồi gửi yêu cầu đặt sân."),
        ("Bước 4: Kiểm tra trùng giờ", "Dịch vụ đặt sân kiểm tra trong cơ sở dữ liệu xem khung giờ đã bị trùng chưa."),
        ("Bước 5: Lấy thông tin sân", "Dịch vụ đặt sân gọi sang dịch vụ sân bóng để lấy giá thuê và kiểm tra trạng thái."),
        ("Bước 6: Lưu đơn thành công", "Dịch vụ đặt sân lưu bản ghi ở trạng thái chờ duyệt và gửi thông báo thành công.")
    ]

    for idx, (stitle, sdesc) in enumerate(steps):
        col = idx % 3
        row = idx // 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(1.6 + row * 2.6)
        add_card(s6, x, y, Inches(3.7), Inches(2.3), stitle, [sdesc], f"Giai đoạn {idx+1}")

    # -------------------------------------------------------------------------
    # SLIDE 7: MÁY TRẠNG THÁI
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Quản lý trạng thái đơn đặt và sân bóng", "07 / 12")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "📋 Trạng thái đơn đặt sân",
             ["⏳ Chờ duyệt: Đơn mới tạo thành công, chờ chủ sân xác nhận",
              "✅ Đã duyệt: Chủ sân chấp nhận, khung giờ chính thức được khóa",
              "❌ Từ chối: Chủ sân từ chối đơn do lý do vận hành sân",
              "🚫 Đã hủy: Khách hàng chủ động hủy lịch trước giờ thi đấu"],
             "Lưu tại bảng đơn đặt trong cơ sở dữ liệu đặt sân")

    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "🏟️ Trạng thái sân bóng",
             ["🟢 Hoạt động: Sân sẵn sàng cho khách hàng tra cứu và đặt lịch",
              "🟡 Bảo trì: Sân đang sửa chữa hoặc bảo dưỡng định kỳ",
              "🚫 Hệ thống tự động từ chối đặt lịch nếu sân đang bảo trì",
              "🛠️ Chủ sân có thể cập nhật trạng thái này bất kỳ lúc nào"],
             "Lưu tại bảng sân bóng trong cơ sở dữ liệu sân")

    # -------------------------------------------------------------------------
    # SLIDE 8: CHỐNG ĐẶT TRÙNG KHUNG GIỜ
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Kỹ thuật chống đặt trùng khung giờ", "08 / 12")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "🔍 Kiểm tra tại tầng dữ liệu",
             ["1. So sánh khoảng thời gian bắt đầu và kết thúc với các đơn đã có",
              "2. Kiểm tra điều kiện loại trừ các đơn đã bị từ chối hoặc đã hủy",
              "3. Gom nhóm thao tác kiểm tra và ghi dữ liệu thành một khối an toàn",
              "4. Phản hồi thông báo lỗi rõ ràng nếu khung giờ đã có người giữ chỗ"],
             "Hùng và Nhật phối hợp triển khai")

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.6), Inches(4.8),
             "⚡ Xử lý yêu cầu gửi cùng lúc",
             ["Khách hàng thứ nhất: Ghi nhận đơn thành công và khóa khung giờ",
              "Khách hàng thứ hai gửi cùng lúc: Hệ thống phát hiện xung đột dữ liệu",
              "Khách hàng thứ hai nhận được thông báo khung giờ đã có người đặt",
              "Ràng buộc tại cơ sở dữ liệu bảo đảm không bao giờ có hai đơn trùng giờ trên cùng một sân"],
             "Bảo đảm tính nhất quán của dữ liệu")

    # -------------------------------------------------------------------------
    # SLIDE 9: XỬ LÝ LỖI VÀ CHỊU LỖI PHÂN TÁN
    # -------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Xử lý lỗi và phòng thủ sự cố", "09 / 12")

    errors = [
        ("Lỗi dữ liệu đầu vào", "Dữ liệu gửi lên sai quy cách", "Tên sân để trống hoặc giá thuê là số âm sẽ bị từ chối ngay lập tức kèm thông điệp rõ ràng."),
        ("Lỗi chưa đăng nhập", "Chưa xác thực danh tính", "Yêu cầu thiếu mã xác thực hoặc mã không đúng sẽ bị từ chối truy cập hệ thống."),
        ("Lỗi không đủ quyền hạn", "Truy cập vượt quá quyền cho phép", "Khách hàng thông thường cố tình gọi chức năng tạo sân hoặc sửa sân sẽ bị chặn."),
        ("Lỗi tài nguyên không có", "Thông tin tra cứu không tồn tại", "Mã định danh sân bóng tra cứu không có trong hệ thống dữ liệu."),
        ("Lỗi dịch vụ gián đoạn", "Phòng thủ sự cố đường truyền", "Khi dịch vụ sân bóng bị tắt, dịch vụ đặt sân báo lỗi gián đoạn an toàn thay vì bị treo hệ thống."),
        ("Tính bao đóng sự cố", "Khoanh vùng phạm vi ảnh hưởng", "Sự cố xảy ra ở một dịch vụ không làm hỏng dữ liệu của các dịch vụ độc lập khác.")
    ]

    for idx, (code, title, desc) in enumerate(errors):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 5.9)
        y = Inches(1.6 + row * 1.7)
        add_card(s9, x, y, Inches(5.6), Inches(1.5), f"🔴 {code} — {title}", [desc])

    # -------------------------------------------------------------------------
    # SLIDE 10: MA TRẬN PHÂN CÔNG & ĐÁNH GIÁ
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Bảng phân công nhiệm vụ và barem điểm", "10 / 12")

    table_shape = s10.shapes.add_table(5, 5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(4.5))
    table = table_shape.table

    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(1.8)
    table.columns[4].width = Inches(1.3)

    headers = ["Thành viên", "Nhiệm vụ lý thuyết", "Nhiệm vụ thực nghiệm", "Phân hệ phụ trách", "Barem điểm"]
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
        ("👑 Hoàng, Nhóm trưởng", "Phân biệt xác thực và phân quyền, cấu trúc mã bảo vệ và các mã lỗi", "Xây dựng dịch vụ xác thực, cấp mã bảo vệ, kiểm thử an toàn", "Dịch vụ xác thực", "3,0 điểm"),
        ("👤 Linh", "Đặc điểm kiến trúc hướng dịch vụ, phân rã các dịch vụ và các giao diện mẫu", "Xây dựng dịch vụ sân bóng, kiểm tra dữ liệu đầu vào và tài liệu giao diện", "Dịch vụ sân bóng", "2,5 điểm"),
        ("👤 Hùng", "Nguyên tắc cơ sở dữ liệu riêng cho từng dịch vụ và rủi ro vi phạm", "Thiết lập ba cơ sở dữ liệu độc lập, cấu trúc bảng và kiểm chứng ghi đĩa", "Quản trị cơ sở dữ liệu", "2,25 điểm"),
        ("👤 Nhật", "Mô tả quy trình giao tiếp giữa hai dịch vụ và mã trạng thái kết quả", "Kết nối trực tiếp hai dịch vụ, sơ đồ tuần tự và xử lý lỗi gián đoạn", "Dịch vụ đặt sân", "2,25 điểm")
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

    bn10 = s10.shapes.add_textbox(Inches(0.8), Inches(6.3), Inches(11.7), Inches(0.5))
    bn10.text_frame.paragraphs[0].text = "Tổng điểm toàn nhóm đạt 10 điểm, các phần việc phân tách rõ ràng và độc lập."
    bn10.text_frame.paragraphs[0].font.size = Pt(12)
    bn10.text_frame.paragraphs[0].font.bold = True
    bn10.text_frame.paragraphs[0].font.color.rgb = C_GREEN

    # -------------------------------------------------------------------------
    # SLIDE 11: KỊCH BẢN DEMO 5 BƯỚC
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Kịch bản kiểm thử và trình diễn thực tế", "11 / 12")

    demo_steps = [
        ("Bước 1: Khởi chạy hệ thống", "Cho thấy các dịch vụ và các cơ sở dữ liệu cần thiết đã hoạt động ổn định."),
        ("Bước 2: Kiểm tra giao diện kết nối", "Thực hiện gọi thử với dữ liệu hợp lệ và trường hợp dữ liệu sai quy cách."),
        ("Bước 3: Kiểm tra giao tiếp giữa các dịch vụ", "Thực hiện nghiệp vụ cần hai dịch vụ, minh họa kết quả khi dịch vụ đích bị tắt."),
        ("Bước 4: Kiểm tra lưu trữ dữ liệu", "Thực hiện ghi dữ liệu đơn đặt, sau đó truy vấn lại để xác minh dữ liệu đã lưu vào đĩa cứng."),
        ("Bước 5: Kiểm tra bảo mật và phân quyền", "Gọi thử khi chưa đăng nhập, khi có mã xác thực và khi người dùng không đủ quyền.")
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
    # SLIDE 12: PHỤ LỤC: SƠ ĐỒ TUẦN TỰ
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    seq_img_path = r'c:\Users\viduc\Downloads\PTPM\docs\images\pitchos-sequence-diagram.png'
    if os.path.exists(seq_img_path):
        s12.shapes.add_picture(seq_img_path, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    else:
        add_header(s12, "Phụ lục: Sơ đồ tuần tự nghiệp vụ đặt sân", "12 / 12")

    # Lưu cả 2 vị trí
    out_ptpm = r'c:\Users\viduc\Downloads\PTPM\docs\PitchOS-mo-hinh-kien-truc.pptx'
    out_downloads = r'c:\Users\viduc\Downloads\PitchOS-mo-hinh-kien-truc.pptx'
    out_downloads_v2 = r'c:\Users\viduc\Downloads\PitchOS-mo-hinh-kien-truc-moi.pptx'

    prs.save(out_ptpm)
    print(f"Saved: {out_ptpm}")

    try:
        prs.save(out_downloads)
        print("Saved to Downloads: " + out_downloads)
    except PermissionError:
        prs.save(out_downloads_v2)
        print("PitchOS-mo-hinh-kien-truc.pptx is locked by PowerPoint. Saved to: " + out_downloads_v2)

if __name__ == '__main__':
    create_deck()
