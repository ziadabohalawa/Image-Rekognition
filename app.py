from flask import Flask, render_template, request, url_for, current_app
import requests
import json
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import argparse
import os
from typing import Dict, List, Any, Tuple, Optional

def create_app(config=None):
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__)
    
    app.config.update(
        S3_BUCKET=None,
        API_URL=None,
        DEBUG=False
    )
    
    if config:
        app.config.update(config)
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        image_url = None
        if request.method == 'POST':
            photo = request.form['photo']
            image_url = process_image(photo)
        return render_template('index.html', image_url=image_url)
    
    return app

def process_image(photo: str) -> str:
    detection_results = get_detection_results(photo)
    
    img = get_and_annotate_image(photo, detection_results)
    
    output_path = os.path.join("static", "output.jpg")
    img.save(output_path)
    
    return url_for('static', filename='output.jpg')

def get_detection_results(photo: str) -> List[Dict[str, Any]]:
    payload = {
        "bucket": current_app.config['S3_BUCKET'],
        "photo": photo
    }
    
    response = requests.post(current_app.config['API_URL'], json=payload)
    
    outer = response.json()
    
    if isinstance(outer, list):
        data = outer
    elif isinstance(outer, dict) and 'body' in outer:
        if isinstance(outer['body'], str):
            data = json.loads(outer['body'])
        else:
            data = outer['body']
    else:
        data = outer
    
    current_app.logger.info(f"API response: {data}")
    return data

def get_and_annotate_image(photo: str, detection_results: List[Dict[str, Any]]) -> Image.Image:
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=current_app.config['S3_BUCKET'], Key=photo)
    img_data = obj['Body'].read()
    img = Image.open(BytesIO(img_data))
    
    draw = ImageDraw.Draw(img)
    for item in detection_results:
        for instance in item.get('Instances', []):
            draw_bounding_box(draw, img.size, instance['BoundingBox'], 
                             f"{item['Label']} ({item['Confidence']}%)")
    
    return img

def draw_bounding_box(draw: ImageDraw.Draw, img_size: Tuple[int, int], 
                      box: Dict[str, float], label: str, color: str = "red", 
                      width: int = 2) -> None:

    w, h = img_size
    left = box['Left'] * w
    top = box['Top'] * h
    width_px = box['Width'] * w
    height_px = box['Height'] * h
    
    shape = [(left, top), (left + width_px, top + height_px)]
    draw.rectangle(shape, outline=color, width=width)
    
    draw.text((left, top - 10), label, fill=color)

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--api-url', required=True, help='API endpoint URL')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()
    
    config = {
        'S3_BUCKET': args.bucket,
        'API_URL': args.api_url,
        'DEBUG': args.debug
    }
    app = create_app(config)
    
    app.run(debug=args.debug)

if __name__ == '__main__':
    main()
