import boto3
import json

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'
    gsi_name = 'GSI1'

    # Get the location_id from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter for location_id")
        }

    location_id = event['pathParameters']['id']

    # Prepare the query for DynamoDB GSI
    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName=gsi_name,
            KeyConditionExpression='location_id = :loc_id',
            ExpressionAttributeValues={
                ':loc_id': {'N': str(location_id)}
            }
        )
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)  # Handle DynamoDB special types
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
