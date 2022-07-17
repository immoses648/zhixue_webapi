from django.urls import path
from student.views import *

urlpatterns = [
    path('', web_student, name='student'),
    path('clazz/', web_get_clazz, name='get_clazz'),
    path('clazzs/', web_get_clazzs, name='get_clazzs'),
    path('classmates/', web_get_classmates, name='get_classmates'),
    path('exam/', web_get_exam, name='get_exam'),
    path('exams/', web_get_exams, name='get_exams'),
    path('original/', web_get_original, name='get_original'),
    path('mark/', web_get_self_mark, name='get_self_mark'),
]
