import os
from io import BytesIO
import base64
from typing import List, Union
import requests
from PIL import Image, PngImagePlugin
import numpy as np


def download_image_from_url(url: str):
    """Return an image object given a url."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    content = response.content
    image = Image.open(BytesIO(content))
    return image


def download_images_from_array_of_urls(urls: List[str]):
    """Given an array of urls returns an array of downloaded images."""
    images = []
    for url in urls:
        image = download_image_from_url(url)
        images.append(image)
    return images


def read_image_base_64(data: str):
    """Returns a Pillow Image given a base64 string."""
    image = Image.open(BytesIO(base64.b64decode(data)))
    return image


def read_image_from_disk_as_base_64(filepath: str):
    """Returns image from disk as base64 encoded string."""
    with open(filepath, 'rb') as file:
        image_data = file.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
    return base64_data


def read_image_from_disk(filepath: str):
    """Returns a PIL image readed fromfrom disk."""
    image = Image.open(filepath)
    return image


def add_metadata_to_image(image: Image, parameters):
    """Add metadata `parameters` to an image on Memory."""
    # Crear el objeto pnginfo y añadir los metadatos
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", parameters)

    image_with_metadata = Image.new("RGBA", image.size)
    image_with_metadata.paste(image, (0, 0))

    output = BytesIO()
    image_with_metadata.save(output, format='PNG', pnginfo=pnginfo)
    output.seek(0)
    image_with_metadata = Image.open(output)

    # Devolver la imagen con los metadatos
    return image_with_metadata


def save_image_to_disk(image: Image, filepath: str, filename: str):
    """Save an image to disk."""
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    fullpath = os.path.join(filepath, filename)
    image.save(fullpath)


def save_pil_image_to_disk(image: Image, filepath: str):
    """Saves a PIL image to disk."""
    image.save(filepath)


def save_array_of_pil_images(images: list, folder_path: str):
    """"Saves an array of Pillow images to disk."""
    for index, image in enumerate(images):
        extension = image.format.lower()
        filename = f"{index}.{extension}"
        filepath = os.path.join(folder_path, filename)
        save_pil_image_to_disk(image, filepath)


def base64_to_image(base64_string: str) -> Image.Image:
    """Returns a PIL image as a base64 encoded string."""

    if ";base64," in base64_string:
        split = base64_string.split(";base64")
        # mime_type = split[0]
        base64_string = split[1]

    image_bytes = base64.b64decode(base64_string)
    buffer = BytesIO(image_bytes)
    image = Image.open(buffer)
    return image


def image_to_base64(
    image: Union[str, Image.Image, np.ndarray],
    _format: str = "jpeg",
    myme: bool = True,
    fixed_rgba: bool = True
) -> str:
    """Returns a base64 string from a PIL Image."""
    if isinstance(image, str):
        return image

    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    if fixed_rgba:
        if image.mode == "RGBA":
            image = image.convert("RGB")

    buffer = BytesIO()
    image.save(buffer, format=_format)
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if myme:
        myme_type = f"data:image/{_format};base64,"
        encoded_image = f"{myme_type}{encoded_image}"

    return encoded_image


def array_of_images_to_base64(images: list):
    """Converts an array of Pillow images to base64 format."""
    results = []
    for image in images:
        base64_image = image_to_base64(image)
        results.append(base64_image)
    return results


def image_to_bytes(image: Image):
    """Convert a Pillow image to bytes."""
    image_bytes = image.tobytes()
    return image_bytes


def array_of_images_to_bytes(images: list):
    """"Converts an array of Pillow images to bytes."""
    results = []
    for image in images:
        image_bytes = image_to_bytes(image)
        results.append(image_bytes)
    return results


def compress_pillow_image_to_jpeg_in_memory(image: Image, quality=75):
    """Compress a Pillow image to JPEG"""
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG', quality=quality)
    output_buffer.seek(0)
    return output_buffer.getvalue()


def parse_image(image: Union[str, Image.Image, np.ndarray]):
    """Returns an image as PIL image"""
    if isinstance(image, str):
        image = base64_to_image(image)

    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    return image


def parse_list_of_images(images: List) -> List[Image.Image]:
    """Converts a list of images as PIL image"""
    results = [parse_image(image) for image in images]
    return results
