import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CANDIDATES_FILE = os.path.join(DATA_DIR, "candidates.csv")
REQUIREMENTS_FILE = os.path.join(DATA_DIR, "requirements.csv")
OUTREACH_FILE = os.path.join(DATA_DIR, "outreach.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def load_candidates() -> pd.DataFrame:
    if os.path.exists(CANDIDATES_FILE):
        return pd.read_csv(CANDIDATES_FILE)
    return pd.DataFrame(columns=[
        "name", "headline", "location", "years_experience", "current_company",
        "skills", "linkedin_url", "email", "connections",
        "ai_score", "ai_reasoning", "status", "notes", "job_title",
    ])


def save_candidates(df: pd.DataFrame):
    df.to_csv(CANDIDATES_FILE, index=False)


def load_requirements() -> pd.DataFrame:
    if os.path.exists(REQUIREMENTS_FILE):
        return pd.read_csv(REQUIREMENTS_FILE)
    return pd.DataFrame(columns=[
        "id", "job_title", "required_skills", "min_years_exp",
        "location", "num_candidates", "status", "created_at",
    ])


def save_requirements(df: pd.DataFrame):
    df.to_csv(REQUIREMENTS_FILE, index=False)


def load_outreach() -> pd.DataFrame:
    if os.path.exists(OUTREACH_FILE):
        return pd.read_csv(OUTREACH_FILE)
    return pd.DataFrame(columns=[
        "candidate_name", "linkedin_url", "email", "job_title",
        "message_sent", "follow_up_1", "follow_up_2",
        "connection_status", "reply_received", "sent_at",
    ])


def save_outreach(df: pd.DataFrame):
    df.to_csv(OUTREACH_FILE, index=False)
