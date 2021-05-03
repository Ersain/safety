from rest_framework import serializers
from django.utils.text import Truncator

from files.models import FileChoices
from files.serializers import FileSerializer
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
    class Meta:
        model = Topic
        fields = ('code', 'title', 'is_active')


class TopicRetrieveSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    comics = serializers.SerializerMethodField()
    articles = ArticleListSerializer(many=True)

    class Meta:
        model = Topic
        fields = ('code', 'title', 'videos', 'comics', 'articles')

    def get_videos(self, obj):
        queryset = obj.files.filter(type=FileChoices.VIDEO)
        return FileSerializer(queryset, many=True).data

    def get_comics(self, obj):
        queryset = obj.files.filter(type=FileChoices.COMIC)
        return FileSerializer(queryset, many=True).data
