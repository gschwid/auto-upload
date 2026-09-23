from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Auto Upload API")

# Allow your frontend origin
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if (file.filename and file.content_type):
            if "video" not in file.content_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file type. Only video files are allowed."
                )
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            count = 0
            with open(file_path, "wb") as buffer:
                chunk = await file.read(1024 * 1024)  # Read the first 1MB of the file
                while chunk:
                    print(f"Processing chunk {count + 1} of the file: {file.filename}")
                    count += 1
                    # Process the chunk (e.g., save to disk, analyze, etc.)
                    buffer.write(chunk)
                    chunk = await file.read(1024 * 1024)  # Read the next chunk\
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the video: {str(e)}"
        )
    finally:
        await file.close()

    return {"filename": file.filename, "message": "File uploaded successfully."}
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)