import boto3
import json

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get the 'id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    # Prepare the key for DynamoDB
    # Since this table uses a sort key, we need 'location_id' from query parameters
    if 'queryStringParameters' not in event or 'location_id' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' query parameter")
        }

    location_id = event['queryStringParameters']['location_id']

    key = {
        'id': {'S': item_id},
        'location_id': {'N': str(location_id)}
    }

    # Get the item from DynamoDB
    try:
        response = dynamo_client.get_item(TableName=table_name, Key=key)
        item = response.get('Item', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)  # Handle types like Decimal
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
