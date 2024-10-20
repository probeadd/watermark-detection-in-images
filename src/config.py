import os


class Config:
    MODEL_DIR = os.getenv("MODEL_DIR", "models/faster_rcnn_resnet50.pt")
    IMAGE_SIZE_ENV = os.getenv("IMAGE_SIZE", None)
    if IMAGE_SIZE_ENV:
        IMAGE_SIZE = tuple(
            map(int, IMAGE_SIZE_ENV.split(","))
        )  # Assuming comma-separated values for tuple
    else:
        IMAGE_SIZE = (
            800,
            800,
        )  # A fallback tuple if the environment variable is not set
