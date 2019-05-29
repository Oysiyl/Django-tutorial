from django.urls import path, include
from django.views.generic.base import TemplateView  # new
from django.contrib import admin

from . import views, apiviews

app_name = 'polls'  # For one app not needed

api_patterns = [
    path('questions/', apiviews.questions_view, name='questions_view'),
    path('questions/<int:question_id>/', apiviews.question_detail_view, name='question_detail_view'),
    path('questions/<int:question_id>/choices/', apiviews.choices_view, name='choices_view'),
    path('questions/<int:question_id>/vote/', apiviews.vote_view, name='vote_view'),
    path('questions/<int:question_id>/result/', apiviews.question_result_view, name='question_result_view'),
]

urlpatterns = [
    # Old views
    # ex: /polls/
    # path('', views.index, name='index'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    # New generic views

    # API
    # path('password_change/', views.password_change, name='password_change'),
    # path('email_change/', views.email_change, name='email_change'),
    # path('change_names/', views.change_names, name='change_names'),
    path('new_question/', views.question_new, name='new_question'),
    path('', include(api_patterns)),
    # path('', views.IndexView.as_view(template_name='polls/index.html'), name='index'),
    path('', views.index, name='index'),

    # path('email/', views.emailView, name='email'),
    # path('success/', views.successView, name='success'),
    # path('logout/', views.logout_view, name='logout'),
    # path('login/', views.login_view, name='login'),
    # path('admin/', admin.site.urls),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('accounts/', include('django.contrib.auth.urls')),  # new
]
