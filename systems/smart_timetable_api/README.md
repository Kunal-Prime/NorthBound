# Smart Timetable API

## 🧠 Idea

Human input is messy. Traditional systems expect structure.

This project compares:
- Rule-based parsing (manual logic)
- LLM-based parsing (AI interpretation)

---

## ⚔️ Manual vs LLM

LLMs handle ambiguity better, while rule-based systems are rigid but predictable.

---

## 🚀 Run

pip install -r requirements.txt  
uvicorn main:app --reload

---

## 🧠 Intelligent Parsing

Instead of choosing one method, the system:

1. Runs both manual and LLM parsers
2. Evaluates their outputs
3. Returns the most reliable result

This mimics real-world hybrid system design.

---

## 🧠 Smart Parsing

Instead of choosing a parser manually, the system:

- Runs both parsers
- Evaluates output quality
- Automatically selects the best result

This mimics real-world hybrid AI systems.

---

## 🧠 Learning Architecture

- `systems/` → Production-style builds
- `concepts/` → Focused experiments
- `archive_learning/` → Raw day-wise logs