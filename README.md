# Tile Place – Flux AI

AI-powered tile visualisation using Flux-2 (img2img). Upload a photo of your room and a tile texture, pick the surface to tile, and get a photorealistic render back.

## Architecture

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python) |
| Image hosting | Cloudinary |
| AI generation | KIE.ai – Flux-2 img2img |
| Frontend | Vanilla HTML/CSS/JS (served by FastAPI) |

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Jassi1000/Tile_Place_flux01.git
cd Tile_Place_flux01
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file
Copy the example file and fill in your own credentials:
```bash
cp .env.example .env
```

Open `.env` in any text editor and replace the placeholder values:
```env
# Cloudinary credentials – https://cloudinary.com/console
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# KIE.ai (Flux-2) API key – https://kie.ai
KIE_API_KEY=your_kie_api_key
```

> **How to get credentials**
> * **Cloudinary** – sign up free at https://cloudinary.com → Dashboard → copy *Cloud name*, *API Key*, *API Secret*.
> * **KIE.ai** – sign up at https://kie.ai → Account settings → copy your *API Key*.

### 4. Run the server

**Option A – startup script (recommended)**
```bash
bash start.sh
```

**Option B – manual**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The app will be available at **http://localhost:8000**.

---

## Usage

1. Open http://localhost:8000 in your browser.
2. Upload a **room image** and a **tile image**.
3. Choose the surface to tile: *Floor*, *Front Wall*, or *Side Wall*.
4. Click **Generate** and wait ~30 seconds for the AI result.
5. Download the generated image.

---

## Project Structure

```
.
├── main.py                  # FastAPI application entry-point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── start.sh                 # One-command startup script
├── routes/
│   ├── upload.py            # POST /upload  – uploads images to Cloudinary
│   └── process.py           # POST /process – calls KIE.ai and returns result URL
├── services/
│   ├── cloudinary_service.py
│   └── ai_service.py
└── static/
    └── index.html           # Single-page UI
```

