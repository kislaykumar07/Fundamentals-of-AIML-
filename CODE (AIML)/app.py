import json
import os
import time
import random
from datetime import datetime, timedelta
from collections import defaultdict
import math



MOOD_LABELS = {
    1: "exhausted",
    2: "low",
    3: "okay",
    4: "good",
    5: "excellent"
}

FOCUS_LABELS = {
    1: "very distracted",
    2: "scattered",
    3: "moderate",
    4: "focused",
    5: "deep flow"
}

SUBJECT_TIPS = {
    "math":    ["Try Pomodoro 25-min blocks.",
                "Solve past papers first, theory second.",
                "Teach the concept out loud — works surprisingly well."],
    "science": ["Draw diagrams, not walls of text.",
                "Link new concepts to everyday examples.",
                "Focus on understanding the 'why', not just the 'what'."],
    "english": ["Read the passage twice before answering.",
                "Summarise every paragraph in one sentence.",
                "Vocabulary cards in odd 5-minute gaps."],
    "history": ["Build a timeline on paper first.",
                "Connect events with cause-and-effect arrows.",
                "Teach it to an imaginary student — seriously."],
    "coding":  ["Code a small toy project, not just tutorials.",
                "Debug slowly — read errors top-to-bottom.",
                "Take breaks: your brain compiles in the background."],
    "general": ["Break big goals into 20-min micro-tasks.",
                "Keep your phone in another room.",
                "Stand up every 45 minutes."]
}


def classify_session(mood: int, focus: int, duration_mins: int) -> dict:
    """
    Rule-based classifier that decides session quality and returns advice.
    Nothing fancy — just conditional logic, the way a human tutor would think.
    """
    score = (mood * 0.4) + (focus * 0.6)          # focus matters more
    duration_penalty = max(0, (duration_mins - 120) * 0.01)
    score = max(1, score - duration_penalty)

    if score >= 4.0:
        quality = "excellent"
        color   = "🟢"
    elif score >= 3.0:
        quality = "decent"
        color   = "🟡"
    elif score >= 2.0:
        quality = "struggling"
        color   = "🟠"
    else:
        quality = "burnout risk"
        color   = "🔴"

    # advice tree
    advice = []
    if mood <= 2:
        advice.append("Your mood is low — consider a 10-min walk before the next block.")
    if focus <= 2:
        advice.append("Focus is scattered. Close extra tabs, silence notifications, try 5 deep breaths.")
    if duration_mins > 90:
        advice.append("You've been at it a while. A proper break will actually make you faster overall.")
    if mood >= 4 and focus >= 4:
        advice.append("You're in the zone — keep this session going, avoid interruptions!")
    if not advice:
        advice.append("Steady progress. Keep the rhythm.")

    return {
        "quality": quality,
        "icon":    color,
        "score":   round(score, 2),
        "advice":  advice
    }


def naive_trend(entries: list) -> str:
    """Look at last N sessions and tell the user if things are getting better or worse."""
    if len(entries) < 3:
        return "Not enough data yet (need at least 3 sessions)."

    recent = entries[-3:]
    scores = [e.get("score", 3) for e in recent]

    delta = scores[-1] - scores[0]
    if delta > 0.5:
        return "📈 Trending upward — you're improving!"
    elif delta < -0.5:
        return "📉 Trending downward — review your sleep & break habits."
    else:
        return "➡️  Roughly stable — consistent is still good."




DATA_FILE = "study_log.json"


def load_log() -> list:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_log(entries: list):
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)



def ascii_bar(value: float, max_val: float = 5.0, width: int = 20) -> str:
    filled = int((value / max_val) * width)
    return "█" * filled + "░" * (width - filled)


def print_history_chart(entries: list):
    if not entries:
        print("  No data to show yet.")
        return

    recent = entries[-7:]          
    print(f"\n  {'Date':<12} {'Mood':^7} {'Focus':^7} {'Quality':<14} Bar (focus)")
    print("  " + "─" * 58)
    for e in recent:
        date_str = e["timestamp"][:10]
        mood_lbl = MOOD_LABELS.get(e["mood"], "?")[:4]
        focus_lbl = FOCUS_LABELS.get(e["focus"], "?")[:4]
        bar = ascii_bar(e["focus"])
        print(f"  {date_str:<12} {mood_lbl:<7} {focus_lbl:<7} {e['quality']:<14} {bar}")



def weekly_summary(entries: list):
    week_ago = datetime.now() - timedelta(days=7)
    week_entries = [
        e for e in entries
        if datetime.fromisoformat(e["timestamp"]) >= week_ago
    ]

    if not week_entries:
        print("  No sessions in the last 7 days.")
        return

    total_mins  = sum(e["duration_mins"] for e in week_entries)
    avg_mood    = sum(e["mood"]  for e in week_entries) / len(week_entries)
    avg_focus   = sum(e["focus"] for e in week_entries) / len(week_entries)
    sessions    = len(week_entries)

    
    subject_counts = defaultdict(int)
    for e in week_entries:
        subject_counts[e.get("subject", "general")] += e["duration_mins"]

    print(f"\n  ┌─── Weekly Summary ──────────────────────────┐")
    print(f"  │  Sessions this week : {sessions:<4}                  │")
    print(f"  │  Total study time   : {total_mins} mins              │")
    print(f"  │  Avg mood           : {avg_mood:.1f}/5 ({MOOD_LABELS.get(round(avg_mood),'?')})        │")
    print(f"  │  Avg focus          : {avg_focus:.1f}/5 ({FOCUS_LABELS.get(round(avg_focus),'?')})   │")
    print(f"  └─────────────────────────────────────────────┘")
    print(f"\n  Subject breakdown:")
    for subj, mins in sorted(subject_counts.items(), key=lambda x: -x[1]):
        bar = ascii_bar(mins, max_val=max(subject_counts.values()))
        print(f"    {subj:<12} {bar}  {mins} min")



def run_pomodoro(minutes: int = 25):
    print(f"\n  🍅 Pomodoro started — {minutes} minutes. Press Ctrl+C to stop early.\n")
    total_secs = minutes * 60
    try:
        for elapsed in range(total_secs):
            remaining = total_secs - elapsed
            mins, secs = divmod(remaining, 60)
            bar_width  = 30
            filled     = int((elapsed / total_secs) * bar_width)
            bar        = "█" * filled + "░" * (bar_width - filled)
            print(f"\r  [{bar}] {mins:02d}:{secs:02d} remaining", end="", flush=True)
            time.sleep(1)
        print("\n\n  ✅ Pomodoro complete! Take a 5-minute break.")
    except KeyboardInterrupt:
        print("\n\n  ⏹  Session interrupted early.")




BANNER = """
╔══════════════════════════════════════════════════════╗
║        SMART STUDY ASSISTANT  v1.0                   ║
║        Mood & Focus Tracker — AIML Project           ║
╚══════════════════════════════════════════════════════╝
"""

MENU = """
  [1]  Log a new study session
  [2]  View recent sessions (chart)
  [3]  Weekly summary
  [4]  Start Pomodoro timer (25 min)
  [5]  Get study tips for a subject
  [6]  View my trend
  [0]  Exit
"""


def get_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            val = int(input(prompt))
            if lo <= val <= hi:
                return val
            print(f"  Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  That doesn't look like a number. Try again.")


def log_session(entries: list):
    print("\n── New Session ──────────────────────────────────")

    print("  Subjects: math / science / english / history / coding / general")
    subject = input("  What are you studying? ").strip().lower() or "general"
    if subject not in SUBJECT_TIPS:
        subject = "general"

    print("\n  Rate your current MOOD (1 = exhausted → 5 = excellent)")
    mood = get_int("  Mood [1-5]: ", 1, 5)

    print("\n  Rate your current FOCUS (1 = very distracted → 5 = deep flow)")
    focus = get_int("  Focus [1-5]: ", 1, 5)

    duration = get_int("\n  How long did you study? (minutes): ", 1, 600)

    notes = input("\n  Any notes? (optional, press Enter to skip): ").strip()

    result = classify_session(mood, focus, duration)

    entry = {
        "timestamp":    datetime.now().isoformat(),
        "subject":      subject,
        "mood":         mood,
        "focus":        focus,
        "duration_mins": duration,
        "quality":      result["quality"],
        "score":        result["score"],
        "notes":        notes
    }
    entries.append(entry)
    save_log(entries)

    print(f"\n  {result['icon']} Session quality : {result['quality'].upper()} (score {result['score']}/5)")
    for tip in result["advice"]:
        print(f"  → {tip}")

    
    tips = SUBJECT_TIPS.get(subject, SUBJECT_TIPS["general"])
    print(f"\n  💡 Tip for {subject}: {random.choice(tips)}")


def show_tips():
    print("\n  Pick a subject:")
    subjects = list(SUBJECT_TIPS.keys())
    for i, s in enumerate(subjects, 1):
        print(f"  [{i}] {s}")
    idx = get_int("  Choice: ", 1, len(subjects))
    subject = subjects[idx - 1]
    print(f"\n  Tips for {subject}:")
    for tip in SUBJECT_TIPS[subject]:
        print(f"   • {tip}")


def main():
    print(BANNER)
    entries = load_log()
    print(f"  Loaded {len(entries)} previous session(s).\n")

    while True:
        print(MENU)
        choice = get_int("  Your choice: ", 0, 6)

        if choice == 1:
            log_session(entries)
        elif choice == 2:
            print_history_chart(entries)
        elif choice == 3:
            weekly_summary(entries)
        elif choice == 4:
            run_pomodoro(25)
        elif choice == 5:
            show_tips()
        elif choice == 6:
            print(f"\n  {naive_trend(entries)}")
        elif choice == 0:
            print("\n  👋 Good luck with your studies!\n")
            break


if __name__ == "__main__":
    main()
