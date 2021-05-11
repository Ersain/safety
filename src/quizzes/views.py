from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import QuizCategory, Quiz, Question
from .serializers import (
    QuizCategoryRetrieveSerializer,
    QuizCategoryListSerializer,
    QuizListSerializer,
    QuizRetrieveSerializer,
    SubmitQuizSerializer
)


class QuizCategoryViewSet(ReadOnlyModelViewSet):
    queryset = QuizCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return QuizCategoryListSerializer
        if self.action == 'retrieve':
            return QuizCategoryRetrieveSerializer


class QuizViewSet(ReadOnlyModelViewSet):
    queryset = Quiz.objects.prefetch_related(
        Prefetch('questions', queryset=Question.objects.order_by('?'))
    )
    serializer_class = QuizListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        if self.action == 'retrieve':
            return QuizRetrieveSerializer


class SubmitQuizView(GenericAPIView):
    serializer_class = SubmitQuizSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
