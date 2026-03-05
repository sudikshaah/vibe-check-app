import os
import json
import re
import time
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load env before anything else
load_dotenv()

from google import genai
from google.genai import types

app = Flask(__name__)
app.debug = False

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

# Initialize the 2026 client
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are VibeCheck, an expert music curator with an encyclopedic knowledge of songs across all genres and eras.
Your job is to analyse a user's mood or vibe description and recommend exactly 5 REAL, well-known songs that perfectly match that energy.

Rules:
- Only recommend songs that genuinely exist.
- Pick songs that truly match the described feeling, not just popular hits.
- Be creative and specific in your "reason" - explain WHY this song fits the vibe in 1-2 vivid sentences.
- Respond ONLY with a valid JSON array. No extra text, no markdown code fences.

Response format (strict JSON array):
[
  {"title": "Song Name", "artist": "Artist Name", "reason": "Why this song fits the vibe."},
  ...
]
"""

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    vibe = data.get("vibe", "").strip() if data else ""

    if not vibe:
        return jsonify({"error": "Please describe your vibe first!"}), 400

    try:
        user_prompt = f"My vibe right now: {vibe}\n\nGive me 5 songs that perfectly match this feeling."
        
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        )

        model_id = "gemini-3.1-flash-lite-preview"
        print(f"Using model: {model_id}")

        client = genai.Client(api_key=GEMINI_API_KEY, http_options={'api_version': 'v1beta'})

        # Retry once on 429 rate limit
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=user_prompt,
                config=config,
            )
        except Exception as quota_err:
            if "429" in str(quota_err) or "ResourceExhausted" in str(quota_err) or "RESOURCE_EXHAUSTED" in str(quota_err):
                time.sleep(3)
                response = client.models.generate_content(
                    model=model_id,
                    contents=user_prompt,
                    config=config,
                )
            else:
                raise
        
        raw_text = response.text.strip()

        # Strip markdown code fences if model wraps response
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)

        songs = json.loads(raw_text)

        if not isinstance(songs, list) or len(songs) == 0:
            return jsonify({"error": "Unexpected response from AI. Please try again."}), 500

        # Normalise keys just in case
        normalised = []
        for s in songs[:5]:
            normalised.append({
                "title": s.get("title", "Unknown Title"),
                "artist": s.get("artist", "Unknown Artist"),
                "reason": s.get("reason", ""),
            })

        return jsonify({"songs": normalised})

    except json.JSONDecodeError:
        return jsonify({"error": "Could not parse the AI's response. Please try again."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
