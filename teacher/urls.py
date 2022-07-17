from django.urls import path
from teacher.views import *

urlpatterns = [
    path("detail/", web_get_exam_detail, name="get_exam_detail"),
    path("progress/", web_get_marking_progress, name="get_marking_progress"),
    path("examClasses/", web_get_school_exam_classes, name="get_school_exam_classes"),
    path("scores/", web_get_scores, name="get_scores"),
    path("extra/", web_get_exam_extra_data, name="get_exam_extra_data"),
]
