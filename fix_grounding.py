import sys
import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
                                // Temporary image_pixel mapping
                                if (currentLayer && currentLayer.bounds) {
                                    if (ev.type === 'bbox' && ev.geometry.coordinates.length === 4) {
                                        const [x1, y1, x2, y2] = ev.geometry.coordinates;
                                        const w = 1024;
                                        const h = 1024;
                                        
                                        // If an AOI was used for VQA, grounding pixels are relative to the AOI, not the full scene!
                                        let bounds = currentLayer.bounds; // [[south, west], [north, east]]
                                        if (aoiData) {
                                            bounds = [[aoiData.south, aoiData.west], [aoiData.north, aoiData.east]];
                                        }
                                        
                                        const s = bounds[0][0], w_ = bounds[0][1], n = bounds[1][0], e_ = bounds[1][1];
                                        
                                        const lat1 = n - (y1 / h) * (n - s);
                                        const lon1 = w_ + (x1 / w) * (e_ - w_);
                                        const lat2 = n - (y2 / h) * (n - s);
                                        const lon2 = w_ + (x2 / w) * (e_ - w_);
'''

js = re.sub(r'// Temporary image_pixel mapping\s*if \(currentLayer && currentLayer\.bounds && currentLayer\.metadata && currentLayer\.metadata\.width && currentLayer\.metadata\.height\) \{\s*if \(ev\.type === \'bbox\' && ev\.geometry\.coordinates\.length === 4\) \{\s*const \[x1, y1, x2, y2\] = ev\.geometry\.coordinates;\s*const w = 1024;\s*const h = 1024;\s*const bounds = currentLayer\.bounds; // \[\[south, west\], \[north, east\]\]\s*const s = bounds\[0\]\[0\], w_ = bounds\[0\]\[1\], n = bounds\[1\]\[0\], e_ = bounds\[1\]\[1\];\s*const lat1 = n - \(y1 / h\) \* \(n - s\);\s*const lon1 = w_ \+ \(x1 / w\) \* \(e_ - w_\);\s*const lat2 = n - \(y2 / h\) \* \(n - s\);\s*const lon2 = w_ \+ \(x2 / w\) \* \(e_ - w_\);', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
