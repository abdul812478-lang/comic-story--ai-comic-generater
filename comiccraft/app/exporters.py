import os
from datetime import datetime
from pathlib import Path

from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent


def save_pdf(layout):
    output_dir = BASE_DIR / "static" / "exports"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        if output_dir.exists() and not output_dir.is_dir():
            output_dir.unlink()
            output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    output_path = output_dir / filename

    pdf = FPDF()

    for panel in layout:
        pdf.add_page()

        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 15, f"Panel {panel['panel']}: {panel['title']}", ln=True)

        image_path = panel["image"]
        resolved_image = None

        if image_path.startswith("/"):
            resolved_image = (BASE_DIR / image_path.lstrip("/")).resolve()
        else:
            resolved_image = (BASE_DIR / image_path).resolve()

        if resolved_image.exists():
            pdf.image(str(resolved_image), x=10, y=30, w=190)

        pdf.set_font("Arial", "", 12)
        pdf.ln(125)
        pdf.multi_cell(0, 8, panel["scene_description"])
        pdf.ln(5)
        pdf.multi_cell(0, 8, panel["story"])

    pdf.output(str(output_path))
    return "/" + str(output_path.relative_to(BASE_DIR)).replace("\\", "/")