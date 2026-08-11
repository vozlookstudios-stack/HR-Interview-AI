def calculate_resume_score(profile: dict) -> dict:
    """
    Calculate a resume score based on extracted profile data.
    """

    skills_score = min(
        sum(len(v) for v in profile.get("skills", {}).values()),
        20,
    )

    experience_score = min(
        len(profile.get("experience", [])) * 10,
        20,
    )

    projects_score = min(
        len(profile.get("projects", [])) * 8,
        24,
    )

    education_score = (
        10 if profile.get("education") else 0
    )

    certifications_score = min(
        len(profile.get("certifications", [])) * 4,
        16,
    )

    achievements_score = min(
        len(profile.get("achievements", [])) * 2,
        10,
    )

    overall = (
        skills_score
        + experience_score
        + projects_score
        + education_score
        + certifications_score
        + achievements_score
    )

    return {
        "overall": overall,
        "skills": skills_score,
        "experience": experience_score,
        "projects": projects_score,
        "education": education_score,
        "certifications": certifications_score,
        "achievements": achievements_score,
    }