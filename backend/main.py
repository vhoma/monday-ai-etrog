from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import uvicorn
import sys
import openai
import requests


app = FastAPI()
# CORS settings
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

action_items = None


@app.post("/recording_ready")
async def process_recording(file: UploadFile = UploadFile(...)):
    contents = await file.read()
    # Process the contents of the MP4 file
    # You can replace the print statement with your desired processing logic
    print(f"Received file: {file.filename}, Size: {len(contents)} bytes")
    res = process_data(contents)
    return {"success": True, "transcript": res}


@app.get("/get_action_items")
def get_action_items():
    global action_items
    if action_items:
        return {"processing_done": True, "action_items": action_items}
    else:
        return {"processing_done": False, "action_items": action_items}


def process_data(file_content):
    transcription = transcribe_audio(file_content)
    print(f"Transcript: {transcription}")
    return transcription


def transcribe_audio(file_content):
    tmp_file_path = "./tmp_audio.m4a"
    with open(tmp_file_path, "wb") as tmp_file:
        tmp_file.write(file_content)

    with open(tmp_file_path, "rb") as audio_file:
        transcript = openai.Audio.translate("whisper-1", audio_file)

    return transcript


def parse_action_items(transcript):
    pass


if __name__ == "__main__":
    config = dotenv_values(".env")
    openai.api_key = config["openai_api_key"]

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
