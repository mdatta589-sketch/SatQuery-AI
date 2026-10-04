with open('backend/app/processing/raster.py', 'r', encoding='utf8') as f:
    content = f.read()

import re

old_code = """    if aoi['west'] == aoi['east'] or aoi['south'] == aoi['north']:"""
new_code = """    bbox = aoi.get('bbox', aoi) if isinstance(aoi, dict) else aoi
    if 'west' not in bbox and hasattr(aoi, 'bbox'):
        # Just in case it's an object with bbox attribute
        pass # Handle gracefully below if needed
    
    if bbox.get('west') == bbox.get('east') or bbox.get('south') == bbox.get('north'):"""

content = content.replace(old_code, new_code)

old_code_2 = """    # aoi must have west, south, east, north in EPSG:4326
    wgs84_bounds = [aoi['west'], aoi['south'], aoi['east'], aoi['north']]"""
new_code_2 = """    # aoi must have west, south, east, north in EPSG:4326
    bbox = aoi.get('bbox', aoi) if isinstance(aoi, dict) else aoi
    wgs84_bounds = [bbox['west'], bbox['south'], bbox['east'], bbox['north']]"""

content = content.replace(old_code_2, new_code_2)

with open('backend/app/processing/raster.py', 'w', encoding='utf8') as f:
    f.write(content)
print("FIXED RASTER AOI SCHEMA IN BACKEND")
