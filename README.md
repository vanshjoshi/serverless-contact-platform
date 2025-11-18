🚀 Serverless Contact Platform

A fully serverless, production-ready contact message system built using AWS services.
This platform powers a frontend contact form (hosted on S3 + CloudFront) and securely stores messages in DynamoDB while sending real-time notifications via Amazon SNS.

Perfect for portfolios, real-world projects, and reusable deployment.

📌 Architecture Overview

This project uses the following AWS services:

S3 – Hosts the static website frontend

CloudFront – Delivers the frontend globally with caching

API Gateway – Acts as the API entry point

Lambda (Python) – Backend logic and validation

DynamoDB – Stores contact form submissions

SNS – Sends email notifications on new messages

📐 ASCII Architecture Diagram
S3 Static Website
        |
        v
   CloudFront CDN
        |
        v
   API Gateway
        |
        v
     Lambda
     /     \
    v       v
DynamoDB   SNS Email
(Store)    (Notify)

📁 Project Structure
serverless-contact-platform/
│
├── frontend/
│   └── index.html               # Contact form with inline JS + CSS
│
├── backend/
│   ├── src/
│   │   └── lambda_function.py   # Main backend logic
│   │
│   └── infrastructure/          # Optional: SAM/Terraform (future use)
│
├── docs/
│   └── architecture.png         # PNG architecture diagram
│
├── .gitignore
└── README.md

💡 How It Works
1️⃣ User submits contact form (name, email, message)

Form is located in frontend/index.html.

2️⃣ JavaScript sends POST request to API Gateway

Example:

fetch("YOUR_API_GATEWAY_URL/contact", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: nameValue,
    email: emailValue,
    message: messageValue,
  }),
});

3️⃣ Lambda validates + saves to DynamoDB

Lambda inserts:

id (UUID)

name

email

message

createdAt (ISO timestamp)

4️⃣ SNS sends email notification

You instantly receive the message in your inbox.

🧠 Backend Lambda Code (Python)

Located in:

backend/src/lambda_function.py


Features:

Input validation

DynamoDB write

SNS email notification

Secure CORS headers for frontend

🏗️ Deploying the Frontend (S3 + CloudFront)
Upload files:
frontend/index.html

Steps:

Create an S3 bucket

Upload frontend files

Create CloudFront distribution pointing to S3

Use CloudFront URL as your live website

🏗️ Deploying the Backend
1. Create DynamoDB table

Partition key:

id (String)

2. Create SNS Topic:

Subscribe with your email.

3. Create Lambda Function:

Runtime: Python 3.12

Handler: lambda_function.lambda_handler

Add environment variables:

TABLE_NAME=your-table
SNS_TOPIC_ARN=your-topic-arn

4. Add IAM permissions:

Lambda must have:

dynamodb:PutItem

sns:Publish

5. Create API Gateway HTTP API:

Route: POST /contact

Integration: Lambda

📬 API Usage
POST /contact

Request Body:

{
  "name": "Vansh",
  "email": "vansh@gmail.com",
  "message": "Hello!"
}


Success Response:

{
  "success": true,
  "id": "uuid-value"
}

🧹 .gitignore

Prevents cache and junk files from entering the repo.

Included in root as:

.gitignore

📄 License

MIT License or your preference.

