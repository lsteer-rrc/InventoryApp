import json
import boto3
import ulid

def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide valid JSON data.")
        }

    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Generate a unique ID using ULID
    unique_id = str(ulid.new())

    # Prepare the item for DynamoDB
    try:
        dynamo_client.put_item(
            TableName=table_name,
            Item={
                'id': {'S': unique_id},
                'location_id': {'N': str(data['location_id'])},
                'item_name': {'S': data['item_name']},
                'item_description': {'S': data.get('item_description', '')},
                'item_qty': {'N': str(data['item_qty'])},
                'item_price': {'N': str(data['item_price'])}
            }
        )
        return {
            'statusCode': 201,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
    
    