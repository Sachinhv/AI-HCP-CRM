from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Text,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Interaction(Base):
    __tablename__ = "interaction"

    id = Column(Integer, primary_key=True, index=True)

    hcp_id = Column(Integer, ForeignKey("hcp.id"))

    interaction_type = Column(String(50))

    date = Column(Date)

    time = Column(Time)

    attendees = Column(Text)

    topics_discussed = Column(Text)

    materials_shared = Column(Text)

    samples_distributed = Column(Text)

    sentiment = Column(String(20))

    outcomes = Column(Text)

    follow_up = Column(Text)

    hcp = relationship("HCP")