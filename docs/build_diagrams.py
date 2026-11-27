"""
Sinh cac so do kien truc cua PitchOS ra file PNG trong docs/architecture/.

Chay:  python docs/build_diagrams.py

Phong cach bam theo cac hinh minh hoa trong tai lieu thuc hanh TH7 va TH8:
hop bo goc nen pastel nhat, tieu de dam kem dong phu mau xam ghi cong/vai tro,
xep theo tang, co dong chu giai o duoi.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "architecture")
os.makedirs(OUT, exist_ok=True)

S = 3  # ve o do phan giai gap 3 roi thu nho lai cho min vien

FONTS = "C:/Windows/Fonts/"


FONT_BOOST = 1.3   # phong to chu de de doc khi in o kho 16cm


def font(size, bold=False, italic=False):
    name = "arial.ttf"
    if bold and italic:
        name = "arialbi.ttf"
    elif bold:
        name = "arialbd.ttf"
    elif italic:
        name = "ariali.ttf"
    return ImageFont.truetype(FONTS + name, int(round(size * S * FONT_BOOST)))


# ------------------------------------------------------------- bang mau
WHITE = "#FFFFFF"
INK = "#1A1A2E"
GREY = "#6B6B7B"
LINE = "#B8BCC8"

PAL = {
    "client":   ("#E3F2FD", "#64B5F6"),
    "registry": ("#E8F5E9", "#81C784"),
    "consumer": ("#EDE7F6", "#9575CD"),
    "provider": ("#FFF3E0", "#FFB74D"),
    "service":  ("#E8EAF6", "#7986CB"),
    "data":     ("#FCE4EC", "#F06292"),
    "panel":    ("#FAFAFC", "#D5D8E0"),
    "volume":   ("#F1F8E9", "#AED581"),
}


class Canvas:
    def __init__(self, w, h, bg=WHITE):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * S, h * S), bg)
        self.d = ImageDraw.Draw(self.img)

    # ---- hop bo goc co tieu de va dong phu
    def card(self, x, y, w, h, title, sub=None, kind="service",
             tsize=11, ssize=8, radius=8):
        fill, border = PAL[kind]
        self.d.rounded_rectangle(
            [x * S, y * S, (x + w) * S, (y + h) * S],
            radius=radius * S, fill=fill, outline=border, width=max(1, S // 2))
        if sub:
            self.text(x + w / 2, y + h / 2 - ssize * 0.75, title, tsize, True, INK)
            self.text(x + w / 2, y + h / 2 + tsize * 0.62, sub, ssize, False, GREY)
        else:
            self.text(x + w / 2, y + h / 2, title, tsize, True, INK)
        return (x + w / 2, y, x + w / 2, y + h)  # tam canh tren / duoi

    # ---- khung bao ngoai
    def panel(self, x, y, w, h, label=None, kind="panel", dashed=False):
        fill, border = PAL[kind]
        self.d.rounded_rectangle(
            [x * S, y * S, (x + w) * S, (y + h) * S],
            radius=10 * S, fill=fill, outline=border, width=max(1, S // 2))
        if label:
            self.text(x + w / 2, y + 11, label, 9, True, GREY)

    def text(self, cx, cy, s, size=10, bold=False, color=INK, anchor="mm",
             italic=False):
        self.d.text((cx * S, cy * S), s, font=font(size, bold, italic),
                    fill=color, anchor=anchor)

    def left_text(self, x, cy, s, size=10, bold=False, color=INK, italic=False):
        self.d.text((x * S, cy * S), s, font=font(size, bold, italic),
                    fill=color, anchor="lm")

    # ---- mui ten
    def arrow(self, x1, y1, x2, y2, label=None, dashed=False, color=LINE,
              lsize=8, lcolor=GREY, width=2, head=5, lside=0):
        if dashed:
            self._dashed(x1, y1, x2, y2, color, width)
        else:
            self.d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=color,
                        width=width * S // 2 or 1)
        self._head(x1, y1, x2, y2, color, head)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if abs(x2 - x1) < abs(y2 - y1):          # mui ten doc
                self.text(mx + 4 + lside, my, label, lsize, False, lcolor, "lm")
            else:                                     # mui ten ngang
                self.text(mx, my - 8 + lside, label, lsize, False, lcolor)

    def _dashed(self, x1, y1, x2, y2, color, width, dash=5, gap=4):
        import math
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        ux, uy = dx / dist, dy / dist
        pos = 0.0
        while pos < dist:
            e = min(pos + dash, dist)
            self.d.line([(x1 + ux * pos) * S, (y1 + uy * pos) * S,
                         (x1 + ux * e) * S, (y1 + uy * e) * S],
                        fill=color, width=width * S // 2 or 1)
            pos = e + gap

    def _head(self, x1, y1, x2, y2, color, size):
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        for d in (2.6, -2.6):
            self.d.line([x2 * S, y2 * S,
                         (x2 + size * math.cos(ang + d)) * S,
                         (y2 + size * math.sin(ang + d)) * S],
                        fill=color, width=max(1, S))

    def elbow(self, x1, y1, x2, y2, via_y, label=None, color=LINE, width=2,
              lsize=8, lcolor=GREY):
        """Duong gap khuc: xuong via_y, sang ngang, roi di tiep toi dich."""
        w = width * S // 2 or 1
        self.d.line([x1 * S, y1 * S, x1 * S, via_y * S], fill=color, width=w)
        self.d.line([x1 * S, via_y * S, x2 * S, via_y * S], fill=color, width=w)
        self.d.line([x2 * S, via_y * S, x2 * S, y2 * S], fill=color, width=w)
        self._head(x2, via_y, x2, y2, color, 5)
        if label:
            self.text((x1 + x2) / 2, via_y + 10, label, lsize, False, lcolor)

    def caption(self, s, size=8):
        self.text(self.w / 2, self.h - 12, s, size, False, GREY, italic=True)

    def save(self, name):
        path = os.path.join(OUT, name)
        self.img.resize((self.w * 2, self.h * 2), Image.LANCZOS).save(path)
        print("  %-36s %dx%d" % (name, self.w * 2, self.h * 2))


# =====================================================================
# Hinh 2.1 - Kien truc tich hop
# =====================================================================
def integration_architecture():
    c = Canvas(1000, 560)
    c.text(500, 26, "KIẾN TRÚC TÍCH HỢP HỆ THỐNG PitchOS", 14, True, INK)

    # --- tang danh ba, keo dai het be ngang vung dich vu
    c.card(255, 56, 710, 48, "Eureka Server",
           "Service Registry — cổng 8761", "registry")

    # --- mot hang ngang: client | auth | booking | LB | pitch 1 | pitch 2
    Y = 250
    c.card(30, Y, 150, 52, "Client", "Postman / Trình duyệt", "client")
    c.card(255, Y, 165, 52, "Auth Service", "pitchos-auth-service · 8081", "service")
    c.card(455, Y, 175, 52, "Booking Service", "CONSUMER · 8083", "consumer")
    c.card(662, Y + 6, 78, 40, "Load", "Balancer", "client",
           tsize=8.5, ssize=8, radius=6)
    c.panel(766, Y - 32, 204, 100, None)
    c.text(868, Y - 20, "pitchos-pitch-service · 2 instance", 8, True, GREY)
    c.card(774, Y, 92, 52, "Pitch #1", "PROVIDER · 8082", "provider",
           tsize=9.5, ssize=7)
    c.card(872, Y, 92, 52, "Pitch #2", "PROVIDER · 8084", "provider",
           tsize=9.5, ssize=7)

    # --- dang ky + heartbeat: moi dich vu mot duong thang dung len danh ba
    for x, y0 in ((337, Y), (542, Y), (820, Y - 32), (918, Y - 32)):
        c.arrow(x, y0, x, 104, None, dashed=True)
    c.text(337, 150, "đăng ký + Heartbeat 10s", 8, False, GREY)

    # --- luong nghiep vu tu client
    c.arrow(180, Y + 18, 255, Y + 18, None)
    c.text(217, Y + 6, "(1) đăng nhập", 8, False, GREY)
    c.elbow(105, Y + 52, 500, Y + 52, 370, "(2) POST /api/v1/bookings")

    # --- consumer goi provider qua Service ID
    c.arrow(630, Y + 26, 662, Y + 26, None, color="#7E57C2", width=3)
    c.arrow(740, Y + 26, 766, Y + 26, None, color="#7E57C2", width=3)
    c.text(700, Y + 70, "(3) gọi bằng Service ID", 8, False, "#5E35B1")
    c.text(700, Y + 84, "Round Robin chọn 1 trong 2", 8, False, "#5E35B1")

    # --- tang du lieu
    yd = 430
    c.card(255, yd, 165, 46, "mysql-auth", "pitchos_user_db · 3307", "data")
    c.card(455, yd, 175, 46, "mysql-booking", "pitchos_booking_db · 3309", "data")
    c.card(775, yd, 190, 46, "mysql-pitch", "pitchos_pitch_db · 3308", "data")
    c.arrow(300, Y + 52, 300, yd, None)
    c.arrow(600, Y + 52, 600, yd, None)
    c.arrow(820, Y + 52, 845, yd, None)
    c.arrow(918, Y + 52, 895, yd, None)
    c.text(870, 395, "hai instance dùng chung một CSDL", 7.5, False, GREY)

    # --- chu giai
    c.d.line([60 * S, 505 * S, 100 * S, 505 * S], fill=LINE, width=2 * S)
    c.left_text(108, 505, "luồng dữ liệu nghiệp vụ", 8, False, GREY)
    c._dashed(400, 505, 440, 505, LINE, 2)
    c.left_text(448, 505, "đăng ký và Heartbeat vào danh bạ (chỉ metadata)", 8, False, GREY)

    c.caption("Eureka Server chỉ cấp địa chỉ, không trung chuyển dữ liệu nghiệp vụ — "
              "Booking Service gọi thẳng tới Pitch Service.")
    c.save("integration-architecture.png")


# =====================================================================
# Hinh 2.2 - Kien truc trien khai
# =====================================================================
def deployment_architecture():
    c = Canvas(960, 620)
    c.text(480, 26, "KIẾN TRÚC TRIỂN KHAI BẰNG DOCKER COMPOSE", 14, True, INK)

    c.panel(30, 48, 900, 452, None)
    c.left_text(48, 66, "DOCKER HOST — cổng ánh xạ ra máy chủ", 9, True, GREY)

    cols = [(120, "8761"), (280, "8081"), (440, "8082"),
            (600, "8084"), (760, "8083")]
    for x, port in cols:
        c.card(x - 40, 78, 80, 24, port, None, "client", tsize=9, radius=5)

    c.panel(55, 122, 850, 290, None, "panel")
    c.left_text(72, 140, "DOCKER NETWORK: pitchos-network (bridge)", 9, True, GREY)

    row1 = [
        (120, "Service Registry", "Eureka · 8761", "registry"),
        (280, "Auth Service", "appuser · 8081", "service"),
        (440, "Pitch #1", "appuser · 8082", "provider"),
        (600, "Pitch #2", "appuser · 8084", "provider"),
        (760, "Booking", "appuser · 8083", "consumer"),
    ]
    for x, t, sub, k in row1:
        c.card(x - 68, 158, 136, 52, t, sub, k, tsize=9.5, ssize=7.5)
        c.arrow(x, 102, x, 158, None)

    row2 = [(200, "mysql-auth", "pitchos_user_db · 3307"),
            (520, "mysql-pitch", "pitchos_pitch_db · 3308"),
            (800, "mysql-booking", "pitchos_booking_db · 3309")]
    for x, t, sub in row2:
        c.card(x - 95, 300, 190, 48, t, sub, "data", tsize=10, ssize=7.5)

    c.arrow(280, 210, 215, 300, None)
    c.arrow(440, 210, 490, 300, None)
    c.arrow(600, 210, 545, 300, None)
    c.arrow(760, 210, 795, 300, None)

    c.text(480, 382, "depends_on: condition: service_healthy   ·   "
                     "healthcheck: GET /actuator/health  và  mysqladmin ping",
           8, False, GREY)

    for x, t in ((200, "mysql_auth_data"), (520, "mysql_pitch_data"),
                 (800, "mysql_booking_data")):
        c.card(x - 95, 430, 190, 40, t, "Named Volume", "volume",
               tsize=9, ssize=7)
        c.arrow(x, 348, x, 430, None)

    c.text(480, 530, "Thứ tự khởi động bám theo sức khỏe ứng dụng chứ không theo "
                     "trạng thái container:", 9, False, INK)
    c.text(480, 548, "MySQL healthy → Service Registry healthy → các dịch vụ nghiệp vụ",
           9, True, INK)
    c.text(480, 572, "Dữ liệu trên Named Volume sống sót qua lệnh docker compose down "
                     "(khi không kèm cờ -v)", 8, False, GREY)

    c.caption("Toàn bộ 8 container khởi chạy bằng một lệnh: docker compose up -d --build")
    c.save("deployment-architecture.png")


# =====================================================================
# Hinh 3.1 - So do tuan tu nghiep vu dat san
# =====================================================================
def booking_sequence():
    c = Canvas(980, 560)
    c.text(490, 26, "LUỒNG NGHIỆP VỤ ĐẶT SÂN QUA SERVICE DISCOVERY", 13, True, INK)

    actors = [(90, "Client", "Postman", "client"),
              (270, "Auth Service", "8081", "service"),
              (470, "Booking Service", "CONSUMER", "consumer"),
              (670, "Eureka", "danh bạ 8761", "registry"),
              (870, "Pitch Service", "PROVIDER", "provider")]
    for x, t, sub, k in actors:
        c.card(x - 70, 56, 140, 42, t, sub, k, tsize=9, ssize=7)
        c.d.line([x * S, 98 * S, x * S, 470 * S], fill="#D8DBE2", width=S)

    steps = [
        (140, 90, 270, "1. POST /auth/login", False),
        (172, 270, 90, "2. 200 OK + accessToken (JWT)", True),
        (214, 90, 470, "3. POST /bookings  kèm Bearer token", False),
        (250, 470, 470, "4. Tự xác thực chữ ký JWT cục bộ", None),
        (292, 470, 670, "5. Tra cứu Service ID trong cache danh bạ", False),
        (324, 670, 470, "6. Danh sách 2 instance đang UP", True),
        (358, 470, 470, "7. LoadBalancer chọn 1 instance (Round Robin)", None),
        (400, 470, 870, "8. GET /api/v1/pitches/1  — gọi trực tiếp", False),
        (432, 870, 470, "9. 200 OK — thông tin sân và đơn giá", True),
        (464, 470, 90, "10. 201 Created — totalPrice = 600000", True),
    ]
    for y, x1, x2, label, dashed in steps:
        if dashed is None:
            c.d.rounded_rectangle([(x1 - 8) * S, (y - 11) * S, (x1 + 192) * S,
                                   (y + 9) * S], radius=4 * S,
                                  fill="#F5F3FA", outline="#C5BDE0",
                                  width=S // 2 or 1)
            c.left_text(x1, y, label, 7.5, False, "#5E35B1")
        else:
            c.arrow(x1, y, x2, y, None, dashed=dashed, width=2)
            c.text((x1 + x2) / 2, y - 10, label, 7.5, False, GREY)

    c.text(490, 505, "Bước 5 và 6 chỉ trao đổi metadata với danh bạ. "
                     "Bước 8 là lời gọi nghiệp vụ, đi thẳng tới Provider.",
           8.5, False, INK)
    c.caption("Eureka không nằm trên đường đi của dữ liệu nghiệp vụ.")
    c.save("booking-sequence.png")


# =====================================================================
# Hinh 4.1 - Co che dang ky va tra cuu
# =====================================================================
def discovery_flow():
    c = Canvas(900, 470)
    c.text(450, 26, "CƠ CHẾ ĐĂNG KÝ VÀ TRA CỨU DỊCH VỤ", 13, True, INK)

    c.panel(286, 52, 328, 104, None, "registry")
    c.text(450, 76, "Eureka Server", 12, True, INK)
    c.text(450, 104, "pitchos-auth-service  →  172.18.0.3:8081  UP", 7, False, GREY)
    c.text(450, 122, "pitchos-pitch-service  →  172.18.0.5:8082  UP", 7, False, GREY)
    c.text(450, 140, "                                  172.18.0.6:8084  UP", 7, False, GREY)

    c.card(50, 250, 200, 56, "Pitch Service", "PROVIDER · 2 instance", "provider")
    c.card(650, 250, 200, 56, "Booking Service", "CONSUMER", "consumer")

    c.arrow(150, 250, 300, 158, None, dashed=True)
    c.left_text(60, 180, "(1) đăng ký Service ID + IP + port", 8, False, GREY)
    c.left_text(60, 196, "(2) Heartbeat mỗi 10 giây", 8, False, GREY)

    c.arrow(600, 158, 750, 250, None, dashed=True)
    c.left_text(600, 180, "(3) tải bản sao danh bạ", 8, False, GREY)
    c.left_text(600, 196, "      làm mới mỗi 30 giây", 8, False, GREY)

    c.card(670, 332, 160, 32, "Cache danh bạ cục bộ", None, "client",
           tsize=8, radius=6)
    c.arrow(750, 306, 750, 332, None)

    c.arrow(650, 278, 250, 278, None, color="#7E57C2", width=3)
    c.text(450, 266, "(4) gọi trực tiếp bằng IP lấy từ cache — KHÔNG đi qua Eureka",
           8, False, "#5E35B1")

    c.text(450, 400, "Nếu Eureka Server tạm dừng, các lời gọi hiện có vẫn hoạt động "
                     "vì Consumer đã giữ bản sao danh bạ trong bộ nhớ.", 8.5, False, INK)
    c.caption("Mô hình Client-side Discovery: Registry chỉ tham gia ở ba bước đầu.")
    c.save("service-discovery-flow.png")


# =====================================================================
# Hinh 4.2 - Can bang tai Round Robin
# =====================================================================
def load_balancing():
    c = Canvas(900, 430)
    c.text(450, 26, "CÂN BẰNG TẢI PHÍA CLIENT — THUẬT TOÁN ROUND ROBIN", 13, True, INK)

    c.card(40, 150, 170, 60, "Booking Service", "CONSUMER · 8083", "consumer")
    c.card(265, 156, 110, 48, "LoadBalancer", "Round Robin", "client",
           tsize=9, ssize=7.5)
    c.arrow(210, 180, 265, 180, None, color="#7E57C2", width=3)

    c.card(470, 100, 180, 54, "Pitch #1", "PROVIDER · 8082", "provider")
    c.card(470, 206, 180, 54, "Pitch #2", "PROVIDER · 8084", "provider")
    c.arrow(375, 170, 470, 127, None, color="#7E57C2", width=3)
    c.arrow(375, 190, 470, 233, None, color="#7E57C2", width=3)

    c.card(700, 100, 160, 54, "10 request", "50%", "data", tsize=12, ssize=9)
    c.card(700, 206, 160, 54, "10 request", "50%", "data", tsize=12, ssize=9)
    c.arrow(650, 127, 700, 127, None)
    c.arrow(650, 233, 700, 233, None)

    c.text(450, 300, "Kết quả đo thực tế TC03 — 20 request tuần tự:", 9, True, INK)
    c.text(450, 320, "8084 → 8082 → 8084 → 8082 → …   luân phiên tuyệt đối",
           9, False, "#5E35B1")
    c.text(450, 352, "Biến đếm nguyên tử tăng 1 sau mỗi lời gọi, chọn instance theo "
                     "phép chia lấy dư cho số instance đang UP.", 8, False, GREY)

    c.caption("Tiêu chí nghiệm thu là cả hai instance đều nhận được request, "
              "không phải tỉ lệ đúng 50/50.")
    c.save("load-balancing.png")


if __name__ == "__main__":
    print("Sinh so do vao", OUT)
    integration_architecture()
    deployment_architecture()
    booking_sequence()
    discovery_flow()
    load_balancing()
