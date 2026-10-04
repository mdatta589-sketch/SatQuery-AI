import re

with open('frontend/app.js', 'r', encoding='utf8') as f:
    content = f.read()

old_rect = '''        const kanchaBounds = [[17.41, 78.32], [17.45, 78.36]];
        map.fitBounds(kanchaBounds);
        
        caseStudyAoiLayer = L.rectangle(kanchaBounds, {color: 'blue', weight: 2, fill: false});
        caseStudyAoiLayer.addTo(map);'''

new_rect = '''        const kanchaBounds = [[17.41, 78.32], [17.45, 78.36]];
        map.fitBounds(kanchaBounds);
        
        caseStudyAoiLayer = L.rectangle(kanchaBounds, {color: 'blue', weight: 2, fill: false});
        caseStudyAoiLayer.addTo(map);
        
        const boundsObj = L.latLngBounds(kanchaBounds);
        const nw = boundsObj.getNorthWest();
        const se = boundsObj.getSouthEast();
        currentAOI = {
            geometry_type: 'Polygon',
            type: 'Polygon',
            bbox: { west: nw.lng, north: nw.lat, east: se.lng, south: se.lat },
            bounds: boundsObj,
            geometry: {
                type: 'Polygon',
                coordinates: [[
                    [nw.lng, nw.lat],
                    [se.lng, nw.lat],
                    [se.lng, se.lat],
                    [nw.lng, se.lat],
                    [nw.lng, nw.lat]
                ]]
            }
        };'''

if old_rect in content:
    content = content.replace(old_rect, new_rect)
    with open('frontend/app.js', 'w', encoding='utf8') as f:
        f.write(content)
    print("REPLACED app.js currentAOI")
else:
    print("NOT FOUND")
