#!/usr/bin/env bash
set -e

# ── Setup .env if it doesn't exist ──────────────────────────────────────────
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo "[setup] Created .env from .env.example"
    echo "[setup] Please open .env and fill in your API credentials, then re-run this script."
    exit 1
  else
    echo "[error] Neither .env nor .env.example found. Cannot start."
    exit 1
  fi
fi

# ── Check that placeholder values have been replaced ────────────────────────
if grep -qE "=(your_cloud_name|your_api_key|your_api_secret|your_kie_api_key)" .env 2>/dev/null; then
  echo "[warning] .env still contains placeholder values. Update them before running."
  echo "          Edit .env with your real Cloudinary and KIE.ai credentials."
  exit 1
fi

# ── Install / verify dependencies ───────────────────────────────────────────
echo "[setup] Checking Python dependencies..."
pip install -q -r requirements.txt
pip check --quiet 2>/dev/null || { echo "[error] Dependency check failed. Run 'pip install -r requirements.txt' manually."; exit 1; }

# ── Start the server ─────────────────────────────────────────────────────────
echo "[start] Starting Tile Place server at http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
