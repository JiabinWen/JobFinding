"""Simple workflow orchestrating the job search."""

from . import data_sourcing, decision_engine, executor
from .config import CONFIG


def run() -> None:
    engine = decision_engine.DecisionEngine()
    jobs = data_sourcing.fetch_jobs()
    for job in jobs:
        result = engine.score(job)
        score = int(result["score"])
        if score >= 70:
            message = (
                f"您好，我看到您的岗位 {job['title']} ，我的背景与需求高度匹配，期待交流。"
            )
            executor.apply_to_job(job, message)
        else:
            print(f"Skipping job {job['title']} with score {score}: {result['reason']}")
