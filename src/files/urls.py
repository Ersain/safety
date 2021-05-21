from django.urls import path

from . import views

urlpatterns = [
    path('profile-photos/', views.ProfilePhotosViewSet.as_view({'get': 'list'})),
    path('profile-photos/<int:pk>/', views.ProfilePhotosViewSet.as_view({'get': 'retrieve'})),

    path('download/<str:code>/', views.ComicDownloadView.as_view()),
    path('<str:code>/', views.FileRetrieveView.as_view()),
]
