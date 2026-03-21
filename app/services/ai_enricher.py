import json
import hashlib
import time
from typing import Dict, Any, List
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from app.utils.logger import get_logger
from config import get_config

logger = get_logger(__name__)
config = get_config()

# Pydantic models for strict JSON validation
class AISkills(BaseModel):
    skills: List[str] = Field(..., min_items=0)

class AIRoles(BaseModel):
    roles: List[str] = Field(..., min_items=0)

class AIExperience(BaseModel):
    experience_level: str = Field(..., min_length=1, max_length=50)

class AISuggestions(BaseModel):
    suggestions: List[str] = Field(..., min_items=0)

class AIResponse(BaseModel):
    skills: List[str] = Field(..., description="Skills extracted/enriched from resume")
    roles: List[str] = Field(..., description="Professional roles detected")
    experience_level: str = Field(..., description="Experience level: junior/mid/senior/executive")
    suggestions: List[str] = Field(..., description="Tailored suggestions based on gaps vs job_desc")

client = OpenAI(api_key=config.AI_API_KEY, base_url=config.AI_BASE_URL) if config.AI_API_KEY else None

def hash_content(resume_text: str, job_desc: str) -> str:
    """Hash inputs to detect identical outputs."""
    combined = f"{resume_text[:2000]}|{job_desc[:2000]}"
    return hashlib.md5(combined.encode()).hexdigest()

def craft_prompt(resume_text: str, job_desc: str, baseline_skills: List[Dict[str, Any]]) -> str:
    skills_str = ", ".join([s["name"] for s in baseline_skills[:20]]) if baseline_skills else "none"
    prompt = f"""Analyze this resume text and job description. Use ONLY content provided. Do NOT generate generic/random outputs.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_desc}

BASELINE SKILLS DETECTED: {skills_str}

Extract/enrich:
- skills: relevant technical/professional skills (array strings, add semantic matches/gaps)
- roles: professional roles/titles detected (array strings)
- experience_level: "junior" | "mid" | "senior" | "executive" based on years/positions
- suggestions: 3-5 specific improvements for skill gaps/ATS/job match (array strings, derived from resume vs job_desc)

Respond with STRICT JSON ONLY, no other text:
{{
  "skills": [...],
  "roles": [...],
  "experience_level": "...",
  "suggestions": [...]
}}"""
    return prompt

def call_ai(prompt: str, max_retries: int = 3) -> Dict[str, Any] | None:
    if not client:
        logger.warning("AI client not configured")
        return None

    input_hash = hash_content(prompt, "")  # Simplified hash
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=config.AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Low for consistency but variability
                max_tokens=800,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            # Parse and validate
            ai_data = json.loads(content)
            validated = AIResponse(**ai_data)
            logger.info("AI response valid", attempt=attempt, skills_len=len(validated.skills))
            return validated.model_dump()
        except (json.JSONDecodeError, ValidationError, Exception) as e:
            logger.warning(f"AI attempt {attempt+1} failed: {str(e)}")
            time.sleep(1)
    logger.error("AI all retries failed")
    return None

def merge_hybrid(baseline: Dict[str, Any], ai_data: Dict[str, Any] | None) -> Dict[str, Any]:
    if not ai_data:
        logger.info("Using baseline fallback")
        return {
            "ai_roles": [],
            "ai_experience_level": "",
            "ai_suggestions": [],
            "hybrid_skills": [{"name": s["name"], "pct": s["pct"]} for s in baseline.get("skills", [])],
        }

    # Dedup/merge skills: baseline + AI uniques
    baseline_skill_names = {s["name"].lower() for s in baseline.get("skills", [])}
    ai_skills = ai_data["skills"]
    hybrid_skills = [{"name": skill, "pct": 80.0} for skill in ai_skills if skill.lower() not in baseline_skill_names]
    hybrid_skills.extend(baseline.get("skills", []))
    hybrid_skills.sort(key=lambda x: x.get("pct", 0), reverse=True)

    # Suggestions: AI primary + baseline recs for gaps
    suggestions = ai_data["suggestions"][:5]
    baseline_recs = baseline.get("recommendations", [])[:3]
    suggestions.extend([r["text"] for r in baseline_recs if r["type"] == "HIGH"])

    result = {
        "ai_roles": ai_data["roles"],
        "ai_experience_level": ai_data["experience_level"],
        "ai_suggestions": ai_data["suggestions"],
        "hybrid_skills": hybrid_skills[:20],  # Limit
        "recommendations": [{"type": "AI", "text": s} for s in suggestions[:5]],
    }
    logger.info("Merged hybrid", ai_skills_len=len(ai_data["skills"]), hybrid_len=len(hybrid_skills))
    return result

def enrich_with_ai(resume_text: str, job_desc: str, baseline: Dict[str, Any]) -> Dict[str, Any]:
    """Main hybrid function: AI enrich + merge."""
    prompt = craft_prompt(resume_text, job_desc, baseline.get("skills", []))
    ai_response = call_ai(prompt)
    return merge_hybrid(baseline, ai_response)

