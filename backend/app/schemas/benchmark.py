from pydantic import BaseModel
from typing import Optional, List

class BenchmarkStatus(BaseModel):
    dataset: str
    task: str
    model: str
    metric: str
    score: Optional[float] = None
    status: str

class BenchmarkResponse(BaseModel):
    benchmarks: List[BenchmarkStatus]
