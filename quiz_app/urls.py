from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_quiz, name='start_quiz'),
    path('get-question/', views.get_question, name='get_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('summary/', views.session_summary, name='summary'),
]
