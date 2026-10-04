with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

import re

old_aoi = """                let aoiData = null;
                if (currentAOI) {
                    const b = currentAOI.bounds;
                    aoiData = { type: 'Polygon', bbox: { west: b.getWest(), north: b.getNorth(), east: b.getEast(), south: b.getSouth() } };
                }"""

new_aoi = """                let aoiData = null;
                if (currentAOI) {
                    if (currentAOI.bounds) {
                        const b = currentAOI.bounds;
                        aoiData = { type: 'Polygon', bbox: { west: b.getWest(), north: b.getNorth(), east: b.getEast(), south: b.getSouth() } };
                    } else if (currentAOI.bbox) {
                        aoiData = { type: 'Polygon', bbox: currentAOI.bbox };
                    } else if (currentAOI.lat !== undefined) {
                        aoiData = { type: 'Point', lat: currentAOI.lat, lng: currentAOI.lng };
                    }
                }"""

content = content.replace(old_aoi, new_aoi)

with open('frontend/app.js', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED AOI LOGIC")
