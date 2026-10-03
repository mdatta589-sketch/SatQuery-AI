from fastapi import APIRouter
from app.schemas.registry import ModelRegistryResponse
from app.services.registry_service import registry_service

router = APIRouter(prefix="/api/v1/models", tags=["Model Registry"])

@router.get("", response_model=ModelRegistryResponse)
async def get_models():
    models = registry_service.get_models()
    return {"models": models}
