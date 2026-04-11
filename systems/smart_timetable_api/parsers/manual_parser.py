import re

# Map short and full day names to standard capitalized form
day_lookup = {
    "mon": "Monday",
    "monday": "Monday",
    "tue": "Tuesday",
    "tuesday": "Tuesday",
    "wed": "Wednesday",
    "wednesday": "Wednesday",
    "thu": "Thursday",
    "thursday": "Thursday",
    "fri": "Friday",
    "friday": "Friday",
    "sat": "Saturday",
    "saturday": "Saturday",
    "sun": "Sunday",
    "sunday": "Sunday"
}

def split_entries(raw_text: str) -> list:
    """
    Split raw text into individual timetable entries.
    Tries comma split first; falls back to day-boundary split if no comma.
    """
    # Try splitting by comma first
    entries = [e.strip() for e in raw_text.split(",") if e.strip()]
    if len(entries) >= 2:
        return entries

    # Regex to match day names
    day_pattern = (
        r'\b(mon|tue|wed|thu|fri|sat|sun|'
        r'monday|tuesday|wednesday|thursday|'
        r'friday|saturday|sunday)\b'
    )

    matches = list(re.finditer(day_pattern, raw_text, re.IGNORECASE))
    
    if len(matches) >= 2:
        entries = []
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i < len(matches) - 1 else len(raw_text)
            chunk = raw_text[start:end].strip()
            if chunk:
                entries.append(chunk)
        return entries

    # Fallback: treat the whole text as a single entry
    return [raw_text]

def parse(raw_text: str) -> dict:
    """
    Main parser function.
    Converts raw timetable text into structured dictionary.
    Handles:
        - Short day names (Mon, Tue)
        - Missing commas
        - Multiple spaces
        - Multi-word subjects
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Input text cannot be empty")

    # Normalize whitespace
    raw_text = re.sub(r'\s+', ' ', raw_text.strip())

    entries = split_entries(raw_text)
    if not entries:
        raise ValueError("Could not find any timetable entries")

    result = {}

    for entry in entries:
        entry = re.sub(r'\s+', ' ', entry.strip())
        words = entry.split()

        if len(words) < 3:
            raise ValueError(
                f"Entry '{entry}' is too short. Format should be: DAY TIME SUBJECT"
            )

        raw_day = words[0].lower()
        day = day_lookup.get(raw_day)
        if day is None:
            raise ValueError(
                f"'{words[0]}' is not a recognized day. Use Monday, Tuesday, etc or Mon, Tue, etc"
            )

        time = words[1]
        subject = " ".join(words[2:])

        if day not in result:
            result[day] = []

        result[day].append({
            "time": time,
            "subject": subject
        })

    return result

