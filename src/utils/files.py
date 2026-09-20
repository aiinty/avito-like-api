from typing import BinaryIO
import uuid
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageOps
from src.config import config
from src.utils.exceptions import ValidationError


def save_image_sync(file: BinaryIO, user_id: str) -> str:
    try:
        img = Image.open(file)
        src_format = (img.format or "").upper()
    except Exception:
        raise ValidationError("File is not an image")

    if src_format not in config.FILE_FORMATS:
        raise ValidationError("Allowed only .jpeg, .png and .webp files")

    # exif_transpose - removes metadata (including orientation)
    # thumbnail - resizes image without changing aspect ratio
    img = ImageOps.exif_transpose(img)
    img.thumbnail((config.FILE_MAX_DIMENSION, config.FILE_MAX_DIMENSION))
    
    # converting to rgb removes alpha channel, saving to buffer
    buffer = BytesIO()
    img.convert("RGB").save(buffer, "JPEG", quality=85)

    user_dir = Path(config.FILE_PREFIX) / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.jpg"
    (user_dir / filename).write_bytes(buffer.getvalue())

    return f"{config.FILE_PREFIX}/{user_id}/{filename}"

def normalize_file_ref(value: str | None) -> str | None:
    # remove image if receive None
    if value is None or value == "":
        return None
    if not value.startswith(f"{config.FILE_PREFIX}/") or ".." in value or not value.endswith(".jpg"):
        raise ValidationError("Invalid url")
    return value

def check_file_owner(url: str, user_id: str) -> None:
    if not url.startswith(f"{config.FILE_PREFIX}/{user_id}/"):
        raise ValidationError("You can use only your own file")
