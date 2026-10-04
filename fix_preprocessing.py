import re
with open('backend/app/models/vqa/preprocessing.py', 'r') as f:
    content = f.read()

new_func = '''
def prepare_image(image_id: str, image_type: str, aoi: dict | None = None) -> str:
    """
    Retrieves or generates the local RGB image file path required by the VQA model.
    """
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    temp_dir = project_root / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    out_path = temp_dir / f"vqa_{image_id}.png"
    
    if image_type == "satellite_scene":
        from app.api.catalog import _render_stac
        response = _render_stac(
            scene_id=image_id, 
            collection="sentinel-2-l2a", 
            bands_to_load=["B04", "B03", "B02"], 
            vmin=None, 
            vmax=None,
            aoi=aoi
        )
        with open(out_path, "wb") as f:
            f.write(response.body)
            
    elif image_type == "raster":
        upload_path = temp_dir / "uploads" / image_id
        if not upload_path.exists():
            upload_path = temp_dir / image_id
            if not upload_path.exists():
                raise FileNotFoundError(f"Selected image file {image_id} not found.")
        
        if aoi:
            # We must crop the uploaded GeoTIFF to the AOI, then save it as PNG!
            # Since VQA needs a PNG anyway, we can create a cropped PNG preview.
            from app.processing.raster import create_raster_preview, get_aoi_window_and_transform
            import rasterio
            from rasterio.windows import bounds as get_window_bounds
            
            with rasterio.open(upload_path) as src:
                window, window_transform = get_aoi_window_and_transform(src, aoi)
                if window is None:
                    raise ValueError("AOI is outside the raster bounds.")
                window_bounds = get_window_bounds(window, window_transform)
                
            # Modify create_raster_preview to accept window_bounds? 
            # Or just read it manually here since it's just for VQA.
            # To keep it simple, we will do a targeted read and PIL save.
            from rasterio.warp import calculate_default_transform
            from rasterio.vrt import WarpedVRT
            from PIL import Image
            import numpy as np
            
            with rasterio.open(upload_path) as src:
                transform, width, height = calculate_default_transform(
                    src.crs, 'EPSG:3857', int(window.width), int(window.height), *window_bounds
                )
                vrt_options = {'crs': 'EPSG:3857', 'transform': transform, 'width': width, 'height': height}
                
                max_dim = 1024
                scale = min(1.0, max_dim / max(width, height))
                dst_width = max(1, int(width * scale))
                dst_height = max(1, int(height * scale))
                
                with WarpedVRT(src, **vrt_options) as vrt:
                    # Read first 3 bands for RGB
                    bands_to_read = min(3, src.count)
                    arr = vrt.read(list(range(1, bands_to_read+1)), out_shape=(bands_to_read, dst_height, dst_width))
                    
                    if bands_to_read == 1:
                        # Grayscale to RGB
                        arr = np.repeat(arr, 3, axis=0)
                    
                    # Normalize
                    valid_mask = (arr[0] != vrt.nodata) if vrt.nodata is not None else np.ones((dst_height, dst_width), dtype=bool)
                    rgb = np.zeros((dst_height, dst_width, 3), dtype=np.uint8)
                    for i in range(3):
                        band = arr[i]
                        valid = band[valid_mask]
                        if len(valid) > 0:
                            p2, p98 = np.percentile(valid, [2, 98])
                            rng = p98 - p2
                            if rng == 0: rng = 1
                            norm = np.clip((band - p2) / rng * 255, 0, 255).astype(np.uint8)
                            rgb[:,:,i] = norm
                    
                    # Black out nodata
                    rgb[~valid_mask] = 0
                    
                    img = Image.fromarray(rgb, 'RGB')
                    img.save(out_path)
            return str(out_path.resolve())
        else:
            return str(upload_path.resolve())
            
    else:
        raise ValueError(f"Unsupported image_type: {image_type}")

    if not out_path.exists():
        raise RuntimeError("Failed to prepare VQA image file.")
        
    return str(out_path.resolve())
'''

content = re.sub(r'def prepare_image\(image_id: str, image_type: str\) -> str:.*?(?=return str\(out_path\.resolve\(\)\)\n)', new_func.strip() + '\n', content, flags=re.DOTALL)
with open('backend/app/models/vqa/preprocessing.py', 'w') as f:
    f.write(content)
