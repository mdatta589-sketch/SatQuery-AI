import re

SENTINEL_2_BANDS = {
    "B01": "Coastal aerosol",
    "B02": "Blue",
    "B03": "Green",
    "B04": "Red",
    "B05": "Vegetation Red Edge",
    "B06": "Vegetation Red Edge",
    "B07": "Vegetation Red Edge",
    "B08": "NIR",
    "B8A": "Narrow NIR",
    "B09": "Water vapour",
    "B10": "SWIR - Cirrus",
    "B11": "SWIR",
    "B12": "SWIR",
}

def identify_band(filename: str) -> dict:
    """
    Attempts to identify the band from the filename.
    Returns a dict with 'id' (e.g., 'B02') and 'description' (e.g., 'Blue').
    If unknown, id is the filename without extension and description is 'Unknown band'.
    """
    match = re.search(r'(B(?:0[1-9]|1[0-2]|8A))', filename, re.IGNORECASE)
    if match:
        band_id = match.group(1).upper()
        return {
            "id": band_id,
            "description": SENTINEL_2_BANDS.get(band_id, "Unknown band")
        }
    
    # Fallback to base filename without extension
    base_name = filename.rsplit('.', 1)[0]
    return {
        "id": base_name,
        "description": "Unknown band"
    }

def check_compatibility(metadata_list: list) -> bool:
    """
    Checks if a list of raster metadata dictionaries are compatible to be grouped into a single dataset.
    Raises ValueError with a specific message if incompatible.
    """
    if not metadata_list:
        return True
        
    base = metadata_list[0]
    
    for i, meta in enumerate(metadata_list[1:], start=1):
        if meta["width"] != base["width"] or meta["height"] != base["height"]:
            raise ValueError(f"Incompatible spatial reference/grid: Dimensions differ between {base.get('filename', 'File 1')} ({base['width']}x{base['height']}) and {meta.get('filename', f'File {i+1}')} ({meta['width']}x{meta['height']})")
        
        if meta["crs"] != base["crs"]:
            raise ValueError(f"Incompatible spatial reference/grid: CRS differ between {base.get('filename', 'File 1')} ({base['crs']}) and {meta.get('filename', f'File {i+1}')} ({meta['crs']})")
            
        # Check resolution if available in the metadata
        if "resolution" in meta and "resolution" in base:
            if meta["resolution"] != base["resolution"]:
                raise ValueError(f"Incompatible spatial reference/grid: Resolutions differ.")
                
    return True
