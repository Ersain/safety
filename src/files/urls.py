from django.urls import path

from . import views

urlpatterns = [
    path('videos/<str:code>/', views.VideoRetrieveView.as_view()),
]
