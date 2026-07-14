from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class InteractionCreate(BaseModel):
    hcp_id: int
    interaction_type: str
    date: date
    time: time
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    follow_up: Optional[str] = None


class InteractionResponse(InteractionCreate):
    id: int

    class Config:
        from_attributes = True