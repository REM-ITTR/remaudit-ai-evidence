from pathlib import Path
from datetime import datetime, timezone

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

TITLE = "Incident Evidence Memorandum — REMAudit-AI (Demo)"
FOOTER_LEFT = "© 2026 REMAudit. All rights reserved."
FOOTER_RIGHT = "Patent Pending. REMAudit™ / REM™ / USSRF™"

def wrap_lines(text: str, max_chars: int = 96):
    lines = []
    for para in text.splitlines():
        if not para.strip():
            lines.append("")
            continue
        s = para.rstrip()
        while len(s) > max_chars:
            cut = s.rfind(" ", 0, max_chars)
            if cut == -1:
                cut = max_chars
            lines.append(s[:cut].rstrip())
            s = s[cut:].lstrip()
        lines.append(s)
    return lines

def build_pdf(md_path: Path, pdf_path: Path):
    raw = md_path.read_text(encoding="utf-8")

    # lightweight "md to text": keep content as-is (headings/bullets already readable)
    text = raw.replace("\t", "    ")

    c = canvas.Canvas(str(pdf_path), pagesize=LETTER)
    width, height = LETTER

    margin_x = 54
    margin_top = 60
    margin_bottom = 54

    y = height - margin_top

    # header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, TITLE)
    y -= 20

    c.setFont("Helvetica", 9)
    gen = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    c.drawString(margin_x, y, f"Generated (UTC): {gen}")
    y -= 18

    c.setFont("Helvetica", 11)
    lines = wrap_lines(text, max_chars=100)

    def footer():
        c.setFont("Helvetica", 8)
        c.drawString(margin_x, 28, FOOTER_LEFT)
        c.drawRightString(width - margin_x, 28, FOOTER_RIGHT)

    c.setFont("Helvetica", 11)
    for line in lines:
        if y <= margin_bottom:
            footer()
            c.showPage()
            y = height - margin_top
            c.setFont("Helvetica", 11)

        if line.startswith("# "):
            c.setFont("Helvetica-Bold", 13)
            c.drawString(margin_x, y, line[2:].strip())
            y -= 18
            c.setFont("Helvetica", 11)
            continue

        if line.startswith("## "):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_x, y, line[3:].strip())
            y -= 16
            c.setFont("Helvetica", 11)
            continue

        c.drawString(margin_x, y, line)
        y -= 14

    footer()
    c.save()

if __name__ == "__main__":
    md = Path("docs/REMAudit-AI_Incident_Evidence_Memorandum.md")
    pdf = Path("docs/REMAudit-AI_Incident_Evidence_Memorandum.pdf")
    if not md.exists():
        raise SystemExit(f"Missing: {md}")
    pdf.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(md, pdf)
    print(f"OK: wrote {pdf}")
