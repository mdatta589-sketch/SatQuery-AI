import re
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = '''
        let aoiData = null;
        if (currentAOI && currentAOI.bounds) {
            let nw = currentAOI.bounds.getNorthWest().wrap();
            let se = currentAOI.bounds.getSouthEast().wrap();
            let west = nw.lng;
            let east = se.lng;
            if (west > east) {
                // crossed dateline, STAC expects standard format but for raster we might need unwrapped.
                // We'll just pass unwrapped to be safe for local raster cropping if it doesn't cross dateline.
                west = currentAOI.bounds.getWest();
                east = currentAOI.bounds.getEast();
            }
            aoiData = {
                type: 'bbox',
                north: currentAOI.bounds.getNorth(),
                south: currentAOI.bounds.getSouth(),
                east: east,
                west: west
            };
        }
'''

js = re.sub(r'let aoiData = null;.*?if \(currentAOI && currentAOI\.bounds\) \{.*?aoiData = \{.*?type: \'bbox\',.*?north: currentAOI\.bounds\.getNorth\(\),.*?south: currentAOI\.bounds\.getSouth\(\),.*?east: currentAOI\.bounds\.getEast\(\),.*?west: currentAOI\.bounds\.getWest\(\).*?\};\s*\}', replacement.strip(), js, flags=re.DOTALL)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
