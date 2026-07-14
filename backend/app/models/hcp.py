from sqlalchemy import Column, Integer, String
from app.database.base import Base


class HCP(Base):
    __tablename__ = "hcp"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    hospital = Column(String(150))
    city = Column(String(100))