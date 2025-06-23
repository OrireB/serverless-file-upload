# 📁 Serverless File Upload System with AWS

A simple, fully serverless system that allows users to upload files to an S3 bucket, stores file metadata in DynamoDB, and lets you view the metadata via an API endpoint or through a simple HTML page.

---

## 🚀 Features
- 📦 Upload files to **S3**
- ⚙️ Automatically triggers **Lambda**
- 📝 Saves metadata (filename, timestamp) to **DynamoDB**
- 🌐 Fetch metadata via **API Gateway**
- 💻 (Optional) HTML page to view uploaded file metadata

---

## 🛠 Technologies Used
- **Amazon S3** – File storage
- **AWS Lambda** – Serverless compute
- **Amazon DynamoDB** – Metadata storage
- **API Gateway** – Public API access
- **Boto3 (Python SDK)** – Used in Lambda
- **HTML + JavaScript** – Optional UI to view metadata

---

## 🧱 Project Architecture Overview

You'll create:

1. ✅ S3 Bucket — For file uploads.
2. ✅ DynamoDB Table — Stores metadata (filename, timestamp).
3. ✅ Lambda Function 1 — Stores file metadata from S3 to DynamoDB.
4. ✅ S3 Trigger — Invokes the Lambda on file upload.
5. ✅ API Gateway + Lambda — Exposes metadata via a public REST API.
6. ✅ (Optional) HTML Viewer — A simple web page that fetches and displays file metadata.

---

## 📂 Step-by-Step Setup

### 🔹 Step 1: Create an S3 Bucket

> The S3 bucket is where your users (or scripts) will upload files. These uploads will automatically trigger the Lambda function.

1. Go to AWS Console → **S3 > Create Bucket**
2. Name: `success-guaranteed` (or a unique name)
3. Leave default settings
4. Click **Create Bucket**

The project follows official [boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) for working with AWS services in Python.

**Or create via code:**

[create_s3_bucket.py](https://github.com/OrireB/serverless-file-upload/commit/72346e7604f417096312fa3238fc8597df41d6ba#diff-5ff7df0666e13dc29b7602c447b4fcb4ce476ba1537778e5153d80a8f277b799)

---

### 🔹 Step 2: Create a DynamoDB Table
> This table will store metadata about uploaded files: filename and upload timestamp.

1. Go to AWS Console → DynamoDB → Tables → Create Table
2. Table Name: FileMetadata
3. Partition Key:
   - Name: id
   - Type: String
4. Capacity Mode: On-Demand
5. Advanced Settings:No changes needed for default access settings unless you’re restricting access.
6. Click Create Table

---

### 🔹 Step 3: Create Lambda Function – MyStoreFileMetadata
> This function is triggered by the S3 bucket and saves metadata to DynamoDB.

1. Go to AWS Console → Lambda → Create Function
2. Choose: **Author from scratch**
3. Function name: **MyStoreFileMetadata**
4. Runtime: **Python 3.13**
5. Architecture: **x86_64**
6. Permissions: **Create a new role with basic Lambda permissions**
7. Click “Create Function”
7. Replace the default code with:
[store_metadata.py](https://github.com/OrireB/serverless-file-upload/commit/9ca0e7e108f0b13fb82168a31284cc49e727704a#diff-b5f8facaa044506a75905c36e30a8e24c93ae52c19520fcb59443ee88d0a0ee3)
8. Click **Deploy**

> This will add DynamoDB Read Permissions
1. Go to: AWS Console → IAM → Roles
2. Find the IAM role created for MyStoreFileMetadata
3. Click the role → Add permissions → Attach policies
4. Search and attach:
   - AmazonDynamoDBReadOnlyAccess (for simplicity, or create a custom policy later)
   - You can replace this with a more restricted policy if needed, but for the project full access is fine.

---

### 🔹 Step 4: Add S3 Trigger to Lambda
> This ensures the Lambda runs every time a file is uploaded to your S3 bucket.

1. Go to: AWS Console → Lambda → Function
2. Click the **“+ Add trigger”** button.
3. Choose:
   - Trigger configuration: Select S3
   - Bucket: **Select success-guaranteed**
   - Event type: Choose **PUT** (this means: when a file is uploaded)
3. Recursive invocation: Check the confirmation box
4. Click **Add**

---

### 🔹 Step 5: Create Lambda Function – GetFileMetadata
> Create an API Gateway + Lambda to Fetch Metadata
The goal:
> You’ll create a new Lambda function that will read all file metadata from DynamoDB and return it via an API Gateway endpoint (so you can access it with a browser or curl).

1. Go to AWS Console → Lambda → Create Function
2. Choose: **Author from scratch**
3. Function name: GetFileMetadata
4. Runtime: Python 3.13
5. Architecture: x86_64
6. Permissions: **Create a new role with basic Lambda permissions**
7. Click “Create Function”
7. Replace the default code with:
[get_metadata.py](https://github.com/OrireB/serverless-file-upload/commit/e66adc27db69682fc6459417167a81965f9bbbba#diff-c559ecb1413fe3931778f8c5d914925ad738426c88134a81372bc1cc7ad80480)
8. Click **Deploy**
9. Go to **IAM** > **Roles** → find this Lambda’s role → **Add policy**: AmazonDynamoDBReadOnlyAccess

---

### 🔹 Step 6: Create REST API with API Gateway
> Exposes the Lambda above via a URL so it can be called from a browser or HTML file.

1. Go to AWS Console → API Gateway → Create API
2. Choose: REST API → Build
3. API Name: FileMetadataAPI
4. Endpoint Type: Keep as Regional
5. IP address type: IPv4
6. Click **Create API**

## Add Resource and Method
1. Under /, click Actions → Create Resource
   - Resource Name: metadata
   - Resource Path: /metadata (auto-filled)
   - CORS (Cross Origin Resource Sharing) Info → Click ✅ checkmark
Click **Create Resource**

## Create a GET Method
2. Select /metadata → Actions → Create Method
- Choose GET from the dropdown → Click ✅ checkmark
- Configure the method:
  - Integration type: Lambda Function
  - Use Lambda Proxy integration: ✅ checked
  - Lambda Function Name: GetFileMetadata
- Click **Save**

## Deploy the API
- Click “Actions” → “Deploy API”
- Deployment stage:
  - Choose [New Stage]
  - Stage name: prod
- Click Deploy

### After deployment, note the Invoke URL
 Exanple:
https://u2shohuema.execute-api.us-east-1.amazonaws.com/prod/metadata

---

### 🔹 Step 7: Upload a File to S3 for Testing
> Uploading any file will trigger Lambda and populate DynamoDB.
When you upload a file like Fierce.jpeg to the success-guaranteed bucket, AWS will:

1.Trigger your Lambda function
2. Lambda will store file metadata in DynamoDB table FileMetadata
[upload_file_to_s3.py](https://github.com/OrireB/serverless-file-upload/commit/dcd21961c2f8bb03b2ac3dc8fae3a2ac2c9c1628#diff-534e5fe1f742a0660dd0fc9b7a7b3c8eb83fe0720ad48b02f0c3146004529cef)


- Go to DynamoDB → FileMetadata → Check if metadata is stored.

---

### 🔹 Step 8: Create and Host HTML Viewer (Optional but Recommended)
> This web page makes it easy to view metadata without using Postman or the browser console.

##Create HTML File
- Save the code below as file-metadata.html in your VS Code or text editor:

---

##Upload and Host HTML in S3
1. Upload the file-metadata.html to your success-guaranteed bucket
2. Enable Static Website Hosting under bucket Properties
3. Set:
   - Index document: file-metadata.html
5. Make the file public (Actions > Make public)
6. Open the S3 website URL to view your HTML page live

---

###🧪 Expected Output
- If all is configured correctly:
- Now,
- Test the Full URL in the Browser
1. Paste this in your browser:
   - https://u2shohuema.execute-api.us-east-1.amazonaws.com/prod/metadata

2. If everything is set up correctly, you’ll see:
   - A JSON array with metadata from your DynamoDB table
   - You should see a JSON response like:

```python
[
  {
    "id": "Fierce.jpeg",
    "filename": "Fierce.jpeg",
    "timestamp": "2025-06-18 18:30:00"
  }
]```

---

###🧹 Cleanup Checklist (Avoid Unexpected Charges)
1. 🗑 Delete S3 Bucket (after emptying it)
2. 🗑 Delete both Lambda functions
3. 🗑 Delete DynamoDB table FileMetadata
4. 🗑 Delete API Gateway
5. 🗑 Delete IAM roles (if not reused)
6. 🗑 Delete CloudWatch logs (optional)

---

###✅ Final Tip
Always double-check your AWS Billing Dashboard to ensure no lingering services are active that may incur charges.
