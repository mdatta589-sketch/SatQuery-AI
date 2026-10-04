import pypdf
reader = pypdf.PdfReader('test.pdf')
text = ''
for page in reader.pages:
    text += page.extract_text()
print('NDVI COLOR INTERPRETATION' in text)
print('AOI NDVI INTERPRETATION' in text)
