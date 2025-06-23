import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FileMetadata')

def lambda_handler(event, context):
    for record in event['Records']:
        filename = record['s3']['object']['key']
        timestamp = record['eventTime']
        
        table.put_item(Item={
            'id': filename,
            'filename': filename,
            'timestamp': timestamp
        })
    
    return {
        'statusCode': 200,
        'body': json.dumps('Metadata stored successfully.')
    }
