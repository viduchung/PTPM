"""
Chuyen docs/BAO_CAO_KT2_PITCHOS.md thanh ban Word docs/BAO_CAO_KT2_PITCHOS.docx.

Chay:  python docs/build_docx.py

Dinh dang theo chuan bao cao hoc thuat Viet Nam:
  - Kho A4, le trai 3cm, le phai 2cm, tren/duoi 2cm
  - Chu Times New Roman 13pt, gian dong 1,5 cho phan van ban
  - Bang va khoi ma nguon dung co chu nho hon, gian dong don
  - Muc luc tu dong cua Word (mo file xong bam Ctrl+A roi F9 de cap nhat)
"""
import io
import os
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "BAO_CAO_KT2_PITCHOS.md")
OUT = os.path.join(HERE, "BAO_CAO_KT2_PITCHOS.docx")

BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"
BODY_SIZE = Pt(13)
TABLE_SIZE = Pt(10.5)
CODE_SIZE = Pt(8)

HEADING_SIZES = {1: 18, 2: 16, 3: 14, 4: 13, 5: 13, 6: 13}


# --------------------------------------------------------------- tien ich
def set_font(run, name, size=None, bold=None, italic=None, color=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rfonts.set(qn(attr), name)
    if size is not None:
        run.font.size = size
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def shade(element, hex_fill):
    """To nen cho mot doan van (truyen p._p) hoac mot o bang (truyen _tc)."""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    if hasattr(element, "get_or_add_tcPr"):
        element.get_or_add_tcPr().append(shd)
    else:
        element.get_or_add_pPr().append(shd)


def left_border(paragraph, hex_color="999999", size=18):
    pbdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(size))
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), hex_color)
    pbdr.append(left)
    paragraph._p.get_or_add_pPr().append(pbdr)


def add_toc_field(paragraph):
    r = paragraph.add_run()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = r'TOC \o "1-3" \h \z \u'
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    placeholder = OxmlElement("w:t")
    placeholder.text = "Bấm Ctrl+A rồi F9 để cập nhật mục lục."
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for e in (fld, instr, sep, placeholder, end):
        r._r.append(e)


# ------------------------------------------------------- dinh dang inline
INLINE_RE = re.compile(
    r"(\*\*\*.+?\*\*\*|\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`|\[[^\]]+\]\([^)]*\))",
    re.S,
)


def add_inline(paragraph, text, size=BODY_SIZE, base_bold=False, font=BODY_FONT,
               base_italic=False, _top=True):
    """Phan tich **dam**, *nghieng*, `ma lenh`, [chu](lien ket).

    Ham goi de quy nen xu ly duoc truong hop long nhau nhu **`docker ps`**.
    """
    if _top:
        text = text.replace("\\|", "|")
    for part in INLINE_RE.split(text):
        if not part:
            continue
        if part.startswith("***") and part.endswith("***"):
            add_inline(paragraph, part[3:-3], size, True, font, True, False)
        elif part.startswith("**") and part.endswith("**"):
            add_inline(paragraph, part[2:-2], size, True, font, base_italic, False)
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            add_inline(paragraph, part[1:-1], size, base_bold, font, True, False)
        elif part.startswith("`") and part.endswith("`"):
            r = paragraph.add_run(part[1:-1])
            set_font(r, CODE_FONT, Pt(size.pt - 2), base_bold, base_italic,
                     color=RGBColor(0xA0, 0x20, 0x20))
        elif part.startswith("["):
            m = re.match(r"\[([^\]]+)\]\(([^)]*)\)", part)
            add_inline(paragraph, m.group(1) if m else part, size, base_bold,
                       font, base_italic, False)
        else:
            for k, seg in enumerate(part.split(" ")):
                if k:
                    paragraph.add_run().add_break()
                if seg:
                    r = paragraph.add_run(seg)
                    set_font(r, font, size, base_bold, base_italic)


# ------------------------------------------------------------- doc nguon
with io.open(SRC, encoding="utf-8") as f:
    lines = f.read().split("\n")

doc = Document()

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin, sec.right_margin = Cm(3), Cm(2)
sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)

normal = doc.styles["Normal"]
normal.font.name = BODY_FONT
normal.font.size = BODY_SIZE
normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_after = Pt(6)

for lvl, pt in HEADING_SIZES.items():
    st = doc.styles["Heading %d" % lvl]
    st.font.name = BODY_FONT
    st.font.size = Pt(pt)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.space_before = Pt(12 if lvl <= 3 else 8)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.3
    st.paragraph_format.keep_with_next = True

# so trang o chan trang
footer_p = sec.footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer_p.add_run()
for tag, kind, txt in (("w:fldChar", "begin", None), ("w:instrText", None, "PAGE"),
                       ("w:fldChar", "end", None)):
    e = OxmlElement(tag)
    if kind:
        e.set(qn("w:fldCharType"), kind)
    if txt:
        e.text = txt
    fr._r.append(e)
set_font(fr, BODY_FONT, Pt(11))


def para(text="", style=None, size=BODY_SIZE, align=None, spacing=None,
         space_after=None, indent=None):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    if spacing is not None:
        p.paragraph_format.line_spacing = spacing
    if space_after is not None:
        p.paragraph_format.space_after = space_after
    if indent is not None:
        p.paragraph_format.left_indent = indent
    if text:
        add_inline(p, text, size)
    return p


def code_block(code_lines):
    widest = max((len(x) for x in code_lines), default=0)
    size = CODE_SIZE if widest <= 110 else Pt(7) if widest <= 140 else Pt(6)
    for i, ln in enumerate(code_lines):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = 1.0
        pf.space_before = Pt(6) if i == 0 else Pt(0)
        pf.space_after = Pt(6) if i == len(code_lines) - 1 else Pt(0)
        pf.left_indent = Cm(0.3)
        shade(p._p, "F2F2F2")
        r = p.add_run(ln if ln else " ")
        set_font(r, CODE_FONT, size)


USABLE_WIDTH = Cm(16)   # 21cm tru le trai 3cm va le phai 2cm


def add_picture(rel_path):
    """Chen anh, tu thu nho cho vua be ngang trang in."""
    path = os.path.join(HERE, rel_path.replace("/", os.sep))
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    if not os.path.exists(path):
        r = p.add_run("[Thiếu file ảnh: %s]" % rel_path)
        set_font(r, BODY_FONT, Pt(11), italic=True, color=RGBColor(0xC0, 0, 0))
        return
    p.add_run().add_picture(path, width=USABLE_WIDTH)


def add_photo_slot():
    """Khung trong danh cho anh chup man hinh se dan vao sau."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    shade(p._p, "F4F6F8")
    pbdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + side)
        e.set(qn("w:val"), "dashed")
        e.set(qn("w:sz"), "8")
        e.set(qn("w:space"), "14")
        e.set(qn("w:color"), "A6ADBB")
        pbdr.append(e)
    p._p.get_or_add_pPr().append(pbdr)
    r = p.add_run("[ DÁN ẢNH CHỤP MÀN HÌNH VÀO ĐÂY ]")
    set_font(r, BODY_FONT, Pt(11), bold=True, color=RGBColor(0x8A, 0x92, 0xA0))


def split_row(raw):
    raw = raw.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    cells, cur, esc = [], "", False
    for ch in raw:
        if esc:
            cur += "|" if ch == "|" else "\\" + ch
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    cells.append(cur.strip())
    return cells


def add_table(rows):
    head, body = rows[0], rows[2:]
    aligns = []
    for spec in rows[1]:
        spec = spec.strip()
        if spec.startswith(":") and spec.endswith(":"):
            aligns.append(WD_ALIGN_PARAGRAPH.CENTER)
        elif spec.endswith(":"):
            aligns.append(WD_ALIGN_PARAGRAPH.RIGHT)
        else:
            aligns.append(WD_ALIGN_PARAGRAPH.LEFT)
    ncol = len(head)
    t = doc.add_table(rows=0, cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True

    cells = t.add_row().cells
    for i, txt in enumerate(head):
        p = cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(2)
        add_inline(p, txt, TABLE_SIZE, base_bold=True)
        shade(cells[i]._tc, "D9E2F3")
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))

    for row in body:
        row = (row + [""] * ncol)[:ncol]
        cs = t.add_row().cells
        for i, txt in enumerate(row):
            p = cs[i].paragraphs[0]
            p.alignment = aligns[i] if i < len(aligns) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            add_inline(p, txt.replace("<br>", " "), TABLE_SIZE)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


# ----------------------------------------------------------- bo may duyet
i = 0
n = len(lines)
first_h1 = True
on_cover = False
in_toc_section = False
pending_break = False

while i < n:
    ln = lines[i]
    stripped = ln.strip()

    # ---- khoi ma nguon
    if stripped.startswith("```"):
        i += 1
        buf = []
        while i < n and not lines[i].strip().startswith("```"):
            buf.append(lines[i])
            i += 1
        i += 1
        while buf and not buf[-1].strip():
            buf.pop()
        if buf and not in_toc_section:
            code_block(buf)
        continue

    # ---- hinh anh
    mi = re.match(r"^!\[[^\]]*\]\(([^)]+)\)$", stripped)
    if mi and not in_toc_section:
        add_picture(mi.group(1))
        i += 1
        continue

    # ---- cho trong de dan anh chup man hinh
    if stripped == "[[ANH]]" and not in_toc_section:
        add_photo_slot()
        i += 1
        continue

    # ---- dong chu thich hinh / bang
    mc = re.match(r"^\*((?:Hình|Bảng)\s+[0-9A-Z]+\.[0-9]+\..*)\*$", stripped)
    if mc and not in_toc_section:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = not mc.group(1).startswith("Hình")
        add_inline(p, mc.group(1), Pt(11), base_italic=True)
        for r in p.runs:
            r.font.italic = True
        i += 1
        continue

    # ---- bang
    if stripped.startswith("|") and i + 1 < n and re.match(
            r"^\|[\s:\-|]+\|?$", lines[i + 1].strip()):
        rows = []
        while i < n and lines[i].strip().startswith("|"):
            rows.append(split_row(lines[i]))
            i += 1
        if not in_toc_section:
            add_table(rows)
        continue

    # ---- tieu de
    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        lvl, title = len(m.group(1)), m.group(2).strip()
        in_toc_section = (title == "MỤC LỤC")

        if first_h1 and lvl == 1:
            first_h1 = False
            on_cover = True
            p = para(title, size=Pt(22), align=WD_ALIGN_PARAGRAPH.CENTER,
                     spacing=1.2)
            for r in p.runs:
                r.font.bold = True
            i += 1
            continue

        # Tieu de o trang bia va chu "MUC LUC": dinh dang tay, khong dung
        # style Heading, de chung khong lot vao muc luc tu dong cua Word.
        if on_cover:
            if in_toc_section:
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            cover_pt = {2: 13, 3: 18, 4: 13, 5: 15}.get(lvl, 13)
            p = para(title, size=Pt(cover_pt),
                     align=WD_ALIGN_PARAGRAPH.CENTER, spacing=1.3)
            for r in p.runs:
                r.font.bold = True
            if in_toc_section:
                on_cover = False
                para("")
                add_toc_field(doc.add_paragraph())
                pending_break = True
            i += 1
            continue

        if lvl <= 3 and len(doc.paragraphs) > 3:
            pending_break = True

        if pending_break:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            pending_break = False

        h = doc.add_heading(level=min(lvl, 6))
        h.alignment = (WD_ALIGN_PARAGRAPH.CENTER if lvl <= 2
                       else WD_ALIGN_PARAGRAPH.LEFT)
        add_inline(h, title, Pt(HEADING_SIZES[min(lvl, 6)]), base_bold=True)
        for r in h.runs:
            r.font.bold = True
        i += 1
        continue

    if in_toc_section:
        i += 1
        continue

    # ---- duong ke ngang
    if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
        i += 1
        continue

    # ---- trich dan
    if stripped.startswith(">"):
        buf = []
        while i < n and lines[i].strip().startswith(">"):
            buf.append(re.sub(r"^>\s?", "", lines[i].strip()))
            i += 1
        text = " ".join(x for x in buf if x.strip())
        if text:
            p = para(text, size=Pt(12), indent=Cm(0.6), spacing=1.3)
            left_border(p)
            shade(p._p, "FFF8E1")
        continue

    # ---- danh sach
    m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", ln)
    if m:
        indent_sp, marker, text = m.group(1), m.group(2), m.group(3)
        depth = min(len(indent_sp) // 2, 2)
        ordered = marker[0].isdigit()
        style = ("List Number" if ordered else "List Bullet")
        if depth:
            style += " %d" % (depth + 1)
        try:
            p = doc.add_paragraph(style=style)
        except KeyError:
            p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(3)
        add_inline(p, text, BODY_SIZE)
        i += 1
        continue

    # ---- doan van
    if stripped:
        # Markdown xuong dong cung = hai dau cach cuoi dong.
        # Danh dau bang U+2028 de add_inline chuyen thanh ngat dong trong Word.
        buf = [stripped + (" " if ln.endswith("  ") else "")]
        i += 1
        while i < n:
            raw = lines[i]
            nxt = raw.strip()
            if (not nxt or nxt.startswith(("#", "|", ">", "```"))
                    or re.match(r"^(\s*)([-*+]|\d+[.)])\s+", raw)
                    or re.match(r"^(-{3,}|\*{3,}|_{3,})$", nxt)):
                break
            buf.append(nxt + (" " if raw.endswith("  ") else ""))
            i += 1
        text = ""
        for k, piece in enumerate(buf):
            if k and not text.endswith(" "):
                text += " "
            text += piece
        text = text.rstrip("  ")
        # Doan co xuong dong cung thi can trai: can deu se keo gian cac dong
        # ngan ra het chieu rong trong rat xau.
        para(text, align=(WD_ALIGN_PARAGRAPH.LEFT if " " in text
                          else WD_ALIGN_PARAGRAPH.JUSTIFY))
        continue

    i += 1

doc.save(OUT)

print("Da tao:", OUT)
print("So doan van :", len(doc.paragraphs))
print("So bang     :", len(doc.tables))
print("Kich thuoc  : %.1f KB" % (os.path.getsize(OUT) / 1024.0))
