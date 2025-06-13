"""Execution module for applying to jobs."""

from typing import Dict


def apply_to_job(job: Dict[str, str], message: str) -> None:
    """Mock function to apply to a job posting."""
    print(f"Applying to {job['title']} with message: {message}")
