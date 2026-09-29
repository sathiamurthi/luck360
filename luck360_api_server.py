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
    calculate_custom_tail_patterns,
    calculate_blind_patterns,
    calc_blind_tweak_patterns,
    get_comprehensive_report
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


@app.get("/daemon_status.json", summary="Raw Daemon Status JSON", tags=["Dashboard"])
@app.get("/api/v1/daemon-status", summary="Daemon Status API", tags=["Dashboard"])
async def serve_daemon_status():
    """Serves background 20-minute auto-service daemon status."""
    status_file = os.path.join(WORKSPACE_DIR, "daemon_status.json")
    if os.path.exists(status_file):
        return FileResponse(status_file, media_type="application/json")
    return JSONResponse(content={"status": "Daemon active"})


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


@app.get("/api/v1/summary_checklist", summary="Summary Checklist for Next Draw (8:00 PM)", tags=["Predictions"])
async def api_summary_checklist(
    base_tail: Optional[str] = Query(None, description="Base tail to derive from (defaults to latest draw tail 398)")
):
    """
    Summary Checklist for the upcoming 8:00 PM Dear Seagull draw.
    Calculates top target picks using identical pattern formulas (H7, H9, H11 & Star Patterns)
    that delivered straight hits today.
    """
    recs = load_draw_records()
    tail = base_tail or (recs[-1]["tail"] if recs else "398")
    d1, d2, d3 = int(tail[0]), int(tail[1]), int(tail[2])

    h7 = f"{(d2 + 1) % 10}{(d1 - d2 - 1) % 10}{(d1 + d3) % 10}"
    h9 = f"{(d3 - d1 - 1) % 10}{(d1 + d3 + 1) % 10}{(10 - d1) % 10}"
    h11 = f"{(d1 + 1) % 10}{(d1 + d3 + 1) % 10}{(d1 + d3) % 10}"
    h8 = f"{(d1 + d3 + 1) % 10}{(d1 + d3 + 1) % 10}{(d2 + 1) % 10}"
    h10 = f"{(d3 + 5) % 10}{(9 - d3) % 10}{(d3 - 1) % 10}"
    h12 = f"{(d1 + 2) % 10}{(d2 - 3) % 10}{(d3 + 5) % 10}"
    h6 = f"{(d1 - d2) % 10}{(d1 + d2 + 1) % 10}{d3}"

    # USER NEW PATTERN H13: Zero-Six Product Tens (Hits 500->053 Straight)
    map_0_6 = (d3 + 6) % 10
    prod13 = d1 * map_0_6
    d3_tens = (prod13 // 10) % 10 if prod13 >= 10 else prod13 % 10
    h13 = f"{d2}{d1}{d3_tens}"

    # USER NEW PATTERN H14: Prefix Difference Sandwich / 615 Pattern (Hits 053->615)
    h14 = f"{(d2 + 1) % 10}{(d1 + 1) % 10}{d2}"

    # USER NEW PATTERN H15: Shift-Difference Rule (Hits 398->053 Straight)
    h15 = f"{(d2 + 1) % 10}{(d3 - d1 + 10) % 10}{d1}"

    # USER NEW PATTERN H16: Twin-Echo Step Rule (Hits 615->626 Straight)
    h16 = f"{d1}{(d2 + 1) % 10}{(d3 + 1) % 10}"
    h16_pal = f"{d1}{(d1 + d3 + 1) % 10}{d1}"

    trans_map = {'0':'5', '1':'6', '2':'7', '3':'8', '4':'9', '5':'8', '6':'1', '7':'2', '8':'3', '9':'0'}
    h2 = f"{(d1 + d2) % 10}{d3}{trans_map.get(str(d2), '0')}"

    # Determine draw context dynamically
    if tail == "626" or (recs and recs[-1].get("time") == "6:00 PM"):
        title = "Summary Checklist for Tonight 8:00 PM (Dear Seagull)"
        upcoming_draw = "Nagaland State Lottery - Dear Seagull (8:00 PM)"
        derived_from = f"Today 6:00 PM Result (Tail {tail})"
        confluence_highlight = f"Front pair {h16[:2]} locked by Star H16 ({h16} & {h16_pal}), and Front-Twin 33 by Star H7 ({h7}) & H8 ({h8})"
    elif tail == "500" or (recs and recs[-1].get("time") == "8:00 PM"):
        title = "Summary Checklist for Tomorrow 1:00 PM (Dear Day)"
        upcoming_draw = "Nagaland State Lottery - Dear Day (Tomorrow 1:00 PM)"
        derived_from = f"Today 8:00 PM Result (Tail {tail})"
        confluence_highlight = f"Front pair {h9[:2]} / {h7[:2]} strongly indicated by Star Patterns H9 ({h9}) and H7 ({h7})"
    elif tail == "398":
        title = "Summary Checklist for 8:00 PM (Dear Seagull)"
        upcoming_draw = "Nagaland State Lottery - Dear Seagull (8:00 PM)"
        derived_from = f"Today 6:00 PM Result (Tail {tail})"
        confluence_highlight = "Front pair 42 is strongly reinforced by both H9 (427) and H11 (421)"
    else:
        title = f"Summary Checklist (Derived from Tail {tail})"
        upcoming_draw = "Next Scheduled Draw"
        derived_from = f"Latest Result (Tail {tail})"
        confluence_highlight = f"Primary target pairs: {h16[:2]}, {h15[:2]}, {h7[:2]}"

    return {
        "title": title,
        "upcoming_draw": upcoming_draw,
        "base_tail": tail,
        "derived_from": derived_from,
        "confluence_highlight": confluence_highlight,
        "confluence_pairs": {
            "top_ab_pairs": [h16[:2], h7[:2], "26", h15[:2], "50", h9[:2]],
            "top_bc_pairs": [h16[1:], h7[1:], h15[1:], h9[1:], h13[1:]],
            "top_ac_pairs": [f"{h16[0]}{h16[2]}", f"{h7[0]}{h7[2]}", f"{h15[0]}{h15[2]}", f"{h9[0]}{h9[2]}"]
        },
        "checklist_targets": [
            {
                "priority": "#1",
                "pattern": "★ Star H15 (Shift-Difference Rule)",
                "target": h15,
                "formula": "(d2+1, d3-d1, d1)",
                "math": f"({d2}+1={(d2+1)%10}, {d3}-{d1}={(d3-d1+10)%10}, {d1}={d1}) = {h15}",
                "pairs": {"AB": h15[:2], "BC": h15[1:], "AC": f"{h15[0]}{h15[2]}"},
                "status": "★ 100% STRAIGHT HIT on 398->053 (Overnight Cycle)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#2",
                "pattern": "★ Star H14 (Prefix Sandwich / 615)",
                "target": h14,
                "formula": "(d2+1, d1+1, d2)",
                "math": f"({d2}+1={(d2+1)%10}, {d1}+1={(d1+1)%10}, {d2}={d2}) = {h14}",
                "pairs": {"AB": h14[:2], "BC": h14[1:], "AC": f"{h14[0]}{h14[2]}"},
                "status": "★ Hits 053->615 via Prefix Difference Sandwich",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#3",
                "pattern": "★ Star H7 (Diff-Diff-Sum)",
                "target": h7,
                "formula": "(d2+1, d1-d2-1, d1+d3) % 10",
                "math": f"({d2}+1={(d2+1)%10}, {d1}-{d2}-1={(d1-d2-1)%10}, {d1}+{d3}={(d1+d3)%10})",
                "pairs": {"AB": h7[:2], "BC": h7[1:], "AC": f"{h7[0]}{h7[2]}"},
                "status": "★ 3 Straight Hits (Proved Today 226->398 Hit at 6 PM)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#2",
                "pattern": "★ Star H9 (Sub-Add-10)",
                "target": h9,
                "formula": "(d3-d1-1, d1+d3+1, 10-d1) % 10",
                "math": f"({d3}-{d1}-1={(d3-d1-1)%10}, {d1}+{d3}+1={(d1+d3+1)%10}, 10-{d1}={(10-d1)%10})",
                "pairs": {"AB": h9[:2], "BC": h9[1:], "AC": f"{h9[0]}{h9[2]}"},
                "status": "★ 3 Straight Hits (Proved Today 226->398 & 457->226)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#3",
                "pattern": "Pattern H11 (Sum-Pair-Plus)",
                "target": h11,
                "formula": "(d1+1, d1+d3+1, d1+d3) % 10",
                "math": f"({d1}+1={(d1+1)%10}, {d1}+{d3}+1={(d1+d3+1)%10}, {d1}+{d3}={(d1+d3)%10})",
                "pairs": {"AB": h11[:2], "BC": h11[1:], "AC": f"{h11[0]}{h11[2]}"},
                "status": "Direct Pair Sum (Proved Today 226->398 at 6 PM)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#4",
                "pattern": "★ Star H8 (Outer-Sum Step)",
                "target": h8,
                "formula": "(d1+d3+1, d1+d3+1, d2+1) % 10",
                "math": f"({d1}+{d3}+1={(d1+d3+1)%10}, {d1}+{d3}+1={(d1+d3+1)%10}, {d2}+1={(d2+1)%10})",
                "pairs": {"AB": h8[:2], "BC": h8[1:], "AC": f"{h8[0]}{h8[2]}"},
                "status": "★ 3 Straight Hits (Proved Today 051->226 at 3 PM)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#5",
                "pattern": "★ Star H10 (Partner-Mirror)",
                "target": h10,
                "formula": "(d3+5, 9-d3, d3-1) % 10",
                "math": f"({d3}+5={(d3+5)%10}, 9-{d3}={(9-d3)%10}, {d3}-1={(d3-1)%10})",
                "pairs": {"AB": h10[:2], "BC": h10[1:], "AC": f"{h10[0]}{h10[2]}"},
                "status": "★ 3 Straight Hits (140->599 & 457->226)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#6",
                "pattern": "★ Star H12 (Mirror Step)",
                "target": h12,
                "formula": "(d1+2, d2-3, d3+5) % 10",
                "math": f"({d1}+2={(d1+2)%10}, {d2}-3={(d2-3)%10}, {d3}+5={(d3+5)%10})",
                "pairs": {"AB": h12[:2], "BC": h12[1:], "AC": f"{h12[0]}{h12[2]}"},
                "status": "★ 3 Total Hits (Proved Today 051->226 at 3 PM)",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#7",
                "pattern": "★ Star H6 (Diff-Sum Plus One)",
                "target": h6,
                "formula": "(d1-d2, d1+d2+1, d3) % 10",
                "math": f"({d1}-{d2}={(d1-d2)%10}, {d1}+{d2}+1={(d1+d2+1)%10}, {d3}={d3})",
                "pairs": {"AB": h6[:2], "BC": h6[1:], "AC": f"{h6[0]}{h6[2]}"},
                "status": "★ Proved on Today 221->051 Hit at 1 PM",
                "recommended_play": "Straight & Box"
            },
            {
                "priority": "#8",
                "pattern": "★ Star H2 (Cross-Swap 5-8)",
                "target": h2,
                "formula": "(d1+d2, d3, trans(d2)) % 10",
                "math": f"({d1}+{d2}={(d1+d2)%10}, {d3}={d3}, trans({d2})={trans_map.get(str(d2),'0')})",
                "pairs": {"AB": h2[:2], "BC": h2[1:], "AC": f"{h2[0]}{h2[2]}"},
                "status": "Proved on 457->978 Straight Hit",
                "recommended_play": "Straight"
            }
        ]
    }


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


@app.get("/api/v1/patterns/blind", summary="Blind & Simple Tweak Cross-Draw Patterns", tags=["Predictions"])
async def api_blind_patterns(
    seed_tail: Optional[str] = Query(None, description="Seed tail to derive from (defaults to 1:00 PM draw tail or latest)")
):
    """
    Computes Blind & Simple Tweak Cross-Draw patterns.
    Captures cross-slot leaps (Nagaland 1 PM -> Nagaland 8 PM), such as:
    - 051 (1 PM) -> 500 (8 PM) [Proved Straight Hit via Rev-AB Tweak -1 on Sep 25]
    - 563 (1 PM) -> 221 (8 PM) [Proved Straight Hit via Diff-Step on Sep 24]
    Includes frequency forecast and expected occurrence windows.
    """
    return calculate_blind_patterns(seed_tail=seed_tail)


@app.get("/api/v1/report/comprehensive", summary="Comprehensive Daily & Multi-Dimension Analytics Report", tags=["Reports"])
async def api_comprehensive_report():
    """
    Comprehensive Daily & Multi-Dimension Pattern Analytics Report:
    - Current Day Pattern Breakdown (Every result today with exact derived previous base & formula proof)
    - Pattern Re-Appearing Trend & Recurrence Matrix
    - Multi-Dimension Analysis: Sequential Flow, Day-to-Day Same-Slot, and Lottery/Agent-wise patterns
    - Executive Next Draw Projections: Expected HOT 5, Hot AB/BC/AC Pairs, and All Single Digit Hot Meter (0-9)
    - Enriched Draw History with attached pattern derivations and proofs
    """
    return get_comprehensive_report()


@app.get("/api/v1/audit", summary="Audit Trail Report", tags=["Audit"])
async def api_audit_report():
    """Full transparency audit of verified historical pattern hits with mathematical proofs."""
    return get_audit_report()


@app.get("/api/v1/fetch-live", summary="Trigger Live Results Scraping (GET)", tags=["System"])
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
