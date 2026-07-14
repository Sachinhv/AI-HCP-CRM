from fastapi import APIRouter

router = APIRouter(
    prefix="/interaction",
    tags=["Interaction"]
)


@router.get("/")
def get_interactions():
    return {
        "message": "Interaction API Working"
    }