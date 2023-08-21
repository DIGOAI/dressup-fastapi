from typing import Union

from PIL import Image

from app.config import Config
from app.repositories.supabase import FileOptions, supabase
from app.utils.files import generate_random_filename
from app.utils.images import (compress_pillow_image_to_jpeg_in_memory,
                              image_to_bytes)

EXPIRES_IN = 60 * 60 * 24 * 365 * 5
DEFAULT_BUCKET = Config.SUPABASE_BUCKET


def get_signed_url(
    bucket_path: str,
    bucket: str = DEFAULT_BUCKET
) -> str | None:
    """Get a signed url given filepath on bucket."""
    response = supabase.storage.from_(
        bucket).create_signed_url(bucket_path, EXPIRES_IN)
    url = response.get("signedURL")
    return url


def upload_file_to_storage(
    file: Union[str, bytes],
    bucket_path: str = DEFAULT_BUCKET,
    file_options: FileOptions | None = None
) -> str | None:
    """Upload a file to the storage"""
    response = supabase.storage.from_(DEFAULT_BUCKET).upload(
        path=bucket_path,
        file=file,
        file_options=file_options
    )
    if not response:
        return None
    url = get_signed_url(bucket_path)
    return url


def upload_image_to_storage(
    image: Image.Image,
    bucket_path: str = DEFAULT_BUCKET,
    compress: bool = True,
    quality: int = 75
) -> str | None:
    """Upload image to the storage."""
    if compress:
        extension = "jpeg"
        file_bytes = compress_pillow_image_to_jpeg_in_memory(image, quality)
    else:
        extension = image.format.lower() if image.format else "jpeg"
        file_bytes = image_to_bytes(image)

    hashname = generate_random_filename(extension=None)
    filename = f"{hashname}.{extension}"
    full_bucket_path = f"{bucket_path}/{filename}"

    file_options: FileOptions = {"content-type": f"image/{extension}"}

    url = upload_file_to_storage(
        file=file_bytes,
        bucket_path=full_bucket_path,
        file_options=file_options
    )

    return url
