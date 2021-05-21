from django.http import FileResponse
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import File, FileChoices, ProfilePhoto
from .serializers import FileSerializer, ProfilePhotoSerializer


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
        file_handle = obj.file.open()
        response = FileResponse(file_handle, content_type='application/pdf')
        response['Content-Length'] = obj.file.size
        response['Content-Disposition'] = f'attachment; filename="{obj.file.name}"'

        return response


class ProfilePhotosViewSet(ReadOnlyModelViewSet):
    queryset = ProfilePhoto.objects.all()
    serializer_class = ProfilePhotoSerializer
