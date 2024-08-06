# aws-lambda-to-gcp-pubsub
AWS Lambda Function to publish a message to a GCP pubsub.

## Installation steps
Following are the steps to create a package to upload to the AWS console in the ZIP option.

### Create and activate an virtual environment in python
```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies/libraries
```
pip install requests google-auth
```

### Create a ZIP file with the dependencies/libraries 
```
cd venv/lib/python3.x/site-packages
zip -r9 ${OLDPWD}/function.zip .
```

### Go back the work parh and include the lambda file to the ZIP file
```
cd ${OLDPWD}
zip -g function.zip lambda_function.py
```

## Store the GCP credentials in AWS Secrets Manager

1. Create a service account in Google Cloud and download the JSON key file.
2. Store the key file in AWS Secrets Manager.
3. Update the IAM Execution Role in Lambda including the following permissions:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:<aws_region>:<aws_account_id>:secret:<secret>"
    }
  ]
}
```

## Configure the Environment Variables in the Lambda Function
In the ``lambda_function.py`` file, there are references to the following environment variables:

| Name | Value |
| ---- | ----- |
| GOOGLE_PROJECT_ID | Google project ID (Static) |
| GOOGLE_TOPIC_ID | Google Topic ID (PubSub) |
| SECRET_GOOGLE_CREDENTIALS | Secret name in AWS Secrets Manager with the google creds file |
