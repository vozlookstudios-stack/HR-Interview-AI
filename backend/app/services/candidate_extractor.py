import re


def extract_candidate_info(header_text: str) -> dict[str, str | None]:
    """
    Extract candidate information from the resume header.
    """

    candidate = {
        "name": None,
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
    }

    if not header_text:
        return candidate

    lines = [
        line.strip()
        for line in header_text.splitlines()
        if line.strip() and line.strip() != "|"
    ]

    # -----------------------------
    # Name
    # -----------------------------
    if lines:
        candidate["name"] = lines[0]

    # -----------------------------
    # Email
    # -----------------------------
    email_pattern = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    email_match = email_pattern.search(header_text)

    if email_match:
        candidate["email"] = email_match.group()

    # -----------------------------
    # Phone
    # -----------------------------
    phone_pattern = re.compile(
        r"(?:\+91[- ]?)?[6-9]\d{9}"
    )

    phone_match = phone_pattern.search(header_text)

    if phone_match:
        candidate["phone"] = phone_match.group()

    # -----------------------------
    # LinkedIn
    # -----------------------------
    linkedin_pattern = re.compile(
        r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s|]+",
        re.IGNORECASE,
    )

    linkedin_match = linkedin_pattern.search(header_text)

    if linkedin_match:
        candidate["linkedin"] = linkedin_match.group().rstrip(".,;)")

    # -----------------------------
    # GitHub
    # -----------------------------
    github_pattern = re.compile(
        r"(?:https?://)?(?:www\.)?github\.com/[^\s|]+",
        re.IGNORECASE,
    )

    github_match = github_pattern.search(header_text)

    if github_match:
        candidate["github"] = github_match.group().rstrip(".,;)")

    return candidate