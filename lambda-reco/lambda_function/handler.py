import json
from model_utils import load_model_from_s3, predict_top_k

def lambda_handler(event, context):
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "*"
            },
            "body": json.dumps({"message": "CORS preflight OK"})
        }

    user_id = event.get("queryStringParameters", {}).get("user_id")
    if not user_id:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Missing user_id"})
        }

    model, user_map, item_map, clicked = load_model_from_s3()
    top_k = predict_top_k(user_id, model, user_map, item_map, clicked)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "user_id": user_id,
            "recommendations": top_k
        })
    }
