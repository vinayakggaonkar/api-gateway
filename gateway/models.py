# models.py - Defines the shape of data coming in and going out of our gateway
from pydantic import BaseModel
from typing import Optional

class GatewayRequest(BaseModel):
    query: str
    user_id: Optional[int] = None

class GatewayResponse(BaseModel):
    intent: str
    service: str
    response: str
    latency_ms: float
    cached: bool = False

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    status_code: int

class RouteDecision(BaseModel):
    intent: str
    confidence: float
    target_url: str
    service_name: str
    service_id: Optional[int] = None
    