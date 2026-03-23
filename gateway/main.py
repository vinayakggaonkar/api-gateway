# main.py - the heart of our API gateway, ties everything together

import time
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from gateway.auth import verify_api_key
from gateway.cache import InMemoryCache
from gateway.rate_limiter import InMemoryRateLimiter
from gateway.models import GatewayRequest, GatewayResponse
from gateway.router import mcp_router

# our FastAPI app and set up our tools:
app = FastAPI(
    title="AI-Powered API Gateway",
    description="HTTP API Gateway with MCP-based intelligent routhing",
    version="1.0.0",
)

rate_limiter = InMemoryRateLimiter()
cache = InMemoryCache()

# now our Middleware:
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response

# out first route
@app.get("/")
def root():
    return {
        "service": "AI-Powered API Gateway",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }

# our health check route:
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "redis": "unavailable",
        "mysql": "unavailable",
    }

# our main gateway route:
@app.post("/gateway/query", response_model=GatewayResponse)
def gateway_query(
    body: GatewayRequest,
    request: Request,
    user: dict = Depends(verify_api_key),
):
    start_time = time.perf_counter()
    api_key = request.headers.get("X-API-Key", "")

    # now the rate limiting check inside the function
    allowed, count, remaining = rate_limiter.is_allowed(api_key)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. {count}/100 requests used",
        )
    cached = cache.get(body.query)
    if cached:
        latency_ms = (time.perf_counter() - start_time) * 1000
        return GatewayResponse(
            intent=cached["intent"],
            service=cached["service"],
            response=cached["response"],
            latency_ms=round(latency_ms, 2),
            cached=True,
        )
    route_decision = mcp_router.route(body.query)
    service_response = mcp_router.get_mock_response(route_decision.intent, body.query)
    cache_payload = {
        "intent": route_decision.intent,
        "service": route_decision.service_name,
        "response": service_response,
    }
    cache.set(body.query, cache_payload)
    latency_ms = (time.perf_counter() - start_time) * 1000
    return GatewayResponse(
        intent=route_decision.intent,
        service=route_decision.service_name,
        response=service_response,
        latency_ms=round(latency_ms, 2),
        cached=False,
    )