#!/usr/bin/env python3
"""
Background Auto-Refresh Daemon for Lottery Predictor & Analytics Engine
Monitors 4 daily draw slots: 1:00 PM, 3:00 PM, 6:00 PM, and 8:00 PM.
After each draw time, automatically triggers the scraper every 20 minutes
until the new official draw result is published, verified, and reflected in SQLite & JSON.
Once reflected, marks that slot completed for the day and waits for the next draw window.
"""

import time
import subprocess
import sys
import os
import json
import sqlite3
from datetime import datetime

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(WORKSPACE_DIR, "lottery.db")
JSON_FILE = os.path.join(WORKSPACE_DIR, "draw_history.json")
STATUS_FILE = os.path.join(WORKSPACE_DIR, "daemon_status.json")
FETCH_SCRIPT = os.path.join(WORKSPACE_DIR, "fetch_results.py")
FREQ_SCRIPT = os.path.join(WORKSPACE_DIR, "generate_frequency_report.py")

# Slot schedule: (Time Slot, Start Hour, Start Minute)
SLOT_CONFIGS = [
    {"slot": "1:00 PM", "company": "Nagaland State Lottery", "start_h": 13, "start_m": 5},
    {"slot": "3:00 PM", "company": "Kerala State Lotteries", "start_h": 15, "start_m": 0},
    {"slot": "6:00 PM", "company": "Sikkim State Lottery", "start_h": 18, "start_m": 5},
    {"slot": "8:00 PM", "company": "Nagaland State Lottery", "start_h": 20, "start_m": 5},
]
RETRY_INTERVAL_SECONDS = 20 * 60  # 20 minutes

def check_slot_reflected_in_db(date_str, slot_time):
    if not os.path.exists(DB_FILE):
        return False, None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ticket_number, lottery_name, tail 
            FROM draws 
            WHERE draw_date = ? AND draw_time = ?
        """, (date_str, slot_time))
        row = cursor.fetchone()
        conn.close()
        if row:
            return True, {"ticket": row[0], "lottery": row[1], "tail": row[2]}
    except Exception as e:
        print(f"DB check error: {e}")
    return False, None

def write_daemon_status(status_data):
    try:
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        print(f"Status file write error: {e}")

def run_fetch_and_update():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering live scraper & analytics sync...")
    try:
        subprocess.run([sys.executable, FETCH_SCRIPT], cwd=WORKSPACE_DIR, check=False)
        subprocess.run([sys.executable, FREQ_SCRIPT], cwd=WORKSPACE_DIR, check=False)
    except Exception as e:
        print(f"Fetch error: {e}")

def run_loop():
    print(f"============================================================")
    print(f"Lottery 20-Min Auto-Service Daemon Started in {WORKSPACE_DIR}")
    print(f"Active Slots: 1:00 PM, 3:00 PM, 6:00 PM, 8:00 PM")
    print(f"Policy: After result time, polls every 20 mins until reflected.")
    print(f"============================================================")

    last_attempt_time = {}

    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        status_info = {
            "last_heartbeat": now.strftime("%Y-%m-%d %H:%M:%S"),
            "today": today_str,
            "slots": {},
            "active_action": "Idle"
        }

        should_fetch_now = False
        fetch_reason = ""

        for cfg in SLOT_CONFIGS:
            slot_name = cfg["slot"]
            start_h = cfg["start_h"]
            start_m = cfg["start_m"]
            slot_start_dt = now.replace(hour=start_h, minute=start_m, second=0, microsecond=0)

            is_reflected, draw_data = check_slot_reflected_in_db(today_str, slot_name)

            if is_reflected:
                status_info["slots"][slot_name] = {
                    "status": "REFLECTED",
                    "details": f"{draw_data['lottery']} ({draw_data['ticket']} -> Tail {draw_data['tail']})"
                }
            elif now < slot_start_dt:
                status_info["slots"][slot_name] = {
                    "status": "UPCOMING",
                    "details": f"Scheduled at {slot_start_dt.strftime('%I:%M %p')} (polls every 20m until reflected)"
                }
            else:
                # Slot draw time has passed, but result is not reflected yet!
                last_try = last_attempt_time.get(slot_name, 0)
                elapsed = time.time() - last_try

                if elapsed >= RETRY_INTERVAL_SECONDS:
                    should_fetch_now = True
                    fetch_reason = f"{slot_name} result pending reflection (20m retry due)"
                    status_info["slots"][slot_name] = {
                        "status": "CHECKING_NOW",
                        "details": f"Running 20-minute cycle check..."
                    }
                else:
                    remaining_sec = int(RETRY_INTERVAL_SECONDS - elapsed)
                    next_slot_check = datetime.fromtimestamp(last_try + RETRY_INTERVAL_SECONDS)
                    status_info["slots"][slot_name] = {
                        "status": "WAITING_20M_RETRY",
                        "details": f"Awaiting publication. Next check at {next_slot_check.strftime('%I:%M:%S %p')} (~{remaining_sec // 60}m remaining)"
                    }

        if should_fetch_now:
            status_info["active_action"] = f"Running scraper: {fetch_reason}"
            write_daemon_status(status_info)
            run_fetch_and_update()
            # Update last attempt time for all pending eligible slots
            for cfg in SLOT_CONFIGS:
                slot_name = cfg["slot"]
                slot_start_dt = now.replace(hour=cfg["start_h"], minute=cfg["start_m"], second=0, microsecond=0)
                is_ref, _ = check_slot_reflected_in_db(today_str, slot_name)
                if now >= slot_start_dt and not is_ref:
                    last_attempt_time[slot_name] = time.time()
        else:
            status_info["active_action"] = "Monitoring draw schedule (20m interval active)"
            write_daemon_status(status_info)

        # Sleep briefly (10 seconds) between scheduler checks
        time.sleep(10)

if __name__ == "__main__":
    run_loop()
