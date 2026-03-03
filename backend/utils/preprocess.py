from PIL import Image, UnidentifiedImageError
import io

# Optional: define a standard input size if your models require it
DEFAULT_IMAGE_SIZE = (224, 224)


def preprocess_image(image_bytes: bytes, resize: bool = False) -> Image.Image:
    """
    Convert raw image bytes into a validated PIL Image.

    Args:
        image_bytes (bytes): Raw image bytes from upload.
        resize (bool): Whether to resize image to DEFAULT_IMAGE_SIZE.

    Returns:
        PIL.Image.Image: Preprocessed image ready for model input.

    Raises:
        ValueError: If the file is not a valid image.
    """

    try:
        # Convert bytes to PIL image
        image = Image.open(io.BytesIO(image_bytes))

        # Ensure RGB format (important for most vision models)
        image = image.convert("RGB")

        # Optional resizing (only if your model requires fixed size)
        if resize:
            image = image.resize(DEFAULT_IMAGE_SIZE)

        return image

    except UnidentifiedImageError:
        raise ValueError("Uploaded file is not a valid image.")