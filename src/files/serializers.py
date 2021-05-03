from rest_framework import serializers

from .models import File
from .services.s3 import S3Services


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for SWAGGER response body example
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('code', 'title', 'url')

    def get_url(self, obj):
        return S3Services.generate_object_url(obj.file.name)
