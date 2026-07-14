from fastapi import FastAPI
from app.routers import interaction, chat
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="AI HCP CRM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(interaction.router)
app.include_router(chat.router)


@app.get("/")
def home():
    return {
        "message": "AI HCP CRM Backend Running"
    }