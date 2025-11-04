from pydantic import BaseModel
from datetime import datetime
import uuid

class Session(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    access_token: str
    refresh_token: str
    expires_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    user_id: uuid.UUID
    access_token: str
    refresh_token: str
    expires_at: datetime
