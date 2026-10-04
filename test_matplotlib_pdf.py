from fpdf import FPDF
import matplotlib.pyplot as plt
import io
import base64

plt.plot([1, 2, 3], [4, 5, 6])
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
img_data = buf.read()
buf.close()

pdf = FPDF()
pdf.add_page()
pdf.set_font('helvetica', size=12)

with io.BytesIO(img_data) as img_io:
    pdf.image(img_io, w=180)

try:
    pdf_bytes = pdf.output(dest='S')
    print('OK')
except Exception as e:
    import traceback
    traceback.print_exc()
