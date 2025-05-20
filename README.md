# AWS Rekognition Image Detection Viewer (Flask + Serverless)

This project demonstrates how to build a lightweight, serverless computer vision pipeline using **Amazon Rekognition**, **AWS Lambda**, and **S3**, wrapped in a simple **Flask** web interface.
![](https://github.com/ziadabohalawa/Image-Rekognition/blob/a3340121ea52083329d834734ec91b333c987c2d/output.jpg)

It allows users to:
- Select an image stored in S3
- Trigger Rekognition to detect labels and objects
- Overlay bounding boxes on the image
- View the result in a browser

---

## System Architecture
![architecture_diagram](https://github.com/ziadabohalawa/Image-Rekognition/blob/14d54528baf7eacd2abd62c94d414e71f27c83a9/architecture_diagram.png)

## Technologies Used
| Component        | Service / Library      |
| ---------------- | ---------------------- |
| Object Detection | Amazon Rekognition     |
| Storage          | Amazon S3              |
| Compute          | AWS Lambda             |
| API Gateway      | AWS API Gateway (HTTP) |
| Frontend         | Flask                  |
| Visualization    | Pillow (PIL), OpenCV   |
| SDKs             | Boto3, Requests        |



## How It Works
User enters the image path (key) from their S3 bucket.

Flask app sends a POST request to an API Gateway endpoint.

The Lambda function reads the image path and sends it to Rekognition.

Rekognition returns labels + bounding boxes.

Flask downloads the image, draws results, and displays the annotated image.

## Setup
Clone this repository:

```
git clone https://github.com/<yourusername>/rekognition-flask-app.git
cd rekognition-flask-app
```
Install dependencies:
```
pip install flask boto3 pillow opencv-python requests
```
Run the Flask app:
```
python app.py
```
Open in browser:
```
http://127.0.0.1:5000
```
## AWS Deployment (Serverless Backend)
### 1. Lambda Setup
- Create Lambda function rekognitionLabelFunction
- Runtime: Python 3.9
- Upload lambda_function.py zipped as function.zip
- Attach policies:
    - AmazonRekognitionFullAccess
    - AmazonS3ReadOnlyAccess

### 2. API Gateway
- Create HTTP API

- Route: POST /detect
 
- Integration: Lambda (rekognitionLabelFunction)

- Enable CORS if needed


