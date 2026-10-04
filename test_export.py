from fpdf import FPDF

def clean_text(text):
    if not isinstance(text, str):
        text = str(text)
    return text.encode('windows-1252', 'replace').decode('windows-1252')

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'SatQuery AI - Analysis Report', border=False, ln=True, align='C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', border=False, align='C')

pdf = PDF()
pdf.add_page()
pdf.set_font('helvetica', size=12)

# Simulate missing fields
req_layer = None
req_aoi = {'bounds': {'north': None, 'south': None, 'east': None, 'west': None}}
req_ndvi = {'statistics': {'min': None, 'max': None}}
req_vqa = None

if req_aoi:
    b = req_aoi['bounds']
    pdf.cell(190, 6, clean_text(f"North: {b.get('_northEast', {}).get('lat', b.get('north'))}"), ln=True)

if req_ndvi:
    stats = req.ndvi.get('statistics', req_ndvi)
    pdf.cell(190, 6, clean_text(f"Minimum: {stats.get('min', 'N/A')}"), ln=True)

try:
    pdf_bytes = pdf.output(dest='S')
    print('OK')
except Exception as e:
    import traceback
    traceback.print_exc()
