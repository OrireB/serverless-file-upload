import boto3

client = boto3.client('s3', region_name='us-east-1')

response = client.create_bucket(
    Bucket='success-guaranteed'
)

print("Bucket created:", response)
