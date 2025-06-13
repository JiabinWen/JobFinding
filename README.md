
A simplified prototype demonstrating an automated job application workflow.

This repository contains a small Python package with the following modules:

- `config` – stores user preferences.
- `data_sourcing` – scrapes job postings from Boss直聘、智联招聘、前程无忧、猎聘
  (falling back to mock data when network access is unavailable).
- `decision_engine` – scores job postings based on the user profile.
- `executor` – applies to jobs with a generated greeting.
- `workflow` – orchestrates the steps.
- `notification` – placeholder for sending notifications.
- `main` – entry point running the workflow.

## Running the demo

Install Python 3.10+ and run the command line demo:

```bash
python -m jobfinding.main
```

Dependencies used by the scrapers are `requests` and `beautifulsoup4`. Install
them with `pip install -r requirements.txt` or manually if needed.

The workflow will attempt to scrape the four platforms above and store the
results in `data/jobs.json`. If the network requests fail (for example, due to
restricted connectivity) the scrapers fall back to returning small mock job
lists so the rest of the demo can still run.

You can also start a small web front-end based on Flask:

```bash
python -m jobfinding.frontend
```

The front-end lets you upload a resume, adjust preferences and run the
workflow from a simple dashboard.

## Node + Vue Web UI

A lightweight web interface built with Node.js (Express) and Vue 3 is located in
`web/`. Start it after installing dependencies with npm:

```bash
cd web
npm install
npm start
```

The interface provides forms for uploading a resume, editing preferences, managing
accounts, running the workflow and viewing scraped jobs.