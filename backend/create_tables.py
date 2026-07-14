from app.database.connection import engine
from app.database.base import Base

# Import models
from app.models.hcp import HCP
from app.models.interaction import Interaction

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")