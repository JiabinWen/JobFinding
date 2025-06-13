"""Configuration management for JobFinding system."""

from dataclasses import dataclass, field
from typing import List, Optional

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

CONFIG = Config(resume_path="resume.pdf")
