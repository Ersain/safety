from django.utils.text import Truncator
from rest_framework import serializers

from files.models import FileChoices
from files.serializers import FileSerializer
from files.services.s3 import S3Services
from quizzes.serializers import QuizListSerializer
from .models import Topic, Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('code', 'title', 'body')

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['body'] = Truncator(result.pop('body', '')).words(15)
        return result


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('code', 'title', 'body')


class TopicListSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('code', 'title', 'is_active', 'icon', 'size')

    def get_icon(self, obj: Topic):
        return S3Services.generate_object_url(obj.icon.name) if obj.icon else None


class TopicRetrieveSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    comics = serializers.SerializerMethodField()
    articles = ArticleListSerializer(many=True)
    quizzes = QuizListSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('code', 'title', 'videos', 'comics', 'articles', 'quizzes')

    def get_videos(self, obj):
        queryset = obj.files.filter(type=FileChoices.VIDEO)
        return FileSerializer(queryset, many=True).data

    def get_comics(self, obj):
        queryset = obj.files.filter(type=FileChoices.COMIC)
        return FileSerializer(queryset, many=True).data
