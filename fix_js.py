with open('frontend/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(r'resolution: currentLayer\.metadata\?\.resolution \? \$\{Math\.abs\(currentLayer\.metadata\.resolution\)\.toFixed\(0\)\} m : \'\-\'', 
                 r'resolution: currentLayer.metadata?.resolution ? ${Math.abs(currentLayer.metadata.resolution).toFixed(0)} m : \'-\'', 
                 content)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
