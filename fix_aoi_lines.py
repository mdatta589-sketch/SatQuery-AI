with open('frontend/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "currentAOI = { type: e.layerType };" in line:
        skip = True
        new_lines.append('''        const geojson = layer.toGeoJSON();
        let area_m2 = null;
        let area_km2 = null;
        
        let nw, se, west, east, north, south;
        if (e.layerType === 'marker') {
            const ll = layer.getLatLng();
            west = ll.lng; east = ll.lng;
            south = ll.lat; north = ll.lat;
        } else {
            const b = layer.getBounds();
            nw = b.getNorthWest().wrap();
            se = b.getSouthEast().wrap();
            west = nw.lng;
            east = se.lng;
            if (west > east) {
                west = b.getWest();
                east = b.getEast();
            }
            south = b.getSouth();
            north = b.getNorth();
            
            try {
                let latlngs = layer.getLatLngs();
                const ring = (latlngs.length > 0 && Array.isArray(latlngs[0])) ? latlngs[0] : latlngs;
                if (L.GeometryUtil && L.GeometryUtil.geodesicArea) {
                    area_m2 = L.GeometryUtil.geodesicArea(ring);
                    area_km2 = area_m2 / 1000000;
                }
            } catch(err) {
                console.warn("Area calculation error", err);
            }
        }

        currentAOI = { 
            geometry_type: e.layerType === 'marker' ? 'Point' : (e.layerType === 'rectangle' ? 'Rectangle' : 'Polygon'),
            geometry: geojson.geometry,
            bbox: { west, south, east, north },
            area_m2: area_m2,
            area_km2: area_km2,
            
            // Legacy attributes to preserve existing UI compatibility
            type: e.layerType === 'marker' ? 'Point' : (e.layerType === 'rectangle' ? 'Rectangle' : 'Polygon'),
            geojson: geojson
        };
        
        if (e.layerType === 'marker') {
            const ll = layer.getLatLng();
            currentAOI.lat = ll.lat;
            currentAOI.lng = ll.lng;
        } else {
            currentAOI.bounds = layer.getBounds();
            currentAOI.area = area_m2;
        }\n''')
        continue
        
    if skip:
        if "updateAOIPanel();" in line:
            skip = False
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
