import re


def extract_skills(skills_text: str) -> dict[str, list[str]]:
    """
    Convert the Skills section into structured categories.

    Example:
    Programming: Python, Java

    becomes

    {
        "programming": ["Python", "Java"]
    }
    """

    skills: dict[str, list[str]] = {}

    if not skills_text:
        return skills

    for raw_line in skills_text.splitlines():

        line = raw_line.strip()

        # Remove bullet symbols
        line = line.lstrip("•-* ").strip()

        if not line:
            continue

        if ":" not in line:
            continue

        category, values = line.split(":", 1)

        category = category.strip().lower()

        category = re.sub(
            r"[^a-z0-9]+",
            "_",
            category,
        ).strip("_")

        skill_list = [
            skill.strip()
            for skill in values.split(",")
            if skill.strip()
        ]

        if category not in skills:
            skills[category] = []

        for skill in skill_list:

            if skill not in skills[category]:
                skills[category].append(skill)

    return skills