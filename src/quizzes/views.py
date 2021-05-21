from django.db.models import Prefetch
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import QuizCategory, Quiz, Question
from .serializers import (
    QuizCategoryRetrieveSerializer,
    QuizCategoryListSerializer,
    QuizListSerializer,
    QuizRetrieveSerializer,
    SubmitQuizSerializer
)
from .services import QuizResultServices


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
        instance = serializer.save(user=user)
        if instance.score >= instance.quiz.pass_mark:
            return QuizResultServices.success_quiz_notification(request.user, instance.quiz, )
        else:
            return QuizResultServices.fail_quiz_notification(request.user, instance.quiz, )
