from fastapi import APIRouter, UploadFile, File, HTTPException
from services.cloudinary_service import upload_to_cloudinary

router = APIRouter()


@router.post("/upload")
async def upload_images(
    room_image: UploadFile = File(...),
    tile_image: UploadFile = File(...),
):
    room_data = await room_image.read()
    tile_data = await tile_image.read()

    room_url = upload_to_cloudinary(room_data, room_image.filename)
    if room_url is None:
        raise HTTPException(status_code=500, detail="Failed to upload room image to Cloudinary")

    tile_url = upload_to_cloudinary(tile_data, tile_image.filename)
    if tile_url is None:
        raise HTTPException(status_code=500, detail="Failed to upload tile image to Cloudinary")

    return {"room_url": room_url, "tile_url": tile_url}
