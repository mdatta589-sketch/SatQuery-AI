import rasterio
from rasterio.warp import transform_bounds

src_crs = rasterio.crs.CRS.from_epsg(32623)
wgs84_bounds = [-47.6, 71.0, -47.4, 71.1]
target_bounds = transform_bounds('EPSG:4326', src_crs, *wgs84_bounds)

src_bounds = rasterio.coords.BoundingBox(left=399960.0, bottom=7790220.0, right=509760.0, top=7900020.0)

print("Target bounds:", target_bounds)
print("Src bounds:", src_bounds)

left = max(target_bounds[0], src_bounds.left)
bottom = max(target_bounds[1], src_bounds.bottom)
right = min(target_bounds[2], src_bounds.right)
top = min(target_bounds[3], src_bounds.top)

print("Intersection left, bottom, right, top:", left, bottom, right, top)
print("Overlap valid?", left < right and bottom < top)
