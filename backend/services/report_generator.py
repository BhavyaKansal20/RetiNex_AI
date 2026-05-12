from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import io
import cv2
import numpy as np
from PIL import Image as PILImage

from backend.config import (
    CLASS_NAMES, SEVERITY_DESCRIPTIONS, SEVERITY_COLORS, REPORTS_DIR,
)


def _np_to_rl_image(np_image: np.ndarray, width: float, height: float) -> RLImage:
    """Convert a numpy RGB image to a ReportLab Image object."""
    pil_img = PILImage.fromarray(np_image)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    return RLImage(buf, width=width, height=height)


def generate_report(
    patient_id: str,
    prediction: dict,
    original_image: np.ndarray,
    heatmap_image: np.ndarray,
    overlay_image: np.ndarray,
    report_id: str = None,
) -> str:
    """Generate a professional medical PDF report and return its file path."""
    if report_id is None:
        report_id = f"RPT-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    filename = f"retinex_report_{report_id}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=4 * mm,
        fontName="Helvetica-Bold",
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#6b7280"),
        spaceAfter=6 * mm,
        alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#1e3a5f"),
        spaceBefore=6 * mm,
        spaceAfter=3 * mm,
        fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#374151"),
        leading=14,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#6b7280"),
    )

    elements = []

    # Header
    elements.append(Paragraph("RetiNex AI", title_style))
    elements.append(Paragraph("Diabetic Retinopathy Screening Report", subtitle_style))
    elements.append(
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb"))
    )
    elements.append(Spacer(1, 4 * mm))

    # Report metadata
    predicted_class = prediction.get("predicted_class", 0)
    severity_color = SEVERITY_COLORS.get(predicted_class, "#6b7280")

    meta_data = [
        ["Report ID:", report_id, "Date:", datetime.utcnow().strftime("%B %d, %Y %H:%M UTC")],
        ["Patient ID:", patient_id, "Model:", "EfficientNetV2-B0"],
    ]
    meta_table = Table(meta_data, colWidths=[25 * mm, 55 * mm, 25 * mm, 60 * mm])
    meta_table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6b7280")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#6b7280")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (3, 0), (3, -1), colors.HexColor("#1a1a2e")),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 5 * mm))

    # Prediction result
    elements.append(Paragraph("Prediction Result", section_style))
    result_data = [
        ["DR Classification:", prediction.get("predicted_label", "N/A")],
        ["Confidence:", f"{prediction.get('confidence', 0) * 100:.1f}%"],
        ["Severity Level:", f"Grade {predicted_class}"],
    ]
    result_table = Table(result_data, colWidths=[45 * mm, 120 * mm])
    result_table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6b7280")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor(severity_color)),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(result_table)
    elements.append(Spacer(1, 3 * mm))

    # Confidence breakdown
    elements.append(Paragraph("Confidence Breakdown", section_style))
    probs = prediction.get("probabilities", {})
    if isinstance(probs, dict):
        prob_rows = [["Class", "Confidence"]]
        for cls_name, prob in probs.items():
            prob_rows.append([cls_name, f"{prob * 100:.2f}%"])
        prob_table = Table(prob_rows, colWidths=[60 * mm, 40 * mm])
        prob_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f9fafb")]),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(prob_table)
    elements.append(Spacer(1, 5 * mm))

    # Images
    elements.append(Paragraph("Retinal Image Analysis", section_style))
    img_width = 55 * mm
    img_height = 55 * mm
    try:
        orig_rl = _np_to_rl_image(original_image, img_width, img_height)
        heat_rl = _np_to_rl_image(heatmap_image, img_width, img_height)
        over_rl = _np_to_rl_image(overlay_image, img_width, img_height)
        img_table_data = [
            [orig_rl, heat_rl, over_rl],
            [
                Paragraph("Original", ParagraphStyle("c", alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#6b7280"))),
                Paragraph("GradCAM Heatmap", ParagraphStyle("c", alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#6b7280"))),
                Paragraph("Overlay", ParagraphStyle("c", alignment=TA_CENTER, fontSize=8, textColor=colors.HexColor("#6b7280"))),
            ],
        ]
        img_table = Table(img_table_data, colWidths=[57 * mm, 57 * mm, 57 * mm])
        img_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(img_table)
    except Exception:
        elements.append(Paragraph("Images could not be embedded.", body_style))
    elements.append(Spacer(1, 5 * mm))

    # Clinical recommendation
    elements.append(Paragraph("Clinical Assessment", section_style))
    description = SEVERITY_DESCRIPTIONS.get(predicted_class, "")
    elements.append(Paragraph(description, body_style))
    elements.append(Spacer(1, 4 * mm))

    # Disclaimer
    elements.append(
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#d1d5db"))
    )
    elements.append(Spacer(1, 3 * mm))
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=7,
        textColor=colors.HexColor("#9ca3af"),
        leading=10,
    )
    elements.append(Paragraph(
        "<b>Disclaimer:</b> This report is generated by an AI system for screening purposes only. "
        "It does not constitute a medical diagnosis. Please consult a qualified ophthalmologist for "
        "clinical decisions. This system is intended to assist healthcare professionals and should "
        "not replace professional medical judgment.",
        disclaimer_style,
    ))
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph(
        f"Generated by RetiNex AI • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, textColor=colors.HexColor("#d1d5db"), alignment=TA_CENTER),
    ))

    doc.build(elements)
    return filepath
