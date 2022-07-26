from django.urls import path
from .views import *


urlpatterns = (
    # 学生接口
    # 学生信息相关接口
    path('student', web_student, name='student'),
    path('student/clazz', web_get_clazz, name='get_clazz'),
    path('student/clazzs', web_get_clazzs, name='get_clazzs'),
    path('student/classmates', web_get_classmates, name='get_classmates'),
    # 学生考试相关接口
    path('student/exam', web_get_exam, name='get_exam'),
    path('student/exams', web_get_exams, name='get_exams'),
    path('student/mark', web_get_self_mark, name='get_self_mark'),
    path('student/allSubject', web_get_all_subjects, name='get_all_subjects'),

    # 教师接口
    path('teacher/examDetail', web_get_exam_detail, name="get_exam_detail"),
    path('teacher/progress', web_get_marking_progress, name="get_marking_progress"),
    path('teacher/examClasses', web_get_school_exam_classes, name="get_school_exam_classes"),
    path('teacher/original', web_get_original_paper, name="get_original_paper"),
    path('teacher/score', web_get_one_score, name="get_one_score"),
)
