"""
Resume Analyzer Module
Detects technical skills, calculates an ATS score, and generates
improvement suggestions based on the resume text.
"""


# ---------------------------------------------------------------------------
# Skills Database — grouped by category
# ---------------------------------------------------------------------------
SKILLS_DATABASE = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "javascript", "typescript",
        "ruby", "go", "rust", "kotlin", "swift", "php", "r",
    ],
    "Web Development": [
        "html", "css", "react", "angular", "vue", "node.js", "express",
        "django", "flask", "fastapi", "next.js", "tailwind",
        "bootstrap", "rest api", "graphql",
    ],
    "Data Science & AI": [
        "machine learning", "deep learning", "natural language processing",
        "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
        "pandas", "numpy", "matplotlib", "data analysis", "data visualization",
        "generative ai", "large language models", "nlp",
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "firebase", "redis",
        "sqlite", "oracle", "dynamodb",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
        "ci/cd", "terraform", "linux", "git", "github",
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "project management", "agile", "scrum", "time management",
        "critical thinking", "collaboration",
    ],
}


def detect_skills(text):
    """
    Scan resume text and return detected skills grouped by category.

    Args:
        text (str): The full resume text.

    Returns:
        dict: {category: [matched_skills, ...]}
    """
    text_lower = text.lower()
    detected = {}

    for category, skills in SKILLS_DATABASE.items():
        found = [skill for skill in skills if skill in text_lower]
        if found:
            detected[category] = found

    return detected


def calculate_ats_score(detected_skills):
    """
    Calculate an ATS (Applicant Tracking System) score out of 100.

    Scoring formula:
      - Each detected skill contributes points.
      - Bonus points for covering multiple categories.

    Args:
        detected_skills (dict): Output of detect_skills().

    Returns:
        int: ATS score between 0 and 100.
    """
    total_skills_in_db = sum(len(v) for v in SKILLS_DATABASE.values())
    total_detected = sum(len(v) for v in detected_skills.values())

    # Base score: proportion of skills found (0-70 points)
    skill_score = (total_detected / total_skills_in_db) * 70

    # Category coverage bonus (0-30 points)
    total_categories = len(SKILLS_DATABASE)
    categories_covered = len(detected_skills)
    category_score = (categories_covered / total_categories) * 30

    ats_score = int(min(skill_score + category_score, 100))
    return ats_score


def generate_suggestions(detected_skills, ats_score):
    """
    Generate actionable suggestions to improve the resume.

    Args:
        detected_skills (dict): Output of detect_skills().
        ats_score (int): The calculated ATS score.

    Returns:
        list[str]: A list of suggestion strings.
    """
    suggestions = []

    # Check for missing categories
    missing_categories = [
        cat for cat in SKILLS_DATABASE if cat not in detected_skills
    ]

    for category in missing_categories:
        example_skills = ", ".join(SKILLS_DATABASE[category][:4]).title()
        suggestions.append(
            f"Consider adding <strong>{category}</strong> skills to your resume "
            f"(e.g., {example_skills})."
        )

    # General suggestions based on score
    if ats_score < 30:
        suggestions.append(
            "Your ATS score is currently low. Focus on incorporating more "
            "relevant technical skills and keywords that align with target "
            "job descriptions."
        )
    if ats_score < 60:
        suggestions.append(
            "Include a dedicated <strong>Projects</strong> section to "
            "demonstrate hands-on experience with the technologies you list."
        )

    if "Data Science & AI" not in detected_skills:
        suggestions.append(
            "AI and ML skills are increasingly sought after across "
            "industries. Consider adding coursework or projects in "
            "Machine Learning or Data Science."
        )

    if "Cloud & DevOps" not in detected_skills:
        suggestions.append(
            "Cloud platform experience (AWS, Azure, Docker) can "
            "significantly strengthen your profile for modern "
            "engineering positions."
        )

    # Always-useful tips
    suggestions.append(
        "Use a clean, ATS-compatible resume format. Avoid tables, "
        "embedded images, and complex multi-column layouts."
    )
    suggestions.append(
        "Tailor your resume to each specific role by mirroring the "
        "keywords and competencies listed in the job posting."
    )

    return suggestions
