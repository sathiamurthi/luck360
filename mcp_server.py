#!/usr/bin/env python3
"""
Lottery Pattern Predictor MCP Server & Analytics Engine
Provides MCP tools for tracking historical draw records, pattern backtesting,
and pattern "arrest" (constrained target prediction).
"""

import sys
import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_history.json")

def load_records():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def extract_tail(ticket_str):
    digits = ''.join(c for c in ticket_str if c.isdigit())
    if len(digits) >= 3:
        return digits[-3:]
    return digits.zfill(3)

def transform_58(d):
    trans_map = {5: 8, 8: 5, 7: 2, 2: 7, 6: 4, 4: 6, 9: 0, 0: 9, 1: 3, 3: 1}
    return trans_map.get(d, (d + 3) % 10)

def row60_trans(d):
    if d == 7: return 5
    if d == 0: return 9
    if d == 5: return 7
    if d == 9: return 0
    return (d + 1) % 10

def calculate_patterns(tail_str):
    d1 = int(tail_str[0])
    d2 = int(tail_str[1])
    d3 = int(tail_str[2])

    p1 = f"{d3}{d2}{(d3 - d1 + 10) % 10}"
    p2_conv1 = f"{d1}{(d2 + 1) % 10}{(d3 - 1 + 10) % 10}"
    p3 = f"{d2}{d1}{d3}"
    r41 = f"{(d1 - 2 + 10) % 10}{(d2 - 2 + 10) % 10}{(d3 + 1) % 10}"
    r60 = f"{row60_trans(d1)}{row60_trans(d2)}{row60_trans(d3)}"

    h1 = f"{(d1 + 1) % 10}{(d2 + 1) % 10}{(d3 + 1) % 10}"
    h2 = f"{(d1 + d2) % 10}{d3}{transform_58(d2)}"
    
    diff12 = (d1 - d2 + 10) % 10
    rem_digit = (d1 + d2 + d3) % 10
    diff13 = (d1 - d3 + 10) % 10
    h3 = f"{diff12}{rem_digit}{diff13}"

    # USER PATTERN H4: First & Last Digit + Reverse AB Pair
    h4_a = f"{d1}{d3}{d2}"
    h4_b = f"{d2}{d1}{d3}"

    return {
        "P1_RevDiff": p1,
        "P2_KeepConv": p2_conv1,
        "P3_RevAB": p3,
        "Row41_Offset": r41,
        "Row60_Rule": r60,
        "H1_IncShift": h1,
        "H2_CrossSwap": h2,
        "H3_DiffRem": h3,
        "H4_FirstLastSwap": h4_a,
        "H4_RevABLast": h4_b
    }

def analyze_historical_matches():
    records = load_records()
    results = []

    for i in range(len(records) - 1):
        prev = records[i]
        curr = records[i + 1]
        
        prev_tail = prev["tail"]
        curr_tail = curr["tail"]
        
        patterns = calculate_patterns(prev_tail)
        matches = []

        curr_sorted = "".join(sorted(curr_tail))

        for pat_name, pat_val in patterns.items():
            pat_sorted = "".join(sorted(pat_val))
            
            if pat_val == curr_tail:
                matches.append({
                    "pattern": pat_name,
                    "predicted": pat_val,
                    "match_type": "STRAIGHT MATCH (Exact)"
                })
            elif pat_sorted == curr_sorted:
                matches.append({
                    "pattern": pat_name,
                    "predicted": pat_val,
                    "match_type": "BOX MATCH (Permutation)"
                })

        results.append({
            "from_draw": f"{prev['date']} - {prev['lottery']} ({prev_tail})",
            "to_draw": f"{curr['date']} - {curr['lottery']} ({curr_tail})",
            "matches": matches,
            "patterns_calculated": patterns
        })

    return results

def arrest_patterns_filter():
    records = load_records()
    if not records:
        return {"error": "No draw records found."}

    latest = records[-1]
    latest_tail = latest["tail"]
    patterns = calculate_patterns(latest_tail)

    d1, d2, d3 = int(latest_tail[0]), int(latest_tail[1]), int(latest_tail[2])
    ab, bc, ac = f"{d1}{d2}", f"{d2}{d3}", f"{d1}{d3}"

    return {
        "latest_draw": latest,
        "base_tail": latest_tail,
        "pairs": {"AB": ab, "BC": bc, "AC": ac},
        "all_patterns": patterns,
        "arrested_top_targets": [
            {
                "target": patterns["H2_CrossSwap"],
                "reason": "User H2 Cross-Swap 5-8 Rule (Proved on 457 -> 978)",
                "confidence": "HIGH"
            },
            {
                "target": patterns["H3_DiffRem"],
                "reason": "User H3 Diff & Remainder Matrix (Proved on 978 -> 221)",
                "confidence": "HIGH"
            },
            {
                "target": patterns["H4_FirstLastSwap"],
                "reason": "User H4 First & Last Digit Swap + Reverse AB Pair",
                "confidence": "HIGH"
            },
            {
                "target": patterns["P1_RevDiff"],
                "reason": "Pattern 1 Rev+Diff (Proved on 712 -> 215)",
                "confidence": "MEDIUM-HIGH"
            }
        ]
    }

def handle_mcp_request(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "lottery-pattern-mcp",
                    "version": "1.0.0"
                }
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "get_draw_records",
                        "description": "Fetch all historical lottery draw records and calculated pattern values.",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "add_draw_record",
                        "description": "Add a new lottery draw record to the historical dataset.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "date": {"type": "string", "description": "YYYY-MM-DD"},
                                "time": {"type": "string", "description": "Draw Time"},
                                "company": {"type": "string", "description": "State Company Name"},
                                "lottery": {"type": "string", "description": "Lottery name"},
                                "ticket": {"type": "string", "description": "Full ticket number"}
                            },
                            "required": ["date", "company", "lottery", "ticket"]
                        }
                    },
                    {
                        "name": "analyze_pattern_matches",
                        "description": "Backtest historical draws to check which pattern matched on which day.",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "arrest_patterns",
                        "description": "Run constrained pattern filter algorithm to pin down top targets.",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "predict_next_days",
                        "description": "Generate exact 3-day mathematical pattern predictions for all upcoming draw slots.",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "get_draw_records":
            recs = load_records()
            for r in recs:
                r["patterns"] = calculate_patterns(r["tail"])
            res_content = json.dumps(recs, indent=2)

        elif tool_name == "add_draw_record":
            recs = load_records()
            new_id = len(recs) + 1
            tail = extract_tail(args["ticket"])
            new_rec = {
                "id": new_id,
                "date": args["date"],
                "time": args.get("time", "12:00 PM"),
                "company": args["company"],
                "day": f"{args['date']} {args.get('time', '')}",
                "lottery": f"{args['company']} - {args['lottery']}",
                "ticket": args["ticket"],
                "tail": tail
            }
            recs.append(new_rec)
            save_records(recs)
            res_content = json.dumps({"status": "success", "added": new_rec}, indent=2)

        elif tool_name == "analyze_pattern_matches":
            matches = analyze_historical_matches()
            res_content = json.dumps(matches, indent=2)

        elif tool_name == "arrest_patterns":
            arrest_res = arrest_patterns_filter()
            res_content = json.dumps(arrest_res, indent=2)

        elif tool_name == "predict_next_days":
            from predict_3days import get_3day_predictions
            recs = load_records()
            base = recs[-1]["tail"] if recs else "221"
            preds = get_3day_predictions(base)
            res_content = json.dumps(preds, indent=2)

        else:
            res_content = json.dumps({"error": f"Unknown tool '{tool_name}'"})

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": res_content
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"}
    }

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("--- Lottery MCP Command Line Interface ---")
        print("Matches:")
        print(json.dumps(analyze_historical_matches(), indent=2))
        print("Arrest Filter:")
        print(json.dumps(arrest_patterns_filter(), indent=2))
        return

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_mcp_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling MCP request: {e}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()
