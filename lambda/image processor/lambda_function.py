import json
import os

import boto3
from botocore.exceptions import ClientError


rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")

table_name = os.getenv("DYNAMODB_TABLE", "ImageResults")
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    """
    Processes SQS messages generated from S3 object creation events.

    For each uploaded image:
    - extracts the S3 bucket/key from the SQS message
    - performs label detection using Rekognition
    - performs face/emotion analysis
    - determines whether driving-related content is present
    - stores the processed result in DynamoDB
    """

    try:
        for record in event["Records"]:
            body = json.loads(record["body"])

            s3_event = body["Records"][0]["s3"]

            bucket = s3_event["bucket"]["name"]
            key = s3_event["object"]["key"]

            print(f"Processing image: s3://{bucket}/{key}")

            label_response = rekognition.detect_labels(
                Image={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": key
                    }
                },
                MaxLabels=10,
                MinConfidence=70
            )

            labels = [
                label["Name"]
                for label in label_response.get("Labels", [])
            ]

            print(f"Detected labels: {labels}")

            driving_keywords = {
                "Car",
                "Vehicle",
                "Driving",
                "Transportation",
                "Automobile",
                "Steering Wheel"
            }

            driving = any(
                label in driving_keywords
                for label in labels
            )

            face_response = rekognition.detect_faces(
                Image={
                    "S3Object": {
                        "Bucket": bucket,
                        "Name": key
                    }
                },
                Attributes=["ALL"]
            )

            angry_confidence = 0.0
            disgusted_confidence = 0.0

            for face in face_response.get("FaceDetails", []):
                for emotion in face.get("Emotions", []):
                    emotion_type = emotion["Type"]
                    confidence = emotion["Confidence"]

                    if emotion_type == "ANGRY":
                        angry_confidence = max(
                            angry_confidence,
                            confidence
                        )

                    elif emotion_type == "DISGUSTED":
                        disgusted_confidence = max(
                            disgusted_confidence,
                            confidence
                        )

            result = {
                "ImageName": key,
                "Driving": driving,
                "AngryConfidence": str(
                    round(angry_confidence, 2)
                ),
                "DisgustedConfidence": str(
                    round(disgusted_confidence, 2)
                )
            }

            table.put_item(Item=result)

            print(f"Stored analysis result: {result}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Images processed successfully"}
            )
        }

    except ClientError as error:
        print(f"AWS service error: {error}")
        raise

    except Exception as error:
        print(f"Unexpected error: {error}")
        raise