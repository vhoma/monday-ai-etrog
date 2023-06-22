from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import uvicorn
import sys
import openai
import requests
import json
import logging


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

ACTION_ITEMS = None
STATES = [
    "Waiting the call recording to arrive in storage...",
    "Processing audio...",
    "Processing transcription text...",
    "Processing DONE!!"
]
STATE_ID = 0


@app.post("/recording_ready")
async def process_recording(file: UploadFile = UploadFile(...)):
    contents = await file.read()
    # Process the contents of the MP4 file
    # You can replace the print statement with your desired processing logic
    print(f"Received file: {file.filename}, Size: {len(contents)} bytes")
    global STATE_ID
    STATE_ID = 1
    res = process_data(contents)
    return {"success": True, "transcript": res}


@app.get("/get_action_items")
def get_action_items():
    global ACTION_ITEMS
    global STATE_ID
    global STATES
    return {"status": STATES[STATE_ID], "action_items": ACTION_ITEMS}


@app.get("/init")
def get_action_items():
    global ACTION_ITEMS
    global STATE_ID
    global STATES
    ACTION_ITEMS = None
    STATE_ID = 0
    return {"status": STATES[STATE_ID], "action_items": ACTION_ITEMS}


def process_data(file_content):
    transcription = transcribe_audio(file_content)
    print(f"Transcript: {transcription}")
    global STATE_ID
    STATE_ID = 2
    global ACTION_ITEMS
    ACTION_ITEMS = parse_action_items(transcription)
    STATE_ID = 3
    return ACTION_ITEMS


def transcribe_audio(file_content):
    tmp_file_path = "./tmp_audio.m4a"
    with open(tmp_file_path, "wb") as tmp_file:
        tmp_file.write(file_content)

    with open(tmp_file_path, "rb") as audio_file:
        transcript = openai.Audio.translate("whisper-1", audio_file)

    return transcript


def parse_action_items(transcript):
    model_input = f"""The input text is: 
"{transcript["text"]}"

Result is list of action items from the input text, in json format. Every action item has keys: 'item', 'person', 'status', 'priority', 'deadline'
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": ''}, {"role": "user", "content": model_input}]
    )
    try:
        print(response.choices[0]["message"]["content"])
        action_items = json.loads(response.choices[0]["message"]["content"])
        return action_items
    except:
        logging.exception("something went wrong when converting LLM response to json")


if __name__ == "__main__":
    config = dotenv_values(".env")
    openai.api_key = config["openai_api_key"]

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
