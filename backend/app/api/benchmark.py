from fastapi import APIRouter
from app.schemas.benchmark import BenchmarkResponse
from app.services.benchmark_service import benchmark_service

router = APIRouter(prefix="/api/v1/benchmark", tags=["Benchmark"])

@router.get("/status", response_model=BenchmarkResponse)
async def get_benchmark_status():
    status = benchmark_service.get_status()
    return {"benchmarks": status}
