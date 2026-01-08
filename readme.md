🎸 Guitar Tab AI - Audio Ingestion Service (MVP)

An early-stage backend service for an AI-powered guitar tab generator.
This service handles secure YouTube audio ingestion and converts videos into audio files that can later be processed for guitar note extraction.

⚠️ This is an MVP focused only on audio extraction.
Guitar separation, note detection, and tab generation are coming next.

🚀 What This Service Does (So Far)

✅ Accepts a YouTube link via API
✅ Downloads the best available audio
✅ Converts audio to .mp3 using FFmpeg
✅ Stores audio locally for further processing
✅ Secured using a secret API key
✅ CORS enabled (frontend-ready)

🧠 Why This Exists

Many guitar solos and riffs on YouTube don’t have tabs or accurate notation available online.

This project aims to:

Extract guitar audio from YouTube videos

Use AI to detect notes and playing techniques

Generate playable guitar tabs and diagrams

This repository currently implements Step 1: Audio ingestion.

🛠 Tech Stack

python 3.11.1
Flask — API framework
yt-dlp — YouTube audio extraction
FFmpeg — audio conversion
Flask-CORS — frontend compatibility
dotenv — environment variable management


Project structure

.
├── app.py                # Flask application
├── cached_audio/         # Downloaded audio files
├── .env                  # Environment variables
├── requirements.txt
└── README.md


Authenticator

Header
X-Secret-Key: your_secret_key_here

POST /health-check:
headers: X-Secret-Key

Response:
{
  "status": "ok"
}

🎵 Download Audio from YouTube

POST /download

Headers

X-Secret-Key
Content-Type: application/json


Body

{
  "yt_link": "https://www.youtube.com/watch?v=VIDEO_ID"
}


Success Response

{
  "message": "Downloaded audio"
}


Output

Audio saved in cached_audio/

Converted to .mp3

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/your-username/guitar-tab-ai.git
cd guitar-tab-ai

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set environment variables

Create a .env file:

SECRET_KEY=your_secret_key_here

5️⃣ Run the server
python app.py


Server runs on:

http://localhost:8008