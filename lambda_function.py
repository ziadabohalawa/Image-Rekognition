import boto3
import json


def lambda_handler(event, context):
    # Parse the JSON body safely
    try:
        body = json.loads(event['body'])  # this line is key
        bucket = body['bucket']
        photo = body['photo']
    except (KeyError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Invalid input format: {str(e)}'})
        }

    # Connect to Rekognition
    client = boto3.client('rekognition')
    
    try:
        response = client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            MaxLabels=10
        )

        results = []
        for label in response['Labels']:
            results.append({
                "Label": label['Name'],
                "Confidence": round(label['Confidence'], 2),
                "Instances": label.get('Instances', [])
            })

        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }