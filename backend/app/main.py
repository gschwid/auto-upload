from typing import Annotated
from fastapi import FastAPI, UploadFile, File, HTTPException, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select


load_dotenv()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Auto Upload API")

app.add_middleware(
    SessionMiddleware, 
    # to generate secret_key run: openssl rand -hex 32
    secret_key=os.environ['super_secret_key']
)  # Repl

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

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.environ['client_id'],
    client_secret=os.environ['client_secret'],
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile", "access_type": "offline", "prompt": "consent"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration"
)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Platforms(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    platform: str = Field(index=True)
    refresh_token: str = Field()
    access_token: str = Field()

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

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
    
@app.get("/auth/google")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(request, redirect_uri="http://localhost:8000/auth/google/callback")

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    print(token)
    return(token)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)