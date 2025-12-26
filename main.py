import json
from collections import Counter
from datetime import date

from agents.ontology_manager import OntologyManager
from agents.categorization_agent import categorize_review
from agents.consolidation_agent import ConsolidationAgent


BATCH_DATE = date(2024, 6, 1)
REVIEWS_FILE = f"data/reviews/{BATCH_DATE.isoformat()}.json"


def run_daily_pipeline():
    # Load reviews
    with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    ontology = OntologyManager("data/ontology.json")

    proposed_topics = []
    assigned_topics = []

    # Step 1: Categorize reviews
    for r in reviews:
        result = categorize_review(r["content"], ontology.get_topics())
        proposed_topics.append(result["topic"])
        assigned_topics.append(result["topic"])

    # Step 2: Consolidate topics
    consolidator = ConsolidationAgent(ontology)
    consolidation_results = consolidator.consolidate(proposed_topics)

    # Step 3: Count final topics
    topic_counts = Counter(assigned_topics)

    print("\n--- DAILY TOPIC COUNTS ---")
    for topic, count in topic_counts.items():
        print(f"{topic}: {count}")

    print("\n--- CONSOLIDATION ACTIONS ---")
    for action in consolidation_results:
        print(action)


if __name__ == "__main__":
    run_daily_pipeline()
