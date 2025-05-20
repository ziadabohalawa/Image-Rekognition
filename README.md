# 🐆📦 Object-Detection Demo on AWS (Flask + API Gateway → Lambda → Rekognition)

A lightweight web app that lets you type an S3 image key, instantly calls **Amazon Rekognition** via a serverless **Lambda** function, and shows the picture with bounding boxes and confidence scores—all running on a tiny CPU EC2 instance.

---

## 🏛️ Architecture

Browser Flask on EC2 API Gateway Lambda Rekognition
┌────────┐ ① POST {key} ┌─────────────┐ ② forward JSON ┌─────────────┐ ③ detect_labels()
│Upload │ ───────────────▶ │ app.py │ ────────────────▶│ handler.py │ ───────────────────▶
│ form │ │ (Python) │ │ (Python) │
└────────┘ │ downloads img│◀───────────────┐ └─────────────┘
▲ │ draws boxes │ ④ JSON result │
│ ⑥ HTML w/ <img> └─────┬────────┘ │
│ │ │
└───────────────────────────┴────────────────────────┘
⑤ GET object from S3 bucket

yaml
Copy
Edit

* **S3 bucket**  
  `my-bucket-name/`  
  &nbsp;&nbsp;&nbsp;&nbsp;└─ **images/** `example.jpg`, …

* **Security** – EC2 gets an IAM _role_ with `s3:GetObject` only.  
  Lambda gets `rekognition:DetectLabels`.

---

## 🚀 Quick Start

### 1  Clone & install on EC2

```bash
git clone https://github.com/<your-user>/rekognition-demo.git
cd rekognition-demo
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt        # Flask, boto3, Pillow, requests
2 Create / configure AWS resources
Resource	Minimum setup
S3	my-bucket-name/images/*.jpg (keep bucket private)
Lambda	Runtime = Python 3.10
Paste code from lambda_handler.py
Environment: none needed
API Gateway	HTTP API → integrate Lambda → public invoke URL
IAM roles	EC2Role: s3:GetObject on bucket · LambdaRole: rekognition:DetectLabels

3 Set environment & run Flask
bash
Copy
Edit
export FLASK_APP=app.py
python app.py \
  --bucket  my-bucket-name \
  --api-url https://abc123.execute-api.eu-central-1.amazonaws.com/
Flask listens on 0.0.0.0:5000 (adjust Security-Group to open port 5000).

4 Browse
cpp
Copy
Edit
http://<EC2-PUBLIC-IP>:5000
Enter images/example.jpg → get bounding-box overlay + confidence list.

🗂️ Files
File	Purpose
app.py	Flask factory + image annotation logic
lambda_handler.py	(Deployed inside Lambda) – calls rekognition.detect_labels
templates/index.html	Simple form & result rendering
static/output.jpg	Generated annotated image (overwritten each request)
requirements.txt	Flask · requests · boto3 · Pillow

🛠️ Tech Stack
Layer	Technology
Frontend	HTML + Jinja2
Backend (web)	Flask 2
Serverless API	AWS Lambda (Python 3.10)
ML service	Amazon Rekognition
Storage	Amazon S3
Compute host	EC2 t3.micro / t3.small (only downloads & draws boxes)
Imaging	Pillow (PIL)

🙏 Acknowledgements
Amazon Rekognition – managed object-detection service

Flask (© Pallets) – BSD-licensed Python micro-framework

Pillow (PIL fork) – image processing library

