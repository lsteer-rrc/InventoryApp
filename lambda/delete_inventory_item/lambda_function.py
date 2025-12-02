import boto3
import json

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Check for required path and query parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }
    if 'queryStringParameters' not in event or 'location_id' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' query parameter")
        }

    item_id = event['pathParameters']['id']
    location_id = event['queryStringParameters']['location_id']

    # Prepare the key for DynamoDB
    key = {
        'id': {'S': item_id},
        'location_id': {'N': str(location_id)}
    }

    # Attempt to delete the item
    try:
        dynamo_client.delete_item(TableName=table_name, Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} at location {location_id} deleted successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
    