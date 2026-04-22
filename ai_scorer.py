import os
import json
import random

# Set to True once you have a real Anthropic API key in .env
USE_REAL_API = False

try:
    import anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        USE_REAL_API = True
except ImportError:
    pass


def score_candidate(candidate: dict, job_spec: dict) -> dict:
    """Score a candidate against a job spec. Returns score (0-100) + reasoning."""
    if USE_REAL_API:
        return _score_with_claude(candidate, job_spec)
    return _mock_score(candidate, job_spec)


def _score_with_claude(candidate: dict, job_spec: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""You are an expert technical recruiter. Score this candidate for the job spec below.

JOB SPEC:
- Title: {job_spec['job_title']}
- Required Skills: {job_spec['required_skills']}
- Minimum Years Experience: {job_spec['min_years_exp']}
- Location: {job_spec.get('location', 'Any')}

CANDIDATE:
- Name: {candidate['name']}
- Headline: {candidate['headline']}
- Current Company: {candidate['current_company']}
- Years Experience: {candidate['years_experience']}
- Skills: {candidate['skills']}
- Location: {candidate['location']}

Return ONLY a JSON object with these exact keys:
{{
  "score": <integer 0-100>,
  "reasoning": "<2-3 sentence explanation>",
  "strengths": ["<strength1>", "<strength2>"],
  "gaps": ["<gap1>", "<gap2>"]
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    text = message.content[0].text.strip()
    return json.loads(text)


def _mock_score(candidate: dict, job_spec: dict) -> dict:
    """Simulate AI scoring based on skill overlap."""
    required_skills = [s.strip().lower() for s in job_spec.get("required_skills", "").split(",")]
    candidate_skills = [s.strip().lower() for s in str(candidate.get("skills", "")).split(",")]

    overlap = [s for s in required_skills if any(s in cs for cs in candidate_skills)]
    skill_score = (len(overlap) / max(len(required_skills), 1)) * 50

    min_years = int(job_spec.get("min_years_exp", 3))
    years = int(candidate.get("years_experience", 0))
    exp_score = min(30, (years / max(min_years, 1)) * 30)

    noise = random.uniform(-5, 10)
    total = min(98, max(20, skill_score + exp_score + noise + 10))

    matched = overlap[:3] if overlap else ["General experience"]
    gaps = [s for s in required_skills if s not in [o.lower() for o in overlap]][:2]

    tier = "Strong match" if total >= 75 else "Partial match" if total >= 50 else "Weak match"

    return {
        "score": round(total),
        "reasoning": f"{tier} for {job_spec['job_title']}. Candidate has {years} years experience and matches {len(overlap)}/{len(required_skills)} required skills.",
        "strengths": matched if matched else ["Years of experience"],
        "gaps": gaps if gaps else ["None identified"],
    }


def generate_outreach_message(candidate: dict, job_spec: dict) -> str:
    """Generate a personalized outreach message."""
    if USE_REAL_API:
        return _message_with_claude(candidate, job_spec)
    return _mock_message(candidate, job_spec)


def _mock_message(candidate: dict, job_spec: dict) -> str:
    skills = candidate.get("skills", "").split(",")
    highlight_skill = skills[0].strip() if skills else "your background"

    return f"""Hi {candidate['name'].split()[0]},

I came across your profile and was impressed by your experience with {highlight_skill} at {candidate['current_company']}.

We're looking for a {job_spec['job_title']} and your background seems like a great fit. The role involves {job_spec.get('required_skills', 'relevant technologies')} and we'd love to hear more about your experience.

Would you be open to a quick 15-minute call this week?

Best regards"""


def _message_with_claude(candidate: dict, job_spec: dict) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Write a short, personalized LinkedIn outreach message (under 100 words) for this candidate.

Candidate: {candidate['name']}, currently at {candidate['current_company']}, skills: {candidate['skills']}
Role: {job_spec['job_title']} requiring {job_spec['required_skills']}

Be friendly, specific, and end with a soft CTA for a 15-min call. No subject line needed."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
