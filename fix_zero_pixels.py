with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "total_pixels = ndvi.size" in line:
        lines.insert(i + 2, "                    if valid_pixels.size == 0:\n                        raise HTTPException(status_code=400, detail=\"Selected AOI contains no valid Sentinel-2 pixels. Please select an area within the actual imagery footprint.\")\n")
        break

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
