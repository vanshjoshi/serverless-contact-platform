import json
import os
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.client("dynamodb")
sns = boto3.client("sns")  # <-- ADDED

TABLE_NAME = os.environ["TABLE_NAME"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]  # <-- ADDED


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        # Validate required fields
        if not body.get("name") or not body.get("email") or not body.get("message"):
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({"error": "Missing fields"})
            }

        # Generate unique ID
        item_id = str(uuid.uuid4())

        # Put item into DynamoDB
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "id": {"S": item_id},
                "name": {"S": body["name"]},
                "email": {"S": body["email"]},
                "message": {"S": body["message"]},
                "createdAt": {"S": datetime.utcnow().isoformat()}
            }
        )

        # ---------- SNS PUBLISH (ADDED) ----------
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="New Portfolio Contact Submission",
            Message=(
                f"New Contact Form Submission:\n\n"
                f"ID: {item_id}\n"
                f"Name: {body['name']}\n"
                f"Email: {body['email']}\n"
                f"Message: {body['message']}\n"
                f"Created At: {datetime.utcnow().isoformat()}"
            )
        )
        # -----------------------------------------

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"success": True, "id": item_id})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"error": str(e)})
        }

