from django.urls import path, include
from django.views.generic.base import TemplateView  # new
from django.contrib import admin

from . import views, apiviews

app_name = 'polls'  # For one app not needed
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
    path('questions/', apiviews.questions_view, name='questions_view'),
    path('questions/<int:question_id>/', apiviews.question_detail_view, name='question_detail_view'),
    path('questions/<int:question_id>/choices/', apiviews.choices_view, name='choices_view'),
    path('questions/<int:question_id>/vote/', apiviews.vote_view, name='vote_view'),
    path('questions/<int:question_id>/result/', apiviews.question_result_view, name='question_result_view'),
    path('password_change/', views.password_change, name='update_password'),
    path('new_question/', views.question_new, name='new_question'),
    # path('', views.IndexView.as_view(template_name='polls/index.html'), name='index'),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', views.SignUp.as_view(template_name='signup.html'), name='signup'),  # new
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/', include('django.contrib.auth.urls')),  # new
]
