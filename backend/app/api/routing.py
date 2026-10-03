from fastapi import APIRouter
from app.schemas.query import RouterRequest, RouterResponse
from app.services.query_router import query_router

router = APIRouter(prefix="/api/v1/query", tags=["Query"])

@router.post("/route", response_model=RouterResponse)
async def route_query(request: RouterRequest):
    result = query_router.route(request.question)
    return RouterResponse(**result)
