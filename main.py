from src.app import WatermarkDetectionApp

# Initialize the WatermarkDetectionApp
fast_api_app = WatermarkDetectionApp()

# Get the app instance from the FastAPIApp class
app = fast_api_app.app
