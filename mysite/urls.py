"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView  # new
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from polls.views import UserListAPIView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
import polls.views as views

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('polls/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('polls/password_change/', views.password_change, name='update_password'),
    # path('api/v1/auth/login/', obtain_jwt_token),
    path('polls/login/', obtain_jwt_token),
    path('api/v1/auth/refresh/', refresh_jwt_token),
    path('api/v1/auth/verify/', verify_jwt_token),
    path('api/v1/users/', UserListAPIView.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
    path('', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # new
    path('polls/login/', TemplateView.as_view(template_name='login.html'), name='login'),  # new
    # path('accounts/', include('accounts.urls')),  # new
]
