"""
survey URL Configuration
"""

from django.urls import path
from . import views


urlpatterns = [
    path('survey/', views.SurveyListView.as_view()),
    path('survey/<int:pk>/', views.SurveyDetailView.as_view()),
    path('answer/<int:user_id>/', views.AnswerDetailView.as_view()),
]
