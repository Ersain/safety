from django.db.models import Max
from django.db.transaction import atomic
from rest_framework import serializers

from files.services.s3 import S3Services
from . import models
from .services import QuizResultServices


class QuizListSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        model = models.Quiz
        fields = ('id', 'title', 'score', 'body')

    def get_score(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        user = request.data.get('user')
        queryset = models.QuizResult.objects.filter(quiz=obj, user=user)
        return queryset.aggregate(score=Max('score'))['score']


class QuizCategoryListSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = models.QuizCategory
        fields = ('id', 'title', 'is_active', 'icon')

    def get_icon(self, obj):
        return S3Services.generate_object_url(obj.icon.name) if obj.icon else None


class QuizCategoryRetrieveSerializer(serializers.ModelSerializer):
    quizzes = QuizListSerializer(many=True)

    class Meta:
        model = models.QuizCategory
        fields = ('id', 'title', 'is_active', 'quizzes')


class QuestionOptionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionOption
        fields = ('id', 'title', 'body')


class QuestionRetrieveSerializer(serializers.ModelSerializer):
    options = QuestionOptionRetrieveSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'title', 'body', 'options')


class QuizRetrieveSerializer(serializers.ModelSerializer):
    questions = QuestionRetrieveSerializer(many=True)

    class Meta:
        model = models.Quiz
        fields = ('id', 'title', 'body', 'questions')


class AcceptedAnswerSerializer(serializers.ModelSerializer):
    is_correct = serializers.SerializerMethodField()

    class Meta:
        model = models.AcceptedAnswer
        fields = ('question', 'option', 'is_correct')

    @staticmethod
    def get_is_correct(obj):
        return obj.option.is_correct


class SubmitQuizSerializer(serializers.ModelSerializer):
    accepted_answers = AcceptedAnswerSerializer(many=True)

    class Meta:
        model = models.QuizResult
        fields = ('quiz', 'accepted_answers')

    @atomic
    def create(self, validated_data):
        answers = validated_data.pop('accepted_answers', [])
        quiz_result_instance = super().create(validated_data)
        QuizResultServices.create_accepted_answers(quiz_result_instance, answers)
        return quiz_result_instance
