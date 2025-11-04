from pydantic import BaseModel
from datetime import datetime
from typing import Literal
import uuid

class Transaction(BaseModel):
    id: uuid.UUID
    from_user: uuid.UUID
    to_creator: uuid.UUID
    amount: float
    stripe_txn: str
    status: Literal["pending", "completed", "failed", "refunded"] = "pending"
    created_at: datetime
    
    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    to_creator: uuid.UUID
    amount: float

class TransactionResponse(BaseModel):
    id: uuid.UUID
    amount: float
    status: str
    created_at: datetime
    stripe_txn: str
