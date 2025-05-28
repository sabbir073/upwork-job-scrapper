# 🛠️ Upwork Job Scraper

A stealth-powered Python application that scrapes Upwork job listings based on keywords pulled from a Google Sheet and writes job data into another sheet. It's designed to mimic human behavior using headless Chromium with anti-bot techniques, and is triggered via webhook (e.g., from `n8n`).

## 📂 Project Structure

```
upwork-job-scrapper/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── constants.py
│   ├── runner.py
│   ├── scraper.py
│   ├── sheets.py
│   ├── utils.py
│   └── webhook.py
├── credentials/
│   └── service_account.json
├── .env
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## ✅ Features

- 🔐 Stealth scraping with `undetected-chromedriver`
- 🔁 Handles pagination and deduplication
- 🧠 Resumes from last scraped job
- 📊 Google Sheets API (input + output)
- 🔗 Triggered via `n8n` webhook
- 🐳 Deployable via Coolify (Docker-based)

## 🚀 Getting Started (Local)

### 1. Clone the repository

```bash
git clone https://github.com/sabbir073/upwork-job-scrapper.git
cd upwork-job-scrapper
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file:

```
WEBHOOK_URL=https://your-n8n-webhook-url
```

Place your Google Service Account JSON in `credentials/service_account.json`.

### 5. Run the FastAPI server

```bash
uvicorn api:app --reload
```

Then you can trigger the scraper by:

```bash
curl -X POST http://127.0.0.1:8000/start
```

## 📦 Deployment with Coolify

Make sure Coolify is configured to build using the included `Dockerfile`.

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Make sure `.env` and `credentials/service_account.json` are configured in your container environment.

## 🧪 Testing with Postman

Use `POST http://localhost:8000/start` or your deployed URL.

## 📄 Required Google Sheets Setup

- 🔑 One sheet for **input** (`keywords` column)
- 📄 Another sheet for **output** (job fields: ID, title, URL, etc.)

See `app/sheets.py` for how the fields are pulled and appended.

## 📌 Notes

- Use only Chrome v137+ for compatibility with the current ChromeDriver.
- Scraper retries and uses random delays to avoid blocks.
- When deploying to Coolify, ensure Chromium is installed in the Docker image if needed.

## 🤝 Contributing

Pull requests welcome. Please remove any credentials before committing.

## ⚠️ Disclaimer

Use responsibly and only for authorized scraping under Upwork’s TOS.

## 📃 License

MIT