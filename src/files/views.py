import requests
from django.http import HttpResponse, FileResponse
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import File, FileChoices
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
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComicDownloadView(GenericAPIView):
    serializer_class = None
    lookup_field = 'code'

    def get_queryset(self):
        return File.objects.filter(type=FileChoices.COMIC)

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        obj: File = self.get_object()
        object_url = S3Services.generate_object_url(obj.file.name)
        r = requests.get(url=object_url, stream=True)
        r.raise_for_status()
        response = HttpResponse(r.raw, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={obj.file.name}'
        return response


class ComicRedirectView(GenericAPIView):
    serializer_class = None
    lookup_field = 'code'

    def get_queryset(self):
        return File.objects.filter(type=FileChoices.COMIC)

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        obj: File = self.get_object()
        file_handle = obj.file.open()
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = obj.file.size
        response['Content-Disposition'] = f'attachment; filename="{obj.file.name}"'

        return response
