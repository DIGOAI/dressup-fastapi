from typing import Union

#
from PIL import Image

# Config
from app.config import config

# Supabase client
from app.repositories.supabase import supabase

# utils
from app.utils.files import generate_random_filename
from app.utils.images import (
    compress_pillow_image_to_jpeg_in_memory,
    image_to_bytes
)


EXPIRES_IN = 60 * 60 * 24 * 365 * 5
DEFAULT_BUCKET = config.get("DEFAULT_BUCKET", "dressupbucket")


def get_signed_url(
    bucket_path: str,
    bucket: str = DEFAULT_BUCKET
) -> str:
    """Get a signed url given filepath on bucket."""
    response = supabase.storage.from_(
        bucket).create_signed_url(bucket_path, EXPIRES_IN)
    url = response.get("signedURL")
    return url


def upload_file_to_storage(
    file: Union[str, bytes],
    bucket_path: str = DEFAULT_BUCKET,
    file_options: dict = None
) -> str:
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
) -> str:
    """Upload image to the storage."""
    if compress:
        extension = "jpeg"
        file_bytes = compress_pillow_image_to_jpeg_in_memory(image, quality)
    else:
        extension = image.format.lower()
        file_bytes = image_to_bytes(image)

    hashname = generate_random_filename(extension=None)
    filename = f"{hashname}.{extension}"
    full_bucket_path = f"{bucket_path}/{filename}"

    file_options = {"content-type": f"image/{extension}"}

    url = upload_file_to_storage(
        file=file_bytes,
        bucket_path=full_bucket_path,
        file_options=file_options
    )

    return url
