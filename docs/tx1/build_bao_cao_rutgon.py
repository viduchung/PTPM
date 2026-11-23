# -*- coding: utf-8 -*-
"""Dựng file Word rút gọn từ BAO_CAO_RUT_GON.md.

Chạy:  python docs/build_bao_cao_rutgon.py
Ra:    docs/BAO_CAO_TONG_HOP_RUTGON.docx  (file gốc BAO_CAO_TONG_HOP.docx không bị đụng tới)

Ảnh sơ đồ được lấy lại từ chính file Word gốc nên không cần export lại từ mermaid.live.
"""
import os
import re
import zipfile
import tempfile

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_MD = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "BAO_CAO_RUT_GON.md")
SRC_DOCX = os.path.join(HERE, "BAO_CAO_TONG_HOP.docx")
OUT_DOCX = os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else "BAO_CAO_TONG_HOP_RUTGON.docx")

BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"
BODY_SIZE = Pt(13)
TABLE_SIZE = Pt(10.5)
CAPTION_SIZE = Pt(11.5)
CODE_SIZE = Pt(9)
LINE_SPACING = 1.3
MAX_IMG_W = Cm(11.5)
MAX_IMG_H = Cm(6.2)

# Times New Roman không có hai ký tự này -> thay bằng chữ cho chắc.
CHAR_FIX = {"✔": "Có", "✘": "–", "✓": "Có", "✗": "–"}


def extract_media(dst_dir):
    """Lấy ảnh sơ đồ đã nhúng trong file Word gốc ra thư mục tạm."""
    with zipfile.ZipFile(SRC_DOCX) as z:
        for name in z.namelist():
            if name.startswith("word/media/"):
                with open(os.path.join(dst_dir, os.path.basename(name)), "wb") as f:
                    f.write(z.read(name))


def set_cell_background(cell, hex_color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shd)


def repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    tr_pr.append(el)


def fix_chars(text):
    for bad, good in CHAR_FIX.items():
        text = text.replace(bad, good)
    return text


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`)", re.S)


def add_runs(par, text, base_size=BODY_SIZE, base_font=BODY_FONT):
    """Ghi text vào paragraph, hiểu **đậm**, *nghiêng* và `mã`."""
    text = fix_chars(text)
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**"):
            run = par.add_run(piece[2:-2])
            run.bold = True
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            run = par.add_run(piece[1:-1])
            run.italic = True
        elif piece.startswith("`") and piece.endswith("`"):
            run = par.add_run(piece[1:-1])
            run.font.name = CODE_FONT
            run.font.size = Pt(base_size.pt - 1.5)
            continue
        else:
            run = par.add_run(piece)
        run.font.name = base_font
        run.font.size = base_size


def body_par(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=3,
             left_indent=None, hanging=None, first_line=Cm(0.7)):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = LINE_SPACING
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(0)
    pf.alignment = align
    if left_indent is not None:
        pf.left_indent = left_indent
    if hanging is not None:
        pf.first_line_indent = -hanging
    elif first_line is not None:
        pf.first_line_indent = first_line
    add_runs(p, text)
    return p


def heading(doc, text, level, first_chapter):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = LINE_SPACING
    pf.keep_with_next = True
    if level == 1:
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.space_before = Pt(0 if first_chapter else 18)
        pf.space_after = Pt(8)
        run = p.add_run(fix_chars(text).upper())
        run.bold = True
        run.font.size = Pt(14)
    elif level == 2:
        pf.space_before = Pt(8)
        pf.space_after = Pt(3)
        run = p.add_run(fix_chars(text))
        run.bold = True
        run.font.size = Pt(13.5)
    else:
        pf.space_before = Pt(6)
        pf.space_after = Pt(2)
        run = p.add_run(fix_chars(text))
        run.bold = True
        run.italic = True
        run.font.size = Pt(13)
    run.font.name = BODY_FONT
    p.style = doc.styles["Heading %d" % min(level, 3)]
    for r in p.runs:
        r.font.color.rgb = RGBColor(0, 0, 0)
        r.font.name = BODY_FONT
    return p


def caption(doc, text, before=4, after=4):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.15
    pf.keep_with_next = True
    run = p.add_run(fix_chars(text))
    run.italic = True
    run.font.name = BODY_FONT
    run.font.size = CAPTION_SIZE
    return p


def add_code(doc, lines, lang):
    for i, line in enumerate(lines):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = 0.95
        pf.space_before = Pt(4 if i == 0 else 0)
        pf.space_after = Pt(4 if i == len(lines) - 1 else 0)
        pf.left_indent = Cm(0.6)
        run = p.add_run(line if line.strip() else " ")
        run.font.name = CODE_FONT
        run.font.size = CODE_SIZE
        rpr = run._element.get_or_add_rPr()
        rf = OxmlElement("w:rFonts")
        rf.set(qn("w:ascii"), CODE_FONT)
        rf.set(qn("w:hAnsi"), CODE_FONT)
        rpr.append(rf)


def add_table(doc, rows):
    header, body = rows[0], rows[1:]
    table = doc.add_table(rows=1, cols=len(header))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, text in enumerate(header):
        cell = table.rows[0].cells[idx]
        cell.text = ""
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.line_spacing = 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(p, "**%s**" % text.replace("**", ""), base_size=TABLE_SIZE)
        set_cell_background(cell, "DCE6F1")
    repeat_header(table.rows[0])
    for row_data in body:
        cells = table.add_row().cells
        for idx, text in enumerate(row_data[:len(header)]):
            cells[idx].text = ""
            p = cells[idx].paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            add_runs(p, text, base_size=TABLE_SIZE)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.line_spacing = 1.0
    for r in spacer.runs:
        r.font.size = Pt(4)
    spacer.add_run().font.size = Pt(4)
    return table


def add_image(doc, path, cap_text):
    from docx.image.image import Image as DocxImage
    img = DocxImage.from_file(path)
    ratio = img.px_height / float(img.px_width)
    width = MAX_IMG_W
    if Cm(width.cm * ratio) > MAX_IMG_H:
        width = Cm(MAX_IMG_H.cm / ratio)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)
    p.add_run().add_picture(path, width=width)
    caption(doc, cap_text, before=1, after=5)


def parse_table_block(lines, i):
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        raw = lines[i].strip()
        cells = [c.strip() for c in raw.strip("|").split("|")]
        if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            rows.append(cells)
        i += 1
    return rows, i


def main():
    media_dir = tempfile.mkdtemp(prefix="pitchos_media_")
    extract_media(media_dir)

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin, sec.right_margin = Cm(3), Cm(2)
    sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = BODY_SIZE
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)

    # Số trang ở chân trang
    footer_p = sec.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_p.add_run()
    run.font.name = BODY_FONT
    run.font.size = Pt(11)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._element.addnext(fld)

    with open(SRC_MD, encoding="utf-8") as f:
        lines = f.read().split("\n")

    first_chapter = True
    pending_caption = None
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            heading(doc, m.group(2), level, first_chapter)
            if level == 1:
                first_chapter = False
            i += 1
            continue

        if stripped.startswith("[TABLE]"):
            pending_caption = stripped[len("[TABLE]"):].strip()
            i += 1
            continue

        if stripped.startswith("|"):
            rows, i = parse_table_block(lines, i)
            if pending_caption:
                caption(doc, pending_caption, before=8, after=3)
                pending_caption = None
            add_table(doc, rows)
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            add_code(doc, block, lang)
            continue

        img = re.match(r"^!\[(.*?)\]\(IMG:(.+?)\)$", stripped)
        if img:
            add_image(doc, os.path.join(media_dir, img.group(2)), img.group(1))
            i += 1
            continue

        if stripped.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip().lstrip(">").strip())
                i += 1
            body_par(doc, " ".join(block), left_indent=Cm(0.8), first_line=None,
                     space_after=8)
            continue

        li = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if li:
            body_par(doc, "%s. %s" % (li.group(1), li.group(2)),
                     left_indent=Cm(1.0), hanging=Cm(0.6), space_after=4)
            i += 1
            continue

        li = re.match(r"^[-*]\s+(.*)$", stripped)
        if li:
            body_par(doc, "• " + li.group(1), left_indent=Cm(1.0),
                     hanging=Cm(0.5), space_after=4)
            i += 1
            continue

        body_par(doc, stripped)
        i += 1

    doc.save(OUT_DOCX)
    print("Da tao:", OUT_DOCX)


if __name__ == "__main__":
    main()
