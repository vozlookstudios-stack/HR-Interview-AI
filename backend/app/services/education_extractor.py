import re


def extract_education(education_text: str | None) -> list[dict]:
    """
    Extract education details from the Education section.
    """

    if not education_text:
        return []

    lines = [
        line.strip()
        for line in education_text.splitlines()
        if line.strip()
    ]

    education = []

    current = {
        "degree": None,
        "branch": None,
        "institution": None,
        "start_year": None,
        "end_year": None,
    }

    year_pattern = re.compile(r"\b(?:19|20)\d{2}\s*[–-]\s*(?:19|20)\d{2}\b")
    for line in lines:

        # Detect year range
        if year_pattern.search(line):

            years = re.findall(r"(?:19|20)\d{2}", line)
            if len(years) >= 2:
                current["start_year"] = years[0]
                current["end_year"] = years[1]

            continue

        # Degree line
        current["institution"] = line

        degree_match = re.match(
            r"(B\.?E\.?|B\.?Tech|M\.?E\.?|M\.?Tech|BSc|MSc|MBA)",
            line,
            re.IGNORECASE,
        )

        if degree_match:

            current["degree"] = degree_match.group()

            remaining = line.replace(
                degree_match.group(),
                "",
                1,
            ).strip()

            parts = remaining.split()

            if len(parts) >= 2:

                current["branch"] = " ".join(parts[:3])

                current["institution"] = " ".join(parts[3:])

    education.append(current)

    return education