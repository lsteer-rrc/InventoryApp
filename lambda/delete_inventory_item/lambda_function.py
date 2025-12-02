import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    try:
        item_id = event['pathParameters']['id']
    except (KeyError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    try:
        location_id = event['queryStringParameters']['location_id']
    except (KeyError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' query parameter")
        }

    key = {
        'id': {'S': item_id},
        'location_id': {'N': str(location_id)}
    }

    try:
        dynamo_client.delete_item(
            TableName=table_name,
            Key=key,
            ConditionExpression="attribute_exists(id) AND attribute_exists(location_id)"
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} at location {location_id} deleted successfully.")
        }
    except dynamo_client.exceptions.ConditionalCheckFailedException:
        return {
            'statusCode': 404,
            'body': json.dumps(f"Item with ID {item_id} at location {location_id} not found.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }
