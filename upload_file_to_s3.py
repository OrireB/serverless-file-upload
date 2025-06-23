import boto3

client = boto3.client('s3')

try:
    client.upload_file(
        Filename='Fierce.jpeg',             
        Bucket='success-guaranteed',        
        Key='Fierce.jpeg'                   
    )
    print("Uploaded file to bucket successfully.")
except Exception as e:
    print("Upload failed:", e)
