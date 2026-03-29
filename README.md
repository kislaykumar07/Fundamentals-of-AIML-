# Fundamentals-of-AIML-
# Smart Study Assistant: Mood & Focus Tracker

**AIML Project | B.Tech / BCA | 2025–26**

---

## What This Is

Most of us sit down to study without really thinking about whether our mind is actually ready for it. This project is a small attempt to fix that. The Smart Study Assistant lets you log how you're feeling before or after a study session — your mood, your focus level, how long you studied — and it gives you back something actually useful: a quality rating, concrete advice, and a running picture of how your study habits are trending over time.

There are two interfaces:

- `app.py` — a terminal program you can run anywhere Python is installed  
- `dashboard.html` — a web dashboard with charts, a Pomodoro timer, and a session history table (open it in any browser, no server needed)

Both use the same rule-based AI logic and can work independently.

---

## Project Structure

```
smart_study_assistant/
│
├── app.py               # Terminal application (main program)
├── dashboard.html       # Web dashboard (open in browser)
├── study_log.json       # Auto-created when you log your first session
└── README.md            # You're reading this
```

---

## How to Run

### Terminal App

```bash
# No external libraries needed — runs on standard Python 3.x
python3 app.py
```

You'll get a menu like this:

```
  [1]  Log a new study session
  [2]  View recent sessions (chart)
  [3]  Weekly summary
  [4]  Start Pomodoro timer (25 min)
  [5]  Get study tips for a subject
  [6]  View my trend
  [0]  Exit
```

### Web Dashboard

Just double-click `dashboard.html` or drag it into a browser tab. No server, no installation, no npm. It stores data in your browser's `localStorage`.

---

## How the AI Logic Works

The "AI" here is a rule-based classifier — no machine learning library, no black-box model. The logic is transparent and you can read every line of it in `app.py`.

### Session Quality Score

Each session gets scored out of 5:

```
score = (mood × 0.4) + (focus × 0.6)
```

Focus is weighted higher because research and common sense both agree: you can study while tired, but you can't study while truly distracted.

For long sessions (over 2 hours), a small penalty is applied, since the quality of attention generally drops beyond that.

### Quality Tiers

| Score | Label        |
|-------|--------------|
| ≥ 4.0 | Excellent    |
| ≥ 3.0 | Decent       |
| ≥ 2.0 | Struggling   |
| < 2.0 | Burnout Risk |

### Advice Tree

The advice is not random. Each piece is triggered by a specific condition:

- Low mood (≤ 2) → suggests a walk or break before continuing  
- Low focus (≤ 2) → suggests removing distractions  
- Duration > 90 min → flags fatigue risk  
- Both mood and focus high (≥ 4) → tells you to protect that state  

### Trend Detection

After at least 3 sessions are logged, the program compares your first and most recent score from the last 3 entries. If the delta is greater than 0.5, it tells you you're improving. If it drops more than 0.5, it flags that.

---

## Features

| Feature | Terminal | Web |
|---|---|---|
| Log mood + focus + duration | ✅ | ✅ |
| Session quality rating | ✅ | ✅ |
| Subject-specific study tips | ✅ | ✅ |
| ASCII bar chart history | ✅ | — |
| Visual focus trend (canvas chart) | — | ✅ |
| Session history table | — | ✅ |
| Weekly summary | ✅ | ✅ (stats bar) |
| Pomodoro timer | ✅ (blocking) | ✅ (animated) |
| Trend analysis | ✅ | ✅ |

---

## Supported Subjects

`math` · `science` · `english` · `history` · `coding` · `general`

Each subject has its own set of tips drawn from practical study strategies.

---

## Sample Run (Terminal)

```
╔══════════════════════════════════════════════════════╗
║        SMART STUDY ASSISTANT  v1.0                   ║
║        Mood & Focus Tracker — AIML Project           ║
╚══════════════════════════════════════════════════════╝

  Loaded 4 previous session(s).

  [1]  Log a new study session
  ...

── New Session ──────────────────────────────────
  Subjects: math / science / english / history / coding / general
  What are you studying? coding

  Rate your current MOOD (1 = exhausted → 5 = excellent)
  Mood [1-5]: 4

  Rate your current FOCUS (1 = very distracted → 5 = deep flow)
  Focus [1-5]: 5

  How long did you study? (minutes): 60

  🟢 Session quality : EXCELLENT (score 4.6/5)
  → You're in the zone — keep this session going!

  💡 Tip for coding: Your brain compiles things during breaks.
```

---

## Design Decisions

**Why rule-based instead of ML?**  
The dataset here is tiny (one person's sessions) and constantly changing. Training an ML model on it would overfit almost immediately and give meaningless results. Rule-based logic is more honest for this scale — it does exactly what's written, nothing more.

**Why no external libraries?**  
The terminal app runs on pure Python 3 standard library. The dashboard uses only a Google Fonts import and native Canvas API. This makes the project easy to run on any machine without setup friction.

**Why two interfaces?**  
The terminal version is the "real" application — you can see and verify every line of logic. The web dashboard is a bonus that makes the data feel alive and is more presentation-friendly.

---

## Possible Extensions

- Export data to CSV for further analysis in Excel or pandas  
- Add sleep hours as an input variable  
- Build a simple linear regression model once enough sessions are logged  
- Notification/reminder system using OS-level alerts  
- Multi-user support with separate log files  

---

## Requirements

- Python 3.6 or later  
- Any modern browser (Chrome, Firefox, Edge) for the dashboard  
- No pip installs required  

---

## Author

[KISLAY KUMAR]  
Roll No: [25BAI10313]  
Department: [CSE (AIML)]  
Institution: [VIT BHOPAL]
