# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load voices from JSON
with open("voices.json", "r") as f:
    VOICES = {v["id"]: v for v in json.load(f)}

app = FastAPI(title="Vox Box API")

class ChatRequest(BaseModel):
    mode_id: str
    prompt: str

@app.get("/voices")
def get_voices():
    """Return list of available voices (id, name, description)."""
    return [
        {"id": v["id"], "name": v["name"], "description": v["description"]}
        for v in VOICES.values()
    ]

@app.post("/chat")
def chat(req: ChatRequest):
    """Send prompt to GPT-5 with selected voice preamble."""
    if req.mode_id not in VOICES:
        raise HTTPException(status_code=404, detail="Mode not found")
    preamble = VOICES[req.mode_id]["preamble"]
    full_prompt = f"{preamble}\n\n{req.prompt}"

    try:
        # GPT-5 API call (replace with correct model name)
        response = openai.ChatCompletion.create(
            model="gpt-5",  # placeholder
            messages=[{"role": "system", "content": preamble},
                      {"role": "user", "content": req.prompt}]
        )
        return {
            "mode_id": req.mode_id,
            "prompt": req.prompt,
            "response": response.choices[0].message["content"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))