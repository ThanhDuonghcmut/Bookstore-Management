from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('refresh', TokenRefreshView.as_view(), name='refresh_token'),
    # path('test-token', views.test_token, name='test_token')
]