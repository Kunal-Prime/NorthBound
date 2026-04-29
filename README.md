# 🧠 NorthBound — From Chaos to Systems

NorthBound is a system built around one practical problem:

> Human input is messy. Software is not.

This repository documents the process of turning vague, inconsistent, real-world input into structured, usable systems.

Instead of building another toy parser, the focus here was simpler and more useful:

> How do systems behave when reality is ambiguous?

---

## 🚀 Featured Project: Smart Timetable API

NorthBound’s core system is a hybrid timetable parser that converts messy human-written schedules into structured JSON.

It is built to handle the kind of input people actually write — incomplete, inconsistent, and often ambiguous.

---

## ⚔️ Two Parsing Approaches

NorthBound uses two fundamentally different parsing systems:

* **Manual Parser** → deterministic, rule-based, fast, strict
* **LLM Parser** → probabilistic, flexible, ambiguity-tolerant

These are not alternatives.

They are deliberately used together.

---

## 🧠 The Twist

Most student projects stop at “it works.”

NorthBound does something more useful.

Instead of trusting one parser blindly, the system:

* runs both parsers
* compares both outputs
* evaluates which result is stronger
* returns the better interpretation

👉 This makes NorthBound a hybrid decision system, not just a parser.

That is the real point of the project.

Not parsing.

Decision logic under ambiguity.

---

## 🔬 Example

**Input:**
`Math Monday 9am, maybe Physics Tuesday afternoon`

**What happens:**

* Manual parser struggles with ambiguity
* LLM parser recovers likely intent
* Evaluation layer compares both
* System returns the stronger output

The goal is not perfect parsing.

The goal is reliable interpretation under imperfect input.

---

## 🏗️ System Architecture

NorthBound is built as a three-layer pipeline:

* **Parsing Layer**
  Two independent parsers process the same input

* **Evaluation Layer**
  Outputs are compared for quality and completeness

* **Decision Layer**
  Best result is selected automatically

This mirrors how practical AI systems are often built:

not one model,
but multiple systems with decision logic in between.

---

## 🌐 Live System

NorthBound is fully deployed and publicly accessible.

* **Frontend** → GitHub Pages
* **Backend API** → Render
* **Interactive API Docs** → FastAPI Swagger

This project was intentionally taken beyond localhost.

Because systems are only interesting once they fail in public.

---

## 🛠️ Tech Stack

* **Frontend** → HTML, CSS, JavaScript
* **Backend** → FastAPI
* **Database** → PostgreSQL
* **ORM** → SQLAlchemy
* **LLM Layer** → Google Gemini
* **Deployment** → Render
* **Frontend Hosting** → GitHub Pages
* **CI/CD** → GitHub Actions

---

## 🏗️ Repository Structure

* `systems/` → core system implementations
* `systems/smart_timetable_api/` → hybrid timetable parser
* `tests/` → API tests
* `.github/workflows/` → CI/CD pipeline
* `index.html` → live frontend
* `models.py` → database models

---

## 🧠 What This Actually Explores

NorthBound is not really about timetables.

It is about system behavior under ambiguity.

More specifically:

* how deterministic systems fail
* where probabilistic systems recover
* how to compare both
* how to design fallback logic
* how to make imperfect systems still useful

The parser is just the surface.

The real project is decision architecture.

---

## 🧠 Key Insight

* Rule-based systems are reliable until reality becomes messy
* LLMs handle ambiguity better, but lose determinism
* Hybrid systems are often more useful than either alone

That tradeoff is the core idea behind NorthBound.

---

## 📂 Explore the System

👉 Core implementation lives here:
`systems/smart_timetable_api/`

---

## ⚡ What’s Next

* Improve evaluation logic
* Add confidence scoring
* Track parser reliability
* Add fallback ranking
* Explore multi-agent parsing systems

---

## 👤 Author

**Kunal**
