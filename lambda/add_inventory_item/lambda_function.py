import json
import boto3
import uuid

def lambda_handler(event, context):
    body = event.get('body')
    
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. No body provided.")
        }

    # If body is already dict (some test setups)
    if isinstance(body, dict):
        data = body
    else:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps("Bad request. Invalid JSON.")
            }

    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'
    unique_id = str(uuid.uuid4())

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
