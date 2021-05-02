import boto3
from botocore.client import Config
from django.conf import settings

s3 = boto3.resource(
    region_name='eu-central-1',
    service_name='s3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)


class S3Services:
    @staticmethod
    def generate_object_url(object_key):
        return s3.meta.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": object_key,
            },
        )
