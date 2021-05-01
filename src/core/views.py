import boto3
import requests
from botocore.client import Config
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.views.generic import View


class MediaDownloadView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        s3 = boto3.resource(
            region_name='eu-central-1',
            service_name='s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4')
        )
        url = s3.meta.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": settings.S3_BUCKET_NAME,
                "Key": '982491acceb6c9dde0d5e49dab1e7540c5faa1de.webm',
            },
        )
        r = requests.get(url=url, stream=True)
        r.raise_for_status()
        response = StreamingHttpResponse(
            (chunk for chunk in r.iter_content(512 * 1024)),
            content_type='video/webm'
        )
        response['Content-Disposition'] = 'inline; filename=982491acceb6c9dde0d5e49dab1e7540c5faa1de.webm'
        return response
