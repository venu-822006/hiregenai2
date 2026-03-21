import re

SKILLS_DB: dict[str, list[str]] = {
    "Programming Languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "kotlin",
        "swift", "php", "ruby", "scala", "dart", "r", "matlab", "perl", "bash", "shell",
    ],
    "Web Frameworks": [
        "react", "angular", "vue", "svelte", "nextjs", "nuxtjs", "django", "flask",
        "fastapi", "express", "nestjs", "spring", "rails", "laravel", "asp.net",
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "mssql",
        "cassandra", "dynamodb", "elasticsearch", "firebase", "supabase",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
        "jenkins", "circleci", "github actions", "gitlab ci", "helm", "nginx", "apache",
    ],
    "Machine Learning": [
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "huggingface", "openai", "langchain", "opencv", "xgboost", "lightgbm",
    ],
    "Tools & Practices": [
        "git", "agile", "scrum", "jira", "confluence", "figma", "linux", "rest", "graphql",
        "grpc", "microservices", "ci/cd", "tdd", "ddd", "solid", "oauth", "jwt",
    ],
    "Data Engineering": [
        "spark", "hadoop", "kafka", "airflow", "dbt", "bigquery", "snowflake", "redshift",
        "databricks", "tableau", "power bi", "looker",
    ],
    "Mobile": [
        "android", "ios", "react native", "flutter", "xamarin",
    ],
}


def extract_skills(text: str) -> list[dict]:
    text_lower = text.lower()
    found: dict[str, float] = {}

    total_words = max(len(text_lower.split()), 1)

    for category, skills in SKILLS_DB.items():
        for skill in skills:
            pattern = r"\b" + re.escape(skill) + r"\b"
            matches = re.findall(pattern, text_lower)
            if matches:
                count = len(matches)
                raw_freq = min(count / total_words * 1000, 100)
                pct = round(min(50 + raw_freq * 5, 100), 1)
                found[skill] = pct

    return [{"name": k, "pct": v} for k, v in sorted(found.items(), key=lambda x: -x[1])]
