from pydantic import BaseModel
from typing import Optional


class ImageMetadata(BaseModel):
    image_id: str
    filename: str
    format: str
    width: int
    height: int
    bands: int
    crs: Optional[str] = None
    dtype: Optional[str] = None
    modality: Optional[str] = None
