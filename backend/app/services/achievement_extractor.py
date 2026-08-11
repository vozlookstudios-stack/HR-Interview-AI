import re


def extract_achievements(achievements_text: str | None) -> list[str]:
    """
    Extract achievements from the achievements section.
    """

    if not achievements_text:
        return []

    achievements = []

    for raw_line in achievements_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Remove bullets
        line = re.sub(r"^[•\-\*]\s*", "", line)

        # Ignore empty lines
        if not line:
            continue

        # Ignore single numbers
        if re.fullmatch(r"\d+", line):
            continue

        # Remove duplicates
        if line not in achievements:
            achievements.append(line)

    return achievements