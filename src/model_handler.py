import torch

from torchvision.models.detection import fasterrcnn_resnet50_fpn  # type: ignore
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor  # type: ignore


class ModelHandler:
    def __init__(self, model_path: str, num_classes: int = 2):
        self.model_path = model_path
        self.num_classes = num_classes  # Number of classes for your model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.load_model()

    def load_model(self):
        """Load the Faster R-CNN model, redefine predictor head, and map to the appropriate device."""
        # Load the base Faster R-CNN model pre-trained on COCO
        model = fasterrcnn_resnet50_fpn(weights=None)

        # Get the number of input features for the classifier
        in_features = model.roi_heads.box_predictor.cls_score.in_features

        # Replace the pre-trained head with a new one for our number of classes
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, self.num_classes)

        # Load the model's weights from the checkpoint, mapping to the appropriate device
        model.load_state_dict(torch.load(self.model_path, map_location=self.device))

        # Move the model to the selected device (CPU or GPU)
        model.to(self.device)
        model.eval()  # Set the model to evaluation mode

        return model

    def predict(self, image_tensor: torch.Tensor):
        """Make predictions using the loaded model."""
        image_tensor = image_tensor.to(self.device)  # Move input to the correct device
        with torch.no_grad():
            predictions = self.model(image_tensor)
        return predictions
