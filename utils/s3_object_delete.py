import boto3
from django.conf import settings

def delete_s3_object(object_name):
    s3 = boto3.client('s3')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3.delete_object(Bucket=bucket_name, Key=object_name)