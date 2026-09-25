#!/usr/bin/env python3
"""
Background Auto-Refresh Daemon for Lottery Predictor
Runs continuously in the background, checks for new draw results every 15 seconds,
updates 'lottery.db' and 'draw_history.json', ensuring the UI auto-updates without page refresh.
"""

import time
import subprocess

def run_loop():
    print("Lottery Live Background Auto-Updater Started...")
    while True:
        try:
            subprocess.run(["python", "fetch_results.py"], check=False)
            subprocess.run(["python", "generate_frequency_report.py"], check=False)
        except Exception as e:
            print(f"Daemon error: {e}")
        time.sleep(15)

if __name__ == "__main__":
    run_loop()
