const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

const DATA_DIR = path.join(__dirname, '..', 'data');
const CONFIG_PATH = path.join(DATA_DIR, 'config.json');
const JOBS_PATH = path.join(DATA_DIR, 'jobs.json');

function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
  }
  return {
    resume_path: 'resume.pdf',
    linkedin_url: null,
    github_url: null,
    preferences: {
      job_titles: ['Python Developer'],
      locations: ['Remote'],
      salary_range: null,
      auto_apply: false
    }
  };
}

function saveConfig(cfg) {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2), 'utf-8');
}

const upload = multer({ dest: DATA_DIR });

app.get('/api/config', (req, res) => {
  res.json(loadConfig());
});

app.post('/api/preferences', (req, res) => {
  const cfg = loadConfig();
  cfg.preferences.job_titles = req.body.job_titles || cfg.preferences.job_titles;
  cfg.preferences.locations = req.body.locations || cfg.preferences.locations;
  cfg.preferences.salary_range = req.body.salary_range || null;
  cfg.preferences.auto_apply = !!req.body.auto_apply;
  saveConfig(cfg);
  res.json({ status: 'ok' });
});

app.post('/api/account', (req, res) => {
  const cfg = loadConfig();
  cfg.linkedin_url = req.body.linkedin_url || null;
  cfg.github_url = req.body.github_url || null;
  saveConfig(cfg);
  res.json({ status: 'ok' });
});

app.post('/api/resume', upload.single('resume'), (req, res) => {
  const cfg = loadConfig();
  if (req.file) {
    const dest = path.join(DATA_DIR, req.file.originalname);
    fs.renameSync(req.file.path, dest);
    cfg.resume_path = dest;
    saveConfig(cfg);
  }
  res.json({ status: 'ok' });
});

app.get('/api/jobs', (req, res) => {
  if (fs.existsSync(JOBS_PATH)) {
    res.json(JSON.parse(fs.readFileSync(JOBS_PATH, 'utf-8')));
  } else {
    res.json([]);
  }
});

app.post('/api/run', (req, res) => {
  exec('python -m jobfinding.main', { cwd: path.join(__dirname, '..') }, (err, stdout, stderr) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ error: 'workflow error' });
    }
    res.json({ status: 'completed', output: stdout });
  });
});

app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
  console.log(`Web UI running at http://localhost:${port}`);
});
