from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls'))
]
