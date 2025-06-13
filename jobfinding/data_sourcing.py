"""Job data sourcing module.

This module contains basic scraping logic for several Chinese job
platforms.  The real websites often require authentication and
advanced anti‑bot handling.  The functions below implement very
lightweight scraping using :mod:`requests` and :mod:`BeautifulSoup`.
They are primarily illustrative – in restricted environments the HTTP
requests will likely fail, so each scraper falls back to returning a
small mocked job list.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

import bs4
import requests

from .config import CONFIG

JobPosting = Dict[str, str]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "jobs.json"


def _write_jobs(jobs: List[JobPosting]) -> None:
    """Persist scraped jobs to ``DATA_FILE`` as JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as fh:
        json.dump(jobs, fh, ensure_ascii=False, indent=2)


def fetch_bosszhipin(keyword: str, page: int = 1) -> List[JobPosting]:
    """Fetch jobs from Boss直职招聘."""
    url = (
        f"https://www.zhipin.com/web/geek/job?query={keyword}&page={page}"
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for item in soup.select("div.job-card-wrapper"):
            title = item.select_one("span.job-name").text.strip()
            location = item.select_one("span.job-area").text.strip()
            desc = item.select_one("div.job-info").get_text(" ", strip=True)
            jobs.append(
                {
                    "id": item.get("data-jobid", ""),
                    "title": title,
                    "location": location,
                    "description": desc,
                    "source": "Boss直聘",
                }
            )
        return jobs
    except Exception:
        # When scraping fails (e.g. due to network restrictions) return mock data
        return [
            {
                "id": "bosszhipin-1",
                "title": f"{keyword} Engineer",
                "location": "Remote",
                "description": "Mock data from Boss直聘",
                "source": "Boss直聘",
            }
        ]


def fetch_zhilian(keyword: str, page: int = 1) -> List[JobPosting]:
    """Fetch jobs from 智联招聘."""
    url = f"https://sou.zhaopin.com/?kw={keyword}&p={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for item in soup.select("div.joblist-box__item"):  # simplified selector
            title = item.select_one("a.joblist-box__iteminfo__name").text.strip()
            location = item.select_one("span.joblist-box__iteminfo__district").text.strip()
            desc = item.select_one("p.joblist-box__iteminfo__descr").get_text(
                " ", strip=True
            )
            jobs.append(
                {
                    "id": item.get("data-jobid", ""),
                    "title": title,
                    "location": location,
                    "description": desc,
                    "source": "智联招聘",
                }
            )
        return jobs
    except Exception:
        return [
            {
                "id": "zhilian-1",
                "title": f"{keyword} Developer",
                "location": "Remote",
                "description": "Mock data from 智联招聘",
                "source": "智联招聘",
            }
        ]


def fetch_51job(keyword: str, page: int = 1) -> List[JobPosting]:
    """Fetch jobs from 前程无忧 (51job)."""
    url = (
        f"https://search.51job.com/list/000000,000000,0000,00,9,99,{keyword},2,{page}.html"
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for item in soup.select("div.j_joblist div.e"):  # simplified selector
            title = item.select_one("p.info a").get_text(strip=True)
            location = item.select_one("span.district").get_text(strip=True)
            desc = item.select_one("p.t1").get_text(" ", strip=True)
            jobs.append(
                {
                    "id": item.get("data-jobid", ""),
                    "title": title,
                    "location": location,
                    "description": desc,
                    "source": "前程无忧",
                }
            )
        return jobs
    except Exception:
        return [
            {
                "id": "51job-1",
                "title": f"{keyword} Engineer",
                "location": "Remote",
                "description": "Mock data from 前程无忧",
                "source": "前程无忧",
            }
        ]


def fetch_liepin(keyword: str, page: int = 1) -> List[JobPosting]:
    """Fetch jobs from 猎职 (LiePin)."""
    url = f"https://www.liepin.com/zhaopin/?key={keyword}&curPage={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        jobs = []
        for item in soup.select("div.sojob-item-main"):  # simplified selector
            title = item.select_one("h3 a").get_text(strip=True)
            location = item.select_one("span.area").get_text(strip=True)
            desc = item.select_one("p.conditions").get_text(" ", strip=True)
            jobs.append(
                {
                    "id": item.get("data-jid", ""),
                    "title": title,
                    "location": location,
                    "description": desc,
                    "source": "猎聘",
                }
            )
        return jobs
    except Exception:
        return [
            {
                "id": "liepin-1",
                "title": f"{keyword} Developer",
                "location": "Remote",
                "description": "Mock data from 猎聘",
                "source": "猎聘",
            }
        ]


def fetch_jobs() -> List[JobPosting]:
    """Aggregate job postings from multiple sources."""
    keyword = CONFIG.preferences.job_titles[0]
    all_jobs: List[JobPosting] = []
    all_jobs.extend(fetch_bosszhipin(keyword))
    all_jobs.extend(fetch_zhilian(keyword))
    all_jobs.extend(fetch_51job(keyword))
    all_jobs.extend(fetch_liepin(keyword))
    _write_jobs(all_jobs)
    return all_jobs

