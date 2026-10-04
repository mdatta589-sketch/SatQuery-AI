import rasterio
from rasterio.warp import transform_bounds

src_crs = rasterio.crs.CRS.from_epsg(32623)
wgs84_bounds = [-180, -90, 180, 90]
try:
    print(transform_bounds('EPSG:4326', src_crs, *wgs84_bounds))
except Exception as e:
    print("FAILED:", e)
