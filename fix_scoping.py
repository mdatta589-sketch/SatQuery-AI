with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Add to module level imports
    if line.strip() == "import rasterio":
        if i < 20: # Make sure it's the top level one
            new_lines.append(line)
            new_lines.append("import rasterio.features\n")
            new_lines.append("import rasterio.warp\n")
            continue
            
    # Remove local imports
    if line.strip() == "import rasterio" and i >= 20:
        continue
    if line.strip() == "import rasterio.features" and i >= 20:
        continue
    if line.strip() == "import rasterio.warp" and i >= 20:
        continue
        
    new_lines.append(line)

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
