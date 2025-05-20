# 🧠 AWS Rekognition Image Detection Viewer (Flask + Serverless)

This project demonstrates how to build a lightweight, serverless computer vision pipeline using **Amazon Rekognition**, **AWS Lambda**, and **S3**, wrapped in a simple **Flask** web interface.

It allows users to:
- Select an image stored in S3
- Trigger Rekognition to detect labels and objects
- Overlay bounding boxes on the image
- View the result in a browser

---

## 📌 Architecture

```text
[User] ──> [Flask Web App]
           │
           ▼
   [API Gateway HTTP Endpoint]
           │
           ▼
       [AWS Lambda]
           │
    ┌──────┴────────────┐
    ▼                   ▼
[AWS Rekognition]   [S3 Bucket]
```
## 🔧 Technologies Used
Component	Service / Library
Object Detection	Amazon Rekognition
Storage	Amazon S3
Compute	AWS Lambda
API Gateway	AWS API Gateway (HTTP)
Frontend	Flask
Visualization	Pillow (PIL), OpenCV
SDKs	Boto3, Requests

## 📁 Project Structure
```
rekognition-flask-app/
├── app.py                     # Flask app to interact with API + draw boxes
├── lambda_function.py         # AWS Lambda handler (deployed separately)
├── static/
│   └── output.jpg             # Image with bounding boxes
├── templates/
├──   └── index.html             # HTML frontend form

```
## 🚀 How It Works
User enters the image path (key) from their S3 bucket.

Flask app sends a POST request to an API Gateway endpoint.

The Lambda function reads the image path and sends it to Rekognition.

Rekognition returns labels + bounding boxes.

Flask downloads the image, draws results, and displays the annotated image.

## 🧪 Local Setup
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
## ☁️ AWS Deployment (Serverless Backend)
### 1. Lambda Setup
Create Lambda function rekognitionLabelFunction

Runtime: Python 3.9

Upload lambda_function.py zipped as function.zip

Attach policies:

AmazonRekognitionFullAccess

AmazonS3ReadOnlyAccess

### 2. API Gateway
Create HTTP API

Route: POST /detect

Integration: Lambda (rekognitionLabelFunction)

Enable CORS if needed

## 📷 Example Output




# 🎯 Object-Detection Demo – Flask × API Gateway × Lambda × Rekognition

Type an S3 image key → the app calls **Amazon Rekognition** through a lightweight **Lambda** endpoint → returns an annotated picture plus JSON labels & confidences.  
Runs happily on the smallest CPU EC2 instance.

---

## 🏛️ High-Level Architecture

Browser EC2 (Flask) API Gateway Lambda Rekognition
─────────┐ ┌─────────────┐ ┌────────────┐ ┌───────────┐ ┌───────────┐
Upload │1. │POST /{key} │2. │proxy JSON │3. │detect_labels│──► │ ML model │
form └──► │downloads img│──► │to Lambda │──► │return JSON │ └───────────┘
▲ │draw boxes │ └────────────┘ └───────────┘
│ │HTML result │
│ └─────────────┘
└─── 4. response (img + JSON) ────────────────┘

S3 bucket
├─ images/ (source jpg/png)
└─ (bucket is private)

yaml
Copy
Edit

---

## 🧰 Tech Stack

| Layer         | Technology |
|---------------|------------|
| Front-end     | Static HTML + JavaScript  |
| Serverless Fn | **AWS Lambda** (Python 3.10) |
| Public API    | **API Gateway** HTTP API |
| ML Service    | **Amazon Rekognition** (`DetectLabels`) |
| Storage       | **Amazon S3** (`images/…`) |

---

## 📋 Prerequisites

| Resource | Minimum setup |
|----------|---------------|
| **S3 bucket** | `<BUCKET>/images/*.jpg` (keep private) |
| **Lambda**    | Paste `lambda_handler.py` code.<br>Execution role permissions:<br>• `rekognition:DetectLabels`<br>• `s3:GetObject` (read originals) |
| **API Gateway** | HTTP API → integrate Lambda → public HTTPS invoke URL `<API-URL>` |

---

## 🚀 Step-by-Step Setup

### 1  SSH & clone repo

```
ssh -i my-key.pem ubuntu@<EC2-IP>
git clone [https://github.com/<your-user>/rekognition-demo.git](https://github.com/ziadabohalawa/Image-Rekognition.git)
cd image-rekognition
```
### 2 Install Python deps
```
pip install -r requirements.txt
```
### 3 Run Flask app
```
python app.py \
    --bucket  <YOUR-BUCKET> \
    --api-url <API-URL> \
    --debug
# Flask binds to 0.0.0.0:5000
```
4 Open in browser
```http://<EC2-PUBLIC-IP>:5000```
Type an image key, e.g. images/dog.jpg → see bounding boxes & JSON.

🗂 Project Layout
```
image-rekognition/
├─ app.py              # Flask factory + drawing logic
├─ lambda_handler.py   # (deploy inside Lambda)
├─ templates/
│   └─ index.html      # form + result view
├─ static/output.jpg   # generated file (runtime)
├─ requirements.txt
└─ README.md
```
🙏 Acknowledgements
Amazon Rekognition – fully managed vision APIs

Flask (© Pallets) – BSD-licensed micro-framework

Pillow – the friendly PIL fork

