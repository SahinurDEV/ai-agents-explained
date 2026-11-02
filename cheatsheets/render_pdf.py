"""Render the cheat-sheet markdown files to dark, course-style A4 PDFs. pip install reportlab"""
import glob, os, re
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

D = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("S", D + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("SB", D + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("M", D + "DejaVuSansMono.ttf"))
BG, TEXT, DIM, ACC, ACC3, CODEBG = "#090B10", "#F2F4F8", "#8A93A6", "#5C9CFF", "#34D399", "#0D1016"
W, H = A4
COURSE = "AI Agents Explained · Cheat Sheet"


def wrap(text, font, size, maxw):
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) > maxw and cur:
            out.append(cur); cur = w
        else:
            cur = t
    return out + [cur]


def render(md, pdf):
    c = canvas.Canvas(pdf, pagesize=A4)
    page = [0]

    def new_page():
        if page[0]:
            c.showPage()
        page[0] += 1
        c.setFillColor(BG); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(ACC); c.rect(0, H - 6, W, 6, fill=1, stroke=0)
        c.setFillColor(DIM); c.setFont("S", 8)
        c.drawString(40, 22, COURSE); c.drawRightString(W - 40, 22, f"page {page[0]}")
        return H - 50

    y = new_page()
    lines = open(md, encoding="utf-8").read().splitlines()
    incode = False
    for ln in lines:
        need = 16
        if y < 60 + need:
            y = new_page()
        if ln.startswith("```"):
            incode = not incode; y -= 4; continue
        if incode:
            c.setFillColor(CODEBG); c.rect(40, y - 4, W - 80, 13, fill=1, stroke=0)
            c.setFillColor(ACC3); c.setFont("M", 8.5); c.drawString(48, y, ln[:105]); y -= 13; continue
        clean = re.sub(r"\*\*(.+?)\*\*|`(.+?)`", lambda m: m.group(1) or m.group(2), ln)
        if ln.startswith("# "):
            c.setFillColor(TEXT); c.setFont("SB", 20); c.drawString(40, y - 6, clean[2:]); y -= 34
        elif ln.startswith("## "):
            y -= 6; c.setFillColor(ACC); c.setFont("SB", 13); c.drawString(40, y, clean[3:]); y -= 18
        elif re.match(r"^\s*- \[ \] ", ln):
            c.setStrokeColor(ACC); c.rect(48, y - 1, 8, 8, fill=0, stroke=1)
            for i, t in enumerate(wrap(clean.split("] ", 1)[1], "S", 10, W - 130)):
                c.setFillColor(TEXT); c.setFont("S", 10); c.drawString(64, y, t); y -= 14
        elif re.match(r"^\s*- ", ln):
            c.setFillColor(ACC); c.circle(52, y + 3, 2, fill=1, stroke=0)
            for t in wrap(clean.strip()[2:], "S", 10, W - 130):
                c.setFillColor(TEXT); c.setFont("S", 10); c.drawString(62, y, t); y -= 14
        elif ln.strip():
            for t in wrap(clean, "S", 10, W - 80):
                c.setFillColor(TEXT); c.setFont("S", 10); c.drawString(40, y, t); y -= 14
        else:
            y -= 6
    c.save()


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for md in sorted(glob.glob(os.path.join(here, "*.md"))):
        if os.path.basename(md) == "README.md":
            continue
        out = os.path.join(here, "pdf", os.path.basename(md)[:-3] + ".pdf")
        render(md, out); print(out)
