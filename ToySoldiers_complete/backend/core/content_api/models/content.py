from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class Content(BaseModel):
    id: uuid.UUID = uuid.uuid4()
    creator_id: uuid.UUID
    title: str
    description: Optional[str] = None
    media_url: Optional[str] = None
    stream_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: List[str] = []
    visibility: Literal["public", "unlisted", "private"] = "public"
    duration: Optional[int] = None
    file_size: Optional[int] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    
    class Config:
        from_attributes = True

class ContentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    tags: List[str] = []
    visibility: Literal["public", "unlisted", "private"] = "public"

class ContentResponse(BaseModel):
    id: uuid.UUID
    creator_id: uuid.UUID
    title: str
    description: Optional[str] = None
    media_url: Optional[str] = None
    stream_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: List[str] = []
    visibility: str
    duration: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    visibility: Optional[Literal["public", "unlisted", "private"]] = None
