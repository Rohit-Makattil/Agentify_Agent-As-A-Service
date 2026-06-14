# 🤖 Agentify — Multi-Agent AI Command Center

[![React](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-blue?style=for-the-badge&logo=react)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/AI%20Power-Gemini%202.5%20Flash-purple?style=for-the-badge&logo=googlegemini)](https://deepmind.google/technologies/gemini/)

**Agentify** is an advanced, unified multi-agent AI platform that helps you automate marketing, sales, and web presence. By providing a single high-level objective, Agentify coordinates a swarm of specialized AI agents to generate marketing emails, create and schedule social media campaigns, scrape and qualify leads, and build fully-functioning landing pages simultaneously.

---

## 🌟 Key Features

### 1. 🎛️ Unified Command Center
- Deploy multiple specialized agents with a single click.
- Enter a high-level goal (e.g., *"Launch an organic juice delivery service in Mumbai"*), and watch the Email, Social, and Website agents execute it in parallel.
- Real-time status indicators and inline interactive previews.

### 2. 🔍 Lead Finder Agent
- Instantly searches for businesses based on keyword and city.
- Integrated geocoding using **Nominatim API** with automatic fallback to **Photon API**.
- Fetches real-world business nodes from **OpenStreetMap (Overpass API)**.
- **Concurrent Web Crawler**: Scrapes websites asynchronously using `httpx` and `BeautifulSoup4` to extract verified business emails via regex.

### 3. 📧 Mail Automation Agent
- **AI-Powered Copywriter**: Generates complete campaign emails with highly converting text and professional HTML layout using Gemini.
- **Campaign Scheduler**: Schedule emails for future delivery using a background `APScheduler` worker.
- **Bulk Uplink**: Supports importing custom audience target CSVs for mass mail merges.
- **Interactive Tracking**: Embeds response buttons (*"Yes, I'm Interested"* / *"Not Interested"*) directly in emails, capturing responses to a centralized **Google Sheets database** and displaying custom landing page response screens.

### 4. 📱 Social Media Agent
- Generates post copy optimized for platforms like Twitter and Instagram.
- **Dynamic Image Generator**: Prompts are dynamically generated based on theme context. Uses a reliable multi-tier fallback system:
  $$\text{Pollinations.ai} \rightarrow \text{FLUX.1-schnell} \rightarrow \text{SDXL-Flash} \rightarrow \text{Gemini Image Model}$$
- **Automated Poster**: Autonomously posts to Twitter (via API) and Instagram (via browser automation using `Playwright` / `instagrapi`).

### 5. 🌐 Website Builder Agent
- Builds responsive, modern HTML/CSS landing pages based on natural language specifications.
- Includes interactive in-app live previews of generated code.
- Supports iterative modifications—simply describe changes (e.g., *"Make the header dark-themed"*), and the agent updates the code instantly.

---

## 🖥️ System Architecture

Refer to [ARCHITECTURE.md](file:///C:/Users/rohit/OneDrive/Desktop/Agentify_main/ARCHITECTURE.md) for the detailed system architecture diagram, fallback flows, API details, and detailed execution paths.

---

## ⚙️ Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS, Framer Motion, Lucide Icons, Axios, React Router v7.
- **Backend**: FastAPI, Uvicorn (standard server), Pydantic v2, APScheduler (background jobs), Pandas & BeautifulSoup4 (data scraping & parsing).
- **Core LLM Provider**: Google Gemini 2.5 Flash, Google Gemini Image generation model.

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 1. Clone & Prepare
```bash
git clone https://github.com/Rohit-Makattil/Agentifyy.git
cd Agentifyy
```

### 2. Backend Setup
1. Navigate to the backend directory and create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows (CMD/PowerShell)**:
     ```powershell
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend/` directory (see [Environment Variables](#-environment-variables) below).

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

---

## 🔑 Environment Variables

Create a `.env` file inside the `backend` folder and populate the variables:

| Variable | Description | Required? |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key for AI generation tasks | **Yes** |
| `SENDER_EMAIL` | The Gmail address used to send automation emails | **Yes** |
| `SENDER_PASSWORD` | App Password for Gmail SMTP (Not standard password) | **Yes** |
| `TWITTER_API_KEY` | Twitter/X API Consumer Key | Optional |
| `TWITTER_API_SECRET` | Twitter/X API Consumer Secret | Optional |
| `TWITTER_ACCESS_TOKEN` | Twitter/X API Access Token | Optional |
| `TWITTER_ACCESS_SECRET`| Twitter/X API Access Secret | Optional |
| `INSTAGRAM_USERNAME` | Instagram account username for Playwright poster | Optional |
| `INSTAGRAM_PASSWORD` | Instagram account password for Playwright poster | Optional |
| `SHEET_ID` | Google Sheet ID for storing response metrics | Optional |
| `GOOGLE_SHEETS_CREDENTIALS_PATH`| Path to Google Service Account JSON file | Optional |

---

## 🏃 Running the Application

For normal operation, start both servers:

1. **Start FastAPI Backend (Port 5000)**:
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn main:app --reload --port 5000
   ```
2. **Start React Frontend (Port 5173)**:
   ```bash
   cd frontend
   npm run dev
   ```

Open [http://localhost:5173](http://localhost:5173) in your browser to access the dashboard. Use default local developer login credentials if prompted.
