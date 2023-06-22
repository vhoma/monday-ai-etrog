from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/recording_ready")
async def process_recording(file: UploadFile = UploadFile(...)):
    contents = await file.read()
    # Process the contents of the MP4 file
    # You can replace the print statement with your desired processing logic
    print(f"Received file: {file.filename}, Size: {len(contents)} bytes")
    return {"message": "Recording processed successfully"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
