from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from files.models import FileChoices, File
from files.serializers import FileSerializer
from quizzes.serializers import QuizListSerializer
from .models import Topic, Article
from .serializers import TopicListSerializer, TopicRetrieveSerializer, ArticleListSerializer, ArticleRetrieveSerializer


class TopicsViewSet(ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    lookup_field = 'code'
    lookup_url_kwarg = 'topic_code'
    serializer_class = TopicListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TopicListSerializer
        elif self.action == 'retrieve':
            return TopicRetrieveSerializer


class TopicVideosViewSet(ReadOnlyModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def retrieve(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, code=kwargs.get('topic_code'))
        try:
            video = topic.files.get(code=kwargs.get('video_code'))
        except File.DoesNotExist:
            raise NotFound()
        serializer = self.get_serializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        topic = get_object_or_404(
            Topic,
            code=kwargs.get('topic_code')
        )
        queryset = topic.files.filter(type=FileChoices.VIDEO)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicComicsViewSet(ReadOnlyModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def retrieve(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, code=kwargs.get('topic_code'))
        try:
            comic = topic.files.get(code=kwargs.get('comic_code'))
        except File.DoesNotExist:
            raise NotFound()
        serializer = self.get_serializer(comic)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        topic = get_object_or_404(
            Topic,
            code=kwargs.get('topic_code')
        )
        queryset = topic.files.filter(type=FileChoices.COMIC)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicArticlesViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleRetrieveSerializer
        elif self.action == 'list':
            return ArticleListSerializer

    def retrieve(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, code=kwargs.get('topic_code'))
        try:
            article = topic.articles.get(code=kwargs.get('article_code'))
        except File.DoesNotExist:
            raise NotFound()
        serializer = self.get_serializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        topic = get_object_or_404(
            Topic,
            code=kwargs.get('topic_code')
        )
        queryset = topic.articles.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicQuizzesViewSet(GenericAPIView):
    serializer_class = QuizListSerializer

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, code=kwargs.get('topic_code'))
        queryset = topic.quizzes.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
