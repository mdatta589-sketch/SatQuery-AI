import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_pattern = re.compile(
    r"let aoiData = null;\s*if \(currentAOI && currentAOI\.bounds\) \{\s*"
    r"let nw = currentAOI\.bounds\.getNorthWest\(\)\.wrap\(\);\s*"
    r"let se = currentAOI\.bounds\.getSouthEast\(\)\.wrap\(\);\s*"
    r"let west = nw\.lng;\s*"
    r"let east = se\.lng;\s*"
    r"if \(west > east\) \{\s*"
    r"west = currentAOI\.bounds\.getWest\(\);\s*"
    r"east = currentAOI\.bounds\.getEast\(\);\s*"
    r"\}\s*"
    r"aoiData = \{\s*"
    r"type: 'bbox',\s*"
    r"shape: currentAOI\.type \|\| 'Rectangle',\s*"
    r"area: currentAOI\.area \|\| 0,\s*"
    r"north: currentAOI\.bounds\.getNorth\(\),\s*"
    r"south: currentAOI\.bounds\.getSouth\(\),\s*"
    r"east: east,\s*"
    r"west: west\s*"
    r"\};\s*"
    r"\}",
    re.MULTILINE
)

replacement = '''let aoiData = null;
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

js = target_pattern.sub(replacement, js)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
