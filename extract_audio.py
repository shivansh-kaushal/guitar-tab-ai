from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import yt_dlp
from flask_cors import CORS
import subprocess
from pathlib import Path
from utils.logger import get_logger

load_dotenv(override=True)

logger = get_logger("user1")

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-Secret-Key"]
    }
})
def verify_secret_key(provided_key):
    expected_key = os.getenv("SECRET_KEY")
    return provided_key == expected_key

@app.route('/health-check', methods=['POST'])
def check():
    provided_key = request.headers.get("X-Secret-Key")
    try:
        if not verify_secret_key(provided_key):
            print("Invalid")
            return jsonify({"error": "Invalid secret key"}), 401
        
        return jsonify({"status": "ok"}), 200
    except Exception as e: 
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    # Implement s-key check
    yt_link = request.json.get("yt_link")
    print("yt_link:",yt_link)

    if not yt_link:
        return jsonify({"error": "Link not valid"}), 400

    # provided_key = request.headers.get("X-Secret-Key")
    # if not verify_secret_key(provided_key):
    #     print("Invalid")
    #     return jsonify({"error": "Invalid secret key"}), 401
    
    try:
        url = yt_link
        ydl_opts = {
            'format': 'best', 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': 'cached_audio/audio1.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("downloaded successfully")
        separate_with_demucs('cached_audio/audio1.wav')
        print("separated successfully")
        return jsonify({"message": "Downloaded audio"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

def separate_with_demucs(audio_path: str):
    audio_path = str(Path(audio_path))
    cmd = [
        "demucs",
        "-n", "htdemucs",
        audio_path
    ]

    try:
        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return  "Success"
    except Exception as e:
        print("Error during demucs execution:", e)
        return "Error"
    
if __name__ == '__main__':
    app.run(host='localhost', port = '8008', debug=True)