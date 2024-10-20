import io
import torch
import torchvision.transforms as T  # type: ignore

from PIL import Image
from fastapi import UploadFile


class ImageProcessor:
    @staticmethod
    def preprocess_image(image: Image.Image, image_size=(800, 800)) -> torch.Tensor:
        """Preprocess the image to be compatible with the model."""
        transform = T.Compose([T.Resize(image_size), T.ToTensor()])
        image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
        return image_tensor

    @staticmethod
    def read_image(file: UploadFile) -> Image.Image:
        """Read and convert the image from the uploaded file."""
        img_bytes = file.file.read()  # Read bytes from the file
        image = Image.open(io.BytesIO(img_bytes)).convert(
            "RGB"
        )  # Convert to a PIL image
        return image
