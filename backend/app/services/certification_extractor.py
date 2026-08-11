import re


def extract_certifications(certification_text: str | None) -> list[dict]:
    """
    Extract structured certifications from the Certifications section.
    """

    if not certification_text:
        return []

    certifications = []

    lines = [
        line.strip()
        for line in certification_text.splitlines()
        if line.strip()
    ]

    year_pattern = re.compile(r"\b(?:19|20)\d{2}\b")
    for line in lines:

        line = line.lstrip("•-* ").strip()

        if not line:
            continue

        certification = {
            "name": line,
            "issuer": None,
            "organization": None,
            "year": None,
        }

        # -----------------------------
        # Year
        # -----------------------------
        year_match = year_pattern.search(line)

        if year_match:
            certification["year"] = year_match.group()

        # -----------------------------
        # Oracle
        # -----------------------------
        if "Oracle" in line:
            certification["issuer"] = "Oracle"

        # -----------------------------
        # NPTEL
        # -----------------------------
        elif "NPTEL" in line:

            certification["issuer"] = "NPTEL"

            org = re.search(r"\((.*?)\)", line)

            if org:
                certification["organization"] = org.group(1)

        # -----------------------------
        # Intel
        # -----------------------------
        elif "Intel" in line:

            certification["issuer"] = "Intel"

        certifications.append(certification)

    return certifications