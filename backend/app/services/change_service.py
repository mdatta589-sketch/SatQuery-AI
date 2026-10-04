import time
from pathlib import Path
import rasterio
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ChangeService:
    def _get_image_path(self, image_id: str) -> Path | None:
        project_root = Path(__file__).resolve().parent.parent.parent
        temp_dir = project_root / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Check uploads first
        upload_path = temp_dir / "uploads" / image_id
        if upload_path.exists():
            if upload_path.is_dir():
                tif_files = list(upload_path.glob("*.tif"))
                if tif_files:
                    b04 = next((f for f in tif_files if "B04" in f.name), None)
                    return b04 if b04 else tif_files[0]
            return upload_path
            
        # Check just temp
        temp_path = temp_dir / image_id
        if temp_path.exists():
            return temp_path
            
        # Check if already downloaded STAC scene
        stac_tif = temp_dir / f"{image_id}.tif"
        if stac_tif.exists() and stac_tif.stat().st_size > 1024:
            return stac_tif
            
        # If it looks like a Sentinel-2 STAC ID, resolve and download
        if image_id.startswith(("S2A_", "S2B_", "S2C_")):
            try:
                import pystac_client
                import planetary_computer
                import urllib.request
                import shutil
                
                logger.info(f"Resolving STAC scene: {image_id}")
                catalog = pystac_client.Client.open(
                    "https://planetarycomputer.microsoft.com/api/stac/v1",
                    modifier=planetary_computer.sign_inplace
                )
                search = catalog.search(collections=["sentinel-2-l2a"], ids=[image_id])
                item = next(search.items(), None)
                if item:
                    visual_url = item.assets["visual"].href
                    logger.info(f"Downloading STAC visual asset for {image_id}")
                    
                    req = urllib.request.Request(visual_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response, open(stac_tif, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                    
                    return stac_tif
            except Exception as e:
                logger.error(f"Failed to fetch STAC image {image_id}: {e}")
                
        return None

    def _unavailable_response(self, status: str, before_id: str, after_id: str, msg: str) -> dict:
        return {
            "status": status,
            "method": "baseline_raster_difference",
            "image_before_id": before_id,
            "image_after_id": after_id,
            "changed_pixel_count": None,
            "total_valid_pixel_count": None,
            "change_percentage": None,
            "threshold": None,
            "message": msg,
            "error": msg,
            "execution_time_ms": None
        }

    def analyze_change(self, image_before_id: str, image_after_id: str, aoi: dict | None = None) -> dict:
        start_time = time.time()
        
        before_path = self._get_image_path(image_before_id)
        after_path = self._get_image_path(image_after_id)
        
        if not before_path or not before_path.exists():
            return self._unavailable_response("invalid_input", image_before_id, image_after_id, f"Image before not found: {image_before_id}")
        if not after_path or not after_path.exists():
            return self._unavailable_response("invalid_input", image_before_id, image_after_id, f"Image after not found: {image_after_id}")
            
        try:
            with rasterio.open(before_path) as src_b, rasterio.open(after_path) as src_a:
                if src_b.shape != src_a.shape:
                    return self._unavailable_response("invalid_input", image_before_id, image_after_id, f"Dimension mismatch: {src_b.shape} vs {src_a.shape}")
                
                if src_b.crs != src_a.crs:
                    return self._unavailable_response("invalid_input", image_before_id, image_after_id, f"CRS mismatch: {src_b.crs} vs {src_a.crs}")
                
                bands_to_read = min(src_b.count, src_a.count, 3)
                if bands_to_read == 0:
                    return self._unavailable_response("invalid_input", image_before_id, image_after_id, "No valid bands found in images.")
                
                from rasterio.enums import Resampling
                from rasterio.windows import from_bounds, Window
                from rasterio.warp import transform_bounds
                
                bbox = aoi.get('bbox', aoi) if isinstance(aoi, dict) else (aoi or {})
                if bbox and "west" in bbox:
                    left, bottom, right, top = bbox["west"], bbox["south"], bbox["east"], bbox["north"]
                    src_left, src_bottom, src_right, src_top = transform_bounds("EPSG:4326", src_b.crs, left, bottom, right, top)
                    
                    window = from_bounds(src_left, src_bottom, src_right, src_top, transform=src_b.transform)
                    window = window.intersection(Window(0, 0, src_b.width, src_b.height))
                    
                    # Convert window attributes to floats, then to ints to avoid math.ceil issues
                    w_w, w_h = float(window.width), float(window.height)
                    # For out dimensions, we can't be negative.
                    out_w, out_h = max(1, int(w_w)), max(1, int(w_h))
                    
                    max_dim = 1024
                    if out_w > max_dim or out_h > max_dim:
                        scale = min(1.0, max_dim / max(out_w, out_h))
                        out_w = max(1, int(out_w * scale))
                        out_h = max(1, int(out_h * scale))
                        
                    b_data = src_b.read(list(range(1, bands_to_read + 1)), window=window, out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    a_data = src_a.read(list(range(1, bands_to_read + 1)), window=window, out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    
                    from rasterio.windows import transform as win_get_transform, bounds as win_get_bounds
                    win_transform = win_get_transform(window, src_b.transform)
                    
                    analysis_transform = win_transform
                    if out_w != int(w_w) or out_h != int(w_h):
                        analysis_transform = win_transform * win_transform.scale(
                            (w_w / out_w),
                            (w_h / out_h)
                        )
                        
                    analysis_bounds = win_get_bounds(window, src_b.transform)
                else:
                    max_dim = 1024
                    scale = min(1.0, max_dim / max(src_b.width, src_b.height))
                    out_w = max(1, int(src_b.width * scale))
                    out_h = max(1, int(src_b.height * scale))
                    
                    b_data = src_b.read(list(range(1, bands_to_read + 1)), out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    a_data = src_a.read(list(range(1, bands_to_read + 1)), out_shape=(bands_to_read, out_h, out_w), resampling=Resampling.bilinear)
                    
                    analysis_transform = src_b.transform * src_b.transform.scale(
                        (src_b.width / out_w),
                        (src_b.height / out_h)
                    )
                    analysis_bounds = src_b.bounds
                
                b_valid = (b_data != src_b.nodata) if src_b.nodata is not None else np.ones_like(b_data, dtype=bool)
                a_valid = (a_data != src_a.nodata) if src_a.nodata is not None else np.ones_like(a_data, dtype=bool)
                
                valid_mask = b_valid & a_valid
                valid_mask_2d = np.all(valid_mask, axis=0)
                
                total_valid = int(np.sum(valid_mask_2d))
                
                if total_valid == 0:
                    return self._unavailable_response("invalid_input", image_before_id, image_after_id, "No overlapping valid pixels found.")
                
                b_float = b_data.astype(np.float32)
                a_float = a_data.astype(np.float32)
                
                diff = np.abs(b_float - a_float)
                denom = np.maximum(np.abs(b_float) + np.abs(a_float), 1e-6)
                relative_diff = diff / denom
                
                mean_rel_diff = np.mean(relative_diff, axis=0)
                threshold = 0.25
                
                valid = valid_mask_2d & np.all(np.isfinite(b_float) & np.isfinite(a_float), axis=0)
                total_valid = int(np.sum(valid))
                
                changed_mask = valid & (mean_rel_diff > threshold)
                changed_pixels = int(np.sum(changed_mask))
                
                change_pct = (changed_pixels / total_valid) * 100.0 if total_valid > 0 else 0.0
                
                # --- VISUALIZATION: Generate Base64 PNG for Leaflet ---
                evidence = []
                try:
                    import io
                    import base64
                    from PIL import Image
                    from rasterio.warp import reproject, Resampling as WarpResampling, calculate_default_transform, transform_bounds
                    
                    # Compute Web Mercator bounds and transform from the downsampled dimension
                    transform, width, height = calculate_default_transform(
                        src_b.crs, 'EPSG:3857', out_w, out_h, *analysis_bounds
                    )
                    
                    src_mask_uint8 = changed_mask.astype(np.uint8) * 255
                    dst_mask = np.zeros((height, width), dtype=np.uint8)
                    
                    reproject(
                        source=src_mask_uint8,
                        destination=dst_mask,
                        src_transform=analysis_transform,
                        src_crs=src_b.crs,
                        dst_transform=transform,
                        dst_crs='EPSG:3857',
                        resampling=WarpResampling.nearest
                    )
                    
                    rgba = np.zeros((height, width, 4), dtype=np.uint8)
                    rgba[dst_mask == 255] = [255, 40, 40, 200]
                    
                    img = Image.fromarray(rgba, 'RGBA')
                    buf = io.BytesIO()
                    img.save(buf, format='PNG')
                    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
                    
                    left, bottom, right, top = rasterio.transform.array_bounds(height, width, transform)
                    west, south, east, north = transform_bounds('EPSG:3857', 'EPSG:4326', left, bottom, right, top)
                    
                    evidence.append({
                        "type": "image_overlay",
                        "data": f"data:image/png;base64,{b64_str}",
                        "bounds": [[south, west], [north, east]]
                    })
                except Exception as ex:
                    logger.warning(f"Failed to generate visual overlay: {ex}")
                
                exec_time = int((time.time() - start_time) * 1000)
                
                return {
                    "status": "success",
                    "method": "baseline_raster_difference",
                    "image_before_id": image_before_id,
                    "image_after_id": image_after_id,
                    "changed_pixel_count": changed_pixels,
                    "total_valid_pixel_count": total_valid,
                    "change_percentage": round(change_pct, 2),
                    "threshold": threshold,
                    "message": "Computed absolute difference using prototype threshold.",
                    "evidence": evidence,
                    "execution_time_ms": exec_time
                }
                
        except Exception as e:
            logger.exception("Change analysis failed")
            return self._unavailable_response("error", image_before_id, image_after_id, f"Processing failed: {str(e)}")

    def answer_change_vqa(self, image_before_id: str, image_after_id: str, question: str, aoi: dict | None = None) -> dict:
        import time
        start_time = time.time()
        
        # 1. Run change analysis
        analysis_result = self.analyze_change(image_before_id, image_after_id, aoi)
        
        if analysis_result.get("status") != "success":
            return {
                "task": "change_vqa",
                "status": "error",
                "question": question,
                "error": analysis_result.get("error", "Change Analysis failed before VQA could be answered."),
                "execution": {
                    "task": "change_vqa",
                    "model": "change_interpreter",
                    "provider": "local",
                    "status": "error"
                }
            }
            
        # 2. Extract statistics
        change_pct = analysis_result.get("change_percentage", 0.0)
        changed_pixels = analysis_result.get("changed_pixel_count", 0)
        valid_pixels = analysis_result.get("total_valid_pixel_count", 0)
        method = analysis_result.get("method", "Baseline Raster Difference")
        threshold = analysis_result.get("threshold", 0.25)
        
        # Format dates from IDs (e.g. S2B_MSIL2A_20250328T050659_...)
        def extract_date(scene_id):
            parts = scene_id.split('_')
            for part in parts:
                if len(part) >= 8 and part[:8].isdigit() and (len(part) == 8 or part[8] == 'T'):
                    return f"{part[:4]}-{part[4:6]}-{part[6:8]}"
            return scene_id
            
        before_date = extract_date(image_before_id)
        after_date = extract_date(image_after_id)
        
        # 3. Generate natural language answer
        # Very simple intent handling
        q_lower = question.lower()
        if "how much" in q_lower or "percentage" in q_lower or "area" in q_lower:
            answer = f"Approximately {change_pct:.2f}% of the valid area was classified as changed between {before_date} and {after_date}."
        elif "where" in q_lower or "location" in q_lower:
            answer = f"The detected changes are highlighted in red on the map within the selected Area of Interest. A total of {changed_pixels:,} pixels changed."
        elif "significant" in q_lower:
            if change_pct > 5.0:
                answer = f"Yes, there is significant change. Approximately {change_pct:.2f}% of the area changed."
            elif change_pct > 1.0:
                answer = f"There is moderate change. Approximately {change_pct:.2f}% of the area changed."
            else:
                answer = f"There is no significant change. Only {change_pct:.2f}% of the area changed."
        else:
            answer = f"The selected AOI shows detectable change between {before_date} and {after_date}. Approximately {change_pct:.2f}% of the valid area was classified as changed using the {method.replace('_', ' ')} method."
            
        exec_time = int((time.time() - start_time) * 1000)
        
        return {
            "task": "change_vqa",
            "status": "success",
            "question": question,
            "answer": answer,
            "change_percentage": change_pct,
            "changed_pixel_count": changed_pixels,
            "total_valid_pixel_count": valid_pixels,
            "threshold": threshold,
            "method": method,
            "before_scene": f"Sentinel-2 — {before_date}",
            "after_scene": f"Sentinel-2 — {after_date}",
            "evidence": analysis_result.get("evidence", []),
            "execution_time_ms": exec_time,
            "execution": {
                "task": "change_vqa",
                "model": "change_interpreter",
                "provider": "local",
                "status": "success"
            }
        }

change_service = ChangeService()
