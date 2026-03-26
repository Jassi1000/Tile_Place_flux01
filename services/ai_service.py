import logging
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

KIE_API_KEY = os.getenv("KIE_API_KEY")
KIE_API_BASE = "https://api.kie.ai"
CREATE_TASK_ENDPOINT = f"{KIE_API_BASE}/api/v1/flux/img2img"
POLL_ENDPOINT = f"{KIE_API_BASE}/api/v1/flux/task"

POLL_INTERVAL = 6
MAX_RETRIES = 5


def generate_prompt(surface: str) -> str:
    surface = surface.lower().strip()
    if surface == "floor":
        return (
            "Apply the tile texture from the second image onto the FLOOR of the room in the first image. "
            "Do not change room structure, furniture, or perspective. Tiles must repeat evenly, maintain scale, "
            "include grout lines, and follow floor perspective. Match lighting and shadows. Only modify the floor."
        )
    if surface == "front wall":
        return (
            "Apply the tile texture onto the FRONT WALL. Preserve room geometry and furniture. "
            "Tiles must repeat evenly with correct scale and grout lines. Match lighting. Only modify the front wall."
        )
    if surface == "side wall":
        return (
            "Apply the tile texture onto the SIDE WALL. Preserve perspective and room structure. "
            "Tiles must repeat evenly with proper scaling and grout lines. Match lighting. Only modify the side wall."
        )
    return (
        "Apply the tile texture from the second image onto the specified surface of the room. "
        "Preserve room structure, furniture, and perspective. Tiles must repeat evenly with grout lines. "
        "Match lighting and shadows."
    )


def call_ai_model(room_url: str, tile_url: str, surface: str) -> str | None:
    if not KIE_API_KEY:
        logger.error("KIE_API_KEY is not set")
        return None

    prompt = generate_prompt(surface)

    payload = {
        "input_urls": [room_url, tile_url],
        "prompt": prompt,
        "aspect_ratio": "original",
        "resolution": "1K",
        "nsfw_checker": False,
    }

    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(CREATE_TASK_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Failed to create AI task: %s", e)
        return None

    task_id = data.get("task_id") or data.get("id") or (data.get("data") or {}).get("task_id")
    if not task_id:
        logger.error("No task_id in response: %s", data)
        return None

    for attempt in range(1, MAX_RETRIES + 1):
        time.sleep(POLL_INTERVAL)
        try:
            poll_response = requests.get(
                f"{POLL_ENDPOINT}/{task_id}",
                headers=headers,
                timeout=30,
            )
            poll_response.raise_for_status()
            poll_data = poll_response.json()
        except requests.exceptions.RequestException as e:
            logger.warning("Polling attempt %d/%d failed: %s", attempt, MAX_RETRIES, e)
            continue

        status = (
            poll_data.get("status")
            or (poll_data.get("data") or {}).get("status")
            or ""
        ).lower()

        if status in ("completed", "succeeded", "success", "finished"):
            output_url = (
                poll_data.get("output_url")
                or poll_data.get("image_url")
                or (poll_data.get("data") or {}).get("output_url")
                or (poll_data.get("data") or {}).get("image_url")
                or (poll_data.get("output") or [None])[0]
            )
            if output_url:
                return output_url
            logger.error("Task completed but no output URL found: %s", poll_data)
            return None

        if status in ("failed", "error"):
            error_msg = poll_data.get("error") or (poll_data.get("data") or {}).get("error") or "Unknown error"
            logger.error("AI task failed: %s", error_msg)
            return None

        error_field = (
            poll_data.get("error")
            or (poll_data.get("data") or {}).get("error")
            or ""
        )
        if isinstance(error_field, str) and "credit" in error_field.lower() and "insufficient" in error_field.lower():
            logger.error("Insufficient credits for AI API")
            return None

        logger.info("Polling attempt %d/%d, status: %s", attempt, MAX_RETRIES, status)

    logger.error("AI task timed out after %d retries", MAX_RETRIES)
    return None
