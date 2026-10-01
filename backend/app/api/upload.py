# backend/app/api/upload.py
import os
import uuid

from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.processing.raster import read_raster_metadata, create_raster_preview
from app.processing.bands import identify_band, check_compatibility
from rasterio.warp import transform_bounds

router = APIRouter(prefix="/api/v1/images", tags=["Images"])

UPLOAD_DIR = "temp/uploads"
PREVIEW_DIR = "temp/previews"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

@router.post("/upload")
async def upload_dataset(files: List[UploadFile] = File(...)):
    allowed_extensions = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}
    
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
        
    dataset_id = str(uuid.uuid4())
    dataset_dir = os.path.join(UPLOAD_DIR, dataset_id)
    os.makedirs(dataset_dir, exist_ok=True)
    
    bands = []
    metadata_list = []
    
    for file in files:
        extension = os.path.splitext(file.filename)[1].lower()
        if extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {extension} in {file.filename}")
            
        file_path = os.path.join(dataset_dir, file.filename)
        
        try:
            with open(file_path, "wb") as f:
                while chunk := await file.read(1024 * 1024):
                    f.write(chunk)
        except Exception as e:
            import logging
            logging.error(f"Error saving file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save file {file.filename}: {str(e)}")
            
        try:
            meta = read_raster_metadata(file_path)
            meta["filename"] = file.filename
            
            # WGS84 bounds
            if meta.get("crs"):
                try:
                    wgs84_bounds = transform_bounds(meta["crs"], "EPSG:4326", *meta["bounds"])
                    meta["bounds_wgs84"] = [[wgs84_bounds[1], wgs84_bounds[0]], [wgs84_bounds[3], wgs84_bounds[2]]]
                except Exception:
                    meta["bounds_wgs84"] = None
            else:
                meta["bounds_wgs84"] = None
                
            metadata_list.append(meta)
            
            band_info = identify_band(file.filename)
            band_info["filename"] = file.filename
            band_info["metadata"] = meta
            bands.append(band_info)
            
        except Exception as e:
            import logging
            logging.error(f"Error processing raster metadata for {file.filename}: {e}")
            raise HTTPException(status_code=400, detail=f"Failed to process {file.filename}: {str(e)}")
            
    try:
        check_compatibility([b["metadata"] for b in bands])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {
        "success": True,
        "dataset_id": dataset_id,
        "filename": files[0].filename,
        "metadata": bands[0]["metadata"],
        "name": files[0].filename.split('.')[0] + " (Multiband)" if bands[0]["metadata"]["bands"] > 1 else (files[0].filename.split('_')[0] + " — B04 + B08" if len(bands) >= 2 and any('B04' in b['id'] for b in bands) and any('B08' in b['id'] for b in bands) else files[0].filename),
        "bands": bands,
        "bounds": bands[0]["metadata"].get("bounds_wgs84")
    }
