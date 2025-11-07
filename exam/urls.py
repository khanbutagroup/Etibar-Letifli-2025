from django.urls import path
from exam.views import *

urlpatterns = [
    path('exams/', exam_list, name='exam_list'),
    path('exam/<int:exam_id>/take/<int:page>/', take_exam, name='take_exam'),
    path('exam/<int:exam_id>/take/', take_exam, name='take_exam_first'),
    path('exam/finish/<int:session_id>/', finish_exam, name='exam_finish'),
    path('buy/<int:exam_id>/', buy_exam, name='buy_exam'),
    path('start-exam/<int:exam_id>/', start_exam, name='start_exam')
]
