from rest_framework import serializers

from .models import Media


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for SWAGGER response body example
    """
    class Meta:
        model = Media
        fields = ('url',)
