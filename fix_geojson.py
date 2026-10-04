import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Store GeoJSON on draw
target1 = '''          currentAOI.bounds = layer.getBounds();
          try {'''
replacement1 = '''          currentAOI.bounds = layer.getBounds();
          currentAOI.geojson = layer.toGeoJSON();
          try {'''
js = js.replace(target1, replacement1)

# Send GeoJSON in NDVI request
target2 = '''              aoiData = {
                  type: 'bbox',
                  shape: currentAOI.type || 'Rectangle',
                  area: currentAOI.area || 0,
                  north: currentAOI.bounds.getNorth(),
                  south: currentAOI.bounds.getSouth(),
                  east: east,
                  west: west
              };'''
replacement2 = '''              aoiData = {
                  type: 'bbox',
                  shape: currentAOI.type || 'Rectangle',
                  area: currentAOI.area || 0,
                  north: currentAOI.bounds.getNorth(),
                  south: currentAOI.bounds.getSouth(),
                  east: east,
                  west: west,
                  geometry: currentAOI.geojson ? currentAOI.geojson.geometry : null
              };'''
js = js.replace(target2, replacement2)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
