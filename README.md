# Scan_spectrum (Render-ready)

This repository is organized for Render deployment.

- `backend/app.py` — Flask backend (serves APIs and UI)
- `frontend/` — static HTML/CSS/JS for the UI
- `requirements.txt` — Python dependencies (uses opencv-python-headless for cloud)
- `Procfile` — `web: gunicorn backend.app:app`
- `render.yaml` — Render blueprint configuration

To deploy:
1. Push this repo to GitHub.
2. Create a new Web Service on Render (or use blueprint) connecting to the repo.
3. Ensure `Start Command` is `gunicorn backend.app:app` (Procfile is present).
4. Set Health Check Path to `/api/health`.
