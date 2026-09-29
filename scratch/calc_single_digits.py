from collections import Counter

# Let's count digits across recent draws (last 5 draws) and projected hot picks (top 5 picks)
recent_tails = ['221', '051', '226', '398', '500']
projected_picks = ['145', '465', '661', '665', '599', '505']

recent_digits = [int(c) for t in recent_tails for c in t]
proj_digits = [int(c) for p in projected_picks for c in p]

recent_counts = Counter(recent_digits)
proj_counts = Counter(proj_digits)

print("Recent 5 draws digit counts:", sorted(recent_counts.items()))
print("Projected picks digit counts:", sorted(proj_counts.items()))

# Compute combined score: weight = 1.0 * proj + 0.8 * recent
scores = {}
for d in range(10):
    sc = (proj_counts.get(d, 0) * 1.5) + (recent_counts.get(d, 0) * 1.0)
    scores[d] = sc

max_score = max(scores.values()) if scores else 1
print("\n--- SINGLE DIGIT HOT FREQUENCY RANKING ---")
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
for rank, (d, sc) in enumerate(sorted_scores, 1):
    pct = round((sc / max_score) * 100)
    tier = "HOTTEST (***)" if pct >= 85 else ("VERY HOT (**)" if pct >= 65 else ("HOT (*)" if pct >= 45 else ("MODERATE" if pct >= 25 else "COOL")))
    print(f"Rank #{rank}: Digit {d} | Score: {sc:.1f} ({pct}%) | Tier: {tier}")
