import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_hung_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Bảng màu chuyên nghiệp dành riêng cho Database & Data Engineering
    C_NAVY_DARK = RGBColor(15, 23, 42)     # Slate 900
    C_BLUE = RGBColor(30, 64, 175)         # Blue 700 (Chủ đạo)
    C_TEAL = RGBColor(13, 148, 136)        # Teal 600 (Database)
    C_GREEN = RGBColor(21, 128, 61)        # Green 700 (Thành công / Xác nhận)
    C_RED = RGBColor(185, 28, 28)          # Red 700 (Rủi ro / Cảnh báo)
    C_GRAY = RGBColor(100, 116, 139)       # Slate 500 (Ghi chú / Phụ)
    C_DARK = RGBColor(30, 41, 59)          # Slate 800 (Text chính)
    C_WHITE = RGBColor(255, 255, 255)      # White
    C_BG_CARD = RGBColor(248, 250, 252)    # Slate 50 (Nền card)
    C_BORDER = RGBColor(226, 232, 240)     # Slate 200 (Viền card)
    C_CODE_BG = RGBColor(241, 245, 249)    # Slate 100 (Nền code)
    C_LIGHT_BLUE = RGBColor(239, 246, 255) # Blue 50
    C_LIGHT_GREEN = RGBColor(240, 253, 244)# Green 50
    C_LIGHT_RED = RGBColor(254, 242, 242)  # Red 50

    def add_header(slide, title_text, page_num_str, sub_text=None):
        # Header title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10.5), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = C_NAVY_DARK

        if sub_text:
            p_sub = tf.add_paragraph()
            p_sub.text = sub_text
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_GRAY
            p_sub.space_before = Pt(2)

        # Page number badge
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
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = title_color

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(10.5)
            p_sub.font.color.rgb = C_GRAY
            p_sub.space_after = Pt(4)

        for item in items:
            p_item = tf.add_paragraph()
            p_item.text = f"- {item}"
            p_item.font.name = "Segoe UI"
            p_item.font.size = Pt(11)
            p_item.font.color.rgb = C_DARK
            p_item.space_after = Pt(3)

        return shape

    # =========================================================================
    # SLIDE 1: BÌA BÁO CÁO CHUYÊN ĐỀ
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(248, 250, 252)
    bg1.line.fill.background()

    # Dải màu trang trí dọc bên trái
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), Inches(7.5))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = C_BLUE
    bar1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(3.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "BÀI KIỂM TRA SỐ 1 - HỌC PHẦN KIẾN TRÚC PHẦN MỀM / PHÁT TRIỂN PHẦN MỀM"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_BLUE
    p0.space_after = Pt(8)

    p1 = tf1.add_paragraph()
    p1.text = "BÁO CÁO CHUYÊN ĐỀ QUẢN TRỊ CƠ SỞ DỮ LIỆU PHÂN TÁN"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(27)
    p1.font.bold = True
    p1.font.color.rgb = C_NAVY_DARK
    p1.space_after = Pt(6)

    p2 = tf1.add_paragraph()
    p2.text = "Hệ thống quản lý đặt sân bóng đá PitchOS (Kiến trúc SOA / Microservices)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(15)
    p2.font.color.rgb = C_GRAY

    # Card thông tin người thực hiện
    info_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.3), Inches(2.9))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = C_WHITE
    info_card.line.color.rgb = C_BORDER
    info_card.line.width = Pt(1.5)

    tb_info = s1.shapes.add_textbox(Inches(1.3), Inches(3.95), Inches(10.7), Inches(2.6))
    tf_info = tb_info.text_frame
    tf_info.word_wrap = True

    pi1 = tf_info.paragraphs[0]
    pi1.text = "THÀNH VIÊN TRÌNH BÀY: HÙNG"
    pi1.font.name = "Segoe UI"
    pi1.font.size = Pt(16)
    pi1.font.bold = True
    pi1.font.color.rgb = C_BLUE
    pi1.space_after = Pt(6)

    pi2 = tf_info.add_paragraph()
    pi2.text = "Vai trò phụ trách: Quản trị Cơ sở Dữ liệu & Kỹ sư Dữ liệu Backend (Database Administrator & Backend Data Engineer)"
    pi2.font.name = "Segoe UI"
    pi2.font.size = Pt(12.5)
    pi2.font.color.rgb = C_DARK
    pi2.space_after = Pt(4)

    pi3 = tf_info.add_paragraph()
    pi3.text = "Phụ trách trọng số: 2,25 / 10,0 Điểm (Câu 1 Ý 2b: 0,75đ Lý thuyết + Câu 2 Ý 3: 1,50đ Thực nghiệm)"
    pi3.font.name = "Segoe UI"
    pi3.font.size = Pt(13)
    pi3.font.bold = True
    pi3.font.color.rgb = C_GREEN
    pi3.space_after = Pt(6)

    pi4 = tf_info.add_paragraph()
    pi4.text = "Nội dung báo cáo: Nguyên tắc Database-per-service | 4 Rủi ro dùng chung DB | 3 CSDL MySQL độc lập | Khóa logic ERD | Thuật toán chống trùng sân | Kiểm chứng ghi đĩa"
    pi4.font.name = "Segoe UI"
    pi4.font.size = Pt(11.5)
    pi4.font.color.rgb = C_GRAY

    # =========================================================================
    # SLIDE 2: MỤC TIÊU VÀ PHẠM VI NHIỆM VỤ
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "MỤC TIÊU & PHẠM VI NHIỆM VỤ CỦA HÙNG", "02 / 10", "Ánh xạ chuẩn đầu ra CĐR L1 theo Barem đề thi kiểm tra số 1")

    create_card(
        s2, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.45),
        "CÂU 1. LÝ THUYẾT - Ý 2b (0,75 ĐIỂM)",
        [
            "Nguyên tắc mỗi dịch vụ quản lý dữ liệu thuộc trách nhiệm của mình (Database-per-service).",
            "Lý giải vì sao một dịch vụ không nên và không được phép truy cập trực tiếp CSDL của dịch vụ khác.",
            "Phân tích chuyên sâu 4 rủi ro kỹ thuật nghiêm trọng khi vi phạm:",
            "  + 1. Ghép nối lược đồ dữ liệu (Schema Coupling)",
            "  + 2. Khóa tranh chấp và Deadlock chéo (Cross-service Deadlock)",
            "  + 3. Phá vỡ tính bao đóng nghiệp vụ (Breaking Business Encapsulation)",
            "  + 4. Cản trở khả năng mở rộng độc lập (Hindering Independent Scalability)",
            "Liên hệ thực tế: Áp dụng phân vùng dữ liệu và giải pháp khắc phục triệt để trong dự án PitchOS."
        ],
        subtitle="Chuẩn đầu ra L1: Phân tích và nắm vững lý thuyết kiến trúc dữ liệu phân tán",
        border_color=C_BLUE
    )

    create_card(
        s2, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.45),
        "CÂU 2. THỰC NGHIỆM - Ý 3 (1,50 ĐIỂM)",
        [
            "Lưu trữ dữ liệu vào hệ quản trị CSDL quan hệ MySQL thay vì chỉ lưu tạm thời trong bộ nhớ RAM.",
            "Thể hiện cấu trúc dữ liệu, mô hình thực thể (JPA Entity) và tầng truy cập dữ liệu (Repository).",
            "Thiết kế 3 CSDL độc lập: CSDL người dùng (pitchos_user_db), CSDL sân bóng (pitchos_pitch_db), CSDL đặt sân (pitchos_booking_db).",
            "Mô hình ERD phân tán sử dụng khóa logic (Logical ID), tuyệt đối không dùng khóa ngoại vật lý giữa các CSDL.",
            "Cài đặt thuật toán kiểm tra chống trùng lịch thi đấu bằng câu truy vấn JPQL tối ưu toán học.",
            "Thực hiện một nghiệp vụ có thao tác dữ liệu và kiểm chứng bản ghi ghi đĩa trên DBeaver / Workbench."
        ],
        subtitle="Chuẩn đầu ra L1: Trực tiếp xây dựng CSDL, lập trình tầng dữ liệu và kiểm chứng thực nghiệm",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 3: NGUYÊN TẮC DATABASE-PER-SERVICE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "NGUYÊN TẮC DATABASE-PER-SERVICE TRONG HỆ THỐNG PITCHOS", "03 / 10", "Đáp ứng Câu 1 Ý 2b: Phân tích 3 trụ cột thiết kế dữ liệu độc lập")

    create_card(
        s3, Inches(0.8), Inches(1.45), Inches(3.7), Inches(5.45),
        "1. Quyền sở hữu độc quyền",
        [
            "Exclusive Data Ownership.",
            "Mỗi dịch vụ chỉ sở hữu và chịu trách nhiệm toàn bộ đối với CSDL thuộc ngữ cảnh nghiệp vụ (Bounded Context) của mình.",
            "Dịch vụ xác thực (Auth Service) độc quyền quản lý thông tin tài khoản người dùng.",
            "Dịch vụ sân bóng (Pitch Service) độc quyền quản lý thông tin sân bóng và bảng giá.",
            "Dịch vụ đặt sân (Booking Service) độc quyền quản lý giao dịch và lịch đặt sân."
        ],
        subtitle="Phân định ranh giới ngữ cảnh rõ ràng",
        border_color=C_BLUE
    )

    create_card(
        s3, Inches(4.8), Inches(1.45), Inches(3.7), Inches(5.45),
        "2. Tính đóng gói dữ liệu",
        [
            "Data Encapsulation.",
            "Cơ sở dữ liệu được xem như là thành phần nội bộ (private implementation detail) của từng dịch vụ.",
            "Tuyệt đối không một dịch vụ nào được cấp tài khoản hoặc chuỗi kết nối để đọc/ghi trực tiếp vào CSDL của dịch vụ khác.",
            "Ngăn chặn việc rò rỉ cấu trúc bảng nội bộ ra các dịch vụ phụ thuộc bên ngoài.",
            "Bảo đảm tính toàn vẹn và độc lập về công nghệ lưu trữ."
        ],
        subtitle="Ẩn giấu chi tiết cài đặt vật lý",
        border_color=C_TEAL
    )

    create_card(
        s3, Inches(8.8), Inches(1.45), Inches(3.7), Inches(5.45),
        "3. Truy xuất qua RESTful API",
        [
            "API-driven Data Access.",
            "Mọi nhu cầu truy vấn hoặc thay đổi dữ liệu từ bên ngoài bắt buộc phải thông qua RESTful API công khai do dịch vụ chủ quản cung cấp.",
            "Ví dụ cụ thể trong hệ thống:",
            "  + Khi tạo đơn đặt, Dịch vụ đặt sân (Booking Service) cần xác thực sân và đơn giá -> Không truy cập trực tiếp CSDL sân bóng.",
            "  + Dịch vụ gửi request GET qua OpenFeign tới Dịch vụ sân bóng (Pitch Service): /api/v1/pitches/{id}."
        ],
        subtitle="Giao tiếp chuẩn hóa theo giao thức HTTP",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 4: 4 RỦI RO KỸ THUẬT KHI VI PHẠM DÙNG CHUNG CSDL
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "4 RỦI RO KỸ THUẬT KHI VI PHẠM DÙNG CHUNG CSDL", "04 / 10", "Đáp ứng Câu 1 Ý 2b: Vì sao không nên truy cập trực tiếp CSDL của dịch vụ khác?")

    create_card(
        s4, Inches(0.8), Inches(1.45), Inches(5.6), Inches(2.6),
        "1. Ghép nối lược đồ dữ liệu (Schema Coupling)",
        [
            "Bản chất: Nhiều dịch vụ cùng đọc/ghi trực tiếp vào chung một bảng SQL.",
            "Hậu quả: Khi một dịch vụ đổi tên cột, xóa cột hoặc sửa kiểu dữ liệu, các dịch vụ khác lập tức bị lỗi khi chạy (Runtime Exception).",
            "Tác động: Đội ngũ buộc phải điều phối triển khai đồng thời toàn bộ dịch vụ, mất hoàn toàn tính triển khai độc lập (Independent Deployment)."
        ],
        subtitle="Rủi ro về tính phụ thuộc mã nguồn",
        border_color=C_RED
    )

    create_card(
        s4, Inches(6.8), Inches(1.45), Inches(5.7), Inches(2.6),
        "2. Khóa tranh chấp và Deadlock chéo (Cross-service Deadlock)",
        [
            "Bản chất: Nhiều giao dịch (Transaction) từ các dịch vụ khác nhau cùng thao tác khóa dòng (Row-level lock) trên các bản ghi liên quan.",
            "Hậu quả: Service A giữ khóa bảng 1 chờ bảng 2, trong khi Service B giữ khóa bảng 2 chờ bảng 1 -> Xảy ra Deadlock chéo giữa các dịch vụ.",
            "Tác động: Treo luồng xử lý (Thread Pool Exhaustion), kéo sập hàng loạt dịch vụ."
        ],
        subtitle="Rủi ro về hiệu năng và tắc nghẽn luồng",
        border_color=C_RED
    )

    create_card(
        s4, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6),
        "3. Phá vỡ tính bao đóng (Breaking Encapsulation)",
        [
            "Bản chất: Dịch vụ ngoài tự ý INSERT/UPDATE trực tiếp vào database mà không thông qua tầng nghiệp vụ (Business Service Layer).",
            "Hậu quả: Toàn bộ quy tắc kiểm tra tính hợp lệ dữ liệu bị bỏ qua (Ví dụ: tự ý sửa trạng thái sân mà không kiểm tra lịch bảo trì).",
            "Tác động: Dữ liệu bị sai lệch, logic nghiệp vụ bị phân tán rải rác khắp nơi."
        ],
        subtitle="Rủi ro về tính toàn vẹn dữ liệu nghiệp vụ",
        border_color=C_RED
    )

    create_card(
        s4, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6),
        "4. Cản trở mở rộng độc lập (Hindering Scalability)",
        [
            "Bản chất: Toàn bộ dịch vụ dồn tải vào một máy chủ CSDL duy nhất.",
            "Hậu quả: Khi Dịch vụ đặt sân (Booking Service) bị nghẽn I/O do lượng giao dịch cao, Dịch vụ xác thực (Auth Service) cũng bị tê liệt theo.",
            "Tác động: Không thể áp dụng lưu trữ đa dạng (Polyglot Persistence) như Redis cho tra cứu nhanh hoặc MongoDB cho tài liệu linh hoạt."
        ],
        subtitle="Rủi ro về hạ tầng và tải hệ thống",
        border_color=C_RED
    )

    # =========================================================================
    # SLIDE 5: LƯỢC ĐỒ 3 CSDL PHÂN TÁN VÀ CẤU TRÚC BẢNG DỮ LIỆU
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "LƯỢC ĐỒ 3 CƠ SỞ DỮ LIỆU PHÂN TÁN CỦA PITCHOS", "05 / 10", "Đáp ứng Câu 2 Ý 3: Lưu trữ dữ liệu nghiệp vụ vào 3 CSDL MySQL độc lập")

    create_card(
        s5, Inches(0.8), Inches(1.45), Inches(3.7), Inches(5.45),
        "CSDL người dùng (pitchos_user_db)",
        [
            "Dịch vụ sở hữu: Dịch vụ xác thực (Auth Service)",
            "Bảng: Bảng người dùng (users)",
            "Cấu trúc các trường:",
            "  + id: BIGINT (PK, AUTO_INCREMENT)",
            "  + username: VARCHAR(50) (UNIQUE, NOT NULL)",
            "  + email: VARCHAR(100) (UNIQUE, NOT NULL)",
            "  + password: VARCHAR(255) (Mã hóa BCrypt)",
            "  + full_name: VARCHAR(100) (NOT NULL)",
            "  + phone: VARCHAR(20) (NULL)",
            "  + role: ENUM('admin', 'chusan', 'user')",
            "  + created_at: TIMESTAMP",
            "Đặc trưng: Mật khẩu băm một chiều qua BCrypt; phân quyền theo vai trò (RBAC) qua ENUM."
        ],
        subtitle="Quản lý định danh và quyền người dùng",
        border_color=C_BLUE
    )

    create_card(
        s5, Inches(4.8), Inches(1.45), Inches(3.7), Inches(5.45),
        "CSDL sân bóng (pitchos_pitch_db)",
        [
            "Dịch vụ sở hữu: Dịch vụ sân bóng (Pitch Service)",
            "Bảng: Bảng sân bóng (pitches)",
            "Cấu trúc các trường:",
            "  + id: BIGINT (PK, AUTO_INCREMENT)",
            "  + name: VARCHAR(150) (Tên sân bóng)",
            "  + pitch_type: ENUM('san_5', 'san_7', 'san_10')",
            "  + price_per_hour: DECIMAL(12, 2) (Giá thuê/h)",
            "  + address: VARCHAR(255) (Địa chỉ sân)",
            "  + thumbnail_url: VARCHAR(500) (Đường dẫn ảnh)",
            "  + google_map_url: TEXT (Tọa độ định vị)",
            "  + status: ENUM('hoat_dong', 'bao_tri')",
            "  + created_at: TIMESTAMP",
            "Đặc trưng: Dùng DECIMAL(12,2) triệt tiêu sai số làm tròn số học khi tính tiền thuê."
        ],
        subtitle="Quản lý danh mục sân và bảng giá",
        border_color=C_TEAL
    )

    create_card(
        s5, Inches(8.8), Inches(1.45), Inches(3.7), Inches(5.45),
        "CSDL đặt sân (pitchos_booking_db)",
        [
            "Dịch vụ sở hữu: Dịch vụ đặt sân (Booking Service)",
            "Bảng: Bảng đơn đặt (bookings)",
            "Cấu trúc các trường:",
            "  + id: BIGINT (PK, AUTO_INCREMENT)",
            "  + user_id: BIGINT (Logical ID - Người đặt)",
            "  + pitch_id: BIGINT (Logical ID - Sân bóng)",
            "  + start_time: DATETIME (Thời gian bắt đầu)",
            "  + end_time: DATETIME (Thời gian kết thúc)",
            "  + total_price: DECIMAL(12, 2) (Tổng tiền thuê)",
            "  + status: ENUM('cho_duyet', 'da_duyet', 'tu_choi')",
            "  + created_at: TIMESTAMP",
            "Đặc trưng: Lưu trữ khóa logic, không tạo ràng buộc FOREIGN KEY vật lý sang các CSDL khác."
        ],
        subtitle="Quản lý giao dịch và lịch thi đấu",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 6: MÔ HÌNH ERD PHÂN TÁN VÀ TRIẾT LÝ KHÓA LOGIC (LOGICAL ID)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "MÔ HÌNH ERD PHÂN TÁN & TRIẾT LÝ KHÓA LOGIC", "06 / 10", "Đáp ứng Câu 2 Ý 3: Bảo đảm toàn vẹn dữ liệu phi tập trung không dùng Khóa ngoại vật lý")

    create_card(
        s6, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.45),
        "MÔ HÌNH THỰC THỂ ERD PHÂN TÁN",
        [
            "Trong hệ thống nguyên khối truyền thống:",
            "  + Sử dụng FOREIGN KEY để Database Engine tự ép toàn vẹn tham chiếu.",
            "  + Hạn chế: Buộc tất cả các bảng phải nằm chung một cơ sở dữ liệu vật lý.",
            "Trong kiến trúc hướng dịch vụ PitchOS:",
            "  + Bảng Bảng đơn đặt (bookings) trong CSDL đặt sân (pitchos_booking_db) chỉ lưu 2 cột Logical ID:",
            "    * user_id: BIGINT NOT NULL",
            "    * pitch_id: BIGINT NOT NULL",
            "  + TUYỆT ĐỐI KHÔNG TỒN TẠI ràng buộc vật lý FOREIGN KEY.",
            "Toàn vẹn tham chiếu được kiểm soát tại tầng ứng dụng:",
            "  + Xác thực thông tin người dùng qua JWT Token (Claims context).",
            "  + Xác thực thông tin sân qua RESTful API của Dịch vụ sân bóng (Pitch Service)."
        ],
        subtitle="Sơ đồ quan hệ thực thể phi tập trung (Decentralized ERD)",
        border_color=C_BLUE
    )

    create_card(
        s6, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.45),
        "ƯU THẾ VƯỢT TRỘI CỦA KHÓA LOGIC",
        [
            "1. Cách ly hoàn toàn tầng lưu trữ vật lý:",
            "  + Có thể di chuyển CSDL người dùng (pitchos_user_db) sang cụm server khác mà không ảnh hưởng tới CSDL đặt sân (pitchos_booking_db).",
            "2. Độc lập triển khai và phát triển (Decoupled Lifecycle):",
            "  + Bảng sân bóng (pitches) có thể bổ sung trường mới, migrate schema mà không sợ làm sập bảng Bảng đơn đặt (bookings).",
            "3. Tuân thủ tuyệt đối chuẩn đầu ra đề thi:",
            "  + Đáp ứng tiêu chí: 'Bảo đảm dịch vụ chỉ truy cập trực tiếp dữ liệu thuộc phạm vi quản lý của mình'.",
            "  + Mọi tương tác lấy giá sân đều qua giao tiếp mạng HTTP/REST chuẩn mực."
        ],
        subtitle="Lợi ích kiến trúc thực tiễn của Microservices",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 7: KIẾN TRÚC TẦNG DỮ LIỆU SPRING DATA JPA & REPOSITORY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "KIẾN TRÚC TẦNG DỮ LIỆU SPRING DATA JPA & HIBERNATE", "07 / 10", "Đáp ứng Câu 2 Ý 3: Mô hình thực thể và cách truy cập dữ liệu thông qua các lớp")

    create_card(
        s7, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.45),
        "MÔ HÌNH THỰC THỂ (JPA ENTITY)",
        [
            "Ánh xạ quan hệ đối tượng ORM (Object-Relational Mapping):",
            "1. Thực thể User (Dịch vụ xác thực - Auth Service):",
            "  + Khai báo @Entity, @Table(name = 'users').",
            "  + @Enumerated(EnumType.STRING) cho Role ('admin', 'chusan', 'user').",
            "  + @CreationTimestamp tự động gán thời gian tạo bản ghi.",
            "2. Thực thể Pitch (Dịch vụ sân bóng - Pitch Service):",
            "  + Khai báo @Entity, @Table(name = 'pitches').",
            "  + @Column(precision = 12, scale = 2) BigDecimal pricePerHour.",
            "  + Enum PitchType ('san_5', 'san_7', 'san_10').",
            "3. Thực thể Booking (Dịch vụ đặt sân - Booking Service):",
            "  + Khai báo @Entity, @Table(name = 'bookings').",
            "  + Ánh xạ @Column Long userId và Long pitchId dạng Logical ID."
        ],
        subtitle="Khai báo tường minh các thuộc tính và kiểu dữ liệu",
        border_color=C_BLUE
    )

    create_card(
        s7, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.45),
        "TẦNG TRUY CẬP DỮ LIỆU (JPA REPOSITORY)",
        [
            "Kế thừa JpaRepository<T, ID> chuẩn Spring Boot:",
            "1. UserRepository: Cung cấp các phương thức truy vấn dẫn xuất (Derived Queries):",
            "  + Optional<User> findByUsername(String username);",
            "  + Optional<User> findByEmail(String email);",
            "  + Boolean existsByUsername(String username);",
            "2. PitchRepository: Hỗ trợ tìm kiếm theo tiêu chí:",
            "  + List<Pitch> findByPitchType(PitchType type);",
            "  + List<Pitch> findByStatus(PitchStatus status);",
            "3. Lợi ích kỹ thuật:",
            "  + Không cần viết mã SQL thuần cho các thao tác CRUD cơ bản.",
            "  + Tự động quản lý vòng đời Transaction và Connection Pool (HikariCP)."
        ],
        subtitle="Tầng Repository chuẩn mực theo mẫu thiết kế DAO",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 8: THUẬT TOÁN CHỐNG TRÙNG LỊCH THI ĐẤU (ĐIỂM NHẤN CỦA HÙNG)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "THUẬT TOÁN & TRUY VẤN CHỐNG TRÙNG LỊCH THI ĐẤU", "08 / 10", "Điểm nhấn kỹ thuật tối ưu hóa do Hùng trực tiếp thiết kế và cài đặt")

    create_card(
        s8, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.45),
        "ĐIỀU KIỆN TOÁN HỌC GIAO THOA THỜI GIAN",
        [
            "Bài toán nghiệp vụ: Một sân bóng tại một thời điểm chỉ cho phép một đội bóng thuê (Tránh Overbooking / Double-booking).",
            "Điều kiện toán học kiểm tra giao nhau giữa đơn cũ [start_old, end_old] và đơn mới [start_new, end_new]:",
            "  + start_old < end_new VÀ end_old > start_new",
            "4 trường hợp giao thoa đều được công thức này bao quát:",
            "  1. Đơn cũ bắt đầu trước, kết thúc ở giữa khung giờ mới.",
            "  2. Đơn cũ bắt đầu ở giữa, kết thúc sau khung giờ mới.",
            "  3. Đơn cũ nằm trọn hoàn toàn bên trong khung giờ mới.",
            "  4. Đơn cũ bao trùm toàn bộ khung giờ mới.",
            "Nghiệp vụ bổ sung: Bỏ qua các đơn có trạng thái 'tu_choi' (sân coi như đang trống ở khung giờ đó)."
        ],
        subtitle="Mô hình toán học kiểm tra xung đột thời gian",
        border_color=C_BLUE
    )

    create_card(
        s8, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.45),
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
            "Tối ưu hóa hiệu năng vượt trội:",
            "  + Dùng hàm COUNT đếm trực tiếp trên Database Engine.",
            "  + Trả về số lượng (0 hoặc > 0), không phải load toàn bộ Entity lên RAM.",
            "  + Nếu count > 0 -> Ném Business Exception chặn ngay từ đầu."
        ],
        subtitle="Cài đặt thực tế bằng truy vấn JPQL tối ưu",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 9: KIỂM CHỨNG GHI ĐĨA CỨNG VÀ KỊCH BẢN DEMO
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "THỰC NGHIỆM KIỂM CHỨNG DỮ LIỆU GHI ĐĨA CỨNG", "09 / 10", "Đáp ứng Câu 2 Ý 3: Thực hiện nghiệp vụ có thao tác dữ liệu và kiểm tra kết quả")

    create_card(
        s9, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.45),
        "KỊCH BẢN THAO TÁC DỮ LIỆU THỰC TẾ",
        [
            "Bước 1: Nạp sẵn dữ liệu ban đầu (Seed Data):",
            "  + CSDL người dùng (pitchos_user_db): 3 tài khoản mẫu.",
            "  + CSDL sân bóng (pitchos_pitch_db): 4 sân bóng mẫu.",
            "  + CSDL đặt sân (pitchos_booking_db): 1 đơn đặt mẫu.",
            "Bước 2: Khách hàng 'user' (ID = 3) đặt Sân 5 Cầu Giấy (ID = 1):",
            "  + Thời gian thuê: 18:00 - 19:30 (1,5 giờ).",
            "Bước 3: Dịch vụ đặt sân (Booking Service) xử lý giao dịch:",
            "  + Chạy câu truy vấn kiểm tra trùng lịch: Kết quả trả về 0.",
            "  + Gửi OpenFeign sang Dịch vụ sân bóng (Pitch Service) lấy giá: 300.000 VNĐ/h.",
            "  + Tính toán tổng tiền: 1,5 h x 300.000 = 450.000 VNĐ.",
            "  + Gọi bookingRepository.save(newBooking) ghi xuống đĩa."
        ],
        subtitle="Luồng nghiệp vụ tạo đơn đặt sân mẫu",
        border_color=C_BLUE
    )

    create_card(
        s9, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.45),
        "MINH CHỨNG TRUY VẤN VẬT LÝ TRÊN DBEAVER / WORKBENCH",
        [
            "Câu lệnh SQL xác minh trực tiếp trên máy chủ MySQL:",
            "SELECT id, user_id, pitch_id, start_time, end_time,",
            "       total_price, status, created_at",
            "FROM pitchos_booking_db.bookings",
            "ORDER BY id DESC LIMIT 1;",
            "Kết quả kiểm chứng hiển thị trên màn hình DBeaver:",
            "  + id: 2 (Tăng tự động AUTO_INCREMENT).",
            "  + user_id = 3 | pitch_id = 1 (Lưu đúng Khóa logic).",
            "  + total_price = 450000.00 (Chính xác đến hàng thập phân).",
            "  + status = 'cho_duyet' (Được ghi bền vững xuống tệp ibd của InnoDB Engine trên đĩa cứng)."
        ],
        subtitle="Xác minh trực tiếp trên cơ sở dữ liệu quan hệ",
        border_color=C_GREEN
    )

    # =========================================================================
    # SLIDE 10: TỔNG KẾT ĐÁNH GIÁ CHUẨN ĐẦU RA (CĐR L1)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "TỔNG KẾT ĐÁNH GIÁ & KHẲNG ĐỊNH KẾT QUẢ CỦA HÙNG", "10 / 10", "Tự đánh giá hoàn thành 100% tiêu chí theo yêu cầu Bài kiểm tra số 1")

    create_card(
        s10, Inches(0.8), Inches(1.45), Inches(5.6), Inches(5.45),
        "ĐỐI CHIẾU CHUẨN ĐẦU RA CĐR L1",
        [
            "Câu 1 Ý 2b (0,75 Điểm - Lý thuyết):",
            "  + Đã giải thích rõ ràng nguyên tắc Database-per-service.",
            "  + Đã làm rõ lý do cấm tuyệt đối truy cập trực tiếp CSDL khác.",
            "  + Đã phân tích đủ 4 rủi ro kỹ thuật: Ghép nối lược đồ, Deadlock chéo, vỡ bao đóng, cản trở scale.",
            "Câu 2 Ý 3 (1,50 Điểm - Thực nghiệm):",
            "  + Đã cài đặt lưu trữ CSDL MySQL vật lý (thay vì in-memory).",
            "  + Thể hiện đầy đủ cấu trúc dữ liệu, Entity và Repository JPA.",
            "  + Đã thực hiện nghiệp vụ tạo booking và kiểm tra ghi đĩa.",
            "  + Bảo đảm giao tiếp qua API RESTful, không chọc chéo DB."
        ],
        subtitle="Mức độ hoàn thành các tiêu chí đề bài",
        border_color=C_BLUE
    )

    create_card(
        s10, Inches(6.8), Inches(1.45), Inches(5.7), Inches(5.45),
        "KẾT LUẬN & SẴN SÀNG BẢO VỆ",
        [
            "Điểm số mục tiêu: Đạt tuyệt đối 2,25 / 2,25 Điểm.",
            "Đóng góp kỹ thuật tiêu biểu:",
            "  + Thiết kế thành công kiến trúc CSDL phân tán với 3 schemas.",
            "  + Đề xuất thuật toán chống trùng lịch thi đấu tối ưu hóa hiệu năng bằng hàm COUNT trong JPQL.",
            "  + Triển khai minh chứng thực nghiệm trực quan trên DBeaver.",
            "Sẵn sàng demo trực tiếp và trả lời các câu hỏi phản biện của Hội đồng chấm thi.",
            "Xin chân thành cảm ơn Quý Thầy/Cô đã chú ý lắng nghe!"
        ],
        subtitle="Khẳng định năng lực và kết quả thực hiện",
        border_color=C_GREEN
    )

    return prs

if __name__ == "__main__":
    deck = build_hung_deck()
    
    out_dir = r"c:\Users\viduc\Downloads\PTPM\docs"
    out_file1 = os.path.join(out_dir, "PitchOS-Bao-Cao-Hung.pptx")
    deck.save(out_file1)
    print(f"Saved: {out_file1}")

    # Fallback to Downloads
    out_file2 = r"c:\Users\viduc\Downloads\PitchOS-Bao-Cao-Hung.pptx"
    try:
        deck.save(out_file2)
        print(f"Saved: {out_file2}")
    except Exception as e:
        print(f"Could not save to Downloads folder directly: {e}")
