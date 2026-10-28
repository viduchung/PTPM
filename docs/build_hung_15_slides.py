import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_hung_15_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Bảng màu kỹ thuật hiện đại cho Database & Data Engineering
    C_NAVY_DARK = RGBColor(15, 23, 42)     # Slate 900
    C_BLUE = RGBColor(30, 64, 175)         # Blue 700 (Chủ đạo)
    C_TEAL = RGBColor(13, 148, 136)        # Teal 600 (Database)
    C_GREEN = RGBColor(21, 128, 61)        # Green 700 (Thành công / Xác nhận)
    C_RED = RGBColor(185, 28, 28)          # Red 700 (Cảnh báo / Rủi ro)
    C_GRAY = RGBColor(100, 116, 139)       # Slate 500 (Phụ chú)
    C_DARK = RGBColor(30, 41, 59)          # Slate 800 (Văn bản chính)
    C_WHITE = RGBColor(255, 255, 255)      # Trắng
    C_BG_CARD = RGBColor(248, 250, 252)    # Slate 50 (Nền thẻ)
    C_BORDER = RGBColor(226, 232, 240)     # Slate 200 (Viền thẻ)
    C_CODE_BG = RGBColor(241, 245, 249)    # Slate 100
    C_LIGHT_BLUE = RGBColor(239, 246, 255) # Blue 50
    C_LIGHT_GREEN = RGBColor(240, 253, 244)# Green 50
    C_LIGHT_RED = RGBColor(254, 242, 242)  # Red 50
    C_LIGHT_AMBER = RGBColor(254, 243, 199)# Amber 50

    def add_header(slide, title_text, page_num_str, sub_text=None):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.5), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_DARK

        if sub_text:
            p_sub = tf.add_paragraph()
            p_sub.text = sub_text
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_GRAY
            p_sub.space_before = Pt(2)

        pb = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.4))
        ptf = pb.text_frame
        ptf.margin_left = ptf.margin_top = ptf.margin_right = ptf.margin_bottom = 0
        pp = ptf.paragraphs[0]
        pp.alignment = PP_ALIGN.RIGHT
        pp.text = page_num_str
        pp.font.name = "Segoe UI"
        pp.font.size = Pt(12)
        pp.font.bold = True
        pp.font.color.rgb = C_BLUE

    def create_card(slide, left, top, width, height, title, items, subtitle=None, border_color=C_BORDER, bg_color=C_BG_CARD, title_color=C_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), height - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = title_color

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(10)
            p_sub.font.color.rgb = C_GRAY
            p_sub.space_after = Pt(4)

        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"- {item}"
            p_item.font.name = "Segoe UI"
            p_item.font.size = Pt(10.5)
            p_item.font.color.rgb = C_DARK
            p_item.space_after = Pt(2.5)

        return shape

    def add_arrow(slide, left, top, width, height, text=""):
        arrow = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, height)
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = C_BLUE
        arrow.line.fill.background()
        if text:
            tf = arrow.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = text
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Segoe UI"
            p.font.size = Pt(9)
            p.font.bold = True
            p.font.color.rgb = C_WHITE
        return arrow

    # =========================================================================
    # SLIDE 1: BÌA BÁO CÁO CHUYÊN ĐỀ CÁ NHÂN
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(248, 250, 252)
    bg1.line.fill.background()

    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.4), Inches(7.5))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = C_BLUE
    bar1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(3.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BÀI KIỂM TRA SỐ 1 - HỌC PHẦN KIẾN TRÚC PHẦN MỀM / PHÁT TRIỂN PHẦN MỀM"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(6)

    p1 = tf1.add_paragraph()
    p1.text = "BÁO CÁO CHUYÊN ĐỀ QUẢN TRỊ CƠ SỞ DỮ LIỆU PHÂN TÁN"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY_DARK
    p1.space_after = Pt(4)

    p2 = tf1.add_paragraph()
    p2.text = "Hệ thống Quản lý Đặt sân Bóng đá PitchOS (Kiến trúc SOA / Microservices)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(15)
    p2.font.color.rgb = C_GRAY

    # Card giới thiệu người thực hiện
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.7), Inches(11.0), Inches(3.1))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = C_BORDER
    card1.line.width = Pt(1.5)

    tb_c1 = s1.shapes.add_textbox(Inches(1.5), Inches(3.85), Inches(10.4), Inches(2.8))
    tfc1 = tb_c1.text_frame
    tfc1.word_wrap = True

    pc1 = tfc1.paragraphs[0]
    pc1.text = "SINH VIÊN TRÌNH BÀY: HÙNG"
    pc1.font.name = "Segoe UI"
    pc1.font.size = Pt(16)
    pc1.font.bold = True
    pc1.font.color.rgb = C_BLUE
    pc1.space_after = Pt(4)

    pc2 = tfc1.add_paragraph()
    pc2.text = "Vai trò trong nhóm: Quản trị Cơ sở Dữ liệu & Kỹ sư Dữ liệu Backend (Database Administrator & Backend Data Engineer)"
    pc2.font.name = "Segoe UI"
    pc2.font.size = Pt(12.5)
    pc2.font.color.rgb = C_DARK
    pc2.space_after = Pt(4)

    pc3 = tfc1.add_paragraph()
    pc3.text = "Trọng số điểm chịu trách nhiệm: 2,25 / 10,0 Điểm (Câu 1 Ý 2b: 0,75đ Lý thuyết + Câu 2 Ý 3: 1,50đ Thực nghiệm)"
    pc3.font.name = "Segoe UI"
    pc3.font.size = Pt(12.5)
    pc3.font.bold = True
    pc3.font.color.rgb = C_GREEN
    pc3.space_after = Pt(4)

    pc4 = tfc1.add_paragraph()
    pc4.text = "Tiến độ thực hiện: Giai đoạn 1 (Làm đầu tiên cả nhóm) — Hoàn thành CSDL và Tầng Repository trước để các dịch vụ khác tích hợp."
    pc4.font.name = "Segoe UI"
    pc4.font.size = Pt(11.5)
    pc4.font.color.rgb = C_GRAY
    pc4.space_after = Pt(2)

    pc5 = tfc1.add_paragraph()
    pc5.text = "Thời lượng thuyết trình dự kiến: 15 Phút (Bao gồm lý thuyết, phân tích nghiệp vụ, mô hình dữ liệu, demo và trả lời phản biện)."
    pc5.font.name = "Segoe UI"
    pc5.font.size = Pt(11)
    pc5.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 2: VAI TRÒ & NỘI DUNG CÂU HỎI THI CỦA HÙNG
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "VAI TRÒ TRONG NHÓM & NỘI DUNG CÂU HỎI CẦN TRẢ LỜI", "02 / 15", "Ánh xạ chuẩn đầu ra CĐR L1 theo Barem đề thi kiểm tra số 1")

    create_card(
        s2, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "CÂU 1. LÝ THUYẾT - Ý 2b (0,75 ĐIỂM)",
        [
            "NỘI DUNG ĐỀ BÀI YÊU CẦU:",
            "  'Giải thích nguyên tắc mỗi dịch vụ quản lý dữ liệu thuộc trách nhiệm của mình.'",
            "  'Vì sao một dịch vụ không nên truy cập trực tiếp cơ sở dữ liệu của dịch vụ khác?'",
            "  'Nêu một rủi ro có thể xảy ra nếu vi phạm nguyên tắc này.'",
            "CÁC ĐẦU VIỆC HÙNG GIẢI QUYẾT:",
            "  + Phân tích nguyên tắc Database-per-service và 3 trụ cột thiết kế.",
            "  + Chứng minh lý do cấm tuyệt đối việc truy cập trực tiếp CSDL khác.",
            "  + Phân tích chuyên sâu 4 rủi ro kỹ thuật: Ghép nối lược đồ (Schema Coupling), Deadlock chéo, Vỡ tính bao đóng, Cản trở khả năng mở rộng độc lập."
        ],
        subtitle="Chuẩn đầu ra L1: Phân tích và nắm vững lý thuyết dữ liệu phân tán",
        border_color=C_BLUE
    )

    create_card(
        s2, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "CÂU 2. THỰC NGHIỆM - Ý 3 (1,50 ĐIỂM)",
        [
            "NỘI DUNG ĐỀ BÀI YÊU CẦU:",
            "  'Lưu trữ dữ liệu nghiệp vụ vào CSDL thay vì chỉ dùng danh sách trong bộ nhớ.'",
            "  'Thể hiện cấu trúc dữ liệu, mô hình thực thể và cách truy cập qua các lớp.'",
            "  'Thực hiện một nghiệp vụ có thao tác dữ liệu và kiểm tra kết quả sau khi chạy.'",
            "  'Bảo đảm dịch vụ chỉ truy cập trực tiếp dữ liệu thuộc phạm vi của mình.'",
            "CÁC ĐẦU VIỆC HÙNG GIẢI QUYẾT:",
            "  + Khởi tạo 3 CSDL MySQL độc lập: CSDL người dùng (pitchos_user_db), CSDL sân bóng (pitchos_pitch_db), CSDL đặt sân (pitchos_booking_db).",
            "  + Mô hình ERD phân tán với Khóa logic (Logical ID), không Foreign Key vật lý.",
            "  + Tầng Entity và Repository JPA, tối ưu giải thuật chống trùng sân.",
            "  + Kiểm chứng bản ghi ghi đĩa trên DBeaver / Workbench."
        ],
        subtitle="Chuẩn đầu ra L1: Cài đặt CSDL thực tế, lập trình tầng dữ liệu và demo kết quả",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 3: PHÂN TÍCH HÀNH VI NGƯỜI DÙNG & Ý TƯỞNG THIẾT KẾ CSDL
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "PHÂN TÍCH NGHIỆP VỤ NGƯỜI DÙNG & Ý TƯỞNG THIẾT KẾ", "03 / 15", "Ý tưởng khởi tạo CSDL xuất phát từ hành vi thực tế của 3 nhóm tác nhân")

    create_card(
        s3, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.5),
        "1. Quản trị viên (Admin)",
        [
            "Hành vi & Trách nhiệm thực tế:",
            "  + Quản lý toàn bộ danh sách tài khoản trong hệ thống.",
            "  + Cấp quyền và phân vai trò người dùng (admin, chusan, user).",
            "  + Giám sát tính an toàn thông tin và tài khoản đăng nhập.",
            "Nhu cầu lưu trữ dữ liệu:",
            "  + Lưu tên đăng nhập (username), email định danh (duy nhất).",
            "  + Mật khẩu băm an toàn một chiều (BCrypt hash).",
            "  + Phân quyền hệ thống dựa trên vai trò (Role-based RBAC).",
            "==> Suy ra yêu cầu bảng người dùng (users)."
        ],
        subtitle="Quản lý định danh và quyền truy cập",
        border_color=C_BLUE
    )

    create_card(
        s3, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.5),
        "2. Chủ sân (Pitch Owner)",
        [
            "Hành vi & Trách nhiệm thực tế:",
            "  + Đăng tải thông tin cơ sở vật chất các sân bóng mini.",
            "  + Cấu hình quy mô: sân 5, sân 7, sân 10 người.",
            "  + Thiết lập đơn giá thuê sân theo giờ (VNĐ/h).",
            "  + Cập nhật tình trạng hoạt động hoặc tạm dừng để bảo trì.",
            "  + Duyệt đơn hoặc từ chối đơn đặt sân của khách.",
            "Nhu cầu lưu trữ dữ liệu:",
            "  + Lưu tên sân, loại sân, đơn giá thuê, địa chỉ, ảnh sân, link tọa độ bản đồ định vị, trạng thái sân.",
            "==> Suy ra yêu cầu bảng sân bóng (pitches)."
        ],
        subtitle="Quản trị sân bóng và cấu hình bảng giá",
        border_color=C_TEAL
    )

    create_card(
        s3, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.5),
        "3. Người thuê sân (User / Player)",
        [
            "Hành vi & Trách nhiệm thực tế:",
            "  + Tìm kiếm danh sách sân trống và xem bảng giá thuê.",
            "  + Lựa chọn khung giờ thi đấu (giờ bắt đầu, giờ kết thúc).",
            "  + Gửi yêu cầu đặt sân và thanh toán tiền thuê.",
            "  + Theo dõi tiến trình duyệt đơn từ chủ sân.",
            "Nhu cầu lưu trữ dữ liệu:",
            "  + Lưu mã người đặt (user_id), mã sân (pitch_id).",
            "  + Lưu khung giờ thuê (start_time, end_time).",
            "  + Lưu tổng tiền thuê (total_price) và trạng thái duyệt (status).",
            "==> Suy ra yêu cầu bảng đơn đặt (bookings)."
        ],
        subtitle="Giao dịch đặt lịch thi đấu bóng đá",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 4: TỪ HÀNH VI SUY RA 3 CSDL ĐỘC LẬP (BOUNDED CONTEXTS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "TỪ HÀNH VI SUY RA 3 CƠ SỞ DỮ LIỆU ĐỘC LẬP", "04 / 15", "Phân rã ngữ cảnh nghiệp vụ (Bounded Contexts) theo tư duy Microservices")

    img_actor_path = os.path.join(r"c:\Users\viduc\Downloads\PTPM\docs\images", "pitchos-actor-to-db.png")
    if os.path.exists(img_actor_path):
        s4.shapes.add_picture(img_actor_path, Inches(1.51), Inches(1.3), width=Inches(10.31), height=Inches(5.8))
    else:
        create_card(
            s4, Inches(0.8), Inches(1.4), Inches(3.7), Inches(5.5),
            "CSDL người dùng (pitchos_user_db)",
            [
                "Xuất phát từ vai trò Quản trị viên & Khách hàng:",
                "  + Ngữ cảnh: Định danh và Xác thực (Identity & Auth).",
                "  + Dịch vụ chủ quản: Dịch vụ xác thực (Auth Service) - Port 8081.",
                "  + Bảng lưu trữ: Bảng người dùng (users).",
                "Đặc trưng nghiệp vụ:",
                "  + Tần suất đọc khi đăng nhập / xác thực JWT.",
                "  + Dữ liệu nhạy cảm cao, yêu cầu mã hóa mật khẩu an toàn.",
                "  + Độc lập hoàn toàn với thông tin sân bóng."
            ],
            subtitle="Thuộc ngữ cảnh Quản lý Danh tính",
            border_color=C_BLUE
        )
        create_card(
            s4, Inches(4.8), Inches(1.4), Inches(3.7), Inches(5.5),
            "CSDL sân bóng (pitchos_pitch_db)",
            [
                "Xuất phát từ vai trò Chủ sân:",
                "  + Ngữ cảnh: Danh mục Sân & Giá cả (Pitch Catalog).",
                "  + Dịch vụ chủ quản: Dịch vụ sân bóng (Pitch Service) - Port 8082.",
                "  + Bảng lưu trữ: Bảng sân bóng (pitches).",
                "Đặc trưng nghiệp vụ:",
                "  + Tần suất đọc rất cao khi khách tra cứu danh sách sân.",
                "  + Tần suất ghi thấp (chủ sân chỉ thêm/sửa khi đổi giá hoặc sửa sân).",
                "  + Có thể áp dụng cache Redis độc lập mà không ảnh hưởng CSDL khác."
            ],
            subtitle="Thuộc ngữ cảnh Quản lý Tài nguyên Sân",
            border_color=C_TEAL
        )
        create_card(
            s4, Inches(8.8), Inches(1.4), Inches(3.7), Inches(5.5),
            "CSDL đặt sân (pitchos_booking_db)",
            [
                "Xuất phát từ vai trò Người thuê sân & Giao dịch:",
                "  + Ngữ cảnh: Giao dịch & Lịch thi đấu (Booking & Schedule).",
                "  + Dịch vụ chủ quản: Dịch vụ đặt sân (Booking Service) - Port 8083.",
                "  + Bảng lưu trữ: Bảng đơn đặt (bookings).",
                "Đặc trưng nghiệp vụ:",
                "  + Tần suất ghi rất cao (khách gửi đơn liên tục).",
                "  + Đòi hỏi tính nhất quán giao dịch và chống xung đột thời gian (trùng lịch).",
                "  + Tách riêng giúp đảm bảo hiệu năng I/O tối đa."
            ],
            subtitle="Thuộc ngữ cảnh Quản lý Giao dịch Đơn hàng",
            border_color=C_GREEN
        )

    # =========================================================================
    # SLIDE 5: NGUYÊN TẮC DATABASE-PER-SERVICE (CÂU 1 Ý 2b)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "NGUYÊN TẮC DATABASE-PER-SERVICE (CÂU 1 Ý 2b)", "05 / 15", "Đáp ứng Câu 1 Ý 2b: Phân tích 3 trụ cột thiết kế dữ liệu độc lập")

    create_card(
        s5, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "3 TRỤ CỘT THIẾT KẾ DỮ LIỆU ĐỘC LẬP",
        [
            "1. Quyền sở hữu độc quyền (Exclusive Data Ownership):",
            "  + Mỗi dịch vụ là chủ thể duy nhất có quyền đọc/ghi vào CSDL của mình.",
            "  + Auth Service độc quyền pitchos_user_db.",
            "  + Pitch Service độc quyền pitchos_pitch_db.",
            "  + Booking Service độc quyền pitchos_booking_db.",
            "2. Tính đóng gói dữ liệu (Data Encapsulation):",
            "  + CSDL là chi tiết nội bộ riêng tư (Private Implementation Detail).",
            "  + Không chia sẻ Connection String hay tài khoản DB ra bên ngoài.",
            "3. Truy xuất qua RESTful API chuẩn hóa (API-driven Access):",
            "  + Mọi nhu cầu lấy dữ liệu từ dịch vụ khác đều phải qua HTTP/REST công khai."
        ],
        subtitle="Nguyên tắc cốt lõi trong kiến trúc SOA / Microservices",
        border_color=C_BLUE
    )

    create_card(
        s5, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "SO SÁNH VỚI KIẾN TRÚC MONOLITH TRUYỀN THỐNG",
        [
            "Kiến trúc Monolith (Dùng chung CSDL):",
            "  + Tất cả module dùng chung 1 database vật lý.",
            "  + Ràng buộc cứng bằng FOREIGN KEY và câu lệnh JOIN phức tạp.",
            "  + Dễ dẫn đến tình trạng 'Spaghetti database' không thể bóc tách.",
            "Kiến trúc Microservices của PitchOS:",
            "  + 3 CSDL tách biệt hoàn toàn trên cổng 3306.",
            "  + Không có liên kết khóa ngoại vật lý giữa các schema.",
            "  + Mỗi dịch vụ tự do tối ưu hóa, bảo trì và phát triển CSDL của mình mà không sợ ảnh hưởng đến các thành phần khác trong hệ thống."
        ],
        subtitle="So sánh đối chiếu giữa 2 mô hình kiến trúc",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 6: 4 RỦI RO KỸ THUẬT KHI DÙNG CHUNG CSDL (CÂU 1 Ý 2b)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "4 RỦI RO KỸ THUẬT KHI VI PHẠM DÙNG CHUNG CSDL", "06 / 15", "Đáp ứng Câu 1 Ý 2b: Vì sao không nên truy cập trực tiếp CSDL của dịch vụ khác?")

    create_card(
        s6, Inches(0.8), Inches(1.4), Inches(5.6), Inches(2.65),
        "1. Ghép nối lược đồ dữ liệu (Schema Coupling)",
        [
            "Bản chất: Nhiều dịch vụ cùng đọc/ghi trực tiếp vào một bảng SQL.",
            "Tình huống PitchOS: Booking Service đọc trực tiếp bảng pitches để lấy giá sân.",
            "Hậu quả: Khi Pitch Service đổi tên cột price_per_hour -> hourly_rate, Booking Service lập tức bị lỗi thời gian chạy (Runtime Exception). Mất hoàn toàn tính triển khai độc lập."
        ],
        subtitle="Rủi ro lớn nhất về sự phụ thuộc mã nguồn",
        border_color=C_RED
    )

    create_card(
        s6, Inches(6.8), Inches(1.4), Inches(5.7), Inches(2.65),
        "2. Khóa tranh chấp và Deadlock chéo",
        [
            "Bản chất: Các transaction từ nhiều dịch vụ cùng tranh chấp khóa dòng (Row lock).",
            "Tình huống: Service 1 khóa bảng users chờ bảng bookings, trong khi Service 2 khóa bảng bookings chờ bảng users.",
            "Hậu quả: Xảy ra Deadlock chéo giữa các dịch vụ, làm treo luồng (Thread Pool Exhaustion) và kéo sập máy chủ."
        ],
        subtitle="Rủi ro về hiệu năng và tắc nghẽn luồng xử lý",
        border_color=C_RED
    )

    create_card(
        s6, Inches(0.8), Inches(4.25), Inches(5.6), Inches(2.65),
        "3. Phá vỡ tính bao đóng nghiệp vụ",
        [
            "Bản chất: Dịch vụ ngoài tự ý INSERT/UPDATE trực tiếp vào DB của dịch vụ khác.",
            "Hậu quả: Bỏ qua toàn bộ tầng Business Service và các quy tắc kiểm tra hợp lệ (Validation).",
            "Ví dụ: Tự ý sửa trạng thái sân thành bao_tri mà không kiểm tra xem sân có đang có khách đá không."
        ],
        subtitle="Rủi ro về tính toàn vẹn dữ liệu nghiệp vụ",
        border_color=C_RED
    )

    create_card(
        s6, Inches(6.8), Inches(4.25), Inches(5.7), Inches(2.65),
        "4. Cản trở khả năng mở rộng độc lập",
        [
            "Bản chất: Toàn bộ dịch vụ dồn tài nguyên vào một máy chủ CSDL duy nhất.",
            "Hậu quả: Khi Booking Service bị nghẽn I/O do lượng đặt sân cao điểm, Auth Service cũng bị sập theo.",
            "Tước đoạt cơ hội áp dụng lưu trữ đa dạng (Polyglot Persistence) như Redis hay MongoDB."
        ],
        subtitle="Rủi ro về tải hệ thống và hạ tầng mở rộng",
        border_color=C_RED
    )

    # =========================================================================
    # SLIDE 7: THIẾT KẾ SCRIPT SQL CSDL 1 & CSDL 2
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "THIẾT KẾ SCRIPT SQL: USER_DB VÀ PITCH_DB", "07 / 15", "Đáp ứng Câu 2 Ý 3: Cấu trúc dữ liệu và kiểu dữ liệu chuẩn mực")

    create_card(
        s7, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "CSDL người dùng (pitchos_user_db)",
        [
            "Script SQL: auth-user-service.sql",
            "Bảng: Bảng người dùng (users)",
            "Cấu trúc các trường dữ liệu:",
            "  + id: BIGINT AUTO_INCREMENT PRIMARY KEY",
            "  + username: VARCHAR(50) NOT NULL UNIQUE",
            "  + email: VARCHAR(100) NOT NULL UNIQUE",
            "  + password: VARCHAR(255) NOT NULL (Chuỗi băm BCrypt)",
            "  + full_name: VARCHAR(100) NOT NULL",
            "  + phone: VARCHAR(20) NULL",
            "  + role: ENUM('admin', 'chusan', 'user') NOT NULL",
            "  + created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "Điểm nhấn kỹ thuật:",
            "  + Mật khẩu băm 1 chiều an toàn: $2a$10$N9qo...",
            "  + Định nghĩa ENUM trực tiếp trong MySQL để tối ưu hiệu năng."
        ],
        subtitle="Quản lý định danh và tài khoản bảo mật",
        border_color=C_BLUE
    )

    create_card(
        s7, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "CSDL sân bóng (pitchos_pitch_db)",
        [
            "Script SQL: pitch-service.sql",
            "Bảng: Bảng sân bóng (pitches)",
            "Cấu trúc các trường dữ liệu:",
            "  + id: BIGINT AUTO_INCREMENT PRIMARY KEY",
            "  + name: VARCHAR(150) NOT NULL",
            "  + pitch_type: ENUM('san_5', 'san_7', 'san_10') NOT NULL",
            "  + price_per_hour: DECIMAL(12, 2) NOT NULL",
            "  + address: VARCHAR(255) NOT NULL",
            "  + thumbnail_url: VARCHAR(500) NULL",
            "  + google_map_url: TEXT NULL",
            "  + status: ENUM('hoat_dong', 'bao_tri') NOT NULL",
            "  + created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "Điểm nhấn kỹ thuật:",
            "  + Dùng DECIMAL(12,2) triệt tiêu sai số làm tròn số học khi tính tiền.",
            "  + Định nghĩa ENUM phân loại sân và trạng thái vận hành."
        ],
        subtitle="Quản lý cơ sở vật chất và bảng giá",
        border_color=C_TEAL
    )

    # =========================================================================
    # SLIDE 8: THIẾT KẾ SCRIPT SQL CSDL 3 & DỮ LIỆU MẪU (SEED DATA)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "THIẾT KẾ SCRIPT SQL: BOOKING_DB & SEED DATA", "08 / 15", "Đáp ứng Câu 2 Ý 3: CSDL đặt sân và nạp dữ liệu mẫu ban đầu để kiểm thử")

    create_card(
        s8, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "CSDL đặt sân (pitchos_booking_db)",
        [
            "Script SQL: booking-service.sql",
            "Bảng: Bảng đơn đặt (bookings)",
            "Cấu trúc các trường dữ liệu:",
            "  + id: BIGINT AUTO_INCREMENT PRIMARY KEY",
            "  + user_id: BIGINT NOT NULL (Khóa logic tham chiếu users.id)",
            "  + pitch_id: BIGINT NOT NULL (Khóa logic tham chiếu pitches.id)",
            "  + start_time: DATETIME NOT NULL",
            "  + end_time: DATETIME NOT NULL",
            "  + total_price: DECIMAL(12, 2) NOT NULL",
            "  + status: ENUM('cho_duyet', 'da_duyet', 'tu_choi') NOT NULL",
            "  + created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "⚠️ QUY TẮC BẤT BIẾN:",
            "  + Tuyệt đối KHÔNG tạo Foreign Key vật lý sang DB khác.",
            "  + Hai trường user_id và pitch_id thuần túy là số nguyên BIGINT."
        ],
        subtitle="Lưu trữ giao dịch đặt sân và lịch thi đấu",
        border_color=C_GREEN
    )

    create_card(
        s8, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "DỮ LIỆU NẠP MẪU BAN ĐẦU (SEED DATA)",
        [
            "Hùng nạp sẵn dữ liệu ban đầu cho cả 3 CSDL:",
            "1. pitchos_user_db: 3 tài khoản đại diện 3 vai trò:",
            "  + admin (Quản trị viên) - pass 123456",
            "  + chusan (Trần Văn Chủ Sân) - pass 123456",
            "  + user (Nguyễn Văn Khách Hàng) - pass 123456",
            "2. pitchos_pitch_db: 4 sân bóng mini cấu hình đa dạng:",
            "  + Sân 5 Cầu Giấy (ID = 1): 300.000đ/h, hoat_dong",
            "  + Sân 7 Mỹ Đình (ID = 2): 500.000đ/h, hoat_dong",
            "  + Sân 10 Tây Hồ (ID = 3): 800.000đ/h, hoat_dong",
            "  + Sân 5 Phúc Diễn (ID = 4): 250.000đ/h, bao_tri",
            "3. pitchos_booking_db: 1 đơn đặt mẫu (ID = 1) để kiểm thử."
        ],
        subtitle="Sẵn sàng nạp vào MySQL trước khi khởi động ứng dụng",
        border_color=C_BLUE
    )

    # =========================================================================
    # SLIDE 9: SƠ ĐỒ THỰC THỂ QUAN HỆ PHÂN TÁN (DISTRIBUTED ERD)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "SƠ ĐỒ THỰC THỂ QUAN HỆ PHÂN TÁN (DISTRIBUTED ERD)", "09 / 15", "Mô hình ERD phân tán phi tập trung - Không có Foreign Key vật lý")

    img_erd_path = os.path.join(r"c:\Users\viduc\Downloads\PTPM\docs\images", "pitchos-distributed-erd.png")
    if os.path.exists(img_erd_path):
        s9.shapes.add_picture(img_erd_path, Inches(1.51), Inches(1.3), width=Inches(10.31), height=Inches(5.8))
    else:
        # Fallback card nếu không tìm thấy file ảnh
        card_u = create_card(
            s9, Inches(0.8), Inches(1.5), Inches(3.6), Inches(4.3),
            "USERS (pitchos_user_db)",
            [
                "id: BIGINT (PK, Auto)",
                "username: VARCHAR(50) (UK)",
                "email: VARCHAR(100) (UK)",
                "password: VARCHAR(255)",
                "full_name: VARCHAR(100)",
                "phone: VARCHAR(20)",
                "role: ENUM(admin, chusan, user)",
                "created_at: TIMESTAMP"
            ],
            subtitle="CSDL người dùng",
            border_color=C_BLUE,
            bg_color=C_LIGHT_BLUE
        )
        card_b = create_card(
            s9, Inches(4.8), Inches(1.5), Inches(3.7), Inches(4.3),
            "BOOKINGS (pitchos_booking_db)",
            [
                "id: BIGINT (PK, Auto)",
                "user_id: BIGINT (Logical ID)",
                "pitch_id: BIGINT (Logical ID)",
                "start_time: DATETIME",
                "end_time: DATETIME",
                "total_price: DECIMAL(12,2)",
                "status: ENUM(cho_duyet, ...)",
                "created_at: TIMESTAMP"
            ],
            subtitle="CSDL đặt sân (Trung tâm giao dịch)",
            border_color=C_GREEN,
            bg_color=C_LIGHT_GREEN
        )
        card_p = create_card(
            s9, Inches(8.9), Inches(1.5), Inches(3.6), Inches(4.3),
            "PITCHES (pitchos_pitch_db)",
            [
                "id: BIGINT (PK, Auto)",
                "name: VARCHAR(150)",
                "pitch_type: ENUM(san_5, 7, 10)",
                "price_per_hour: DECIMAL(12,2)",
                "address: VARCHAR(255)",
                "thumbnail_url: VARCHAR(500)",
                "status: ENUM(hoat_dong, ...)",
                "created_at: TIMESTAMP"
            ],
            subtitle="CSDL sân bóng",
            border_color=C_TEAL,
            bg_color=C_BG_CARD
        )
        create_card(
            s9, Inches(0.8), Inches(5.95), Inches(11.7), Inches(1.15),
            "ĐẶC ĐIỂM QUAN HỆ: LIÊN KẾT LOGIC HOÀN TOÀN - KHÔNG FOREIGN KEY VẬT LÝ",
            [
                "bookings.user_id liên kết logic với users.id (Xác thực qua JWT Claims khi gửi request).",
                "bookings.pitch_id liên kết logic với pitches.id (Xác thực qua RESTful API của Pitch Service: GET /api/v1/pitches/{id}).",
                "Ba CSDL hoàn toàn cách ly, có thể tách sang 3 máy chủ vật lý độc lập mà không bị ràng buộc cơ học."
            ],
            subtitle="Cơ chế toàn vẹn dữ liệu phi tập trung (Decentralized Integrity)",
            border_color=C_BLUE,
            bg_color=C_WHITE
        )

    # =========================================================================
    # SLIDE 10: TRIẾT LÝ KHÓA LOGIC & TOÀN VẸN PHI TẬP TRUNG
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "TRIẾT LÝ KHÓA LOGIC & TOÀN VẸN DỮ LIỆU PHI TẬP TRUNG", "10 / 15", "Giải pháp bảo đảm tính nhất quán khi không có Foreign Key trong Microservices")

    create_card(
        s10, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "VẤN ĐỀ ĐẶT RA: KHÔNG CÓ FK THÌ TOÀN VẸN THẾ NÀO?",
        [
            "Trong hệ thống Monolith:",
            "  + Dùng FOREIGN KEY để database tự ép toàn vẹn tham chiếu.",
            "  + Không cho phép tạo đơn với user_id hoặc pitch_id không tồn tại.",
            "  + Nhược điểm: Bắt buộc tất cả bảng phải nằm chung 1 schema.",
            "Trong kiến trúc hướng dịch vụ PitchOS:",
            "  + Không thể tạo Foreign Key qua các database độc lập.",
            "  + Toàn vẹn tham chiếu được chuyển giao lên TẦNG ỨNG DỤNG (Decentralized Data Integrity).",
            "  + Dịch vụ tự chịu trách nhiệm kiểm tra tính hợp lệ của dữ liệu trước khi thực thi lệnh ghi đĩa."
        ],
        subtitle="Sự chuyển dịch cơ chế kiểm soát dữ liệu",
        border_color=C_BLUE
    )

    create_card(
        s10, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "CƠ CHẾ BẢO ĐẢM TOÀN VẸN TRONG PITCHOS",
        [
            "1. Bảo đảm tính hợp lệ của user_id:",
            "  + Client gửi JWT Token trong Header Authorization.",
            "  + Filter giải mã token, xác thực chữ ký số bí mật (HMAC-SHA256).",
            "  + Lấy user_id từ claims của token đã được chứng thực.",
            "2. Bảo đảm tính hợp lệ của pitch_id:",
            "  + Booking Service gọi OpenFeign GET /api/v1/pitches/{id}.",
            "  + Nếu sân không tồn tại -> Bắt lỗi 404, hủy luồng tạo đơn.",
            "  + Nếu sân đang bảo trì -> Ném lỗi nghiệp vụ từ chối tạo đơn.",
            "3. Xử lý khi xóa tài nguyên (Xóa mềm - Soft Delete):",
            "  + Sân bóng không xóa cứng khỏi DB mà chỉ đổi status thành bao_tri, bảo đảm đơn cũ trong quá khứ không bị mồ côi."
        ],
        subtitle="Các giải pháp kỹ thuật thực tế được áp dụng",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 11: KIẾN TRÚC TẦNG DỮ LIỆU JPA ENTITY & HIBERNATE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "KIẾN TRÚC TẦNG DỮ LIỆU: JPA ENTITY & HIBERNATE ORM", "11 / 15", "Đáp ứng Câu 2 Ý 3: Mô hình thực thể và ánh xạ quan hệ đối tượng")

    create_card(
        s11, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "MÔ HÌNH THỰC THỂ (JPA ENTITY)",
        [
            "Ánh xạ quan hệ đối tượng ORM (Object-Relational Mapping):",
            "1. Thực thể Booking.java (Booking Service):",
            "  + @Entity, @Table(name = 'bookings')",
            "  + @Id, @GeneratedValue(strategy = GenerationType.IDENTITY)",
            "  + @Column(name = 'user_id', nullable = false) Long userId",
            "  + @Column(name = 'pitch_id', nullable = false) Long pitchId",
            "  + @Column(precision = 12, scale = 2) BigDecimal totalPrice",
            "  + @Enumerated(EnumType.STRING) BookingStatus status",
            "  + @CreationTimestamp LocalDateTime createdAt",
            "2. Thực thể Pitch.java (Pitch Service):",
            "  + @Entity, @Table(name = 'pitches')",
            "  + Ánh xạ pitchType, pricePerHour, status qua Enum.",
            "3. Thực thể User.java (Auth Service):",
            "  + @Entity, @Table(name = 'users')"
        ],
        subtitle="Khai báo tường minh các thuộc tính và annotation chuẩn",
        border_color=C_BLUE
    )

    create_card(
        s11, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "Ý NGHĨA KỸ THUẬT CỦA CÁC ANNOTATION",
        [
            "@Table(name = '...'):",
            "  + Gắn kết thực thể Java với bảng SQL tương ứng trong CSDL.",
            "@Enumerated(EnumType.STRING):",
            "  + Lưu giá trị Enum dưới dạng chuỗi văn bản thuần túy trong MySQL ('cho_duyet', 'da_duyet', 'tu_choi').",
            "  + Tránh sai lệch thứ tự chỉ số số nguyên khi mở rộng code.",
            "BigDecimal cho giá tiền:",
            "  + @Column(precision = 12, scale = 2): Triệt tiêu lỗi làm tròn của kiểu Double/Float.",
            "@CreationTimestamp:",
            "  + Tự động gán thời điểm hệ thống khi INSERT, không cần viết code thủ công."
        ],
        subtitle="Chuẩn hóa dữ liệu giữa Java OOP và RDBMS",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 12: TẦNG TRUY CẬP DỮ LIỆU SPRING DATA JPA REPOSITORY
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "TẦNG TRUY CẬP DỮ LIỆU: SPRING DATA JPA REPOSITORY", "12 / 15", "Đáp ứng Câu 2 Ý 3: Cách truy cập dữ liệu thông qua các lớp phù hợp")

    create_card(
        s12, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "CẤU TRÚC TẦNG REPOSITORY (MẪU THIẾT KẾ DAO)",
        [
            "Kế thừa interface JpaRepository<T, ID> của Spring Data JPA:",
            "1. UserRepository.java (Auth Service):",
            "  + Kế thừa: JpaRepository<User, Long>",
            "  + Cung cấp Derived Queries tự động sinh SQL:",
            "    * Optional<User> findByUsername(String username);",
            "    * Optional<User> findByEmail(String email);",
            "    * Boolean existsByUsername(String username);",
            "2. PitchRepository.java (Pitch Service):",
            "  + Kế thừa: JpaRepository<Pitch, Long>",
            "  + Lọc sân: findByPitchTypeAndStatus(...)",
            "3. BookingRepository.java (Booking Service):",
            "  + Kế thừa: JpaRepository<Booking, Long>",
            "  + Tra cứu lịch sử: findByUserIdOrderByCreatedAtDesc(...)"
        ],
        subtitle="Tối ưu hóa thao tác CRUD và truy vấn dẫn xuất",
        border_color=C_BLUE
    )

    create_card(
        s12, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "ƯU THẾ VƯỢT TRỘI CỦA SPRING DATA JPA",
        [
            "1. Triệt tiêu boilerplate code:",
            "  + Không cần mở/đóng kết nối Connection, Statement, ResultSet thủ công như JDBC truyền thống.",
            "2. Quản trị Connection Pool qua HikariCP:",
            "  + HikariCP được cấu hình mặc định mang lại hiệu năng truy cập CSDL nhanh nhất hiện nay.",
            "  + Tự động quản lý số lượng connection chờ và tái sử dụng.",
            "3. Quản lý vòng đời Transaction (@Transactional):",
            "  + Tự động COMMIT khi hàm nghiệp vụ thành công.",
            "  + Tự động ROLLBACK khi có ngoại lệ Exception, bảo đảm tính toàn vẹn (Atomicity)."
        ],
        subtitle="Hiệu năng cao, bảo mật và an toàn dữ liệu",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 13: THUẬT TOÁN CHỐNG TRÙNG SÂN (ĐIỂM NHẤN CỦA HÙNG)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "THUẬT TOÁN & TRUY VẤN CHỐNG TRÙNG LỊCH THI ĐẤU", "13 / 15", "Điểm nhấn kỹ thuật tối ưu hóa do Hùng trực tiếp thiết kế và cài đặt")

    img_algo_path = os.path.join(r"c:\Users\viduc\Downloads\PTPM\docs\images", "pitchos-time-overlap-algorithm.png")
    if os.path.exists(img_algo_path):
        s13.shapes.add_picture(img_algo_path, Inches(1.51), Inches(1.3), width=Inches(10.31), height=Inches(5.8))
    else:
        create_card(
            s13, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
            "ĐIỀU KIỆN TOÁN HỌC GIAO THOA THỜI GIAN",
            [
                "Bài toán: Một sân bóng tại một thời điểm chỉ cho 1 đội thuê.",
                "Điều kiện toán học kiểm tra trùng giữa đơn cũ [start_old, end_old] và đơn mới [start_new, end_new]:",
                "  + start_old < end_new VÀ end_old > start_new",
                "Bao trùm toàn bộ 4 trường hợp giao thoa:",
                "  1. Đơn cũ bắt đầu trước, kết thúc ở giữa khung giờ mới.",
                "  2. Đơn cũ bắt đầu ở giữa, kết thúc sau khung giờ mới.",
                "  3. Đơn cũ nằm lọt hoàn toàn bên trong khung giờ mới.",
                "  4. Đơn cũ bao trùm toàn bộ khung giờ mới.",
                "Quy tắc nghiệp vụ: Bỏ qua đơn có status = 'tu_choi' (sân coi như đang trống ở khung giờ đó)."
            ],
            subtitle="Mô hình toán học kiểm tra xung đột thời gian",
            border_color=C_BLUE
        )
        create_card(
            s13, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
            "CÀI ĐẶT TRUY VẤN JPQL TRONG BOOKINGREPOSITORY",
            [
                "@Query(\"SELECT COUNT(b) FROM Booking b \" +",
                "       \"WHERE b.pitchId = :pitchId \" +",
                "       \"  AND b.status <> com.pitchos.booking.entity.BookingStatus.tu_choi \" +",
                "       \"  AND b.startTime < :endTime \" +",
                "       \"  AND b.endTime > :startTime\")",
                "Long countOverlappingBookings(@Param(\"pitchId\") Long pitchId,",
                "                              @Param(\"startTime\") LocalDateTime start,",
                "                              @Param(\"endTime\") LocalDateTime end);",
                "Tối ưu hiệu năng vượt trội:",
                "  + Dùng COUNT đếm trực tiếp trên Database Engine.",
                "  + Trả về con số duy nhất (0 hoặc > 0), không nạp Entity lên RAM.",
                "  + Nếu count > 0 -> Ném ngoại lệ chặn ngay từ đầu."
            ],
            subtitle="Cài đặt thực tế bằng truy vấn JPQL tối ưu",
            border_color=C_GREEN
        )

    # =========================================================================
    # SLIDE 14: THỰC NGHIỆM KIỂM CHỨNG GHI ĐĨA CỨNG & DEMO (CÂU 2 Ý 3)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "THỰC NGHIỆM KIỂM CHỨNG DỮ LIỆU GHI ĐĨA CỨNG", "14 / 15", "Đáp ứng Câu 2 Ý 3: Thực hiện một nghiệp vụ có thao tác dữ liệu và kiểm tra kết quả")

    img_seq_path = os.path.join(r"c:\Users\viduc\Downloads\PTPM\docs\images", "pitchos-data-sequence.png")
    if os.path.exists(img_seq_path):
        s14.shapes.add_picture(img_seq_path, Inches(1.51), Inches(1.3), width=Inches(10.31), height=Inches(5.8))
    else:
        create_card(
            s14, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
            "KỊCH BẢN THAO TÁC DỮ LIỆU THỰC TẾ",
            [
                "Khách hàng 'user' (ID = 3) đặt Sân 5 Cầu Giấy (ID = 1):",
                "  + Khung giờ: 18:00 - 19:30 (1,5 giờ).",
                "Luồng thực thi trong Booking Service:",
                "  1. Chạy countOverlappingBookings: Trả về 0 (Không trùng).",
                "  2. Gửi OpenFeign GET /api/v1/pitches/1 sang Pitch Service:",
                "     Nhận về đơn giá: 300.000 VNĐ/giờ.",
                "  3. Tính tổng tiền: 1,5 h x 300.000 = 450.000 VNĐ.",
                "  4. Gọi bookingRepository.save(newBooking) ghi xuống đĩa.",
                "  5. Trả về mã HTTP 201 Created."
            ],
            subtitle="Quy trình thực thi nghiệp vụ mẫu",
            border_color=C_BLUE
        )
        create_card(
            s14, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
            "KẾT QUẢ XÁC MINH TRỰC TIẾP TRÊN DBEAVER",
            [
                "Câu lệnh SQL kiểm chứng:",
                "SELECT id, user_id, pitch_id, start_time, end_time,",
                "       total_price, status, created_at",
                "FROM pitchos_booking_db.bookings",
                "ORDER BY id DESC LIMIT 1;",
                "Kết quả hiển thị trên bảng dữ liệu DBeaver:",
                "  + id = 2 (Tăng tự động AUTO_INCREMENT).",
                "  + user_id = 3 | pitch_id = 1 (Lưu đúng Khóa logic).",
                "  + total_price = 450000.00 (Chính xác đến số thập phân).",
                "  + status = 'cho_duyet' (Lưu bền vững vào tệp bookings.ibd của InnoDB trên đĩa cứng)."
            ],
            subtitle="Minh chứng thực nghiệm trực quan",
            border_color=C_GREEN
        )

    # =========================================================================
    # SLIDE 15: TỔNG KẾT ĐÁNH GIÁ & BỘ CÂU HỎI PHẢN BIỆN (Q&A)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "TỔNG KẾT ĐÁNH GIÁ & SẴN SÀNG TRẢ LỜI PHẢN BIỆN", "15 / 15", "Tự đánh giá hoàn thành 100% tiêu chí đề thi - Mục tiêu 2,25 / 2,25 Điểm")

    create_card(
        s15, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5),
        "ĐỐI CHIẾU CHUẨN ĐẦU RA CĐR L1",
        [
            "Hoàn thành 100% tiêu chí đề bài:",
            "1. Câu 1 Ý 2b (0,75đ - Lý thuyết):",
            "  + Giải thích nguyên tắc Database-per-service rõ ràng.",
            "  + Làm rõ lý do cấm truy cập trực tiếp CSDL khác.",
            "  + Phân tích đủ 4 rủi ro: Schema Coupling, Deadlock chéo, vỡ bao đóng, cản trở scale.",
            "2. Câu 2 Ý 3 (1,50đ - Thực nghiệm):",
            "  + Cài đặt 3 CSDL MySQL vật lý (không lưu RAM tạm).",
            "  + Thể hiện mô hình ERD với Logical ID, tầng JPA Entity / Repo.",
            "  + Thực hiện nghiệp vụ tạo đơn và kiểm chứng ghi đĩa.",
            "  + Bảo đảm cách ly dữ liệu và giao tiếp qua Feign API."
        ],
        subtitle="Mức độ hoàn thành các tiêu chí đề bài",
        border_color=C_BLUE
    )

    create_card(
        s15, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.5),
        "BỘ CÂU HỎI PHẢN BIỆN TRỌNG TÂM",
        [
            "Hội đồng thường hỏi & Chìa khóa trả lời:",
            "1. Vì sao không dùng chung 1 DB? -> Trả lời: Tránh Schema Coupling, Deadlock chéo, giữ tính độc lập.",
            "2. Không có FK thì dữ liệu có bị mồ côi? -> Trả lời: Áp dụng Xóa mềm (Soft Delete) và xác thực qua API/JWT.",
            "3. Vì sao không dùng BETWEEN cho trùng giờ? -> Trả lời: BETWEEN bỏ sót trường hợp khung giờ mới bao trùm hoàn toàn khung giờ cũ.",
            "4. Xử lý khi 2 người cùng đặt 1 sân cùng lúc? -> Trả lời: Dùng @Transactional, Pessimistic Lock hoặc Redis Distributed Lock.",
            "5. Chứng minh dữ liệu đã ghi đĩa? -> Trả lời: Khởi động lại service dữ liệu vẫn còn, tệp bookings.ibd tăng kích thước."
        ],
        subtitle="Chuẩn bị sẵn sàng bảo vệ tự tin trước Hội đồng",
        border_color=C_GREEN
    )

    return prs

if __name__ == "__main__":
    deck = build_hung_15_deck()
    
    out_dir = r"c:\Users\viduc\Downloads\PTPM\docs"
    out_file1 = os.path.join(out_dir, "PitchOS-Bao-Cao-Hung.pptx")
    deck.save(out_file1)
    print(f"Saved: {out_file1}")

    # Also save to Downloads
    out_file2 = r"c:\Users\viduc\Downloads\PitchOS-Slide-Hung-Visual.pptx"
    try:
        deck.save(out_file2)
        print(f"Saved: {out_file2}")
    except Exception as e:
        print(f"Could not save out_file2: {e}")

    out_file3 = r"c:\Users\viduc\Downloads\PitchOS-Bao-Cao-Hung.pptx"
    try:
        deck.save(out_file3)
        print(f"Saved: {out_file3}")
    except Exception as e:
        print(f"Note on out_file3: {e}")
