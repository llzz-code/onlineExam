from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from student.views import StuIndex, QueryGrade, Center, Email, exam, check_answer

urlpatterns = [
    path('index/', StuIndex.as_view(), name='index'),
    path('query/', QueryGrade.as_view(), name='query'),
    path('center/', Center.as_view(), name='center'),
    path('email/', Email.as_view(), name='email'),
    url(r'exam/(\d+)/$', exam, name='exam'),
    path('check/', check_answer, name='check'),
]
