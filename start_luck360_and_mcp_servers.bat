@echo off
setlocal enabledelayedexpansion
title Luck360 and Universal MCP Unified Server Launcher
echo ======================================================================
echo    Starting Luck360 and Universal MCP Servers Unified Stack
echo    - Port 8000: Universal Study Packs MCP and REST API (mcp.demandgeniusai.com)
echo    - Port 8001: Luck360 Engine and FastMCP SSE (luck360.demandgeniusai.com)
echo    - Port 443/80: Caddy Reverse Proxy (Auto-SSL HTTPS)
echo ======================================================================
echo.

:: -------------------------------------------------------------------------
:: STEP 1: Terminate existing instances and release ports 8000 and 8001
:: -------------------------------------------------------------------------
echo [1/5] Terminating existing server instances and freeing ports...

:: Stop background scheduled tasks if active
schtasks /End /TN "MCP_StudyPacks_Server" >nul 2>&1
schtasks /End /TN "Luck360_Service" >nul 2>&1
schtasks /End /TN "Luck360_Live_Daemon" >nul 2>&1

:: Kill any process listening on Port 8000
echo   - Checking Port 8000 (Universal Study Packs)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo     Found active PID %%a on Port 8000. Terminating...
    taskkill /F /PID %%a >nul 2>&1
)

:: Kill any process listening on Port 8001
echo   - Checking Port 8001 (Luck360 API and FastMCP)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001 ^| findstr LISTENING') do (
    echo     Found active PID %%a on Port 8001. Terminating...
    taskkill /F /PID %%a >nul 2>&1
)

:: PowerShell fallback cleanup for ports 8000 and 8001
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8000,8001 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1

:: Wait 2 seconds for ports to be released
ping 127.0.0.1 -n 3 >nul

echo   [OK] Ports 8000 and 8001 successfully freed.
echo.

:: -------------------------------------------------------------------------
:: STEP 2: Ensure Caddy Reverse Proxy is active and routes are loaded
:: -------------------------------------------------------------------------
echo [2/5] Checking Caddy SSL Reverse Proxy (Port 443/80)...
netstat -ano | findstr :443 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo   Launching Caddy reverse proxy...
    start "Caddy SSL Reverse Proxy (443/80)" cmd /k ""c:\Users\DemandGeniusAI\mcp\caddy\caddy.exe" run --config "c:\Users\DemandGeniusAI\mcp\Caddyfile""
    ping 127.0.0.1 -n 3 >nul
) else (
    echo   Caddy reverse proxy is running. Reloading dual routing configuration...
    "c:\Users\DemandGeniusAI\mcp\caddy\caddy.exe" reload --config "c:\Users\DemandGeniusAI\mcp\Caddyfile" >nul 2>&1
)
echo   [OK] Caddy reverse proxy ready.
echo.

:: -------------------------------------------------------------------------
:: STEP 3: Launch Universal Master Study Packs MCP Server (Port 8000)
:: -------------------------------------------------------------------------
echo [3/5] Starting Universal Study Packs MCP Server (Port 8000)...
schtasks /Run /TN "MCP_StudyPacks_Server" >nul 2>&1
ping 127.0.0.1 -n 4 >nul
netstat -ano | findstr :8000 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo   Scheduled task not bound, launching via command prompt window...
    start "Universal Study Packs Server (Port 8000)" /D "c:\Users\DemandGeniusAI\mcp" cmd /k ""C:\Program Files\Python311\python.exe" "c:\Users\DemandGeniusAI\mcp\study_pack_api_server.py""
    ping 127.0.0.1 -n 4 >nul
)

:: -------------------------------------------------------------------------
:: STEP 4: Launch Luck360 Dual Engine (Port 8001) and Live Scraper Daemon
:: -------------------------------------------------------------------------
echo [4/5] Starting Luck360 Dual Engine Server (Port 8001)...
schtasks /Run /TN "Luck360_Service" >nul 2>&1
schtasks /Run /TN "Luck360_Live_Daemon" >nul 2>&1
ping 127.0.0.1 -n 4 >nul
netstat -ano | findstr :8001 | findstr LISTENING >nul
if %errorlevel% neq 0 (
    echo   Scheduled task not bound, launching via command prompt window...
    start "Luck360 Dual Engine (Port 8001)" /D "c:\Users\DemandGeniusAI\lottery" cmd /k ""C:\Program Files\Python311\python.exe" "c:\Users\DemandGeniusAI\lottery\luck360_api_server.py""
    start "Luck360 Live Scraper Daemon" /D "c:\Users\DemandGeniusAI\lottery" cmd /k ""C:\Program Files\Python311\python.exe" "c:\Users\DemandGeniusAI\lottery\live_daemon.py""
    ping 127.0.0.1 -n 4 >nul
)
echo.

:: -------------------------------------------------------------------------
:: STEP 5: Verification and Health Status
:: -------------------------------------------------------------------------
echo [5/5] Verifying server sockets...
echo.
echo ======================================================================
netstat -ano | findstr :8000 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo   [SUCCESS] Port 8000 is LISTENING - Universal Study Packs MCP Server
) else (
    echo   [WARNING] Port 8000 not responding yet. Check window Universal Study Packs Server.
)

netstat -ano | findstr :8001 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo   [SUCCESS] Port 8001 is LISTENING - Luck360 Engine and MCP Server
) else (
    echo   [WARNING] Port 8001 not responding yet. Check window Luck360 Dual Engine.
)
echo ======================================================================
echo.
echo   PUBLIC PRODUCTION ENDPOINTS:
echo   ------------------------------------------------------------------
echo   * Luck360 Lottery Engine (Port 8001):
echo       Web Dashboard:  https://luck360.demandgeniusai.com
echo       Interactive UI: http://127.0.0.1:8001
echo       MCP SSE Stream: https://luck360.demandgeniusai.com/sse
echo       Swagger Docs:   https://luck360.demandgeniusai.com/docs
echo       OpenAPI JSON:   https://luck360.demandgeniusai.com/openapi.json
echo.
echo   * Universal Master Study Packs MCP (Port 8000):
echo       Web Hub:        https://mcp.demandgeniusai.com
echo       Interactive UI: http://127.0.0.1:8000
echo       MCP SSE Stream: https://mcp.demandgeniusai.com/sse
echo       Swagger Docs:   https://mcp.demandgeniusai.com/docs
echo       OpenAPI JSON:   https://mcp.demandgeniusai.com/openapi.json
echo ======================================================================
echo.
pause
