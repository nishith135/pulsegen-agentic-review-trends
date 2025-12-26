import json
import os
from datetime import date


class OntologyManager:
    def __init__(self, ontology_path="data/ontology.json"):
        self.ontology_path = ontology_path
        self.ontology = {}
        self.load()

    def load(self):
        if os.path.exists(self.ontology_path):
            with open(self.ontology_path, "r", encoding="utf-8") as f:
                self.ontology = json.load(f)
        else:
            self.ontology = {}

    def save(self):
        os.makedirs(os.path.dirname(self.ontology_path), exist_ok=True)
        with open(self.ontology_path, "w", encoding="utf-8") as f:
            json.dump(self.ontology, f, indent=2, ensure_ascii=False)

    def get_topics(self):
        return list(self.ontology.keys())

    def topic_exists(self, topic_name):
        return topic_name in self.ontology

    def add_topic(self, topic_name, first_seen=None):
        if not self.topic_exists(topic_name):
            self.ontology[topic_name] = {
                "aliases": [],
                "first_seen": first_seen or date.today().isoformat()
            }

    def add_alias(self, topic_name, alias):
        if topic_name in self.ontology:
            if alias not in self.ontology[topic_name]["aliases"]:
                self.ontology[topic_name]["aliases"].append(alias)

    def find_topic_by_alias(self, alias):
        for topic, data in self.ontology.items():
            if alias in data["aliases"]:
                return topic
        return None


# Add this block to test the script
if __name__ == "__main__":
    manager = OntologyManager()
    print("Current topics:", manager.get_topics())

    # Example: Add a new topic
    manager.add_topic("Artificial Intelligence")
    manager.add_alias("Artificial Intelligence", "AI")
    manager.save()

    print("Updated topics:", manager.get_topics())
    print("Find topic by alias 'AI':", manager.find_topic_by_alias("AI"))
