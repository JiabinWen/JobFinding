"""AI-based decision engine for job matching."""

from typing import Dict

from .config import CONFIG


class DecisionEngine:
    def score(self, job: Dict[str, str]) -> Dict[str, str]:
        """Compute match score and reason for a job posting."""
        # In real implementation, use NLP and ML models
        score = 0
        reason = []

        if any(title.lower() in job.get("title", "").lower() for title in CONFIG.preferences.job_titles):
            score += 50
            reason.append("Title matches user preference")

        if CONFIG.preferences.locations and job.get("location") in CONFIG.preferences.locations:
            score += 30
            reason.append("Preferred location")

        if "python" in job.get("description", "").lower():
            score += 20
            reason.append("Python mentioned in description")

        return {
            "id": job.get("id", ""),
            "score": str(score),
            "reason": "; ".join(reason) or "Low relevance",
        }
