from rest_framework import serializers

from .models import File, ProfilePhoto
from .services.s3 import S3Services


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for SWAGGER response body example
    """
    url = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('code', 'title', 'url', 'icon')

    def get_url(self, obj):
        return S3Services.generate_object_url(obj.file.name)

    def get_icon(self, obj: File):
        return S3Services.generate_object_url(obj.icon.name) if obj.icon else None


class ProfilePhotoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = ProfilePhoto
        fields = ('id', 'photo')

    def get_photo(self, obj: ProfilePhoto):
        return S3Services.generate_object_url(obj.photo.name) if obj.photo else None
