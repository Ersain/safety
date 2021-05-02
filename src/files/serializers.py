from rest_framework import serializers

from .models import File


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for SWAGGER response body example
    """

    class Meta:
        model = File
        fields = ('url',)
