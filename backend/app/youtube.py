from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from backend_types import Video

def upload_to_youtube(file_path: str, refresh_token: str, video: Video):
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token
    )

    request = Request()
    credentials.refresh(request)

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video.title,
                "description": video.bio,
                "tags": video.keywords
            },
            "status": {
                "privacyStatus": video.visibility
            }
        },
        media_body=MediaFileUpload(
            file_path,
            resumable=True
        )
    )

    response = request.execute()

    return response