from django.urls import path

from core.views import MediaDownloadView

urlpatterns = [
    path('testing/', MediaDownloadView.as_view())
]
