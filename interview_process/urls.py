from django.urls import path, include
from .views import *

urlpatterns = [
     
  path('question/',QuestionView.as_view(),name='question'),
  path('question/<int:question_id>/',QuestionView.as_view(),name='question'),
  path('candidate_register/',CandidateRegister.as_view(),name='candidate_register'),
  path('interview_question/',InterviewQuestionView.as_view(),name='interview_question'),
  path('interview_question/<int:question_id>/',InterviewQuestionView.as_view(),name='interview_question'),
  path('interview_api/',InterviewView.as_view(),name='interview'),
   
]
