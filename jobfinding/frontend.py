from __future__ import annotations

"""Simple Flask front-end for JobFinding demo."""

from pathlib import Path
from typing import List

from flask import Flask, redirect, render_template, request, url_for

from . import workflow
from .config import CONFIG, save_config, load_config, CONFIG_PATH

app = Flask(__name__)

DATA_DIR = CONFIG_PATH.parent
RESUME_DIR = DATA_DIR


@app.route("/")
def index():
    return render_template("index.html", config=CONFIG)


@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    if request.method == "POST":
        job_titles = request.form.get("job_titles", "").split(",")
        locations = request.form.get("locations", "").split(",")
        CONFIG.preferences.job_titles = [t.strip() for t in job_titles if t.strip()]
        CONFIG.preferences.locations = [l.strip() for l in locations if l.strip()]
        CONFIG.preferences.salary_range = request.form.get("salary_range") or None
        CONFIG.preferences.auto_apply = bool(request.form.get("auto_apply"))
        save_config(CONFIG)
        return redirect(url_for("index"))
    return render_template("preferences.html", config=CONFIG)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "resume" in request.files:
        resume = request.files["resume"]
        if resume.filename:
            RESUME_DIR.mkdir(parents=True, exist_ok=True)
            dest = RESUME_DIR / resume.filename
            resume.save(dest)
            CONFIG.resume_path = str(dest)
            save_config(CONFIG)
            return redirect(url_for("index"))
    return render_template("upload.html", config=CONFIG)


@app.route("/notifications", methods=["GET", "POST"])
def notifications():
    if request.method == "POST":
        CONFIG.linkedin_url = request.form.get("linkedin_url") or None
        CONFIG.github_url = request.form.get("github_url") or None
        save_config(CONFIG)
        return redirect(url_for("index"))
    return render_template("notifications.html", config=CONFIG)


@app.route("/dashboard")
def dashboard():
    jobs_file = DATA_DIR / "jobs.json"
    jobs: List[dict] = []
    if jobs_file.exists():
        import json

        with jobs_file.open("r", encoding="utf-8") as fh:
            jobs = json.load(fh)
    return render_template("dashboard.html", jobs=jobs)


@app.route("/run")
def run_workflow():
    workflow.run()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
