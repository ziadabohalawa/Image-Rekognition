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

| Layer | Technology |
|-------|------------|
| UI & Backend | **Flask 2** (Python 3.10) |
| Image Ops    | Pillow (PIL) |
| Serverless   | **AWS Lambda** (Python run-time) |
| API Gateway  | HTTP API – forwards to Lambda |
| ML Service   | **Amazon Rekognition** (`detect_labels`) |
| Storage      | **Amazon S3** (`images/…`) |
| Compute node | **EC2 t3.micro** (or larger) |

---

## 📋 Prerequisites

| What | Minimum setup |
|------|---------------|
| **S3 bucket** | `<YOUR-BUCKET>/images/*.jpg`  |
| **Lambda**    | Paste `lambda_handler.py` code & give it **`rekognition:DetectLabels`** |
| **API Gateway** | HTTP API → integrate Lambda → public invoke URL `<API‐URL>` |
| **EC2 security group** | Inbound TCP 22 (SSH) & 5000 (Flask) |
| **IAM role on EC2** | `s3:GetObject` (read-only) on the bucket |

---

## 🚀 Step-by-Step Setup

### 1  SSH & clone repo

```
ssh -i my-key.pem ubuntu@<EC2-IP>
git clone https://github.com/<your-user>/rekognition-demo.git
cd rekognition-demo
python3 -m venv venv && source venv/bin/activate
```
### 2 Install Python deps
```
pip install -r requirements.txt   # Flask, boto3, Pillow, requests
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
rekognition-demo/
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

