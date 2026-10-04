from fpdf import FPDF
import base64
import io

# A 1x1 transparent PNG
b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
img_data = base64.b64decode(b64)

pdf = FPDF()
pdf.add_page()
with io.BytesIO(img_data) as img_io:
    pdf.image(img_io, w=180)

try:
    pdf_bytes = pdf.output(dest='S')
    print('OK')
except Exception as e:
    import traceback
    traceback.print_exc()
