"""
Gop cac bai viet trong docs/kt2/ thanh mot quyen bao cao KT2 hoan chinh.

Chay:  python docs/build_report.py
Ket qua: docs/BAO_CAO_KT2_PITCHOS.md

Cau truc theo mo hinh quyen bao cao cua nhom o TX1, noi dung bam dung bay
phan ma de bai quy dinh:

  Trang bia -> Muc luc -> 7 CHUONG -> Phu luc

Bon bai ly thuyet (Cau 1.1-1.4) khong tach thanh khoi rieng ma tro thanh
muc "Co so ly thuyet" mo dau chuong tuong ung, giong cach TX1 lam.
Phu luc A doi chieu tung y cua barem voi muc trong bao cao de nguoi cham
tim duoc ngay.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "kt2")
OUT = os.path.join(HERE, "BAO_CAO_KT2_PITCHOS.md")

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
META_RE = re.compile(
    r"^\*\*(Học phần|Sinh viên thực hiện|Mục tiêu điểm số|Nhóm|Lớp|Vùng mã nguồn"
    r"|Minh chứng mã nguồn|Kết quả kiểm thử chi tiết|File ảnh cần xuất kèm"
    r"|Liên quan|Bộ kiểm thử|Hệ thống|Người thực hiện|Ngày thực hiện):",
    re.UNICODE)
NUM_RE = re.compile(r"^\d+(\.\d+)*\.?\s+")

# --------------------------------------------------------------------------
# Hinh anh chen vao sau mot tieu de nhat dinh.
# Khoa: (ten file nguon, phan dau cua tieu de).  Gia tri: danh sach hinh.
#   ("duong dan hoac None", "chu thich")  -> None nghia la cho trong de dan anh
# --------------------------------------------------------------------------
FIGURES = {
    ("PHAN_2_HOANG.md", "## 2. KIẾN TRÚC TÍCH HỢP"): [
        ("architecture/integration-architecture.png",
         "Kiến trúc tích hợp hệ thống PitchOS. Nét liền là luồng dữ liệu nghiệp "
         "vụ, nét đứt là luồng đăng ký và Heartbeat vào danh bạ. Không có đường "
         "nét liền nào đi xuyên qua Eureka Server."),
    ],
    ("PHAN_2_HOANG.md", "## 3. KIẾN TRÚC TRIỂN KHAI"): [
        ("architecture/deployment-architecture.png",
         "Kiến trúc triển khai bằng Docker Compose: 8 container trong mạng nội "
         "bộ pitchos-network, ba Named Volume giữ dữ liệu bền vững, thứ tự khởi "
         "động điều khiển bằng healthcheck."),
    ],
    ("PHAN_3_NHAT.md", "## 2. QUY TRÌNH NGHIỆP VỤ"): [
        ("architecture/booking-sequence.png",
         "Sơ đồ tuần tự nghiệp vụ đặt sân. Bước 5 và 6 chỉ trao đổi metadata với "
         "danh bạ; bước 8 là lời gọi nghiệp vụ đi thẳng từ Consumer tới Provider."),
    ],
    ("PHAN_4_HOANG.md", "## 3. CƠ CHẾ ĐĂNG KÝ CỦA EUREKA CLIENT"): [
        ("architecture/service-discovery-flow.png",
         "Cơ chế đăng ký và tra cứu dịch vụ. Consumer giữ bản sao danh bạ trong "
         "bộ nhớ của chính nó nên lời gọi nghiệp vụ không đi qua Eureka Server."),
    ],
    ("PHAN_4_HOANG.md", "## 4. CƠ CHẾ SPRING CLOUD LOADBALANCER"): [
        ("architecture/load-balancing.png",
         "Cân bằng tải phía client bằng thuật toán Round Robin, kèm kết quả đo "
         "thực tế của ca kiểm thử TC03: 20 request chia đều 10/10 cho hai instance."),
        (None,
         "Kết quả Postman Collection Runner gửi 20 request liên tiếp vào endpoint "
         "GET /api/v1/bookings/pitch-instance, cột phản hồi cho thấy cổng 8082 và "
         "8084 xuất hiện luân phiên."),
    ],
    ("PHAN_4_HOANG.md", "## 2. CẤU HÌNH EUREKA SERVER"): [
        (None,
         "Eureka Dashboard tại http://localhost:8761 sau khi toàn hệ thống khởi "
         "động: bảng Instances currently registered with Eureka hiển thị đủ ba "
         "Service ID, trong đó PITCHOS-PITCH-SERVICE ở trạng thái UP (2) với hai "
         "Instance ID phân biệt là pitch-instance-1 và pitch-instance-2."),
    ],
    ("PHAN_4_HOANG.md", "## 6. KIỂM THỬ DỪNG VÀ KHỞI ĐỘNG LẠI PROVIDER"): [
        (None,
         "Eureka Dashboard sau khi dừng instance thứ nhất: PITCHOS-PITCH-SERVICE "
         "chỉ còn UP (1). Thời gian từ lúc dừng đến lúc danh bạ cập nhật đo được "
         "là 18,2 giây."),
        (None,
         "Postman trả về 201 Created khi đặt sân ở thời điểm chỉ còn một instance "
         "Provider — minh chứng hệ thống suy giảm năng lực nhưng không mất chức năng."),
        (None,
         "Postman trả về 503 Service Unavailable khi đã dừng cả hai instance, "
         "kèm ảnh /actuator/health của Booking Service vẫn báo UP."),
    ],
    ("PHAN_5_LINH.md", "## 5.5."): [
        (None,
         "Kết quả lệnh docker compose ps: toàn bộ 8 container đạt trạng thái "
         "healthy. Cần phân biệt cột State hiển thị Up với cột Health hiển thị "
         "healthy — Up chỉ nghĩa là tiến trình đang chạy."),
        (None,
         "Kết quả lệnh docker images cho thấy kích thước ảnh sau khi áp dụng "
         "Dockerfile multi-stage."),
    ],
    ("PHAN_6_HUNG.md", "## 6.1."): [
        (None,
         "Phản hồi của GET /actuator/health trên cả bốn dịch vụ, tất cả đều trả "
         "về {\"status\":\"UP\"}."),
    ],
    ("PHAN_6_HUNG.md", "## 6.2."): [
        (None,
         "Nhật ký đồng thời của Booking Service và Pitch Service trong cùng một "
         "nghiệp vụ đặt sân, cho thấy request được instance nào tiếp nhận."),
    ],
    ("PHAN_6_HUNG.md", "## 6.5."): [
        (None,
         "Bảng bookings trong cơ sở dữ liệu sau khi chạy docker compose down rồi "
         "up -d: các bản ghi đơn đặt sân vẫn còn nguyên nhờ Named Volume."),
    ],
}

# Tieu de muc ly thuyet khi dua vao dau chuong
THEORY_TITLE = "CƠ SỞ LÝ THUYẾT"

# (so chuong, tieu de chuong, file ly thuyet | None, cac file noi dung)
CHAPTERS = [
    (1, "GIỚI THIỆU HỆ THỐNG PitchOS", None, ["PHAN_1_LINH.md"]),
    (2, "THIẾT KẾ KIẾN TRÚC HỆ THỐNG", None,
     ["PHAN_2_HOANG.md", "PHAN_2_HUNG.md"]),
    (3, "TÍCH HỢP VÀ TIÊU THỤ DỊCH VỤ", "CAU1_1_NHAT.md", ["PHAN_3_NHAT.md"]),
    (4, "SERVICE REGISTRY VÀ CÂN BẰNG TẢI", "CAU1_2_HOANG.md", ["PHAN_4_HOANG.md"]),
    (5, "CONTAINER HÓA VÀ TRIỂN KHAI HỆ THỐNG", "CAU1_3_LINH.md", ["PHAN_5_LINH.md"]),
    (6, "VẬN HÀNH VÀ GIÁM SÁT HỆ THỐNG", "CAU1_4_HUNG.md", ["PHAN_6_HUNG.md"]),
    (7, "ĐÁNH GIÁ VÀ KẾT LUẬN", None, ["PHAN_7_HUNG.md"]),
]


def read(fn):
    with io.open(os.path.join(SRC, fn), encoding="utf-8") as f:
        return f.read().strip()


def fence_rows(text):
    rows, inf = [], False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            inf = not inf
            rows.append((ln, True))
        else:
            rows.append((ln, inf))
    return rows


class Numberer:
    """Danh so muc theo chuong va dem bang / hinh."""

    def __init__(self, chapter):
        self.ch = chapter
        self.sec = 0
        self.sub = 0
        self.table = 0
        self.fig = 0

    def next_section(self, name):
        self.sec += 1
        self.sub = 0
        return "%d.%d. %s" % (self.ch, self.sec, NUM_RE.sub("", name))

    def next_sub(self, name):
        self.sub += 1
        return "%d.%d.%d. %s" % (self.ch, self.sec, self.sub, NUM_RE.sub("", name))

    def next_table(self):
        self.table += 1
        return "%d.%d" % (self.ch, self.table)

    def next_fig(self):
        self.fig += 1
        return "%d.%d" % (self.ch, self.fig)


_seen_headings = {}

# Tu viet tat va ten rieng can giu nguyen dang khi ha chu hoa tieu de
KEEP = {
    "PITCHOS": "PitchOS", "KT1": "KT1", "KT2": "KT2", "TX1": "TX1", "TX2": "TX2",
    "API": "API", "URL": "URL", "HTTP": "HTTP", "HTTPS": "HTTPS", "JWT": "JWT",
    "REST": "REST", "SQL": "SQL", "ID": "ID", "IP": "IP", "CSDL": "CSDL",
    "JPA": "JPA", "RBAC": "RBAC", "DTO": "DTO", "BCRYPT": "BCrypt",
    "DOCKER": "Docker", "DOCKERFILE": "Dockerfile", "COMPOSE": "Compose",
    "EUREKA": "Eureka", "SPRING": "Spring", "ACTUATOR": "Actuator",
    "PROVIDER": "Provider", "CONSUMER": "Consumer", "SERVICE": "Service",
    "REGISTRY": "Registry", "DISCOVERY": "Discovery", "CLIENT": "Client",
    "SERVER": "Server", "LOADBALANCER": "LoadBalancer", "HEARTBEAT": "Heartbeat",
    "HEALTHCHECK": "Healthcheck", "VOLUME": "Volume", "VOLUMES": "Volumes",
    "MICROSERVICES": "Microservices", "MICROSERVICE": "Microservice",
    "CONTAINER": "container", "CONTAINERS": "container",
    "GATEWAY": "Gateway", "OPENFEIGN": "OpenFeign", "FEIGN": "Feign",
    "MYSQL": "MySQL", "NAMED": "Named", "ROUND": "Round", "ROBIN": "Robin",
    "LOGGING": "Logging", "DISTRIBUTED": "Distributed",
    "AUTH": "Auth", "BOOKING": "Booking", "PITCH": "Pitch",
    "INSTANCE": "instance", "ENDPOINT": "endpoint", "TOKEN": "token",
}

# Tu viet tat chi gom chu cai ASCII, giu nguyen dang viet hoa
EXTRA = {"SOA", "CRUD", "CORS", "TCP", "DNS", "SSL", "LTS", "JDK", "JVM",
         "AP", "CP", "UI", "UX", "CI", "CD", "DEP", "IT", "TC", "XML",
         "JSON", "YAML", "HTML", "TH6", "TH7", "TH8"}


def sentence_case(s):
    """Ha chu hoa cho tieu de viet hoa toan bo, giu lai tu viet tat."""
    out = []
    for tok in re.split(r"(\W+)", s):
        up = tok.upper()
        if up in KEEP:
            out.append(KEEP[up])
        elif up in EXTRA:
            out.append(up)
        else:
            out.append(tok.lower())
    t = "".join(out).strip()
    return t[:1].upper() + t[1:] if t else t


def caption_for(header_cells, heading):
    """Sinh chu thich cho mot bang tu muc dang dung o tren.

    Bang dau tien trong mot muc lay thang ten muc. Tu bang thu hai tro di,
    them ten cot dau de phan biet.
    """
    base = re.sub(r"^\d+(\.\d+)*\.?\s+", "", heading or "").strip()
    base = sentence_case(base) if base else "Bảng dữ liệu"
    base = re.sub(r"^(Bảng|Danh mục)\s+", "", base)
    base = base[:1].upper() + base[1:] if base else "Bảng dữ liệu"
    k = _seen_headings.get(base, 0) + 1
    _seen_headings[base] = k
    if k == 1:
        return base
    first = re.sub(r"[*`]", "", header_cells[0]).strip() if header_cells else ""
    return "%s — theo %s" % (base, first.lower()) if first else "%s (tiếp)" % base


def prepare(text, num, demote, drop_title=False, figkey=None, force_title=None,
            as_sub=False):
    """Chuan hoa mot file con: bo metadata, danh so muc, danh so bang va hinh."""
    rows = fence_rows(text)
    out = []
    cur_heading = force_title or ""
    i = 0
    while i < len(rows):
        ln, in_code = rows[i]

        if in_code:
            out.append(ln)
            i += 1
            continue

        if META_RE.match(ln.strip()):
            i += 1
            continue

        m = HEAD_RE.match(ln)
        if m:
            lvl, name = len(m.group(1)), m.group(2).strip()
            if lvl == 1:
                if drop_title:
                    i += 1
                    continue
                out.append("#" * min(lvl + demote, 6) + " " + name)
                i += 1
                continue
            if lvl == 2:
                name = num.next_sub(name) if as_sub else num.next_section(name)
            elif lvl == 3:
                name = NUM_RE.sub("", name) if as_sub else num.next_sub(name)
            else:
                name = NUM_RE.sub("", name)
            cur_heading = name
            out.append("#" * min(lvl + demote, 6) + " " + name)

            # chen hinh ngay sau tieu de neu co khai bao
            if figkey:
                for key, figs in FIGURES.items():
                    if key[0] != figkey:
                        continue
                    if not m.group(0).strip().startswith(key[1]):
                        continue
                    for path, cap in figs:
                        n = num.next_fig()
                        out.append("")
                        if path:
                            out.append("![](%s)" % path)
                        else:
                            out.append("[[ANH]]")
                        out.append("")
                        out.append("*Hình %s. %s*" % (n, cap))
                        out.append("")
            i += 1
            continue

        # bang: chen dong chu thich phia truoc
        if ln.strip().startswith("|") and i + 1 < len(rows) and re.match(
                r"^\|[\s:\-|]+\|?$", rows[i + 1][0].strip()):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            n = num.next_table()
            if out and out[-1].strip():
                out.append("")
            out.append("*Bảng %s. %s*" % (n, caption_for(cells, cur_heading)))
            out.append("")
            while i < len(rows) and rows[i][0].strip().startswith("|"):
                out.append(rows[i][0])
                i += 1
            continue

        out.append(ln)
        i += 1

    body = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return body


doc = []
add = doc.append

# ======================================================================= BIA
add("# TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP HÀ NỘI")
add("## TRƯỜNG CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG")
add("")
add("### BÁO CÁO BÀI KIỂM TRA SỐ 2")
add("#### HỌC PHẦN: PHÁT TRIỂN PHẦN MỀM HƯỚNG DỊCH VỤ")
add("")
add("##### ĐỀ TÀI")
add("##### HỆ THỐNG QUẢN LÝ ĐẶT LỊCH SÂN BÓNG ĐÁ — PitchOS")
add("")
add("Nhóm: **13**  ")
add("Lớp: **20261IT6151005**  ")
add("Giáo viên hướng dẫn: **Hoàng Quang Huy**")
add("")
add("| Sinh viên thực hiện | Mã sinh viên | Nội dung phụ trách |")
add("|---|---|---|")
add("| Lê Đức Hoàng *(Nhóm trưởng)* | 2024606110 | Chương 2 (kiến trúc) · Chương 4 |")
add("| Đỗ Hoàng Linh | 2024606897 | Chương 1 · Chương 5 |")
add("| Hoàng Minh Nhật | 2024607325 | Chương 3 |")
add("| Vi Đức Hùng | 2024605681 | Chương 2 (dữ liệu) · Chương 6 · Chương 7 |")
add("")
add("**HÀ NỘI, 2026**")
add("")
add("---")
add("")

# =================================================================== MUC LUC
add("## MỤC LỤC")
add("")
add("<!-- MUC_LUC -->")
add("")
add("---")
add("")

# =================================================================== CAC CHUONG
for ch, title, theory, files in CHAPTERS:
    num = Numberer(ch)
    add("---")
    add("")
    add("### CHƯƠNG %d. %s" % (ch, title))
    add("")

    if theory:
        add("#### %s" % num.next_section(THEORY_TITLE))
        add("")
        doc.append(prepare(read(theory), num, demote=3, drop_title=True, as_sub=True))
        add("")

    for fn in files:
        doc.append(prepare(read(fn), num, demote=2, drop_title=True, figkey=fn))
        add("")

# =================================================================== PHU LUC
add("---")
add("")
add("### PHỤ LỤC A. ĐỐI CHIẾU NỘI DUNG BÁO CÁO VỚI BAREM CHẤM ĐIỂM")
add("")
add("Phụ lục này giúp đối chiếu nhanh từng ý trong barem của đề bài với vị trí "
    "trình bày tương ứng trong báo cáo.")
add("")
add("*Bảng A.1. Đối chiếu barem Câu 1 — Lý thuyết (2,0 điểm)*")
add("")
add("| Ý trong barem | Điểm | Trình bày tại |")
add("|---|:---:|---|")
add("| 1.1. Provider và Consumer, quy trình gọi API, xử lý lỗi | 0,5 | Mục 3.1 |")
add("| 1.2. Service Registry, Service Discovery, Eureka và API Gateway, Service ID | 0,5 | Mục 4.1 |")
add("| 1.3. Docker Image và Container, vai trò Dockerfile và Compose | 0,5 | Mục 5.1 |")
add("| 1.4. Ba mức trạng thái, vai trò Health Check, Log, Volume | 0,5 | Mục 6.1 |")
add("")
add("*Bảng A.2. Đối chiếu barem Câu 2 — Thực nghiệm (8,0 điểm)*")
add("")
add("| Ý trong barem | Điểm | Trình bày tại |")
add("|---|:---:|---|")
add("| 2.1. Phân tích và thiết kế kiến trúc tích hợp, triển khai | 1,0 | Chương 2 |")
add("| 2.2. Triển khai tích hợp và tiêu thụ dịch vụ | 2,0 | Chương 3 (từ mục 3.2) |")
add("| 2.3. Microservices và Service Registry | 1,5 | Chương 4 (từ mục 4.2) |")
add("| 2.4. Container hóa và triển khai | 2,0 | Chương 5 (từ mục 5.2) |")
add("| 2.5. Vận hành, giám sát và kiểm thử sự cố | 1,5 | Chương 6 (từ mục 6.2) |")
add("")
add("---")
add("")
add("### PHỤ LỤC B. DANH MỤC MÃ NGUỒN VÀ MINH CHỨNG")
add("")
add("*Bảng B.1. Danh mục mã nguồn và tài liệu minh chứng kèm theo báo cáo*")
add("")
add("| Hạng mục | Đường dẫn trong kho lưu trữ |")
add("|---|---|")
for name, path in [
    ("Service Registry (Eureka Server)", "`pitchos-service-registry/`"),
    ("Auth Service", "`pitchos-auth-service/`"),
    ("Pitch Service (Provider, 2 instance)", "`pitchos-pitch-service/`"),
    ("Booking Service (Consumer)", "`pitchos-booking-service/`"),
    ("Script khởi tạo cơ sở dữ liệu", "`pitchos-database/*.sql`"),
    ("Điều phối container", "`docker-compose.yml`"),
    ("Mẫu biến môi trường", "`.env.example`"),
    ("Hướng dẫn cài đặt và chạy", "`README.md`"),
    ("Hợp đồng API", "`docs/api/api-contract.md`"),
    ("Biên bản kiểm thử tích hợp IT01–IT07", "`docs/testing/integration-test.md`"),
    ("Biên bản kiểm thử Service Discovery TC01–TC06",
     "`docs/testing/service-discovery-test.md`"),
    ("Biên bản kiểm thử vận hành DEP01–DEP08", "`docs/testing/operation-test.md`"),
    ("Bộ sưu tập Postman", "`postman/collection.json`"),
    ("Sơ đồ kiến trúc", "`docs/architecture/`"),
]:
    add("| %s | %s |" % (name, path))
add("")

text = "\n".join(doc)


# ------------------------------------------------------------- sinh muc luc
def slug(s):
    s = s.lower()
    s = re.sub(r"[^\w\s\u00c0-\u1ef9-]", "", s)
    return re.sub(r"\s+", "-", s.strip())


entries = []
for ln, in_code in fence_rows(text):
    if in_code:
        continue
    m = HEAD_RE.match(ln)
    if not m:
        continue
    lvl, name = len(m.group(1)), m.group(2).strip()
    if lvl == 3 and (name.startswith("CHƯƠNG") or name.startswith("PHỤ LỤC")):
        entries.append("- [%s](#%s)" % (name, slug(name)))
    elif lvl == 4 and re.match(r"^\d+\.\d+\.", name):
        entries.append("  - [%s](#%s)" % (name, slug(name)))

text = text.replace("<!-- MUC_LUC -->", "\n".join(entries))
text = re.sub(r"\n{4,}", "\n\n\n", text)

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text + "\n")

nfig = text.count("*Hình ")
ntab = text.count("*Bảng ")
print("Da gop xong:", OUT)
print("So dong      :", text.count("\n") + 1)
print("Muc trong TOC:", len(entries))
print("So hinh      :", nfig, "- cho dan anh:", text.count("[[ANH]]"))
print("So bang      :", ntab)
