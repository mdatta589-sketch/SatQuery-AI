with open('backend/app/api/export.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

target_text = """    # NDVI ANALYSIS
    if req.ndvi:
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "NDVI ANALYSIS", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.cell(190, 6, "Formula: (NIR - Red) / (NIR + Red)", ln=True)
        pdf.cell(190, 6, f"Minimum: {req.ndvi.get('min', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Maximum: {req.ndvi.get('max', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Mean: {req.ndvi.get('mean', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Total pixels: {req.ndvi.get('total_pixel_count', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Valid pixels: {req.ndvi.get('valid_pixel_count', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"No-data pixels: {req.ndvi.get('nodata_pixel_count', 'N/A')}", ln=True)
        pdf.ln(5)"""

replacement_text = """    # NDVI ANALYSIS
    if req.ndvi:
        stats = req.ndvi.get('statistics', req.ndvi)
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(190, 8, "NDVI ANALYSIS", ln=True)
        pdf.set_font("helvetica", size=10)
        pdf.cell(190, 6, f"Formula: {req.ndvi.get('formula', '(NIR - Red) / (NIR + Red)')}", ln=True)
        pdf.cell(190, 6, f"Minimum: {stats.get('min', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Maximum: {stats.get('max', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Mean: {stats.get('mean', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Median: {stats.get('median', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Total pixels: {stats.get('total_pixel_count', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Valid pixels: {stats.get('valid_pixel_count', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"No-data pixels: {stats.get('nodata_pixel_count', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Source CRS: {req.ndvi.get('source_crs', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Display CRS: {req.ndvi.get('display_crs', 'N/A')}", ln=True)
        pdf.cell(190, 6, f"Resolution: {req.ndvi.get('resolution', 'N/A')}", ln=True)
        pdf.ln(5)"""

content = content.replace(target_text, replacement_text)

with open('backend/app/api/export.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
