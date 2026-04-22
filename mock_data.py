import random
import pandas as pd
from faker import Faker

fake = Faker()

SKILLS_POOL = {
    "AWS Data Engineer": ["AWS", "S3", "Glue", "Redshift", "Athena", "Lambda", "EMR", "Spark", "Python", "SQL", "Airflow", "Kafka", "Terraform", "Data Lake"],
    "Frontend Developer": ["React", "TypeScript", "JavaScript", "CSS", "HTML", "Next.js", "Redux", "GraphQL", "Tailwind", "Vue.js"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Jenkins", "Terraform", "AWS", "Azure", "Ansible", "Linux", "Prometheus"],
    "Data Scientist": ["Python", "ML", "TensorFlow", "PyTorch", "Pandas", "NumPy", "SQL", "Tableau", "Statistics", "NLP"],
    "Backend Developer": ["Python", "Java", "Node.js", "REST APIs", "PostgreSQL", "Redis", "Docker", "Microservices", "Spring Boot", "FastAPI"],
}

COMPANIES = [
    "Google", "Amazon", "Microsoft", "Meta", "Netflix", "Uber", "Airbnb",
    "Stripe", "Atlassian", "Canva", "Afterpay", "REA Group", "Seek",
    "Commonwealth Bank", "Westpac", "Telstra", "Optus", "Deloitte", "KPMG",
]

LOCATIONS = ["Melbourne, VIC", "Sydney, NSW", "Brisbane, QLD", "Remote", "Perth, WA", "Adelaide, SA"]

HEADLINES = [
    "Senior {role} @ {company}",
    "{role} | {company}",
    "Lead {role} at {company}",
    "Principal {role} | Open to opportunities",
    "{role} @ {company} | {skill} specialist",
]


def generate_candidates(job_title: str, count: int = 20) -> pd.DataFrame:
    skills_pool = SKILLS_POOL.get(job_title, SKILLS_POOL["AWS Data Engineer"])
    candidates = []

    for _ in range(count):
        years_exp = random.randint(1, 15)
        num_skills = random.randint(4, 10)
        candidate_skills = random.sample(skills_pool, min(num_skills, len(skills_pool)))
        company = random.choice(COMPANIES)
        headline_template = random.choice(HEADLINES)
        headline = headline_template.format(
            role=job_title,
            company=company,
            skill=random.choice(candidate_skills),
        )

        candidates.append({
            "name": fake.name(),
            "headline": headline,
            "location": random.choice(LOCATIONS),
            "years_experience": years_exp,
            "current_company": company,
            "skills": ", ".join(candidate_skills),
            "linkedin_url": f"https://linkedin.com/in/{fake.user_name()}",
            "email": fake.email(),
            "connections": random.randint(200, 5000),
            "ai_score": None,
            "ai_reasoning": None,
            "status": "New",
            "notes": "",
        })

    return pd.DataFrame(candidates)
