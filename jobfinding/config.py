"""Configuration management for JobFinding system."""

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

import json

@dataclass
class UserPreferences:
    job_titles: List[str] = field(default_factory=lambda: ["Python Developer"])
    locations: List[str] = field(default_factory=lambda: ["Remote"])
    salary_range: Optional[str] = None
    auto_apply: bool = False

@dataclass
class Config:
    resume_path: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    preferences: UserPreferences = field(default_factory=UserPreferences)

CONFIG_PATH = Path(__file__).resolve().parent.parent / "data" / "config.json"


def load_config() -> Config:
    """Load configuration from ``CONFIG_PATH`` if it exists."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        prefs = data.get("preferences", {})
        return Config(
            resume_path=data.get("resume_path", "resume.pdf"),
            linkedin_url=data.get("linkedin_url"),
            github_url=data.get("github_url"),
            preferences=UserPreferences(
                job_titles=prefs.get("job_titles", ["Python Developer"]),
                locations=prefs.get("locations", ["Remote"]),
                salary_range=prefs.get("salary_range"),
                auto_apply=prefs.get("auto_apply", False),
            ),
        )
    return Config(resume_path="resume.pdf")


def save_config(config: Config) -> None:
    """Persist configuration to ``CONFIG_PATH``."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as fh:
        json.dump(asdict(config), fh, ensure_ascii=False, indent=2)


CONFIG = load_config()
