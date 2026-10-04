import re

with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''                    valid_mask = (red_data > 0) & (nir_data > 0)
                    denominator = nir_data + red_data
                    np.putmask(denominator, denominator == 0, 1e-10)
                    ndvi = (nir_data - red_data) / denominator
                    ndvi[~valid_mask] = np.nan'''

replacement = '''                    valid_mask = (red_data > 0) & (nir_data > 0)
                    
                    if req.aoi and req.aoi.get('geometry'):
                        import rasterio.features
                        import rasterio.warp
                        # Scale transform for the scaled output
                        scaled_transform = transform * transform.scale((width / dst_width), (height / dst_height))
                        
                        geom_3857 = rasterio.warp.transform_geom('EPSG:4326', 'EPSG:3857', req.aoi['geometry'])
                        poly_mask = rasterio.features.geometry_mask(
                            [geom_3857],
                            out_shape=(dst_height, dst_width),
                            transform=scaled_transform,
                            invert=True,
                            all_touched=True
                        )
                        valid_mask = valid_mask & poly_mask
                    
                    denominator = nir_data + red_data
                    np.putmask(denominator, denominator == 0, 1e-10)
                    ndvi = (nir_data - red_data) / denominator
                    ndvi[~valid_mask] = np.nan'''

code = code.replace(target, replacement)

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)
