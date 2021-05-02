from django.urls import path

from . import views

urlpatterns = [
    path('media/<str:code>/', views.FileRetrieveView.as_view()),
]
