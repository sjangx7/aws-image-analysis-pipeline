☁️ AWS Event-Driven Image Analysis Pipeline
A cloud-native, event-driven image processing pipeline built with AWS, Python and Boto3.
The system automatically processes uploaded images using Amazon Rekognition, stores analysis results in DynamoDB and generates an SNS email alert when predefined conditions are met.
Developed as part of my BSc (Hons) Computing studies and reorganised here as a portfolio project demonstrating cloud architecture, serverless computing and Infrastructure as Code.
________________________________________
📌 Project Overview
This project demonstrates how multiple managed AWS services can be combined into an automated event-driven workflow.
Images are uploaded from an EC2-based client to Amazon S3. Object creation events are sent to Amazon SQS, which triggers an AWS Lambda function. The Lambda function analyses the image using Amazon Rekognition and stores the processed results in DynamoDB.
DynamoDB Streams then triggers a second Lambda function, which evaluates the stored data and publishes an alert through Amazon SNS when the configured conditions are satisfied.
________________________________________
🏗️ Architecture
                    ┌──────────────┐
                    │     EC2      │
                    │ Upload Client│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │      S3      │
                    │ Image Storage│
                    └──────┬───────┘
                           │ Object Created
                           ▼
                    ┌──────────────┐
                    │     SQS      │
                    │ Message Queue│
                    └──────┬───────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │      Lambda 1       │
                 │   Image Processor   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Rekognition      │
                 │ Labels + Emotions   │
                 └──────────┬──────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   DynamoDB   │
                    │   Results    │
                    └──────┬───────┘
                           │ DynamoDB Stream
                           ▼
                 ┌─────────────────────┐
                 │      Lambda 2       │
                 │ Notification Logic  │
                 └──────────┬──────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │     SNS      │
                    │ Email Alert  │
                    └──────────────┘
________________________________________
✨ Key Features
📤 Automated Image Upload
A Python/Boto3 script uploads images from the client environment into an Amazon S3 bucket.
📨 Asynchronous Processing
Amazon SQS separates image upload from downstream processing, allowing components to operate independently.
🤖 Image Analysis with Rekognition
Amazon Rekognition is used to perform:
•	Label detection
•	Vehicle/driving-related object detection
•	Face detection
•	Facial emotion analysis
•	Confidence scoring
🗄️ DynamoDB Storage
Processed results are stored in DynamoDB using the image name as the partition key.
Each result contains:
•	ImageName
•	Driving
•	AngryConfidence
•	DisgustedConfidence
🚨 Automated Alerting
DynamoDB Streams trigger a second Lambda function whenever new analysis data is written.
An SNS alert is generated when:
Driving = True
AND
AngryConfidence > 80%
🏗️ Infrastructure as Code
Amazon S3 and Amazon SQS resources are provisioned using AWS CloudFormation.
Python/Boto3 scripts demonstrate programmatic creation of EC2 and DynamoDB resources.
________________________________________
🛠️ Technology Stack
AWS
•	Amazon EC2
•	Amazon S3
•	Amazon SQS
•	AWS Lambda
•	Amazon Rekognition
•	Amazon DynamoDB
•	DynamoDB Streams
•	Amazon SNS
•	Amazon CloudWatch
•	AWS CloudFormation
Development
•	Python
•	Boto3
•	YAML
•	Git
•	GitHub
________________________________________
📁 Repository Structure
aws-image-analysis-pipeline/
│
├── infrastructure/
│   └── cloudformation.yaml
│
├── scripts/
│   ├── create_ec2.py
│   ├── create_dynamodb.py
│   └── upload_images.py
│
├── lambda/
│   ├── image_processor/
│   │   └── lambda_function.py
│   │
│   └── notification/
│       └── lambda_function.py
│
├── docs/
│   └── images/
│
├── .gitignore
└── README.md
________________________________________
🔄 Processing Workflow
1. Image Upload
The Python client uploads an image to the configured S3 bucket.
2. S3 Event
Amazon S3 generates an object-created event.
3. SQS Message
The event is delivered to Amazon SQS for asynchronous processing.
4. Image Processing Lambda
The SQS message triggers the image-processing Lambda function.
The function extracts the bucket and object key and sends the image to Amazon Rekognition.
5. Rekognition Analysis
Rekognition performs label and facial analysis.
The application extracts driving-related labels and emotion confidence values.
6. DynamoDB Storage
Processed results are written to the ImageResults DynamoDB table.
7. DynamoDB Stream
A new database item produces a DynamoDB Stream event.
8. Notification Lambda
The second Lambda evaluates the newly stored result.
9. SNS Alert
If driving is detected and anger confidence exceeds 80%, an SNS notification is published.
________________________________________
⚙️ Configuration
The portfolio version avoids hard-coded credentials and environment-specific resource names.
Example environment variables include:
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-image-bucket
DYNAMODB_TABLE=ImageResults
SNS_TOPIC_ARN=your-sns-topic-arn
AMI_ID=your-ami-id
AWS credentials should be configured using normal AWS authentication mechanisms and must never be committed to the repository.
________________________________________
🏗️ CloudFormation
The CloudFormation template provisions:
•	Amazon S3 image bucket
•	Amazon SQS image-processing queue
A project suffix is provided as a parameter so resource names can be reused in different AWS environments.
________________________________________
🔐 Security Considerations
The original project was developed within an AWS Academy environment, where IAM configuration was restricted.
For a production implementation, I would improve the architecture by introducing:
•	Least-privilege IAM roles
•	Restrictive S3 bucket policies
•	Encryption using AWS KMS
•	CloudTrail auditing
•	Input validation
•	CloudWatch alarms
•	Dead-letter queues for failed SQS messages
________________________________________
📈 Architecture Improvements
Several improvements could make the pipeline more resilient and production-ready:
Dead-Letter Queue
Messages that repeatedly fail processing should be moved to an SQS DLQ rather than retried indefinitely.
Monitoring
CloudWatch alarms could provide proactive alerts for:
•	Lambda failures
•	Queue depth
•	Processing latency
•	DynamoDB errors
Least-Privilege IAM
Each Lambda and service should receive only the permissions required for its specific function.
Infrastructure Automation
The entire architecture could be moved into CloudFormation, AWS SAM, CDK or Terraform rather than combining console configuration and scripts.
Testing
Automated tests could validate:
•	SQS event parsing
•	Rekognition response handling
•	DynamoDB writes
•	Notification threshold logic
________________________________________
📚 What This Project Demonstrates
This project demonstrates practical experience with:
•	Event-driven cloud architecture
•	Serverless computing
•	Asynchronous messaging
•	AWS managed services
•	Infrastructure as Code
•	Python AWS automation
•	NoSQL databases
•	Cloud-based image analysis
•	Event-driven notifications
•	Security and cost considerations
________________________________________
⚠️ Disclaimer
This repository is a portfolio reconstruction of an academic cloud project.
Some source files have been cleaned and generalised to remove university-specific resource names and AWS Academy configuration.
The Lambda implementations reflect the architecture and behaviour of the completed system while avoiding publication of environment-specific identifiers or credentials.
________________________________________
👨‍💻 Author
Sae Jang
First-Class BSc (Hons) Computing Graduate
Glasgow Caledonian University
Interested in Software Engineering, Cloud Development, AI and Full-Stack Development.

