import os

import boto3
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError


sns = boto3.client("sns")
deserializer = TypeDeserializer()

topic_arn = os.getenv("SNS_TOPIC_ARN")


def deserialize_item(item):
    return {
        key: deserializer.deserialize(value)
        for key, value in item.items()
    }


def lambda_handler(event, context):
    """
    Processes DynamoDB Stream records.

    Sends an SNS notification when:
    - driving-related content was detected
    - anger confidence is greater than 80%
    """

    if not topic_arn:
        raise ValueError(
            "SNS_TOPIC_ARN environment variable must be configured."
        )

    try:
        for record in event["Records"]:
            if record.get("eventName") not in {"INSERT", "MODIFY"}:
                continue

            new_image = (
                record
                .get("dynamodb", {})
                .get("NewImage")
            )

            if not new_image:
                continue

            item = deserialize_item(new_image)

            image_name = item.get("ImageName", "Unknown image")
            driving = item.get("Driving", False)
            angry_confidence = float(
                item.get("AngryConfidence", 0)
            )

            print(
                f"Image={image_name}, "
                f"Driving={driving}, "
                f"AngryConfidence={angry_confidence}"
            )

            if driving and angry_confidence > 80:
                message = (
                    "Driver behaviour alert\n\n"
                    f"Image: {image_name}\n"
                    "Driving-related content detected: Yes\n"
                    f"Anger confidence: {angry_confidence:.2f}%\n\n"
                    "The configured alert threshold has been exceeded."
                )

                sns.publish(
                    TopicArn=topic_arn,
                    Subject="AWS Image Analysis Alert",
                    Message=message
                )

                print("SNS alert sent successfully.")

        return {
            "statusCode": 200,
            "message": "Stream records processed"
        }

    except ClientError as error:
        print(f"AWS service error: {error}")
        raise

    except Exception as error:
        print(f"Unexpected error: {error}")
        raise