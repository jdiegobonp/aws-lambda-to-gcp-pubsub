import boto3
import json
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import base64
import requests
import os

def get_secret(secret_name):
    """Recuperar el secreto desde AWS Secrets Manager."""
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    secret = response['SecretString']
    return json.loads(secret)

def get_google_access_token(credentials_info):
    """Obtener el token de acceso de Google Cloud usando la clave de servicio."""
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_request = Request()
    credentials.refresh(auth_request)
    return credentials.token

def lambda_handler(event, context):
    message = event.get('name', 'Hello, Pub/Sub!')

    project_id = os.getenv('GOOGLE_PROJECT_ID')
    topic_id = os.getenv('GOOGLE_TOPIC_ID')
    url = f"https://pubsub.googleapis.com/v1/projects/{project_id}/topics/{topic_id}:publish"

    secret_name = os.getenv('SECRET_GOOGLE_CREDENTIALS')
    credentials_info = get_secret(secret_name)
    
    # Obtener la clave de servicio desde la variable de entorno
    encoded_credentials = os.getenv('SECRET_GOOGLE_CREDENTIALS')
    
    if not encoded_credentials:
        return {
            "statusCode": 500,
            "body": "Error: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set"
        }

    # Obtener el token de acceso de Google Cloud
    access_token = get_google_access_token(credentials_info)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    encoded_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
    
    data = {
        "messages": [
            {
                "data": encoded_message
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return {
            "statusCode": 200,
            "body": "Message published successfully"
        }
    else:
        return {
            "statusCode": response.status_code,
            "body": response.text
        }
