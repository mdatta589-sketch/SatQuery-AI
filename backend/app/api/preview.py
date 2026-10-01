import os
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.processing.raster import create_raster_preview
from app.processing.composites import create_rgb_composite

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets Preview"])

UPLOAD_DIR = "temp/uploads"
PREVIEW_DIR = "temp/previews"

@router.get("/{dataset_id}/preview")
async def get_dataset_preview(
    dataset_id: str,
    band: str = None,
    red: str = None,
    green: str = None,
    blue: str = None,
    vmin: float = None,
    vmax: float = None
):
    dataset_dir = os.path.join(UPLOAD_DIR, dataset_id)
    if not os.path.isdir(dataset_dir):
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    
    # Helper to find a file by band ID (e.g., 'B02')
    def find_file(band_id):
        for fname in os.listdir(dataset_dir):
            if band_id.upper() in fname.upper():
                return os.path.join(dataset_dir, fname)
        return None

    if red and green and blue:
        # RGB Composite mode
        r_path = find_file(red)
        g_path = find_file(green)
        b_path = find_file(blue)
        
        if not (r_path and g_path and b_path):
            raise HTTPException(status_code=400, detail="Missing required bands for RGB composite")
            
        preview_name = f"{dataset_id}_RGB_{red}_{green}_{blue}.png"
        preview_path = os.path.join(PREVIEW_DIR, preview_name)
        
        # Only generating dynamically without caching for simplicity in dev, 
        # but we can cache it if it exists.
        if not os.path.exists(preview_path):
            create_rgb_composite(r_path, g_path, b_path, preview_path)
            
        return FileResponse(preview_path, media_type="image/png")
        
    elif band:
        # Single band mode
        src_path = find_file(band)
        if not src_path:
            raise HTTPException(status_code=404, detail=f"Band {band} not found in dataset")
            
        if vmin is not None and vmax is not None:
            preview_name = f"{dataset_id}_{band}_{vmin}_{vmax}.png"
        else:
            preview_name = f"{dataset_id}_{band}.png"
            
        preview_path = os.path.join(PREVIEW_DIR, preview_name)
        
        if not os.path.exists(preview_path) or os.path.getmtime(src_path) > os.path.getmtime(preview_path):
            create_raster_preview(src_path, preview_path, vmin=vmin, vmax=vmax)
            
        return FileResponse(preview_path, media_type="image/png")
        
    else:
        # Default: just grab the first file
        files = os.listdir(dataset_dir)
        if not files:
            raise HTTPException(status_code=404, detail="Dataset is empty")
        src_path = os.path.join(dataset_dir, files[0])
        preview_name = f"{dataset_id}_default.png"
        preview_path = os.path.join(PREVIEW_DIR, preview_name)
        if not os.path.exists(preview_path):
            create_raster_preview(src_path, preview_path)
        return FileResponse(preview_path, media_type="image/png")
