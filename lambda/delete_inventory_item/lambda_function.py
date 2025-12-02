import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get ID from path parameters
    try:
        item_id = event['pathParameters']['id']
    except (KeyError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key = {'id': {'S': item_id}}  # Use only partition key

    try:
        dynamo_client.delete_item(
            TableName=table_name,
            Key=key,
            ConditionExpression="attribute_exists(id)"
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} deleted successfully.")
        }
    except dynamo_client.exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 404,
            'body': json.dumps(f"Item with ID {item_id} not found.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
