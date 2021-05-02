from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import File
from .serializers import FileSerializer
from .services.s3 import S3Services


class FileRetrieveView(GenericAPIView):
    serializer_class = FileSerializer
    lookup_field = 'code'
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return File.objects.all()

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        obj: File = self.get_object()
        url = S3Services.generate_object_url(obj.file.name)
        return Response({'url': url})
