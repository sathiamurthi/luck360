@echo off
echo ========================================================
echo   Starting Luck360 Dual FastMCP & REST API Engine
echo   Permanent Domain: https://luck360.demandgeniusai.com
echo ========================================================

cd /d "c:\Users\DemandGeniusAI\lottery"

:: Reload Caddy reverse proxy to ensure luck360 host routing is active
"c:\Users\DemandGeniusAI\mcp\caddy\caddy.exe" reload --config "c:\Users\DemandGeniusAI\mcp\Caddyfile" >nul 2>&1

:: Start Python FastAPI & FastMCP Backend on Port 8001
echo Starting Luck360 API & MCP Server on Port 8001...
start "Luck360 API & MCP (Port 8001)" cmd /k ""C:\Program Files\Python311\python.exe" "c:\Users\DemandGeniusAI\lottery\luck360_api_server.py""

echo.
echo All services launched!
echo Access Luck360 permanently at:
echo   - Web Dashboard: https://luck360.demandgeniusai.com
echo   - Swagger Docs:  https://luck360.demandgeniusai.com/docs
echo   - MCP SSE:       https://luck360.demandgeniusai.com/sse
echo   - OpenAPI JSON:  https://luck360.demandgeniusai.com/openapi.json
echo   - Local Direct:  http://127.0.0.1:8001
echo.
pause
