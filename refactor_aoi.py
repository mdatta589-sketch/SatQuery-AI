import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = '''        currentAOI = { type: e.layerType };
        if (e.layerType === 'marker') {
            currentAOI.type = 'Point';
            const ll = layer.getLatLng();
            currentAOI.lat = ll.lat;
            currentAOI.lng = ll.lng;
        } else if (e.layerType === 'rectangle' || e.layerType === 'polygon') {
            currentAOI.type = e.layerType === 'rectangle' ? 'Rectangle' : 'Polygon';
            currentAOI.bounds = layer.getBounds();
            currentAOI.geojson = layer.toGeoJSON();
            try {
                let latlngs = layer.getLatLngs();
                const ring = (latlngs.length > 0 && Array.isArray(latlngs[0])) ? latlngs[0] : latlngs;
                if (L.GeometryUtil && L.GeometryUtil.geodesicArea) {
                    currentAOI.area = L.GeometryUtil.geodesicArea(ring);
                }
            } catch(err) {
                console.warn("Area calculation error", err);
            }
        }'''

replacement = '''        const geojson = layer.toGeoJSON();
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
            // New standardized fields
            geometry_type: e.layerType === 'marker' ? 'Point' : (e.layerType === 'rectangle' ? 'Rectangle' : 'Polygon'),
            geometry: geojson.geometry,
            bbox: { west, south, east, north },
            area_m2: area_m2,
            area_km2: area_km2,
            
            // Legacy fields to preserve existing UI functionality
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
        }'''

js = js.replace(target, replacement)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
