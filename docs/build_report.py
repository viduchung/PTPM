"""
Gop 12 file bai viet trong docs/kt2/ thanh mot quyen bao cao KT2 hoan chinh.

Chay:  python docs/build_report.py
Ket qua: docs/BAO_CAO_KT2_PITCHOS.md

Script lam cac viec sau:
  - Sap xep dung thu tu: Cau 1 (4 y) roi Cau 2 (7 phan theo cau truc de bai)
  - Gop Phan 2.1a va 2.1b thanh mot "PHAN 2: THIET KE KIEN TRUC" cho dung
    cau truc 7 phan ma de bai de nghi
  - Bo cac dong metadata noi bo cua tung file (Hoc phan, Sinh vien thuc hien,
    Muc tieu diem so...) vi da co bang phan cong o trang bia
  - Danh so lai cac muc theo dang <so phan>.<so muc> cho thong nhat toan quyen
  - Sinh muc luc tu dong
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "kt2")
OUT = os.path.join(HERE, "BAO_CAO_KT2_PITCHOS.md")

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# Dong metadata dau file con - bo khi gop vao quyen chung
META_RE = re.compile(
    r"^\*\*(Học phần|Sinh viên thực hiện|Mục tiêu điểm số|Nhóm|Lớp):",
    re.UNICODE,
)
# So thu tu san co o dau tieu de, vi du "3.", "5.2.", "1. "
NUM_RE = re.compile(r"^\d+(\.\d+)*\.?\s+")


def read(fn):
    with io.open(os.path.join(SRC, fn), encoding="utf-8") as f:
        return f.read().strip()


def split_fence_aware(text):
    """Tra ve danh sach (line, dang_trong_khoi_code)."""
    rows = []
    in_fence = False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            rows.append((ln, True))
            continue
        rows.append((ln, in_fence))
    return rows


def prepare(text, part_no, demote, drop_title=False, keep_meta=False):
    """Chuan hoa mot file con truoc khi ghep vao quyen bao cao.

    part_no : so phan dung de danh so lai muc, vi du 3 -> "3.1", "3.2"
    demote  : so bac ha cap tieu de
    """
    rows = split_fence_aware(text)
    out = []
    seen_title = False
    sub = 0
    subsub = 0
    for ln, in_code in rows:
        if in_code:
            out.append(ln)
            continue

        if not keep_meta and META_RE.match(ln.strip()):
            continue

        m = HEAD_RE.match(ln)
        if not m:
            out.append(ln)
            continue

        lvl, name = len(m.group(1)), m.group(2).strip()

        if lvl == 1:
            seen_title = True
            if drop_title:
                continue
            out.append("#" * min(lvl + demote, 6) + " " + name)
            continue

        if lvl == 2 and part_no is not None:
            sub += 1
            subsub = 0
            name = NUM_RE.sub("", name)
            name = "%d.%d. %s" % (part_no, sub, name)
        elif lvl == 3 and part_no is not None:
            subsub += 1
            name = NUM_RE.sub("", name)
            name = "%d.%d.%d. %s" % (part_no, sub, subsub, name)

        out.append("#" * min(lvl + demote, 6) + " " + name)

    body = "\n".join(out)
    # Don bot dong trong thua sinh ra sau khi bo metadata
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return body


doc = []


def add(s=""):
    doc.append(s)


# ======================================================================= BIA
add("# BÁO CÁO BÀI KIỂM TRA SỐ 2")
add("## HỆ THỐNG QUẢN LÝ ĐẶT LỊCH SÂN BÓNG ĐÁ — PitchOS")
add("")
add("**Học phần:** Phát triển phần mềm Hướng dịch vụ (SOA / Microservices) — 2026  ")
add("**Chuẩn đầu ra:** CĐR L2  ")
add("**Phạm vi kiến thức:** TH6 — Tích hợp và tiêu thụ dịch vụ · TH7 — Microservices và Service Registry · TH8 — Container hóa và vận hành  ")
add("**Hình thức:** Bài tập nhóm, thực hiện tại nhà trong 01 tuần  ")
add("**Tổng điểm:** 10,0")
add("")
add("### Danh sách thành viên và phân công")
add("")
add("| Thành viên | Vai trò kỹ thuật | Nội dung phụ trách trong báo cáo | Điểm |")
add("|---|---|---|:---:|")
add("| **Hoàng** *(Nhóm trưởng)* | Service Registry (Eureka), Auth Service | Câu 1.2 · Phần 2 (kiến trúc) · Phần 4 | 2,50 |")
add("| **Linh** | Pitch Service (Provider), container hóa | Câu 1.3 · Phần 1 · Phần 5 | 2,50 |")
add("| **Nhật** | Booking Service (Consumer), tích hợp | Câu 1.1 · Phần 3 | 2,50 |")
add("| **Hùng** | Cơ sở dữ liệu, vận hành và giám sát | Câu 1.4 · Phần 2 (dữ liệu) · Phần 6 · Phần 7 | 2,50 |")
add("")
add("> **Phạm vi kế thừa và bổ sung:** theo yêu cầu của đề bài, phần nào đã thực hiện từ các bài thực hành trước và phần nào được bổ sung để hoàn thành bài kiểm tra số 2 được trình bày chi tiết tại **Mục 1.4** của Phần 1.")
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

# ==================================================================== CAU 1
add("## CÂU 1 — LÝ THUYẾT (2,0 ĐIỂM)")
add("")
add("Câu 1 gồm bốn ý, mỗi ý 0,5 điểm.")
add("")
for fn in ("CAU1_1_NHAT.md", "CAU1_2_HOANG.md", "CAU1_3_LINH.md", "CAU1_4_HUNG.md"):
    add("---")
    add("")
    doc.append(prepare(read(fn), part_no=None, demote=2))
    add("")

# ==================================================================== CAU 2
add("---")
add("")
add("## CÂU 2 — THỰC NGHIỆM VÀ BÁO CÁO HỆ THỐNG (8,0 ĐIỂM)")
add("")
add("Câu 2 được trình bày theo đúng cấu trúc bảy phần mà đề bài đề nghị.")
add("")

# --- Phan 1
add("---")
add("")
doc.append(prepare(read("PHAN_1_LINH.md"), part_no=1, demote=2))
add("")

# --- Phan 2: gop 2.1a (Hoang) va 2.1b (Hung) thanh MOT phan
add("---")
add("")
add("### PHẦN 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG")
add("")
add("Phần 2 gồm hai nội dung bổ trợ nhau: **sơ đồ kiến trúc tích hợp và triển khai** (mục 2.1, Hoàng thực hiện) và **thiết kế dữ liệu phân tán cùng bảng mô tả dịch vụ** (mục 2.2, Hùng thực hiện).")
add("")
add("#### 2.1. Sơ đồ kiến trúc tích hợp và kiến trúc triển khai")
add("")
doc.append(prepare(read("PHAN_2_HOANG.md"), part_no=None, demote=3, drop_title=True))
add("")
add("#### 2.2. Thiết kế dữ liệu phân tán và bảng mô tả dịch vụ")
add("")
doc.append(prepare(read("PHAN_2_HUNG.md"), part_no=None, demote=3, drop_title=True))
add("")

# --- Phan 3 den 7
for part_no, fn in ((3, "PHAN_3_NHAT.md"), (4, "PHAN_4_HOANG.md"),
                    (5, "PHAN_5_LINH.md"), (6, "PHAN_6_HUNG.md"),
                    (7, "PHAN_7_HUNG.md")):
    add("---")
    add("")
    doc.append(prepare(read(fn), part_no=part_no, demote=2))
    add("")

# ==================================================================== PHU LUC
add("---")
add("")
add("## PHỤ LỤC: DANH MỤC MÃ NGUỒN VÀ MINH CHỨNG")
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
    ("Biên bản kiểm thử tích hợp (IT01–IT07)", "`docs/testing/integration-test.md`"),
    ("Biên bản kiểm thử Service Discovery (TC01–TC06)", "`docs/testing/service-discovery-test.md`"),
    ("Biên bản kiểm thử vận hành (DEP01–DEP08)", "`docs/testing/operation-test.md`"),
    ("Bộ sưu tập Postman", "`postman/collection.json`"),
    ("Sơ đồ kiến trúc", "`docs/architecture/`"),
]:
    add("| %s | %s |" % (name, path))
add("")

text = "\n".join(doc)


# ------------------------------------------------------------- sinh muc luc
def slug(s):
    s = s.lower()
    s = re.sub(r"[^\w\sÀ-ỹ-]", "", s)
    return re.sub(r"\s+", "-", s.strip())


entries = []
for ln, in_code in split_fence_aware(text):
    if in_code:
        continue
    m = HEAD_RE.match(ln)
    if not m:
        continue
    lvl, name = len(m.group(1)), m.group(2).strip()
    if lvl not in (2, 3, 4) or name == "MỤC LỤC":
        continue
    if lvl == 4 and not name.startswith("2."):
        continue  # chi dua 2 muc con cua Phan 2 vao muc luc
    indent = {2: "", 3: "  ", 4: "    "}[lvl]
    entries.append("%s- [%s](#%s)" % (indent, name, slug(name)))

text = text.replace("<!-- MUC_LUC -->", "\n".join(entries))
text = re.sub(r"\n{4,}", "\n\n\n", text)

with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(text + "\n")

print("Da gop xong:", OUT)
print("So dong      :", text.count("\n") + 1)
print("Muc trong TOC:", len(entries))
