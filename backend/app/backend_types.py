from dataclasses import dataclass
from enum import Enum, auto
from pydantic import BaseModel

class Visibility(str, Enum):
    public = "public"
    private = "private"

class Video(BaseModel):
    file_path: str
    title: str
    bio: str
    visibility: Visibility
    keywords: list[str] | None


