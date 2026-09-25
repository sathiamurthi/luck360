#!/usr/bin/env python3
"""
Luck360 Dual FastMCP & REST API Server
Production Domain: luck360.demandgeniusai.com
Default Port: 8001

Combines:
1. FastMCP Model Context Protocol SSE Engine (/sse, /messages) for AI clients
2. Full FastAPI REST API (/api/v1/..., /docs, /openapi.json)
3. Live Web App Dashboard (/ serving index.html)
"""

import os
import sys
import json
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, Response, Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import FastMCP instance and tools from luck360_mcp_server
from luck360_mcp_server import (
    mcp,
    WORKSPACE_DIR,
    JSON_FILE,
    FREQ_FILE,
    DB_FILE,
    load_draw_records,
    get_draw_records,
    add_draw_record,
    analyze_pattern_matches,
    arrest_patterns,
    predict_next_days,
    get_pattern_frequencies,
    get_audit_report,
    fetch_latest_live_results,
    calculate_custom_tail_patterns
)

# FastAPI App Definition
app = FastAPI(
    title="Luck360 Lottery Pattern Predictor & Analytics Engine",
    description="Unified API & Model Context Protocol (MCP) service for state lottery draw tracking, 12-pattern mathematical backtesting, constrained target arrest, and 3-day predictive projections.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enable CORS for external AI agents, web builders, Lovable.dev, etc.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount MCP SSE routes for remote MCP clients (Cursor, Claude Desktop, Antigravity, Windsurf)
mcp_sse_app = mcp.sse_app()
for route in mcp_sse_app.routes:
    app.routes.append(route)


# Request Models
class NewDrawRequest(BaseModel):
    date: str = Field(..., example="2026-09-25", description="Draw date YYYY-MM-DD")
    time: str = Field(..., example="3:00 PM", description="Draw slot time")
    company: str = Field(..., example="Kerala State Lotteries", description="State company name")
    lottery: str = Field(..., example="Nirmal NR-412", description="Lottery scheme name")
    ticket: str = Field(..., example="PU 614457", description="Full winning ticket number")


# -------------------------------------------------------------
# Web Dashboard & Static Asset Endpoints
# -------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, summary="Luck360 Web Dashboard", tags=["Dashboard"])
async def serve_dashboard():
    """Serves the live interactive Luck360 Analytics & Prediction Dashboard."""
    index_file = os.path.join(WORKSPACE_DIR, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Luck360 API & MCP Server Online</h1><p>Visit <a href='/docs'>/docs</a> or <a href='/sse'>/sse</a></p>")


@app.get("/draw_history.json", summary="Raw Draw History JSON", tags=["Dashboard"])
async def serve_draw_history():
    """Serves the current draw history JSON for dashboard data binding."""
    if os.path.exists(JSON_FILE):
        return FileResponse(JSON_FILE, media_type="application/json")
    return JSONResponse(content=load_draw_records())


@app.get("/pattern_frequency.json", summary="Raw Pattern Frequency JSON", tags=["Dashboard"])
async def serve_pattern_frequency():
    """Serves current pattern frequency statistics for the dashboard."""
    if os.path.exists(FREQ_FILE):
        return FileResponse(FREQ_FILE, media_type="application/json")
    return JSONResponse(content=get_pattern_frequencies())


@app.get("/kerala.jpeg", summary="Kerala Lottery Header Image", tags=["Dashboard"])
async def serve_kerala_image():
    """Serves the hero image asset."""
    img_path = os.path.join(WORKSPACE_DIR, "kerala.jpeg")
    if os.path.exists(img_path):
        return FileResponse(img_path, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Image not found")


# -------------------------------------------------------------
# System & Health
# -------------------------------------------------------------

@app.get("/health", summary="Health Check", tags=["System"])
@app.get("/api/v1/health", summary="API Health Check", tags=["System"])
async def health_check():
    """System health check and MCP configuration details."""
    recs = load_draw_records()
    return {
        "status": "online",
        "service": "Luck360 Lottery Pattern Predictor & Analytics Engine",
        "domain": "luck360.demandgeniusai.com",
        "mcp_sse_endpoint": "/sse",
        "mcp_messages_endpoint": "/messages",
        "openapi_url": "/openapi.json",
        "docs_url": "/docs",
        "total_records": len(recs),
        "latest_draw": recs[-1] if recs else None
    }


# -------------------------------------------------------------
# REST API Endpoints (v1)
# -------------------------------------------------------------

@app.get("/api/v1/draws", summary="Get Draw Records", tags=["Draws"])
async def api_get_draws(
    limit: int = Query(50, ge=1, le=500, description="Max number of draw records to return"),
    include_patterns: bool = Query(True, description="Whether to include computed 12-pattern values")
):
    """Retrieve historical draw records with optional pattern calculations."""
    return get_draw_records(limit=limit, include_patterns=include_patterns)


@app.post("/api/v1/draws", summary="Add Draw Record", tags=["Draws"])
async def api_add_draw(req: NewDrawRequest):
    """Record a new official draw outcome and recalculate statistics."""
    res = add_draw_record(
        date=req.date,
        time=req.time,
        company=req.company,
        lottery=req.lottery,
        ticket=req.ticket
    )
    return res


@app.get("/api/v1/patterns/matches", summary="Analyze Pattern Matches (Backtesting)", tags=["Analytics"])
async def api_pattern_matches():
    """Backtest all sequential draw transitions against the 12 pattern formulas."""
    return analyze_pattern_matches()


@app.get("/api/v1/patterns/arrest", summary="Arrest Top Target Patterns", tags=["Predictions"])
async def api_arrest_patterns():
    """Execute constrained target filter on the latest draw to isolate high-confidence next-draw plays."""
    return arrest_patterns()


@app.get("/api/v1/patterns/predict", summary="3-Day Predictions Matrix", tags=["Predictions"])
async def api_predict_next_days(
    starting_tail: Optional[str] = Query(None, description="Starting 3-digit tail (defaults to latest draw tail)")
):
    """Generate multi-draw projection matrix across upcoming draw slots."""
    return predict_next_days(starting_tail=starting_tail)


@app.get("/api/v1/patterns/frequencies", summary="Pattern Frequency & Age Statistics", tags=["Analytics"])
async def api_pattern_frequencies():
    """Retrieve pattern hit rates, straight vs box breakdown, and gap age."""
    return get_pattern_frequencies()


@app.get("/api/v1/patterns/calculate/{tail}", summary="Calculate Custom Tail Patterns", tags=["Analytics"])
async def api_calculate_custom(
    tail: str,
    ticket: str = Query("", description="Optional full ticket number for outer digit rules")
):
    """Compute all 12 mathematical transformation patterns for any custom 3-digit number."""
    return calculate_custom_tail_patterns(tail=tail, ticket_str=ticket)


@app.get("/api/v1/audit", summary="Audit Trail Report", tags=["Audit"])
async def api_audit_report():
    """Full transparency audit of verified historical pattern hits with mathematical proofs."""
    return get_audit_report()


@app.post("/api/v1/fetch-live", summary="Trigger Live Results Scraping", tags=["System"])
async def api_trigger_fetch():
    """Trigger background scraper to fetch latest draw results from official portals."""
    return fetch_latest_live_results()


# -------------------------------------------------------------
# Main Runner
# -------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    print("=" * 65)
    print("  Luck360 Dual FastMCP & REST API Engine")
    print(f"  Production Domain: https://luck360.demandgeniusai.com")
    print(f"  Local Port:        http://127.0.0.1:{port}")
    print(f"  MCP SSE Endpoint:  http://127.0.0.1:{port}/sse")
    print(f"  Swagger Docs:      http://127.0.0.1:{port}/docs")
    print("=" * 65)
    uvicorn.run("luck360_api_server:app", host="0.0.0.0", port=port, reload=False)
