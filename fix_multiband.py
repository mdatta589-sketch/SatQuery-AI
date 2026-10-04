import re

with open('backend/app/api/analysis.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''            b04_path = None
            b08_path = None
            
            for f in files:
                if "B04" in f.name.upper():
                    b04_path = str(f)
                elif "B08" in f.name.upper():
                    b08_path = str(f)
                    
            if not b04_path or not b08_path:
                raise HTTPException(status_code=400, detail="NDVI requires Red (B04) and NIR (B08) bands. The selected raster does not contain both required bands.")
                
            b04_url = b04_path
            b08_url = b08_path'''

replacement = '''            b04_path = None
            b08_path = None
            b04_idx = 1
            b08_idx = 1
            
            for f in files:
                if "B04" in f.name.upper():
                    b04_path = str(f)
                elif "B08" in f.name.upper():
                    b08_path = str(f)
                    
            if not b04_path or not b08_path:
                if len(files) == 1:
                    import rasterio
                    with rasterio.open(str(files[0])) as test_src:
                        if test_src.count >= 4:
                            b04_path = str(files[0])
                            b08_path = str(files[0])
                            b04_idx = 3
                            b08_idx = 4
                
            if not b04_path or not b08_path:
                raise HTTPException(status_code=400, detail="NDVI requires Red (B04) and NIR (B08) bands. The selected raster does not contain both required bands.")
                
            b04_url = b04_path
            b08_url = b08_path'''

code = code.replace(target, replacement)

target2 = '''        else:
            catalog = pystac_client.Client.open('''
replacement2 = '''        else:
            b04_idx = 1
            b08_idx = 1
            catalog = pystac_client.Client.open('''
code = code.replace(target2, replacement2)

target3 = '''                with WarpedVRT(src_red, **vrt_options) as vrt_red, WarpedVRT(src_nir, **vrt_options) as vrt_nir:
                    red_data = vrt_red.read(1, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)
                    nir_data = vrt_nir.read(1, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)'''
replacement3 = '''                with WarpedVRT(src_red, **vrt_options) as vrt_red, WarpedVRT(src_nir, **vrt_options) as vrt_nir:
                    red_data = vrt_red.read(b04_idx, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)
                    nir_data = vrt_nir.read(b08_idx, out_shape=(dst_height, dst_width), resampling=Resampling.bilinear).astype(np.float32)'''
code = code.replace(target3, replacement3)

with open('backend/app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)
