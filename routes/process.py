from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import call_ai_model

router = APIRouter()

VALID_SURFACES = {"floor", "front wall", "side wall"}


class ProcessRequest(BaseModel):
    room_url: str
    tile_url: str
    surface: str


@router.post("/process")
async def process_images(request: ProcessRequest):
    surface = request.surface.lower().strip()
    if surface not in VALID_SURFACES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid surface '{request.surface}'. Must be one of: floor, front wall, side wall",
        )

    result = call_ai_model(request.room_url, request.tile_url, surface)

    if result is None:
        raise HTTPException(status_code=500, detail="AI model failed to produce an output image")

    return {"output_url": result}
