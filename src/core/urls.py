from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('topics', views.TopicsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('topics/<str:topic_code>/videos/', views.TopicVideosViewSet.as_view({'get': 'list'})),
    path('topics/<str:topic_code>/videos/<str:video_code>/', views.TopicVideosViewSet.as_view({'get': 'retrieve'})),
    path('topics/<str:topic_code>/comics/', views.TopicComicsViewSet.as_view({'get': 'list'})),
    path('topics/<str:topic_code>/comics/<str:comic_code>/', views.TopicComicsViewSet.as_view({'get': 'retrieve'})),
    path('topics/<str:topic_code>/articles/', views.TopicArticlesViewSet.as_view({'get': 'list'})),
    path('topics/<str:topic_code>/articles/<str:article_code>/',
         views.TopicArticlesViewSet.as_view({'get': 'retrieve'})),
    path('topics/<str:topic_code>/quizzes/', views.TopicQuizzesViewSet.as_view())
]
