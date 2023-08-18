import random
import string
from typing import Optional


def generate_random_filename(
    extension: Optional[str] = ".jpeg",
    length: int = 24
) -> str:
    """Generates a random hash name. If you pass the `extension` parameter it will be concatenated with the hash name."""
    random_hash_name = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for i in range(length)
    )

    if extension is None:
        return random_hash_name

    if "." not in extension:
        extension = "." + extension

    extension = extension.replace(" ", "")
    extension = extension.lower()
    random_hash_name += extension

    return random_hash_name
