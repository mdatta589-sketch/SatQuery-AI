from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', size=10)

legend_items = [
    ((165, 0, 38), "Negative NDVI (< 0.0): Water, shadows, clouds, or non-vegetated surfaces."),
    ((255, 255, 191), "Low NDVI (0.0 to 0.3): Bare soil, built-up surfaces, roads, or sparse vegetation."),
    ((127, 179, 123), "Moderate NDVI (0.3 to 0.6): Moderate vegetation or partially vegetated areas."),
    ((0, 104, 55), "High NDVI (> 0.6): Dense and healthy vegetation.")
]

for color, text in legend_items:
    pdf.set_fill_color(*color)
    pdf.cell(8, 6, "", border=1, fill=True)
    pdf.cell(4, 6, "") # spacer
    pdf.cell(178, 6, text, ln=True)
    pdf.ln(1)

pdf.output("test_legend.pdf")
print("OK")
