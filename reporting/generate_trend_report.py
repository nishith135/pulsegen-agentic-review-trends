# ===============================
# PATH FIX — MUST BE FIRST
# ===============================
from agents.consolidation_agent import ConsolidationAgent
from agents.categorization_agent import categorize_review
from agents.ontology_manager import OntologyManager
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import csv
import json
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ===============================
# STANDARD LIBRARIES
# ===============================

# ===============================
# PROJECT IMPORTS (NOW SAFE)
# ===============================

# ===============================
# CONFIG
# ===============================
DATA_DIR = "data/reviews"
ONTOLOGY_PATH = "data/ontology.json"
OUTPUT_PATH = "output/trend_report.csv"

START_DATE = datetime(2024, 6, 1)
WINDOW_DAYS = 30  # T-30 to T inclusive


# ===============================
# HELPERS
# ===============================
def load_reviews(date_str):
    path = os.path.join(DATA_DIR, f"{date_str}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ===============================
# MAIN LOGIC
# ===============================
def generate_trend_report():
    ontology = OntologyManager(ONTOLOGY_PATH)
    daily_topic_counts = defaultdict(dict)

    dates = [
        (START_DATE + timedelta(days=i)).date().isoformat()
        for i in range(WINDOW_DAYS + 1)
    ]

    for date_str in dates:
        reviews = load_reviews(date_str)
        if not reviews:
            continue

        proposed_topics = []
        assigned_topics = []

        for r in reviews:
            result = categorize_review(r["content"], ontology.get_topics())
            proposed_topics.append(result["topic"])
            assigned_topics.append(result["topic"])

        consolidator = ConsolidationAgent(ontology)
        consolidator.consolidate(proposed_topics)

        counts = Counter(assigned_topics)
        for topic, count in counts.items():
            daily_topic_counts[topic][date_str] = count

    os.makedirs("output", exist_ok=True)

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Topic"] + dates)

        for topic, counts in daily_topic_counts.items():
            row = [topic] + [counts.get(d, 0) for d in dates]
            writer.writerow(row)

    print(f"Trend report generated → {OUTPUT_PATH}")


# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    generate_trend_report()
