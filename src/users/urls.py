from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views

urlpatterns = [
    path('register-request/', views.RequestRegisterView.as_view(), name='register-request'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('login-refresh/', TokenRefreshView.as_view(), name='login-refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password-forgot/', views.ForgotPasswordView.as_view(), name='password-forgot'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password-reset'),

    path('user-profile/', views.UserProfileView.as_view(), name='current-user-profile'),
    path('user-profile/achievements/', views.UserAchievementsViewSet.as_view({
        'get': 'list'
    })),
    path('user-profile/notifications/', views.UserNotificationsViewSet.as_view({
        'get': 'list'
    })),
    path('user-profile/notifications/<int:pk>/', views.UserNotificationsViewSet.as_view({
        'get': 'retrieve'
    })),
]
