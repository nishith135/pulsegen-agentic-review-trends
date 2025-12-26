import os
import json
from dotenv import load_dotenv

# Optional: only needed if you ever turn USE_LLM = True
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv()

# =========================
# AGENT MODE SWITCH
# =========================
USE_LLM = False  # 🔴 KEEP FALSE for testing & submission

client = None
if USE_LLM and OpenAI:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# SYSTEM PROMPT (LLM MODE)
# =========================
SYSTEM_PROMPT = """
You are a Categorization Agent for app review analysis.

Your task:
- Read a single app review
- Decide whether it belongs to an EXISTING topic
- OR if it introduces a NEW topic

Rules:
1. Prefer existing topics when meaning overlaps.
2. Recognize abbreviations and slang (e.g., MK = Mega Knight).
3. If a review discusses a newly introduced feature, propose a new topic.
4. Output ONLY valid JSON.

JSON format:
{
  "decision": "existing" or "new",
  "topic": "<topic_name>",
  "confidence": 0.0 to 1.0
}
"""

# =========================
# CATEGORIZATION AGENT
# =========================


def categorize_review(review_text, existing_topics):
    """
    Agent decision:
    - Takes a single review
    - Returns a topic decision (existing / new)
    """

    text = review_text.lower()

    # --------------------------------------------------
    # OFFLINE / FALLBACK AGENT (USED FOR TESTING)
    # --------------------------------------------------
    if not USE_LLM:
        # Mega Knight logic
        if "mega knight" in text or "mk" in text:
            return {
                "decision": "existing" if "Mega Knight Balance Issues" in existing_topics else "new",
                "topic": "Mega Knight Balance Issues",
                "confidence": 0.9
            }

        # Goblin Queen Journey
        if "goblin queen" in text:
            return {
                "decision": "new",
                "topic": "Goblin Queen's Journey Feedback",
                "confidence": 0.85
            }

        # Stability / crash issues
        if "crash" in text or "bug" in text or "freeze" in text:
            return {
                "decision": "new",
                "topic": "Game Stability Issues",
                "confidence": 0.8
            }

        # Default bucket
        return {
            "decision": "new",
            "topic": "General Gameplay Feedback",
            "confidence": 0.6
        }

    # --------------------------------------------------
    # ONLINE / LLM AGENT (OPTIONAL, FUTURE)
    # --------------------------------------------------
    prompt = f"""
{SYSTEM_PROMPT}

Review:
\"{review_text}\"

Existing Topics:
{existing_topics}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned:\n{content}")
