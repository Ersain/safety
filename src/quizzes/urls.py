from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuizViewSet.as_view({'get': 'list'}), name='quizzes-list'),
    path('<int:pk>/', views.QuizViewSet.as_view({'get': 'retrieve'}), name='quizzes-retrieve'),

    path(
        'categories/',
        views.QuizCategoryViewSet.as_view({'get': 'list'}),
        name='quiz-categories-list'
    ),
    path(
        'categories/<int:pk>/',
        views.QuizCategoryViewSet.as_view({'get': 'retrieve'}),
        name='quiz-categories-retrieve'
    ),

    path('submit-quiz/', views.SubmitQuizView.as_view(), name='submit-quiz')
]
