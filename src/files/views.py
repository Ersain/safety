from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import File
from .serializers import FileSerializer


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
