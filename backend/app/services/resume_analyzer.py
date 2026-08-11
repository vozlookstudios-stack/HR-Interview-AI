import re

from app.services.candidate_extractor import extract_candidate_info
from app.services.skill_extractor import extract_skills
from app.services.achievement_extractor import extract_achievements
from app.services.project_extractor import extract_projects
from app.services.education_extractor import extract_education
from app.services.experience_extractor import extract_experience
from app.services.certification_extractor import extract_certifications
from app.services.resume_score import calculate_resume_score

# ============================================================
# Resume Section Aliases
# ============================================================

SECTION_ALIASES = {
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "technologies",
        "technical expertise",
    },

    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internships",
        "internship",
        "work history",
    },

    "projects": {
        "projects",
        "academic projects",
        "personal projects",
        "project experience",
        "major projects",
    },

    "education": {
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
        "educational background",
    },

    "certifications": {
        "certifications",
        "certificates",
        "licenses and certifications",
        "courses and certifications",
    },

    "achievements": {
        "achievements",
        "achievements activities",
        "achievements & activities",
        "awards",
        "awards and achievements",
        "activities",
        "accomplishments",
    },
}


# ============================================================
# 1. Clean Resume Text
# ============================================================

def clean_resume_text(text: str) -> str:
    """Clean and normalize extracted resume text."""

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Clean markdown-style mailto links
    text = re.sub(
        r"\[([^\]]+)\]\(mailto:[^)]+\)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace("\xa0", " ")

    # Normalize spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# ============================================================
# 2. Normalize Section Heading
# ============================================================

def normalize_heading(line: str) -> str:
    """Normalize potential section headings."""

    line = line.strip().lower()

    line = line.rstrip(":|-")

    line = re.sub(
        r"\s+",
        " ",
        line,
    )

    return line.strip()


# ============================================================
# 3. Identify Section
# ============================================================

def identify_section(line: str) -> str | None:
    """Identify whether a line is a resume section heading."""

    normalized = normalize_heading(line)

    for section, aliases in SECTION_ALIASES.items():

        if normalized in aliases:
            return section

    return None


# ============================================================
# 4. Detect Sections
# ============================================================

def detect_sections(text: str) -> dict[str, str]:
    """Split resume into major sections."""

    cleaned_text = clean_resume_text(text)

    sections = {
        "header": [],
        "skills": [],
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
        "achievements": [],
    }

    current_section = "header"

    for raw_line in cleaned_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        detected_section = identify_section(line)

        if detected_section:

            current_section = detected_section

            continue

        sections[current_section].append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
    }


# ============================================================
# 10. Main Resume Analyzer
# ============================================================

def analyze_resume(text: str) -> dict:
    """
    Analyze resume and create structured candidate data.
    """

    # Clean text
    cleaned_text = clean_resume_text(text)

    # Detect sections
    sections = detect_sections(
        cleaned_text
    )

    # Candidate information
    candidate_info = extract_candidate_info(
        sections.get("header", "")
    )

    # Skills
    structured_skills = extract_skills(
        sections.get("skills", "")
    )
    # Achievements
    structured_achievements = extract_achievements(
        sections.get("achievements", "")
    )

    # Experience
    structured_experience = extract_experience(
        sections.get("experience", "")
    )

    structured_projects = extract_projects(
        sections.get("projects", "")
    )
    structured_education = extract_education(
        sections.get("education", "")
    )
    structured_certifications = extract_certifications(
        sections.get("certifications", "")
)

    # Sections that contain content
    sections_found = [
        section
        for section, content in sections.items()
        if content
    ]

    # Candidate profile
    structured_profile = {
        "candidate": candidate_info,
        "skills": structured_skills,
        "experience": structured_experience,
        "projects": structured_projects,
        "education": structured_education,
        "certifications": structured_certifications,
        "achievements": structured_achievements,
    }

    resume_score = calculate_resume_score(
        structured_profile
    )

    return {
        "characters": len(cleaned_text),
        "sections_found": sections_found,
        "structured_profile": structured_profile,
        "resume_score": resume_score,
        "sections": sections,
    }
