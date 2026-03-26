import io
import logging
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_to_cloudinary(file_data: bytes, filename: str) -> str | None:
    try:
        result = cloudinary.uploader.upload(
            io.BytesIO(file_data),
            public_id=f"tile_place/{filename}",
            overwrite=True,
            resource_type="image",
        )
        return result.get("secure_url")
    except Exception as e:
        logger.error("Cloudinary upload error for file '%s': %s", filename, e)
        return None
