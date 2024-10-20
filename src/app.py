from fastapi import FastAPI, UploadFile, File, Depends
from src.config import Config
from src.model_handler import ModelHandler
from src.image_processor import ImageProcessor


class WatermarkDetectionApp:
    def __init__(self):
        self.app = FastAPI()
        self.config = Config()

        # Create a ModelHandler instance with the path from the config
        self.model_handler = ModelHandler(self.config.MODEL_DIR)

        # Register the routes
        self.register_routes()

    def register_routes(self):
        """Register all routes for the FastAPI app."""

        @self.app.get("/v1/")
        async def root():
            """Root endpoint for health check or welcome message."""
            return {"message": "Welcome to the Watermark Detection API!"}

        @self.app.post("/v1/predict/")
        async def predict(
            file: UploadFile = File(...),
            model: ModelHandler = Depends(self.get_model_handler),
        ):
            """API endpoint for model predictions."""
            # Read and preprocess the image
            image = ImageProcessor.read_image(file)
            image_tensor = ImageProcessor.preprocess_image(
                image, image_size=self.config.IMAGE_SIZE
            )

            # Make predictions
            predictions = model.predict(image_tensor)

            # Extract prediction results
            boxes = predictions[0]["boxes"].tolist()
            labels = predictions[0]["labels"].tolist()
            scores = predictions[0]["scores"].tolist()

            return {"boxes": boxes, "labels": labels, "scores": scores}

    def get_model_handler(self):
        """Provide the model handler for dependency injection."""
        return self.model_handler
