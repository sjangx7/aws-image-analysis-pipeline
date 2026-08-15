import os
import boto3
from botocore.exceptions import ClientError


def create_ec2_instance():
    """
    Creates a small EC2 instance using Boto3.

    Environment variables:
        AWS_REGION  - AWS region, defaults to us-east-1
        AMI_ID      - Amazon Machine Image ID
        KEY_NAME    - Optional EC2 key pair name
    """

    region = os.getenv("AWS_REGION", "us-east-1")
    ami_id = os.getenv("AMI_ID")

    if not ami_id:
        raise ValueError(
            "AMI_ID environment variable must be set before creating an EC2 instance."
        )

    key_name = os.getenv("KEY_NAME")

    ec2 = boto3.client("ec2", region_name=region)

    try:
        instance_config = {
            "ImageId": ami_id,
            "InstanceType": "t2.micro",
            "MinCount": 1,
            "MaxCount": 1,
            "TagSpecifications": [
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "image-analysis-client"
                        }
                    ]
                }
            ]
        }

        if key_name:
            instance_config["KeyName"] = key_name

        response = ec2.run_instances(**instance_config)

        instance_id = response["Instances"][0]["InstanceId"]

        print(f"EC2 instance created successfully: {instance_id}")

        return instance_id

    except ClientError as error:
        print(f"AWS error while creating EC2 instance: {error}")
        raise


if __name__ == "__main__":
    create_ec2_instance()