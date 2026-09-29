#!/usr/bin/env python3
"""
Automated Draw Result Scraper & Live Database Updater
Fetches real-time draw results for Dear Lottery (1PM, 6PM, 8PM) and Kerala Lottery (3PM),
updates SQLite 'lottery.db', and syncs 'draw_history.json' automatically.
"""

import urllib.request
import re
import json
import sqlite3
import os
from datetime import datetime

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(WORKSPACE_DIR, "lottery.db")
JSON_FILE = os.path.join(WORKSPACE_DIR, "draw_history.json")

def fetch_web_page(url, timeout=12):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Fetch warning for {url}: {e}")
        return ""

def extract_tail(ticket_str):
    digits = ''.join(c for c in ticket_str if c.isdigit())
    if len(digits) >= 3:
        return digits[-3:]
    return digits.zfill(3)

def parse_dear_slot(slot_name, url):
    html = fetch_web_page(url)
    if not html:
        return None
    now = datetime.now()
    today_short = now.strftime('%d/%m/%y')
    today_str = now.strftime('%Y-%m-%d')
    m = re.search(r'class="rb-num">([^<]+)<.*?class="rb-date">([^<]+)<', html, re.DOTALL)
    if m:
        ticket = m.group(1).strip()
        pub_date = m.group(2).strip()
        if pub_date == today_short:
            return {"date": today_str, "ticket": ticket, "tail": extract_tail(ticket)}
        else:
            print(f"[WAIT] {slot_name} page date is {pub_date}, expected today {today_short}. Live draw not published yet.")
            return None
    # Fallback to general ticket pattern if rb-date not found
    tickets = re.findall(r'\b\d{2}[A-Z]\s*\d{5}\b', html)
    if tickets:
        t = tickets[0]
        return {"date": today_str, "ticket": t, "tail": extract_tail(t)}
    return None

def parse_latest_draws():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    weekday_name = now.strftime("%A")
    current_hour = now.hour
    current_minute = now.minute
    
    live_results = []

    # 1. Dear 1:00 PM Draw (eligible after 1:05 PM = 13:05)
    if (current_hour > 13) or (current_hour == 13 and current_minute >= 5):
        res_1pm = parse_dear_slot("Dear 1 PM", "https://dearlottery.in/result-today-1pm")
        if res_1pm:
            t1 = res_1pm["ticket"]
            live_results.append({
                "date": today_str,
                "time": "1:00 PM",
                "company": "Nagaland State Lottery",
                "lottery": f"Dear Victory {weekday_name} (1 PM)" if weekday_name == "Friday" else f"Dear 1 PM ({weekday_name})",
                "ticket": t1,
                "tail": extract_tail(t1)
            })
            print(f"[LIVE] Dear 1 PM 1st Prize: {t1} -> Tail {extract_tail(t1)}")

    # 2. Kerala 3:00 PM Draw (eligible from 3:00 PM = 15:00 onwards)
    if current_hour >= 15:
        html_kerala_home = fetch_web_page("https://www.keralalotteries.net/")
        kerala_post_links = re.findall(r'https://www.keralalotteries.net/\d{4}/\d{2}/[^\"]+today-\d{2}-\d{2}-\d{4}\.html', html_kerala_home)
        if not kerala_post_links:
            # Fallback to any recent post for today
            today_dmy = now.strftime('%d-%m-%Y')
            kerala_post_links = [l for l in re.findall(r'https://www.keralalotteries.net/\d{4}/\d{2}/[^\"]+\.html', html_kerala_home) if today_dmy in l]
        html_kerala_post = fetch_web_page(kerala_post_links[0]) if kerala_post_links else html_kerala_home

        # Look specifically for 1st Prize ticket first
        first_prize_m = re.search(r'(?:1st Prize|First Prize)[^\n<]*?([A-Z]{2}\s*\d{6})', html_kerala_post, re.I)
        tk = None
        if first_prize_m:
            tk = first_prize_m.group(1).strip()
        else:
            kerala_tickets = re.findall(r'\b[A-Z]{2}\s*\d{6}\b', html_kerala_post)
            if kerala_tickets:
                tk = kerala_tickets[0]

        if tk:
            scheme_match = re.search(r'([A-Za-z\s]+(SK|NR|KR|SS|KN|DL|BH|SM|BR)[\s\-]?\d+)', html_kerala_post)
            scheme_name = scheme_match.group(1).strip() if scheme_match else f"Kerala Thiruvonam Bumper BR-111"
            live_results.append({
                "date": today_str,
                "time": "3:00 PM",
                "company": "Kerala State Lotteries",
                "lottery": f"{scheme_name} (3 PM)" if "(3 PM)" not in scheme_name else scheme_name,
                "ticket": tk,
                "tail": extract_tail(tk)
            })
            print(f"[LIVE] Kerala 3 PM 1st Prize: {tk} -> Tail {extract_tail(tk)}")

    # 3. Dear 6:00 PM Draw (eligible after 6:05 PM = 18:05)
    if (current_hour > 18) or (current_hour == 18 and current_minute >= 5):
        res_6pm = parse_dear_slot("Dear 6 PM", "https://dearlottery.in/result-today-6pm")
        if res_6pm:
            t6 = res_6pm["ticket"]
            live_results.append({
                "date": today_str,
                "time": "6:00 PM",
                "company": "Sikkim State Lottery",
                "lottery": f"Dear Mountain {weekday_name} (6 PM)" if weekday_name == "Friday" else f"Dear 6 PM ({weekday_name})",
                "ticket": t6,
                "tail": extract_tail(t6)
            })
            print(f"[LIVE] Dear 6 PM 1st Prize: {t6} -> Tail {extract_tail(t6)}")

    # 4. Dear 8:00 PM Draw (eligible after 8:05 PM = 20:05)
    if (current_hour > 20) or (current_hour == 20 and current_minute >= 5):
        res_8pm = parse_dear_slot("Dear 8 PM", "https://dearlottery.in/result-today-8pm")
        if res_8pm:
            t8 = res_8pm["ticket"]
            live_results.append({
                "date": today_str,
                "time": "8:00 PM",
                "company": "Nagaland State Lottery",
                "lottery": f"Dear Seagull {weekday_name} (8 PM)" if weekday_name == "Friday" else f"Dear 8 PM ({weekday_name})",
                "ticket": t8,
                "tail": extract_tail(t8)
            })
            print(f"[LIVE] Dear 8 PM 1st Prize: {t8} -> Tail {extract_tail(t8)}")

    return live_results

def update_database(results):
    if not results:
        print("No eligible live results to update at this hour.")
        return 0, 0

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    updated_count = 0
    for r in results:
        cursor.execute("""
            SELECT id FROM draws 
            WHERE draw_date = ? AND draw_time = ? AND company = ?
        """, (r["date"], r["time"], r["company"]))
        row = cursor.fetchone()

        if row is None:
            cursor.execute("""
                INSERT INTO draws (draw_date, draw_time, company, lottery_name, ticket_number, tail)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (r["date"], r["time"], r["company"], r["lottery"], r["ticket"], r["tail"]))
            updated_count += 1
            print(f"Inserted new draw: {r['date']} {r['time']} - {r['lottery']} ({r['ticket']})")
        else:
            cursor.execute("""
                UPDATE draws 
                SET lottery_name = ?, ticket_number = ?, tail = ?
                WHERE id = ?
            """, (r["lottery"], r["ticket"], r["tail"], row[0]))
            print(f"Verified existing draw record id {row[0]}: {r['lottery']} ({r['ticket']})")

    conn.commit()
    conn.close()

    # Re-sync draw_history.json
    import db_manager
    records = db_manager.sync_json()

    # Recalculate frequency & age stats
    try:
        from generate_frequency_report import run_frequency_and_age_analysis
        run_frequency_and_age_analysis()
    except Exception as e:
        print(f"Frequency update note: {e}")
    
    return updated_count, len(records)

# Alias for MCP server compatibility
update_database_and_json = update_database

if __name__ == "__main__":
    print("Running Live Result Scraper & Auto-Updater...")
    draws = parse_latest_draws()
    new_records, total = update_database(draws)
    print(f"Auto-Update complete. {new_records} new/updated records. Total records in DB: {total}")

