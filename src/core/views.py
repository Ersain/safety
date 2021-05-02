from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Media, MediaChoices
from .serializers import VideoSerializer
from .services.s3 import S3Services


class VideoRetrieveView(GenericAPIView):
    serializer_class = VideoSerializer
    lookup_field = 'code'
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Media.objects.filter(type=MediaChoices.VIDEO)

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        obj: Media = self.get_object()
        url = S3Services.generate_object_url(obj.file.name)
        return Response({'url': url})
