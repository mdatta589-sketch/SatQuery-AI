import sys
with open('backend/app/api/catalog.py', 'r') as f:
    content = f.read()

import re

new_func = '''
def _render_stac(scene_id: str, collection: str, bands_to_load: list, vmin: Optional[float], vmax: Optional[float], aoi: Optional[dict] = None):
    try:
        catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace
        )
        search = catalog.search(collections=[collection], ids=[scene_id])
        item = next(search.items(), None)
        if not item:
            raise HTTPException(status_code=404, detail="Scene not found")

        for b in bands_to_load:
            if b not in item.assets:
                raise HTTPException(status_code=400, detail=f"Band {b} not found in scene")

        with rasterio.Env(CPL_VSIL_CURL_ALLOWED_EXTENSIONS='tif'):
            href0 = item.assets[bands_to_load[0]].href
            with rasterio.open(href0) as src:
                if aoi:
                    from app.processing.raster import get_aoi_window_and_transform
                    window, window_transform = get_aoi_window_and_transform(src, aoi)
                    if window is None:
                        raise HTTPException(status_code=400, detail="AOI is outside scene bounds")
                    window_bounds = rasterio.windows.bounds(window, window_transform)
                    transform, width, height = calculate_default_transform(
                        src.crs, 'EPSG:3857', int(window.width), int(window.height), *window_bounds
                    )
                else:
                    transform, width, height = calculate_default_transform(
                        src.crs, 'EPSG:3857', src.width, src.height, *src.bounds
                    )
                    
                vrt_options = {
                    'crs': 'EPSG:3857',
                    'transform': transform,
                    'width': width,
                    'height': height
                }
                max_dim = 1024
                scale = min(1.0, max_dim / max(width, height))
                dst_width = max(1, int(width * scale))
                dst_height = max(1, int(height * scale))
                out_shape = (dst_height, dst_width)

            data_list = []
            for b in bands_to_load:
                href = item.assets[b].href
                with rasterio.open(href) as src:
                    with WarpedVRT(src, **vrt_options) as vrt:
                        arr = vrt.read(1, out_shape=out_shape, resampling=Resampling.bilinear)
                        data_list.append(arr)
'''

content = re.sub(r'def _render_stac.*?data_list\.append\(arr\)', new_func.strip(), content, flags=re.DOTALL)
with open('backend/app/api/catalog.py', 'w') as f:
    f.write(content)
