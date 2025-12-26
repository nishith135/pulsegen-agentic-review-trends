# Agentic Review Trend Analysis System

## Overview
This project implements an **Agentic AI system** that analyzes daily batches of app reviews and generates a rolling **T to T-30 trend report** of user issues, requests, and feedback.

The system was built as part of a Senior AI Engineer assignment and focuses on:
- High-recall topic deduplication
- Stable topic tracking over time
- Agentic reasoning with persistent memory

The target application used for demonstration is **Clash Royale**, chosen due to its high-volume, slang-heavy, and rapidly evolving user feedback.

---

## Problem Statement
User reviews often describe the same issue in many different ways (e.g., “MK too OP”, “Nerf Mega Knight”, “Mega Knight broken”).  
Naive systems fragment these into separate topics, breaking trend analysis.

The goal is to:
- Consolidate semantically similar feedback into canonical topics
- Preserve new and evolving topics
- Produce a clean daily trend matrix across a rolling 30-day window

---

## System Architecture (Agentic Design)

The system is composed of multiple autonomous agents:

### 1. Categorization Agent
- Reads individual reviews
- Assigns them to existing topics or proposes new ones
- Supports both LLM-based reasoning and deterministic fallback logic
- Handles slang and abbreviations (e.g., MK → Mega Knight)

### 2. Consolidation Agent
- Audits newly proposed topics
- Merges semantically similar topics with high recall
- Maintains canonical topics and aliases
- Prevents topic explosion over time

### 3. Ontology Manager
- Persistent memory layer (`ontology.json`)
- Stores canonical topics, aliases, and metadata
- Ensures consistency across daily batches

### 4. Daily Pipeline
- Processes reviews in daily batches (one file per day)
- Coordinates agents
- Produces per-day topic frequency counts

### 5. Trend Reporting Engine
- Aggregates daily counts from T to T-30
- Outputs a topic × date frequency matrix
- Generates a CSV trend report

---

## Data Assumptions
The assignment specifies:
> “Assume starting from June 1st, 2024, everyday you receive data with reviews.”

Due to limitations in reliably scraping historical Google Play reviews, **daily review batches are simulated**.  
The ingestion interface remains identical to a production setup, allowing the agentic pipeline to be evaluated independently of external platform constraints.

---

## Project Structure

pulsegen-agentic-review-trends/
├── agents/
│ ├── init.py
│ ├── categorization_agent.py
│ ├── consolidation_agent.py
│ └── ontology_manager.py
├── reporting/
│ ├── init.py
│ └── generate_trend_report.py
├── data/
│ ├── reviews/
│ │ └── YYYY-MM-DD.json
│ └── ontology.json
├── output/
│ └── trend_report.csv
├── main.py
└── README.md

yaml
Copy code

---

## How to Run

### 1. Activate virtual environment
```bash
.venv\Scripts\activate   # Windows
2. Run daily pipeline
bash
Copy code
python main.py
3. Generate 30-day trend report
bash
Copy code
python -m reporting.generate_trend_report
Output Format
The final output is a CSV file:

elm
Copy code
output/trend_report.csv
Format:

Rows → Canonical Topics

Columns → Dates (T to T-30)

Values → Frequency counts

Example:

apache
Copy code
Topic,2024-06-01,2024-06-02,...,2024-07-01
Mega Knight Balance Issues,3,2,...,5
Goblin Queen's Journey Feedback,1,0,...,2
Key Design Decisions
Agentic approach instead of traditional topic modeling (no LDA / TopicBERT)

High recall over precision to ensure stable trends

Persistent ontology memory instead of stateless clustering

LLM-agnostic design with deterministic fallback for reliability and testing

