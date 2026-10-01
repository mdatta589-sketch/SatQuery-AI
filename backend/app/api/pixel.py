import os
from fastapi import APIRouter, HTTPException, Query
import rasterio
from rasterio.warp import transform
from rasterio.windows import Window
from app.processing.bands import identify_band

router = APIRouter(prefix="/api/v1/datasets", tags=["Datasets Pixel"])

UPLOAD_DIR = "temp/uploads"

@router.get("/{dataset_id}/pixel")
async def get_dataset_pixel(dataset_id: str, lat: float = Query(...), lon: float = Query(...)):
    dataset_dir = os.path.join(UPLOAD_DIR, dataset_id)
    if not os.path.isdir(dataset_dir):
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    files = os.listdir(dataset_dir)
    if not files:
        raise HTTPException(status_code=404, detail="Dataset is empty")
        
    # We assume all files in the dataset share the same grid (as verified by check_compatibility)
    base_file = os.path.join(dataset_dir, files[0])
    
    try:
        with rasterio.open(base_file) as src:
            if not src.crs:
                raise HTTPException(status_code=400, detail="Image has no CRS defined.")
            
            try:
                xs, ys = transform("EPSG:4326", src.crs, [lon], [lat])
                x, y = xs[0], ys[0]
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"CRS transform failed: {str(e)}")
            
            try:
                row, col = src.index(x, y)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Index computation failed: {str(e)}")
            
            if not (0 <= row < src.height and 0 <= col < src.width):
                return {
                    "status": "outside",
                    "latitude": lat,
                    "longitude": lon,
                    "message": "Outside raster extent"
                }
                
            base_dtype = str(src.dtypes[0])
            res_x, res_y = src.res[0], src.res[1]

        # Read the pixel value for all bands
        values = []
        window = Window(col, row, 1, 1)
        
        for fname in files:
            file_path = os.path.join(dataset_dir, fname)
            band_info = identify_band(fname)
            
            try:
                with rasterio.open(file_path) as src:
                    data = src.read(1, window=window)
                    val = data[0, 0]
                    try:
                        val = val.item()
                    except AttributeError:
                        pass
                    
                    values.append({
                        "filename": fname,
                        "band": band_info["id"],
                        "description": band_info["description"],
                        "value": val
                    })
            except Exception as e:
                values.append({
                    "filename": fname,
                    "band": band_info["id"],
                    "description": band_info["description"],
                    "error": str(e)
                })

        return {
            "status": "success",
            "latitude": lat,
            "longitude": lon,
            "row": int(row),
            "column": int(col),
            "values": values,
            "dtype": base_dtype,
            "resolution_x": res_x,
            "resolution_y": res_y
        }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
