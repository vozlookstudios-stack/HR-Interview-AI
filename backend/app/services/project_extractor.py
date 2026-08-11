import re


TECHNOLOGIES = {
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "React.js",
    "Next.js",
    "Angular",
    "Vue",
    "Node.js",
    "Express",
    "Flask",
    "FastAPI",
    "Django",
    "Spring",
    "Spring Boot",
    "MySQL",
    "MongoDB",
    "PostgreSQL",
    "SQLite",
    "Firebase",
    "Docker",
    "Git",
    "GitHub",
    "TensorFlow",
    "PyTorch",
    "OpenCV",
    "YOLO",
    "Gemini",
    "Gemini API",
    "REST API",
    "REST APIs",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
}

def extract_technologies(text: str) -> list[str]:
    """
    Extract technologies mentioned inside project descriptions.
    """

    found = []

    for technology in sorted(TECHNOLOGIES):

        pattern = rf"\b{re.escape(technology)}\b"

        if re.search(pattern, text, re.IGNORECASE):

            found.append(technology)

    return found
def extract_projects(project_text: str | None) -> list[dict]:
    """
    Convert the Projects section into structured project data.
    """

    if not project_text:
        return []

    lines = [
        line.strip()
        for line in project_text.splitlines()
        if line.strip()
    ]

    projects = []
    current_project = None

    for line in lines:

        # Description line
        if line.startswith(("•", "-", "*")):

            if current_project is not None:

                description = line.lstrip("•-* ").strip()

                if description:
                    current_project["description"].append(
                        description
                    )

            continue

        # Save previous project
        if current_project is not None:

            text = " ".join(
                current_project["description"]
            )

            current_project["technologies"] = (
                extract_technologies(text)
            )

            projects.append(current_project)

        # Start new project
        current_project = {
            "name": line,
            "description": [],
            "technologies": [],
        }

    # Save last project
    if current_project is not None:

        text = " ".join(
            current_project["description"]
        )

        current_project["technologies"] = (
            extract_technologies(text)
        )

        projects.append(current_project)

    return projects
