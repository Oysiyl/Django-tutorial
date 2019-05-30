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
from rest_framework.schemas import get_schema_view
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(title='Pastebin API')

api_patterns = [
    path('schema/', schema_view),
    path('api/v1/auth/login/', obtain_jwt_token),
    path('api/v1/auth/refresh/', refresh_jwt_token),
    path('api/v1/auth/verify/', verify_jwt_token),
    path('api/v1/users/', UserListAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

registration_patterns = [
    path('password_change/', views.password_change, name='password_change'),
    path('email_change/', views.email_change, name='email_change'),
    path('change_names/', views.change_names, name='change_names'),
    # path('signup/', views.SignUp.as_view(template_name='registration/signup.html'), name='signup'),  # new
    path('signup/', views.signup_view, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),  # new
    path('login/', views.login_view, name='login'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),  # new
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('password_reset/', auth_views.password_reset, name='password_reset'),

]

front_patterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('my_profile/', views.my_profile, name='my_profile'),
    # API again!
    path('email/', views.emailView, name='email'),
    path('success/', views.successView, name='success'),
]

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('', include(api_patterns)),
    path('', include(registration_patterns)),
    path('', include(front_patterns)),
    # path('api-auth/', include('rest_framework.urls')),
    path('', include('rest_framework.urls')),

    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # new
    path('', include('django.contrib.auth.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),  # new
]
