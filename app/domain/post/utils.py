import re


def slugify(value: str) -> str:
    """
    Convert a string into a URL-friendly slug.
    Example: "Hello World!" -> "hello-world"
    """
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value)
    return value.strip("-")
