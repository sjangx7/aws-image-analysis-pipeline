import os
import sys
import time

import boto3
from botocore.exceptions import ClientError


def upload_images(image_files):
    """
    Uploads image files to the S3 bucket used by the image-analysis pipeline.

    Environment variables:
        AWS_REGION     - AWS region, defaults to us-east-1
        S3_BUCKET_NAME - Destination S3 bucket
    """

    region = os.getenv("AWS_REGION", "us-east-1")
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not bucket_name:
        raise ValueError(
            "S3_BUCKET_NAME environment variable must be set before uploading images."
        )

    s3 = boto3.client("s3", region_name=region)

    for image_file in image_files:
        try:
            object_name = os.path.basename(image_file)

            print(f"Uploading {image_file} to {bucket_name}...")

            s3.upload_file(
                image_file,
                bucket_name,
                object_name
            )

            print(f"{object_name} uploaded successfully.")

            print("Waiting 30 seconds before the next upload...\n")
            time.sleep(30)

        except FileNotFoundError:
            print(f"File not found: {image_file}")

        except ClientError as error:
            print(f"AWS error uploading {image_file}: {error}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python upload_images.py "
            "<image1> [image2] [image3 ...]"
        )
        sys.exit(1)

    upload_images(sys.argv[1:])