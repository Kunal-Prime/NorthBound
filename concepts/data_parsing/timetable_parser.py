def parse_timetable(raw_text: str) -> dict:
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

    result = {}
    entries = raw_text.split(",")
    
    for entry in entries:
        entry = entry.strip()

        if not entry:
            continue
        parts = entry.split()

        if len(parts) < 3:
            raise ValueError(
                f"Entry '{entry}' is not in correct format."
                f"expected : day time subject"
            )
        
        raw_day = parts[0].lower
        day = day_lookup.get(raw_day)

        if day is None:
            raise ValueError(f"'{parts[0]}' is not a recognized day")
        
        time = parts[1]
        subject = " ".join(parts[2:])

        if day not in result:
            result[day] = []

        result[day].append({
            "time": time,
            "subject": subject
        })
    return result