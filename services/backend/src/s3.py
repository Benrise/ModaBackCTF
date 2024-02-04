import boto3
from config import settings

def s3_upload(content: bytes, key: str):
    session = boto3.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=settings.YANDEX_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.YANDEX_S3_SECRET_ACCESS_KEY,
    )
    
    bucket_name = settings.YANDEX_S3_BUCKET_NAME
    
    s3.put_object(Body=content, Bucket=bucket_name, Key=key)