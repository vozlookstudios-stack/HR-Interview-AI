import re


MONTH_PATTERN = (
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
)


def extract_experience(experience_text: str | None) -> list[dict]:
    """
    Extract structured work experience from the Experience section.
    """

    if not experience_text:
        return []

    lines = [
        line.strip()
        for line in experience_text.splitlines()
        if line.strip()
    ]

    experiences = []
    current = None

    date_pattern = re.compile(
        rf"{MONTH_PATTERN}\s+\d{{4}}\s*[–-]\s*{MONTH_PATTERN}\s+\d{{4}}"
    )

    for line in lines:

        # -----------------------------
        # Responsibilities
        # -----------------------------
        if line.startswith(("•", "-", "*")):

            if current is not None:

                responsibility = line.lstrip("•-* ").strip()

                if responsibility:
                    current["responsibilities"].append(
                        responsibility
                    )

            continue

        # -----------------------------
        # Date Line
        # -----------------------------
        if date_pattern.search(line):

            if current is not None:

                dates = re.split(r"\s*[–-]\s*", line)

                if len(dates) == 2:

                    current["start_date"] = dates[0].strip()
                    current["end_date"] = dates[1].strip()

            continue

        # -----------------------------
        # New Experience
        # -----------------------------
        if current is not None:
            experiences.append(current)

        role = line
        organization = ""

        if "–" in line:
            role, organization = line.split("–", 1)

        elif "-" in line:
            role, organization = line.split("-", 1)

        current = {
            "role": role.strip(),
            "organization": organization.strip(),
            "start_date": None,
            "end_date": None,
            "responsibilities": [],
        }

    # -----------------------------
    # Last Experience
    # -----------------------------
    if current is not None:
        experiences.append(current)

    return experiences