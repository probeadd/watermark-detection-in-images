# Watermark Detection in Images API

This repository contains a FastAPI-based service that detects watermarks in images using a Faster R-CNN model. The guide below will walk you through how to:

- Run the code and model locally
- Deploy the model using Docker and Kubernetes
- Use the API for watermark detection

**Note:** This is only for a take-home test for the Senior Machine Learning Engineer position at 99 Group.


---

## Table of Contents

- [Watermark Detection in Images API](#watermark-detection-in-images-api)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Running Locally](#running-locally)
  - [Deploying with Docker](#deploying-with-docker)
  - [Deploying with Kubernetes](#deploying-with-kubernetes)
  - [Using the API](#using-the-api)
  - [Environment Variables](#environment-variables)
  - [Notes](#notes)

---

## Requirements

- **Python 3.10+**
- **PyTorch** (for model execution)
- **FastAPI** (for the web framework)
- **Docker** (for containerization)
- **Kubernetes/Minikube** (for deployment)

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```

## Running Locally

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```
2. Set environment variables
Create a .env file in the project root and define the model directory:

```bash
MODEL_DIR=/path/to/your/model/directory
```

3. Start the FastAPI app
```bash
uvicorn src.main:app --reload
```
FastAPI will start on <http://127.0.0.1:8000>. You can test the API as described in Using the API.

## Deploying with Docker

1. Build the Docker image
From the project root, build the image:

```bash
docker build -t watermark-detection-in-images-api .
```

2. Run the Docker container
Run the container with the following command:

```bash
docker run -d --name watermark-api-container -p 8000:8000 --env MODEL_DIR=/app/models watermark-detection-in-images-api
```
This will start the container, exposing the API at <http://127.0.0.1:8000>.

3. Verify the container is running
```bash
docker ps
```
This command lists all running containers and their status.

## Deploying with Kubernetes

1. Start Minikube (or your Kubernetes setup)

```bash
minikube start
```

2. Apply Kubernetes YAML files
Navigate to the k8s/ directory and apply the deployment and service files:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

3. Verify the deployment
Check the pods and services with:

```bash
kubectl get pods
kubectl get services
```

4. Access the API
Forward the Kubernetes service to your local machine:

```bash
kubectl port-forward service/watermark-detection-in-images-service 8000:8000
```
The API is now accessible via <http://127.0.0.1:8000>.

## Using the API

1. Upload an image for prediction

- Endpoint: `/predict/`
- Method: `POST`
- Content Type: `multipart/form-data`
- Input: Upload an image file in the form-data.

Example using `curl`

```bash
curl -X POST "<http://127.0.0.1:8000/predict/>" -F "file=@/path/to/image.jpg"
```
Example response
```json
{
  "boxes": [
    [45.0, 56.0, 123.0, 210.0],
    [200.0, 250.0, 350.0, 400.0]
  ],
  "labels": [1, 1],
  "scores": [0.95, 0.87]
}
```

2. Root endpoint
Check if the API is running by hitting the root endpoint:

- Endpoint: `/`
- Method: `GET`
Example

```bash
curl <http://127.0.0.1:8000/>
```
This should return: "Watermark Detection API is running".

## Environment Variables

To configure the application, you need to set the following environment variables:

- **MODEL_DIR**: The directory where your trained model is stored.
You can set these in a `.env` file or pass them directly when running Docker or Kubernetes.

## Notes

- Make sure your model is located in the directory specified by `MODEL_DIR`.
- Adjust resource limits in the Kubernetes deployment file if needed for better performance.
