from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import datetime
import io
import base64
from fpdf import FPDF

router = APIRouter(prefix="/api/v1/export", tags=["Export"])

class ExportRequest(BaseModel):
    layer: Optional[Dict[str, Any]] = None
    aoi: Optional[Dict[str, Any]] = None
    ndvi: Optional[Dict[str, Any]] = None
    vqa: Optional[Dict[str, Any]] = None
    image_data: Optional[str] = None  # Base64 data URL for map image

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    # Replaces unmappable characters with ?
    return text.encode('windows-1252', 'replace').decode('windows-1252')

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 15)
        self.cell(0, 10, "SatQuery AI - Analysis Report", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", border=False, align="C")

@router.post("/pdf")
async def export_pdf(req: ExportRequest):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    # REPORT METADATA
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(190, 8, "REPORT METADATA", ln=True)
    pdf.set_font("helvetica", size=10)
    pdf.cell(190, 6, clean_text(f"Generation Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
    pdf.ln(5)

    # PROJECT / DATASET
    if req.layer:
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "PROJECT / DATASET", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.cell(190, 6, clean_text(f"Selected dataset/scene: {req.layer.get('name', 'Unknown')}"), ln=True)
        props = req.layer.get('stac_properties', {})
        if 'datetime' in props:
            pdf.cell(190, 6, clean_text(f"Acquisition date: {props.get('datetime')}"), ln=True)
        pdf.ln(5)

    # AREA OF INTEREST
    if req.aoi:
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "AREA OF INTEREST", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.cell(190, 6, clean_text(f"Geometry type: {req.aoi.get('type', 'Unknown')}"), ln=True)
        if 'area' in req.aoi:
            pdf.cell(190, 6, clean_text(f"AOI area: {req.aoi.get('area')} m2"), ln=True)
        if 'bounds' in req.aoi:
            b = req.aoi['bounds']
            pdf.cell(190, 6, clean_text(f"North: {b.get('_northEast', {}).get('lat', b.get('north'))}"), ln=True)
            pdf.cell(190, 6, clean_text(f"South: {b.get('_southWest', {}).get('lat', b.get('south'))}"), ln=True)
            pdf.cell(190, 6, clean_text(f"East: {b.get('_northEast', {}).get('lng', b.get('east'))}"), ln=True)
            pdf.cell(190, 6, clean_text(f"West: {b.get('_southWest', {}).get('lng', b.get('west'))}"), ln=True)
        pdf.ln(5)

    # NDVI ANALYSIS
    if req.ndvi:
        stats = req.ndvi.get('statistics') or {}
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "NDVI ANALYSIS", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.cell(190, 6, clean_text(f"Formula: {req.ndvi.get('formula', '(NIR - Red) / (NIR + Red)')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Minimum: {stats.get('min', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Maximum: {stats.get('max', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Mean: {stats.get('mean', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Median: {stats.get('median', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Total pixels: {stats.get('total_pixel_count', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Valid pixels: {stats.get('valid_pixel_count', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"No-data pixels: {stats.get('nodata_pixel_count', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Source CRS: {req.ndvi.get('source_crs', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Display CRS: {req.ndvi.get('display_crs', 'N/A')}"), ln=True)
        pdf.cell(190, 6, clean_text(f"Resolution: {req.ndvi.get('resolution', 'N/A')}"), ln=True)
        pdf.ln(5)

        # NDVI COLOR INTERPRETATION
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "NDVI COLOR INTERPRETATION", ln=True)
        pdf.set_font("helvetica", size=10)
        
        legend_items = [
            ((165, 0, 38), "Negative / very low NDVI (< 0.0): Water, shadows, clouds, or non-vegetated surfaces."),
            ((255, 255, 191), "Low NDVI (0.0 to 0.3): Bare soil, built-up surfaces, roads, or sparse vegetation."),
            ((127, 179, 123), "Moderate NDVI (0.3 to 0.6): Moderate vegetation or partially vegetated areas."),
            ((0, 104, 55), "High NDVI (> 0.6): Dense and healthy vegetation.")
        ]
        
        for color, text in legend_items:
            pdf.set_fill_color(*color)
            pdf.cell(8, 6, "", border=1, fill=True)
            pdf.cell(4, 6, "")
            pdf.cell(178, 6, clean_text(text), ln=True)
            pdf.ln(1)
        
        pdf.ln(4)
        
        # AOI NDVI INTERPRETATION
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "AOI NDVI INTERPRETATION", ln=True)
        pdf.set_font("helvetica", size=10)
        
        if stats and isinstance(stats.get('mean'), (int, float)) and isinstance(stats.get('min'), (int, float)) and isinstance(stats.get('max'), (int, float)):
            mean_val = stats['mean']
            min_val = stats['min']
            max_val = stats['max']
            
            if mean_val < 0.1:
                mean_desc = "which is relatively low and indicates that vegetation is not dominant across the AOI"
            elif mean_val < 0.4:
                mean_desc = "which suggests a mixture of sparse to moderate vegetation across the AOI"
            else:
                mean_desc = "which suggests that healthy vegetation is prominent across the AOI"
                
            if max_val < 0.15:
                range_desc = "suggesting that the area consists primarily of non-vegetated surfaces, water, or shadows."
            elif max_val < 0.35:
                range_desc = "showing that the area contains mostly sparse vegetation or bare surfaces."
            elif min_val < 0.15 and max_val >= 0.35:
                range_desc = "showing that the area contains a mixture of low/non-vegetated surfaces and portions with moderate to dense vegetation."
            else:
                range_desc = "suggesting a predominantly vegetated area."
                
            paragraph = f"The selected AOI has a mean NDVI of {mean_val:.3f}, {mean_desc}. NDVI values range from {min_val:.3f} to {max_val:.3f}, {range_desc}"
            pdf.multi_cell(190, 6, clean_text(paragraph))
        else:
            pdf.multi_cell(190, 6, clean_text("Statistics unavailable. Could not generate AOI interpretation."))
            
        pdf.ln(5)

    # QUERY / VQA
    if req.vqa:
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "QUERY / VQA", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.multi_cell(190, 6, clean_text(f"User question: {req.vqa.get('question', 'N/A')}"))
        pdf.multi_cell(190, 6, clean_text(f"AI answer: {req.vqa.get('answer', 'N/A')}"))
        pdf.cell(190, 6, clean_text(f"Confidence/status: {req.vqa.get('confidence_status', 'N/A')}"), ln=True)
        if 'execution' in req.vqa:
            pdf.cell(190, 6, clean_text(f"Model: {req.vqa['execution'].get('model', 'N/A')}"), ln=True)
        pdf.ln(5)

    # MAP/RESULT IMAGE
    if req.image_data and req.image_data.startswith('data:image'):
        try:
            # Format: data:image/png;base64,...
            header, encoded = req.image_data.split(",", 1)
            img_data = base64.b64decode(encoded)
            with io.BytesIO(img_data) as img_io:
                pdf.add_page()
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(190, 8, "MAP / RESULT IMAGE", ln=True)
                pdf.ln(5)
                # Keep aspect ratio roughly, fit to width 180
                pdf.image(img_io, w=180)
        except Exception as e:
            pdf.set_font("helvetica", size=10)
            pdf.cell(190, 6, clean_text(f"Error embedding image: {e}"), ln=True)

    pdf_bytes = pdf.output(dest='S')
    return Response(content=bytes(pdf_bytes), media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=satquery_report.pdf"
    })
