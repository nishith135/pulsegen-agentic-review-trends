import re


class ConsolidationAgent:
    """
    Responsible for merging semantically similar topics
    and updating the ontology with canonical topics + aliases.
    """

    def __init__(self, ontology_manager):
        self.ontology_manager = ontology_manager

        # Domain-specific normalization rules
        self.synonym_map = {
            "mega knight": ["mk", "mega knight", "mid ladder menace"],
            "dagger duchess": ["dd", "dagger duchess", "tower troop dd"],
            "little prince": ["lp", "little prince"],
        }

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text.strip()

    def find_canonical_topic(self, proposed_topic: str):
        normalized = self.normalize(proposed_topic)

        for canonical in self.ontology_manager.get_topics():
            canon_norm = self.normalize(canonical)

            # Direct match
            if normalized == canon_norm:
                return canonical

            # Synonym-based match
            for key, variants in self.synonym_map.items():
                if key in canon_norm:
                    for v in variants:
                        if v in normalized:
                            return canonical

        return None

    def consolidate(self, proposed_topics: list):
        """
        Input: list of newly proposed topic strings
        Output: consolidation decisions (for logging/debugging)
        """

        decisions = []

        for topic in proposed_topics:
            existing = self.find_canonical_topic(topic)

            if existing:
                # Merge into existing topic
                self.ontology_manager.add_alias(existing, topic)
                decisions.append({
                    "action": "merged",
                    "from": topic,
                    "to": existing
                })
            else:
                # New genuinely novel topic
                self.ontology_manager.add_topic(topic)
                decisions.append({
                    "action": "created",
                    "topic": topic
                })

        self.ontology_manager.save()
        return decisions
