import os
import boto3
from botocore.exceptions import ClientError


def create_dynamodb_table():
    """
    Creates the DynamoDB table used to store image-analysis results.

    Environment variables:
        AWS_REGION     - AWS region, defaults to us-east-1
        DYNAMODB_TABLE - Table name, defaults to ImageResults
    """

    region = os.getenv("AWS_REGION", "us-east-1")
    table_name = os.getenv("DYNAMODB_TABLE", "ImageResults")

    dynamodb = boto3.resource("dynamodb", region_name=region)

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "ImageName",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "ImageName",
                    "AttributeType": "S"
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        print(f"Creating DynamoDB table: {table_name}")

        table.wait_until_exists()

        print("DynamoDB table created successfully.")

        return table

    except ClientError as error:
        print(f"AWS error while creating DynamoDB table: {error}")
        raise


if __name__ == "__main__":
    create_dynamodb_table()