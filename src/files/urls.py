from django.urls import path

from . import views

urlpatterns = [
    path('<str:code>/', views.FileRetrieveView.as_view()),
    path('download/<str:code>/', views.ComicDownloadView.as_view()),
]
