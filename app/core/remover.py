from pathlib import Path

from PIL import Image
from rembg import remove, new_session


class BackgroundRemover:
    """
    Handles local AI-based background removal using rembg.
    """

    def __init__(self, model_name="u2net"):
        self.model_name = model_name
        self.session = None

    def load_model(self):
        """
        Loads the AI model once and keeps it in memory.
        """
        if self.session is None:
            self.session = new_session(self.model_name)

    def remove_background(self, image: Image.Image) -> Image.Image:
        """
        Removes the background from a PIL Image.

        Returns:
            PIL.Image.Image: Image with transparent background.
        """
        self.load_model()

        # Ensure compatible input format
        image = image.convert("RGBA")

        result = remove(
            image,
            session=self.session
        )

        return result

    def remove_from_file(
        self,
        input_path: str,
        output_path: str
    ):
        """
        Removes background from an image file and saves the result.
        """

        input_path = Path(input_path)
        output_path = Path(output_path)

        with Image.open(input_path) as image:
            result = self.remove_background(image)
            result.save(output_path, "PNG")

        return output_path