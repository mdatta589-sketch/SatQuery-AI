with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = '''          let aoiData = null;
          if (currentAOI && currentAOI.bounds) {
              let nw = currentAOI.bounds.getNorthWest().wrap();
              let se = currentAOI.bounds.getSouthEast().wrap();
              let west = nw.lng;
              let east = se.lng;
              if (west > east) {
                  west = currentAOI.bounds.getWest();
                  east = currentAOI.bounds.getEast();
              }
              aoiData = {
                  type: 'bbox',
                  shape: currentAOI.type || 'Rectangle',
                  area: currentAOI.area || 0,
                  north: currentAOI.bounds.getNorth(),
                  south: currentAOI.bounds.getSouth(),
                  east: east,
                  west: west
              };
          }'''

replacement = '''          let aoiData = null;
          if (currentAOI) {
              aoiData = {
                  type: 'bbox',
                  shape: currentAOI.geometry_type,
                  area: currentAOI.area_m2 || 0,
                  north: currentAOI.bbox.north,
                  south: currentAOI.bbox.south,
                  east: currentAOI.bbox.east,
                  west: currentAOI.bbox.west,
                  geometry: currentAOI.geometry
              };
          }'''

js = js.replace(target, replacement)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
