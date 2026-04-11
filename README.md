# 🧠 Northbound — From Chaos to Systems

This repository documents my journey of transforming messy, real-world input into structured, usable systems.

Instead of just learning tools, I focused on one core question:

> How do systems handle ambiguity?

---

## 🚀 Featured Project: Smart Timetable API

A hybrid system that converts messy human timetable input into structured JSON.

### ⚔️ Two Approaches

* **Manual Parser** → deterministic, rule-based
* **LLM Parser** → probabilistic, AI-based

---

## 🧠 The Twist (What makes this different)

Instead of choosing one approach manually, the system:

* runs both parsers
* evaluates their outputs
* automatically selects the best result

👉 This mimics real-world hybrid AI systems.

---

## 🔬 Example

**Input:**
"Math Monday 9am, maybe Physics Tuesday afternoon"

**System Output:**

* Manual parser struggles with ambiguity
* LLM parser interprets intent correctly
* System selects LLM as best approach

---

## 🏗️ Repository Structure

* `systems/` → real-world system implementations
* `concepts/` → focused technical explorations
* `archive_learning/` → raw day-by-day learning logs

---

## 🧠 Key Insight

* Rule-based systems break with ambiguity
* LLMs handle ambiguity but lack strict guarantees
* Hybrid systems combine both strengths

---

## 📂 Explore the System

👉 Check the full implementation here:  
`systems/smart_timetable_api/`

---

## ⚡ What's Next

* Improve evaluation logic
* Add confidence scoring
* Explore multi-agent parsing systems

---

## 👤 Author

Kunal
